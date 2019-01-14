# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 17:19:36 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
import GPSData as GD #调用第5次课“基于GPS调研与数据读取”的程序

'''异常值判断，参考 Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and Handle Outliers", The ASQC Basic References in Quality Control: Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 可自行网络搜索下载，或者从caDesign设计下载'''
def is_outlier(points, threshold=3.5):
    if len(points.shape) == 1: 
        points=points[:,None] #转换为二维数组
    median=np.median(points, axis=0) #数组中位数
    diff=np.sum((points-median)**2, axis=-1) #计算方差
    diff=np.sqrt(diff) #标准差    
    med_abs_deviation=np.median(diff) #中位数绝对偏差
    # compute modified Z-score
    modified_z_score=0.6745 * diff/med_abs_deviation
    print(modified_z_score)
    return modified_z_score>threshold #判断后，返回布尔值

'''测试数据。可以先通过简单的数据测试和调试代码，待正确执行后，实验实际数据'''
'''
x=np.array([2.1,2.6,2.4,2.5,2.3,2.1,2.3,2.6,8.2,8.3])
filtered = x[~is_outlier(x)]
print(is_outlier(x))
buckets=50
plt.figure()
plt.subplot(211)
plt.hist(x, buckets)
plt.xlabel('Raw')

plt.subplot(212)
plt.hist(filtered, buckets)
plt.xlabel('Cleaned')

plt.show()
'''
'''调整第5次课“D读取经纬度坐标，根据.kml文件打印成路径,同时定位图片位置并显示高程变化”部分程序，主要是调整输入参数，直接修改为剔除异常值后的数组并对应修改相应变量，其它部分保持不变'''

def researchPath(coordiSubArrayC,kmlSubArray):
    fig,ax=plt.subplots()
    ax.plot(kmlSubArray[:,0],kmlSubArray[:,1],'r-',lw=0.5,markersize=5)
    #print(kmlSubArray[:,0][0:30].tolist())
    #ax.plot(coordiValuesArray[:,2],coordiValuesArray[:,1],'r+-',lw=0.5,markersize=5)
    cm=plt.cm.get_cmap('hot') #具体的`matplotlib.colors.Colormap'实例可以查看matplotlib官网 http://matplotlib.org/users/colormaps.html，替换不同色系
    sc=ax.scatter(coordiSubArrayC[:,1],coordiSubArrayC[:,0],c=coordiSubArrayC[:,2],s=50,alpha=0.8,cmap=cm)  #按高程显示散点颜色
    fig.colorbar(sc)
    ax.set_xlabel('lng')
    ax.set_ylabel('lat')
    #print(coordiValues[0][1],coordiValues[0][2])
    ax.annotate('origin',xy=(coordiSubArrayC[0][2],coordiSubArrayC[0][1]),xycoords='data',xytext=(coordiSubArrayC[0][2]+0.015, coordiSubArrayC[0][1]-0.006),fontsize=14,arrowprops=dict(facecolor='black',shrink=0.05))
    fig.text(0.50,0.92,'research path',fontsize=20,color='gray',horizontalalignment='center',va='top',alpha=0.5)    
    fig.set_figheight(10)
    fig.set_figwidth(10)
    plt.show()

'''定义直方图函数，通过绘制直方图，直观查看数据分布情况，可以帮助确定threshold值''' 
  
def histDrawing(dataX,filtered,buckets=50): 
    plt.figure()
    plt.subplot(211)
    plt.hist(dataX, buckets)
    plt.xlabel('Raw')
    
    plt.subplot(212)
    plt.hist(filtered, buckets)
    plt.xlabel('Cleaned')    
    plt.show()

'''主执行程序，前半部分同第5次课，后部分增加了剔除异常值的操作'''

def main():    
    fileInfo=GD.filePath(GD.dirpath,GD.fileType)
    coordiInfo=GD.coordiExtraction(fileInfo)
    coordiSubKey=list(coordiInfo.keys())[0] #选取不同的数据
    coordiSub=coordiInfo[coordiSubKey]
    kmlInfo=GD.filePath(GD.dirpath,GD.kmlType)
    kmlInfo.pop((list(kmlInfo.keys())[0]))
    kmlCoordiInfo=GD.kmlCoordi(kmlInfo)
    kmlSub=kmlCoordiInfo[coordiSubKey]
    coordiValues=list(coordiSub.values())   
    coordiValuesPart=[i[1:-1] for i in coordiValues]     
    coordiValuesArray=np.array(coordiValuesPart) 
    kmlSubValues=list(kmlSub.values())[0]
    kmlSubArray=np.array(kmlSubValues)
    
    #对图片信息数据的清理
    coordiX=coordiValuesArray[:,1]
    coordiValuesArrayClean=coordiValuesArray[~is_outlier(coordiX,threshold=100)]
    print(coordiValuesArrayClean.shape,coordiValuesArray.shape)
    histDrawing(dataX=coordiX,filtered=coordiValuesArrayClean[:,1])
    #对.kml数据的清理
    kmlX=kmlSubArray[:,0]
    kmlSubArrayClean=kmlSubArray[~is_outlier(kmlX)]
    print(kmlSubArrayClean.shape,kmlX.shape)
    histDrawing(dataX=kmlX,filtered=kmlSubArrayClean[:,0])
    
    researchPath(coordiValuesArrayClean,kmlSubArrayClean)    

main()  #执行主程序
