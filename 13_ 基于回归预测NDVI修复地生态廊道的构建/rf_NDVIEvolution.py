# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 11:16:59 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
print(__doc__)
import gdal,ogr,os,osr,gdalnumeric
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scipy.ndimage.filters import convolve
import moviepy.editor as mpy
import time

import re
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import sys
import ospybook as pb
from ospybook.vectorplotter import VectorPlotter 

from sklearn.datasets import fetch_olivetti_faces
from sklearn.utils.validation import check_random_state

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import RidgeCV

from sklearn.externals import joblib

from skimage.morphology import disk
from skimage.filters import rank
import matplotlib.image as mpimg
from scipy import misc

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码/针对gdal
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码/针对gdal

fn=r'D:\MUBENAcademy\pythonSystem\dataB\LC81240422017022LGN01'  #用于建立回归模型的学习数据存储路径
raster_lyr=r'flaash.tif' #用于建立回归模型的学习数据文件名，该实验中用其计算植被指数NDVI，用NDVI来作为学习数据。此次实验为遥感影像landsat8 OLI数据

fn_mask=r'D:\project\gisData\design'  #mask数据存储路径
maskFn=r'ecoMake.tif'  #mask数据是根据自定义自由图形范围建立，cell栅格单元为1和0两个数值，分别用于解释变量和目标变量
row=299  #根据mask栅格大小(分辨率)，确定行数量
col=299 #根据mask栅格大小(分辨率)，确定列数量

studyRegionPath=r'D:\project\gisData\design'  #用于预测的数据路径。同时用于预测数据的保存路径              
studyRegionFn=r'outclipraster.tif' #用于预测的数据文件名。此次实验为遥感影像landsat8 OLI数据                              

'''读取只有一个波段(band)的栅格文件'''
def singleRaster(fn,raster_lyr):
    gdal.UseExceptions()
    
    '''打开栅格数据'''
    try:
        src_ds=gdal.Open(os.path.join(fn,raster_lyr))
    except RuntimeError as e:
        print( 'Unable to open %s'% os.path.join(fn,raster_lyr))
        sys.exit(1)
    print("metadata:",src_ds.GetMetadata())       
    
    '''获取所有波段'''
    band=src_ds.GetRasterBand(1).ReadAsArray().astype(np.float)
    return band #返回该波段，为数组形式
    
'''landsat8 OIL计算植被指数(NDVI)，用于修复地中植被廊道的预测'''
def rasterCal(fn,raster_lyr,raster_lyr_w):   
    gdal.UseExceptions()
    
    '''打开栅格数据'''
    try:
        src_ds=gdal.Open(os.path.join(fn,raster_lyr))
    except RuntimeError as e:
        print( 'Unable to open %s'% os.path.join(fn,raster_lyr))
        print(e)
        sys.exit(1)
    print("metadata:",src_ds.GetMetadata())   
    
    '''获取所有波段'''
    srcband=[]
    for band_num in range(1,8):
        try:
            srcband.append(src_ds.GetRasterBand(band_num))
        except RuntimeError as e:
            print('Band ( %i ) not found' % band_num)
            print(e)
            sys.exit(1)
    print(srcband)
    
    '''获取用于NDVI计算的红和近红波段数组,并计算ndvi'''
    red=srcband[3].ReadAsArray().astype(np.float)
    nir=srcband[4].ReadAsArray()
    red=np.ma.masked_where(nir+red==0,red)  #确定分母不为零
    ndvi=(nir-red)/(nir+red)
    ndvi=ndvi.filled(-99)
    print(ndvi.shape,ndvi.std(),ndvi.max(),ndvi.min(),ndvi.mean())
    
    '''初始化输出栅格'''
    driver=gdal.GetDriverByName('GTiff')
    if os.path.exists(os.path.join(fn,raster_lyr_w)):
        driver.Delete(os.path.join(fn,raster_lyr_w))
    out_raster=driver.Create(os.path.join(fn,raster_lyr_w),src_ds.RasterXSize,src_ds.RasterYSize,1,gdal.GDT_Float64)
    out_raster.SetProjection(src_ds.GetProjection()) #设置投影与参考栅格同
    out_raster.SetGeoTransform(src_ds.GetGeoTransform()) #配置地理转换与参考栅格同
    
    '''将数组传给栅格波段，为栅格值'''
    out_band=out_raster.GetRasterBand(1)
    out_band.WriteArray(ndvi)
    
    '''设置overview'''
    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    out_raster.BuildOverviews('average', overviews)
    
    '''清理缓存与移除数据源'''
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    del src_ds,out_raster,out_band
    return ndvi

