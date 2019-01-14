# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:44:49 2017

@author:richieBao-caDesign设计(cadesign.cn)
借鉴SIR传染病模型
"""
import gdal,ogr,os,osr,gdalnumeric
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scipy.ndimage.filters import convolve
import moviepy.editor as mpy
import time

'''读取“空间用地分类”.tif地理信息数据'''
#rasterPath=r'D:\MUBENAcademy\pythonSystem\dataA\testClip6.tif'
rasterPath=r'C:\Users\Richi\Music\SIR\testClip6.tif'
try:
    srcArray=gdalnumeric.LoadFile(rasterPath)  #加载栅格数据为gdal数组格式
except RuntimeError:
    print("Unable to open %s"%rasterPath)
print(srcArray.shape)
originalRaster=srcArray.copy()
print(np.unique(originalRaster))
uniqueValues=np.unique(srcArray)
#print(uniqueValues)

'''配置空间阻力并归一化到[0,1]'''
#costMapping_LandType={"空值A":(0,0),"空值B":(256,0),"农田":(2,1),"河流":(3,7),"建设":(4,0),"森林山":(5,10),"森林平":(6,10)}
costMapping_LandType={"空值A":(0,0),"空值B":(256,0),"农田":(2,200),"河流":(3,500),"建设":(4,0),"森林山":(5,1000),"森林平":(6,1000)}  #根据用地类型配置“空间阻力”值映射。256为潜在的异常值。
for idx,(identity,costValue) in enumerate(costMapping_LandType.items()):
#    print(identity,costValue)
    srcArray[srcArray==costValue[0]]=costValue[1]
mappingRaster=srcArray
mms=MinMaxScaler()
normalizeCostArray=mms.fit_transform(srcArray)
print(normalizeCostArray.max(),normalizeCostArray.std())

'''配置SIR模型初始值，将S设置为空间阻力值'''
SIR=np.zeros((3,srcArray.shape[0], srcArray.shape[1]),dtype=float)
print(SIR.shape)
SIR[0]=normalizeCostArray
print(SIR[0].std())

'''配置SIR模型中I的初始值。1，可以从设置的1个或多个点开始；2，可以将森林部分直接设置为I有值，而其它部分保持0。'''
start = int(0.9*srcArray.shape[0]), int(0.9*srcArray.shape[1])  #根据行列拾取点位置
print(start)
#print(ok)
#SIR[1,start[0], start[1]]=0.8
SIR[1,120,90]=0.8  #设置的点位置
#SIR[1,60,130]=0.8

'''设置转换系数，以及卷积核'''
infection_rate = 0.3 #β值
incubation_rate = 0.1 #γ值
dispersion_rates  = [0, 0.07, 0.03]  #扩散系数
dispersion_kernelA = np.array([[0.5, 1 , 0.5],
                                [1  , -6, 1],
                                [0.5, 1, 0.5]])  #卷积核    
dispersion_kernelB = np.array([[0, 1 , 0],
                                [1 ,1, 1],
                                [0, 1, 0]])  #卷积核  
dispersion_kernel=dispersion_kernelA
dt=1.0  #时间记录值，开始值
hours_per_second=7*24  #终止值(条件)
world={'SIR':SIR,'t':0} #建立字典，方便数据更新

'''SIR模型'''
def infection(SIR,infection_rate,incubation_rate):
    S,I,R=SIR
    newly_infected=infection_rate*I*S  #I*S or R*S
    newly_rampaging=incubation_rate*I
    dS=-newly_infected
    dI=newly_infected-newly_rampaging
    dR=newly_rampaging
    return np.array([dS, dI, dR])

'''卷积'''
def dispersion(SIR,dispersion_kernel, dispersion_rates):
    return np.array([convolve(e,dispersion_kernel,cval=0)*r for (e,r) in zip(SIR,dispersion_rates)])

'''执行SIR模型和卷积，更新world字典'''
def update(world):
    infect=infection(world['SIR'],infection_rate,incubation_rate)
    disperse = dispersion(world['SIR'], dispersion_kernel, dispersion_rates)
    world['SIR'] += dt*( infect + disperse)    
    world['t'] += dt

'''将模拟计算的值转换到[0,255]RGB色域空间'''
def world_to_npimage(world):
#    print(world['SIR'].max())
    coefs=np.array([2,20,25]).reshape((3,1,1))
    accentuated_world=255*coefs*world['SIR']
#    print(accentuated_world.max())
    image=accentuated_world[::-1].swapaxes(0,2).swapaxes(0,1) #调整数组格式为用于图片显示的（x,y,3）形式
    return np.minimum(255, image)

'''显示图像'''
def imageShow(img,t):
#    print(img.shape)
    if t%20==0: #根据图像大小和待观察数据的变化程度调整图像显示步幅
        fig, axes = plt.subplots(nrows=1, ncols=4,facecolor='w', figsize=(10,5))
        ax0, ax1,ax2,ax3= axes.flatten()
        ax0.imshow(img)  #显示S
        ax1.imshow(img[...,2])  #显示R
        ax2.imshow(img[...,1])
        ax3.imshow(img[...,0])
        fig.tight_layout()
        plt.show()
    else:
        pass

'''返回每一步的SIR和卷积综合蔓延结果'''
def make_frame(t):
    while world['t']<hours_per_second*t:
        update(world)        
        imageShow(world_to_npimage(world),world['t'])  #显示指定步幅的图像，观察蔓延过程
#        print(world['t'])
    return world_to_npimage(world)

'''将蔓延后的结果数据保持为.tif地理信息数据，可以在GIS平台下加载使用'''
def array2raster(newRasterfn,rasterRef,rasterArray):  
    try:
        source_ds=gdal.Open(rasterRef)
    except RuntimeError:
        print("Unable to open %s" % rasterRef,)
    print("..............................")
    print(rasterArray.shape)
    gt=source_ds.GetGeoTransform() #获取栅格的地理空间变换数据
    print(gt)    
    cols=rasterArray.shape[1] #获取列数量
    rows=rasterArray.shape[0] #获取行数量
    originX=gt[0] #获取起始点X值
    originY=gt[3] #获取起始点Y值
    pixelWidth=gt[1] #单元(cell)栅格宽
    pixelHeight=gt[5] #单元(cell)栅格高
    '''A:建立栅格'''
    driver=gdal.GetDriverByName('GTiff') #用于栅格输出的驱动实例化
    outRaster=driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float64) #建立输出栅格.Create(Driver self, char const * utf8_path, int xsize, int ysize, int bands=1, GDALDataType eType, char ** options=None) -> Dataset
    '''B:设置空间变换'''
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight)) #设置输出栅格的空间变换参数，或者直接使用gt，保持与参考栅格相同设置
    '''C:给栅格波段赋值'''
    outband=outRaster.GetRasterBand(1) #获取输出栅格的一个输出波段
    outband.WriteArray(rasterArray) #将数组写入该波段
    '''D:设置栅格坐标系(投影)'''
    outRasterSRS=osr.SpatialReference() #空间参考实例化
    outRasterSRS.ImportFromWkt(source_ds.GetProjectionRef()) #设置空间参考为参考栅格的投影值
    outRaster.SetProjection(outRasterSRS.ExportToWkt()) #设置输出栅格的投影
    '''E:清空缓存与关闭栅格'''
    outband.FlushCache() #清空缓存
    source_ds=None #关闭栅格

'''显示栅格数据，主要目的方便查看栅格坐标，从而方便定位初始点'''
def rasterShow(rasterImage):    
    colorMapping_LandType={"空值A":(0,0),"空值B":(256,0),"农田":(2,10),"河流":(3,40),"建设":(4,100),"森林山":(5,170),"森林平":(6,250)}
    print(np.unique(rasterImage))
    for idx,(identity,colorValue) in enumerate(colorMapping_LandType.items()):
                rasterImage[rasterImage==colorValue[0]]=colorValue[1]
    print("......................................................................")
    print(np.unique(rasterImage))
#    imgRGB=
    fig=plt.figure(figsize=(20, 12))
    ax=fig.add_subplot(111)
    plt.xticks([x for x in range(rasterImage.shape[0]) if x%20==0])
    plt.yticks([y for y in range(rasterImage.shape[0]) if y%10==0])
    ax.imshow(rasterImage)

if __name__=="__main__":     
    make_frame(30)      
#    rasterShow(originalRaster)
    rasterShow(originalRaster)
#    print(ok)
    animation=mpy.VideoClip(make_frame,duration=12)
    animation.write_videofile(r'C:\Users\Richi\Music\SIR\testC.mp4', fps=20)
    animation.write_gif(r"C:\Users\Richi\Music\SIR\testC.gif", fps=15)
#    rootPath=r'D:\MUBENAcademy\pythonSystem\dataA'
    rootPath=r'C:\Users\Richi\Music\SIR'    
    rasterName=r'forestEvolution.tif'
    array2raster(os.path.join(rootPath,rasterName),rasterPath,world['SIR'][2])