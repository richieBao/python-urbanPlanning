# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:25:36 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""

import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import math,gdal,sys,time,os,re,gdalnumeric,h5py,gc
from tqdm import tqdm
import psutil
print(psutil.virtual_memory())
#为减缓内存压力，使用h5py在硬盘中存储较大的数据，并在内存中del掉对应变量，减缓内存压力。此次实验中，部分np.save数据，亦可自行尝试存储为h5py格式文件。
#为增加计算速度，避免使用python的循环，而是直接使用numpy数组计算方法
from memory_profiler import profile #用于内存监测
import tables


#数组延直线截面提取单元值
# @profile #内存监测所标识的函数
def lineProfile(zValue,originalPoint,endPoint,qualDistance,saveN,j): 
    num=equalDistance+1
    
    x0_O=originalPoint[:,0]
    if "x0" in f.keys(): #如果索引存在于h5py数据库中，则移除该数据，为下次循清空
        del f["x0"]    
    x0=f.create_dataset("x0",data=x0_O.reshape(-1,1))
    del x0_O
    x1_O=endPoint[:,:,0]
    if "x1" in f.keys():
        del f["x1"]          
    x1=f.create_dataset("x1",data=x1_O)
    del x1_O
    
    # x=np.linspace(x0.reshape(-1,1), x1, num) 
    x_O=np.linspace(x0, x1, num,dtype=np.int) #可以不用修改数组类型。出于内存优化考虑,会加快后续np.stack计算速度
    if "x" in f.keys():
        del f["x"]      
    x=f.create_dataset("x",data=x_O)
    del x_O    
    # print("x linspace finished!")
    
    y0_O=originalPoint[:,1]  
    if "y0" in f.keys():
        del f["y0"]       
    y0=f.create_dataset("y0",data=y0_O.reshape(-1,1))
    del y0_O
    y1_O=endPoint[:,:,1]
    if "y1" in f.keys():
        del f["y1"]       
    y1=f.create_dataset("y1",data=y1_O)
    del y1_O
    # y=np.linspace(y0.reshape(-1,1), y1, num)
    y_O=np.linspace(y0, y1, num,dtype=np.int)
    if "y" in f.keys():
        del f["y"]       
    y=f.create_dataset("y",data=y_O)
    del y_O
    # print("y linspace finished!")
    
    # x=np.around(x).astype(np.int)
    # y=np.around(y).astype(np.int)
    
    # print("+"*50,"\nfinish computing linspace!")
    xStack=np.stack(x,axis=-1)
    xStackSplit=np.array_split(xStack,saveN) #为减缓单次数组计算量，切分数组为saveN个单个数组，切分量越大，单个数组越小，计算所占用内存越小
    # xStackSplit=f.create_dataset("xStackSplit",data=xStackSplit_O)
    # del xStackSplit_O
    del xStack #清空该变量，释放内存.关于numpy array占据内存的大小，查找确认
    # print("xStack finished!")
    
    yStack=np.stack(y,axis=-1)
    yStackSplit=np.array_split(yStack,saveN)
    # yStackSplit=f.create_dataset("yStackSplit",data=yStackSplit_O)
    # del yStackSplit_O
    del yStack
    # print("yStack finished!")
    # print("finish computing xy_stack seperately!\n")
    
    zi=np.array([])
    #待计算数组切分后，循环计算
    for i in range(len(xStackSplit)):
        ziSub = scipy.ndimage.map_coordinates(zValue,[xStackSplit[i],yStackSplit[i]] ,cval=0,mode="nearest",order=0) #根据数组索引值，提取实际值
        zi=np.append(zi,np.array(ziSub))      
       
        # LineProfileFn=os.path.join(saveFp,"LF_%d"%(j))            
        # np.save(LineProfileFn, zi)
        
        ziReshape=zi.reshape(xStackSplit[i].shape)
        SVFValueFn=SVF(radious,equalDistance,ziReshape,j)
        
        zi=np.array([])
        #记录每次存储的数据路径为.txt文件，最后通过该文件读取所有数据，组合与写入raster格式文件
        with open(os.path.join(saveFp,"SVFValue_filenames.txt"), "a") as text_file:
            text_file.write("%s\n"%SVFValueFn)
        j+=1 #用于文件名的标识
    # return os.path.join(saveFp,"SVFValue_filenames.txt")
    return j