'''显示栅格数据，用于数据查看'''
def rasterShow(fn,rasterImageName):    
    NDVIPath=os.path.join(fn,rasterImageName)
    try:
        rasterArray=gdalnumeric.LoadFile(NDVIPath)  #加载栅格数据为gdal数组格式
    except RuntimeError:
        print("Unable to open %s"%rasterPath)
    fig=plt.figure(figsize=(20, 12))
    ax=fig.add_subplot(111)
    plt.xticks([x for x in range(rasterArray.shape[0]) if x%200==0])
    plt.yticks([y for y in range(rasterArray.shape[0]) if y%200==0])
    ax.imshow(rasterArray)

'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]

'''将栅格数据分为多个单元块，每一个单元块为一个样本(sample)数据，划分的单元数量越多，越有利于模型训练，最好大于200，不同数量可以自行尝试比较'''
def trainBlock(array,row,col):
    arrayShape=array.shape
    print(arrayShape)
    rowPara=divmod(arrayShape[1],row)  #divmod(a,b)方法为除法取整，以及a对b的余数
    colPara=divmod(arrayShape[0],col)
    extractArray=array[:colPara[0]*col,:rowPara[0]*row]  #移除多余部分，规范数组，使其正好切分均匀
#    print(extractArray.shape)
    hsplitArray=np.hsplit(extractArray,rowPara[0])
    vsplitArray=flatten_lst([np.vsplit(subArray,colPara[0]) for subArray in hsplitArray])
    dataBlock=flatten_lst(vsplitArray)
    print("样本量：%s"%(len(dataBlock)))  #此时切分的块数据量，就为样本数据量
    
    '''显示查看其中一个样本'''     
    subShow=dataBlock[-10]
    print(subShow,'\n',subShow.max(),subShow.std())
    fig=plt.figure(figsize=(20, 12))
    ax=fig.add_subplot(111)
    plt.xticks([x for x in range(subShow.shape[0]) if x%400==0])
    plt.yticks([y for y in range(subShow.shape[1]) if y%200==0])
    ax.imshow(subShow)    
    
    dataBlockStack=np.append(dataBlock[:-1],[dataBlock[-1]],axis=0) #将列表转换为数组
    print(dataBlockStack.shape)
    return dataBlockStack

'''训练回归模型'''
def regressPre(data,mask,X_test=False):
    print(data.shape)
    dataFlatten=data.reshape(data.shape[0],-1)
    print(dataFlatten.shape)
    trainNum=int(dataFlatten.shape[0]*0.7) #确定划分训练数据集和测试数据集的比例
    print(trainNum)    
    train=dataFlatten[:trainNum]  #提取训练数据集
    test=dataFlatten[trainNum:]  #提取测试数据集
    print(train.shape,test.shape)        

    n_pred=5  #从测试数据集中提取n_pred个样本测试
    rng=check_random_state(4) #Turn seed into a np.random.RandomState instance，可通过help()查看说明
    pred_ids=rng.randint(test.shape[0], size=(n_pred, ))
    test=test[pred_ids, :] #调整后的测试数据集

    '''根据mask的定义，分开解释变量和目标变量'''
    maskFlatten=mask.reshape(-1)
    maskBool=maskFlatten==1  #将mask的0和1的数据转换为布尔值，用于数据提取
    X_train=train[:,maskBool]    
    y_train=train[:,maskBool==False]  #对换maskBool中布尔值，即Ture为False，False为True
    X_test=test[:,maskBool]
    y_test=test[:,maskBool==False]

    '''回归模型估计器(estimator),可以对比不同回归算法'''
    ESTIMATORS = {
        "Extratrees": ExtraTreesRegressor(n_estimators=10, max_features=32,random_state=0), #计算时间短
#        "K-nn": KNeighborsRegressor(),
#        "Linear regression": LinearRegression(), #计算时间较长
#        "Ridge": RidgeCV(),  #计算时间估计极长
    }

    y_test_predict=dict()  
    for name, estimator in ESTIMATORS.items():
        estimator.fit(X_train, y_train)
        joblib.dump(estimator,os.path.join(fn,raster_lyr[:-4]+name+'.pkl'))  #如果数据量大，模型训练将会花费较多时间，因此保存训练好的模型到硬盘空间，方便之后直接调用
        y_test_predict[name] = estimator.predict(X_test)
    
    '''打印测试数据时的原始数据和预测数据，查看比较训练结果。需要注意按照mask还原数据'''
    image_shape = (row, col)    
    n_cols = 1 + len(ESTIMATORS)
    plt.figure(figsize=(2. * n_cols*3, 2.26 * n_pred*3))
    plt.suptitle("pred completion with multi-output estimators", size=16)
    
    for i in range(n_pred):
        true_pred=test[i]
        true_pred[maskBool==False]=y_test[i]    
        if i:
            sub = plt.subplot(n_pred, n_cols, i * n_cols + 1)
        else:
            sub = plt.subplot(n_pred, n_cols, i * n_cols + 1,title="true faces")    
        sub.axis("off")
        sub.imshow(true_pred.reshape(image_shape),cmap=plt.cm.gray,interpolation="nearest")    
        for j, est in enumerate(sorted(ESTIMATORS)):
            completed_pred=test[i]
            completed_pred[maskBool==False]=y_test_predict[est][i]    
            if i:
                sub = plt.subplot(n_pred, n_cols, i * n_cols + 2 + j)    
            else:
                sub = plt.subplot(n_pred, n_cols, i * n_cols + 2 + j,title=est)    
            sub.axis("off")
            sub.imshow(completed_pred.reshape(image_shape),cmap=plt.cm.gray,interpolation="nearest")    
    plt.show()

'''加载已经训练好的模型，并用于数据的预测，此次实验为预测修复地NDVI，植被廊道的修复预测'''
def loadModelPredict(studyRegionFn,modelPath,mask):
    gdal.UseExceptions()    
    '''打开栅格数据'''
    try:
        src_ds=gdal.Open(studyRegionFn)
    except RuntimeError as e:
        print( 'Unable to open %s'% studyRegionFn)
#        print(e)
        sys.exit(1)
    print("metadata:",src_ds.GetMetadata())       
    
    '''获取波段'''
    studyRegion=src_ds.GetRasterBand(1).ReadAsArray().astype(np.float)
 
    '''按照mask划分解释变量和目标变量'''
    image_shape=(row, col)    
    dataFlatten=np.copy(studyRegion).reshape(-1)  
    maskFlatten=mask.reshape(-1)
    maskBool=maskFlatten==1
    X=dataFlatten[maskBool].reshape(1,-1)
    
    model=joblib.load(modelPath) #加载已经训练好的回归模型，用于预测
    y_p=model.predict(X)
    
    print(X.std(),y_p.std(),X.max(),y_p.max())
    y_p_scaled=(y_p - y_p.min()) / (y_p.max() - y_p.min()) * (X.max() - X.min()) + X.min() #调整预测数据的区间与解释变量的区间同，也可忽略
    print(dataFlatten.shape,maskBool.shape,y_p_scaled.shape)
    
    true_pred=dataFlatten
    true_pred[maskBool==False]=y_p_scaled.reshape(-1)   #拼合解释变量和预测数据

    '''打印显示结果'''
    fig, (ax1, ax2) = plt.subplots(figsize=(17, 17), ncols=2)
    pre=ax1.imshow(studyRegion, cmap=plt.cm.RdYlGn, interpolation='none')
#    fig.colorbar(pre, ax=ax1)
    ori=ax2.imshow(true_pred.reshape(image_shape), cmap=plt.cm.RdYlGn, interpolation='none')
#    fig.colorbar(ori, ax=ax2)
    plt.show() 
    
    return true_pred.reshape(image_shape)