#计算首尾坐标，用到三角函数
# @profile #内存监测所标识的函数
def equalCircleDivide(originalCoordiArray,radious,lineProfileAmount):
    # print(originalCoordiArray.shape)
    angle_s=360/lineProfileAmount
    angle_array=np.array([i*angle_s for i in range(lineProfileAmount)])
   
    opposite=np.sin(np.radians(angle_array))*radious
    yCoordi_O=np.add(opposite,originalCoordiArray[:,1].reshape(-1,1))
    # print("!"*50)
    # print(yCoordi_O)
    if "yCoordi" in f.keys():
        del f["yCoordi"]
    yCoordi=f.create_dataset("yCoordi",data=yCoordi_O)
    del yCoordi_O  
    
    adjacent=np.cos(np.radians(angle_array))*radious
    xCoordi_O=np.add(adjacent,originalCoordiArray[:,0].reshape(-1,1))
    if "xCoordi" in f.keys():
        del f["xCoordi"]
    xCoordi=f.create_dataset("xCoordi",data=xCoordi_O)
    del xCoordi_O
    
    CoordiArray=np.stack((xCoordi,yCoordi),axis=-1)
    # print("+"*50,"\nfinish computing coordiArray!")
    # del xCoordi
    # del yCoordi
    return CoordiArray

#计算障碍角度和高度,以及SVF值。参考文献：城区复杂下垫面天空视域因子参数化方法——以北京鸟巢周边地区为例
# @profile #内存监测所标识的函数
def SVF(radious,equalDistance,ziList,j):
    segment=radious/equalDistance
    distanceList=[i*segment for i in range(equalDistance+1)]
    distanceList=distanceList[1:]

    ziListSub=ziList[:,:,1:]
    ziListOrigin=ziList[:,:,0]
    
    sinValues=np.true_divide(np.subtract(ziListSub,np.expand_dims(ziListOrigin, axis=2)),np.sqrt(np.add(np.power(distanceList,2),np.power(np.subtract(ziListSub,np.expand_dims(ziListOrigin, axis=2)),2))))
    
    sinMaxValue=np.amax(sinValues,axis=2)
    SVFValue=1-np.true_divide(np.sum(sinMaxValue, axis=1),sinMaxValue.shape[-1])
    SVFValueFn=os.path.join(saveFp,"SVFValue_%d"%(j))            
    np.save(SVFValueFn, SVFValue)    
    # print("SVF Value saved:%d"%i)    

    return SVFValueFn
    
'''栅格数据读取程序，.tif,单波段。读取需要的波段数据并存储。未裁切影像方法'''
def singleBand(rasterFp):
    gdal.UseExceptions()        
    '''打开栅格数据'''
    try:
        src_ds=gdal.Open(rasterFp)
    except RuntimeError as e:
        # print( 'Unable to open %s'% rasterFp)
        sys.exit(1)
    #获取栅格信息
    rasterInfo={"RasterXSize":src_ds.RasterXSize,
                "RasterYSize":src_ds.RasterYSize,
                "RasterProjection":src_ds.GetProjection(),
                "GeoTransform":src_ds.GetGeoTransform()}
    
    '''获取单波段像元值'''
    bandValue=src_ds.GetRasterBand(1).ReadAsArray().astype(np.float)
    # print("readed rasterDate!")
    return bandValue,rasterInfo #返回该波段，为数组形式 


'''保存栅格数据，1个波段'''      
def rasterRW(rasterValue,resultsPath,rasterSavingFn,para):
    gdal.UseExceptions()    
#    '''打开栅格数据'''
#    try:
#        src_ds=gdal.Open(os.path.join(resultsPath,rasterSavingFn))
#    except RuntimeError as e:
#        print( 'Unable to open %s'% os.path.join(resultsPath,rasterSavingFn))
#        print(e)
#        sys.exit(1)
#    print("metadata:",src_ds.GetMetadata())   
  
    '''初始化输出栅格'''
    driver=gdal.GetDriverByName('GTiff')
    # print(para['RasterXSize'],para['RasterYSize'])
    out_raster=driver.Create(os.path.join(resultsPath,rasterSavingFn),para['RasterXSize'],para['RasterYSize'],1,gdal.GDT_Float64)
    out_raster.SetProjection(para['RasterProjection']) #设置投影与参考栅格同
    out_raster.SetGeoTransform(para['GeoTransform']) #配置地理转换与参考栅格同
    
    '''将数组传给栅格波段，为栅格值'''
    out_band=out_raster.GetRasterBand(1)
    out_band.WriteArray(rasterValue)
    
#    '''设置overview'''
#    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
#    out_raster.BuildOverviews('average', overviews)
    
    '''清理缓存与移除数据源'''
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
#    del src_ds,out_raster,out_band        
    del out_raster,out_band    