'''raster栅格数据的读写，仅包1个波段。用于保存预测的数据为栅格形式'''
def rasterRW(fn,raster_lyr,raster_pred,raster_lyr_w):
    gdal.UseExceptions()    
    '''打开栅格数据'''
    try:
        src_ds=gdal.Open(os.path.join(fn,raster_lyr))
    except RuntimeError as e:
        print( 'Unable to open %s'% os.path.join(fn,raster_lyr))
        print(e)
        sys.exit(1)
    print("metadata:",src_ds.GetMetadata())   
  
    '''初始化输出栅格'''
    driver=gdal.GetDriverByName('GTiff')
    print(src_ds.RasterXSize,src_ds.RasterYSize)
    out_raster=driver.Create(os.path.join(fn,raster_lyr_w),col,row,1,gdal.GDT_Float64)
#    out_raster=driver.Create(os.path.join(fn,raster_lyr_w),row,col,1,gdal.GDT_CInt16)
    out_raster.SetProjection(src_ds.GetProjection()) #设置投影与参考栅格同
    out_raster.SetGeoTransform(src_ds.GetGeoTransform()) #配置地理转换与参考栅格同
    
    '''将数组传给栅格波段，为栅格值'''
    out_band=out_raster.GetRasterBand(1)
    out_band.WriteArray(raster_pred)
    
    '''设置overview'''
    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    out_raster.BuildOverviews('average', overviews)
    
    '''清理缓存与移除数据源'''
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    del src_ds,out_raster,out_band

'''重分类栅格数据(根据指定阈值，划分数据为n类，此次实验为2类)'''    
def reclassifyPre(value,threshold):
    print(threshold)
    reclassifyPre=np.copy(value)
    
    mask=reclassifyPre>threshold #根据阈值建立mask
    reclassifyPre[mask]=0
    reclassifyPre[mask==False]=1
    print(reclassifyPre.min(),reclassifyPre.max(),reclassifyPre.shape)

    '''打印显示结果'''    
    fig=plt.figure(figsize=(12, 12))
    ax=fig.add_subplot(111)
    plt.xticks([x for x in range(reclassifyPre.shape[0]) if x%200==0])
    plt.yticks([y for y in range(reclassifyPre.shape[0]) if y%200==0])
    ax.imshow(reclassifyPre)
    
    return reclassifyPre
    
if __name__=="__main__":
    '''计算训练用NDVI数据'''    
    raster_lyr_w=r'NDVI_a.tif' #计算的NDVI输出文件名                          
    ndvi=rasterCal(fn,raster_lyr,raster_lyr_w)  #训练阶段的NDVI数据           
    '''根据mask，切分样本，并训练回归模型'''
    maskArray=singleRaster(fn_mask,maskFn) #读取mask
    dataBlockStack=trainBlock(ndvi,row,col)  #切分样本           
    regressPre(dataBlockStack,maskArray,X_test=False) #训练回归模型
    '''读取用于预测数据，计算NDVI'''  
    nvdiPreFn=r'ndvi_pre.tif'  #用于预测数据NDVI保存文件名                                     
    ndviPre=rasterCal(studyRegionPath,studyRegionFn,nvdiPreFn)    
    '''加载已经训练好的回归模型，预测修复地的NDVI'''
    modelPath=os.path.join(fn,raster_lyr[:-4]+"Extratrees"+'.pkl')    
    studyRegionM=os.path.join(studyRegionPath,nvdiPreFn)
    raster_pred=loadModelPredict(studyRegionM,modelPath,maskArray)   
    '''重分类栅格数据'''     
    alpha=-0.11 #指定调节参数
    threshold=np.median(raster_pred)+alpha #根据预测数据中位数和调节参数，定义阈值
    reclassiPre=reclassifyPre(raster_pred,threshold)
    '''分别保存预测栅格和重分类栅格'''    
    pre_w=r'pred_raster_%s%s%s%s%s%s.tif'%time.gmtime()[:6]
    rasterRW(studyRegionPath,studyRegionFn,raster_pred,pre_w) #保存预测栅格
    reclassiPreFn=r'reclassiPreknn_%s%s%s%s%s%s.tif'%time.gmtime()[:6]    
    rasterRW(studyRegionPath,studyRegionFn,reclassiPre,reclassiPreFn) #保存重分类栅格