'''按块读取数据，与批量计算，减缓内存压力'''
# @profile #内存监测所标识的函数
def combo_SVF_Save(rasterFp,saveFp,sliceNum=100000):    
    bandValue_O,rasterInfo=singleBand(rasterFp)     
    print("raster loaded!")
    bandValue=f.create_dataset("bandValue",data=bandValue_O)
    del bandValue_O
    
    relativeCellCoords=np.indices(bandValue.shape)
    relativeCellCoords2D_O=np.stack(relativeCellCoords,axis=2).reshape(-1,2)
    del relativeCellCoords
    relativeCellCoords2D=f.create_dataset("relativeCellCoords2D",data=relativeCellCoords2D_O)
    del relativeCellCoords2D_O

    # 建立块索引区间
    sliceDomain=[]
    maxNum=relativeCellCoords2D.shape[0]
    for i in range(0,maxNum,sliceNum):        
        if i+sliceNum>maxNum:
            sliceDomain.append((i,maxNum))
        else:
            sliceDomain.append((i,i+sliceNum))
            
    # print(sliceDomain)
    # 按块循环计算        
    open(os.path.join(saveFp,"SVFValue_filenames.txt"), "w").close() #清除文本内容   
    j=0
    for sliceCount in tqdm(range(len(sliceDomain))):
        domain=sliceDomain[sliceCount]
        T=relativeCellCoords2D[domain[0]:domain[1]]
        # print(T)
        # print(T.shape)
        coordiArray=equalCircleDivide(T,radious,lineProfileAmount)            
        
        # print(coordiArray)
        # print(coordiArray.shape)
        j=lineProfile(bandValue,T,coordiArray,equalDistance,saveN,j)

        
    # print("-"*50)
    return os.path.join(saveFp,"SVFValue_filenames.txt"),bandValue.shape,rasterInfo

#读取临时存储文件，重新组合为原栅格大小数组，并存储为raster格式文件。   
# @profile #内存监测所标识的函数
def combo_SVF(SVFValue_fns,SVFShape,rasterInfo):  
    with open(SVFValue_fns,"r") as f:                  
        SVFValue_fnsList=f.readlines()   
    SVF=np.array([])
    for i in SVFValue_fnsList:
        SVF=np.append(SVF,np.load(i.replace("\n","")+".npy"))
    # print("$"*50)
    # print(SVF.shape)
    
    SVFArray=SVF.reshape(SVFShape)
    # rasterRW(SVFArray,saveFp,"SVFArray_01_%s.tif"%time.time(),rasterInfo)
    # rasterRW(SVFArray,rasterFn,"SVFArray_chicago_loop_tile_0_0.tif",rasterInfo)
    rasterRW(SVFArray,rasterFn,"SVFArray_d0.tif",rasterInfo)
    print("_"*50,"\nSVFArray raster has been built!")


if __name__=="__main__":  
    tables.file._open_files.close_all() #关闭文件。该程序可忽略
    gc.collect() #释放缓存，IPython console 命令：%reset -f
    rasterFp=r"D:\data\lidar\pdal_data\d.tif" #待计算SVF的栅格
    # rasterFp=r"D:\data\lidar\pdal_data\chicago_loop_tile_0_0.tif"
    saveFp=r"D:\data\lidar\pdal_save"
    rasterFn=r"D:\data\lidar\pdal_raster"
    
    hdf5Fn=os.path.join(saveFp,"cacheSVF.hdf5")
    if os.path.exists(hdf5Fn):
        os.remove(hdf5Fn)
    else:
        print("Can not delete the file as it doesn't exists,built new one!")
    f=h5py.File(hdf5Fn, "a")

    #参数配置        
    rasterResolution=1 #计算栅格的分辨率    
    radious=500*rasterResolution #扫描半径
    lineProfileAmount=36#扫描截面数量
    equalDistance=50 #每条扫描线的等分数量     
    saveN=12 #配置每块计算时，numpy数组一次性计算量，数值越大，单次数组计算量越小，单次计算占用内存越小。numpy 数组大小在1，000，000量时，内存16G，测试达到最大，如果超过该量值，则需要增加该参数值，即降低单次数组的大小。
    sliceNum=100000 #设置按块读取时，每一块的大小，即0轴的数量。默认为100000，值越大，占用内存量越大。需要根据自身内存大小配置该值
    
    localtime = time.asctime( time.localtime(time.time()) )
    print ("start time :", localtime)
    #为增加计算速度，计算过程使用numpy数组方式计算。如果数据较大，切分数据为多批次，由saveN配置，如果内存溢出，或计算失败可以尝试调大此参数。
    SVFValue_fns,SVFShape,rasterInfo=combo_SVF_Save(rasterFp,saveFp,sliceNum)    
    combo_SVF(SVFValue_fns,SVFShape,rasterInfo)
    localtime = time.asctime( time.localtime(time.time()) )
    print ("end time :", localtime)
    # bandValue,rasterInfo=singleBand(rasterFp)
    # print("bandValue shape:",bandValue.shape)

    