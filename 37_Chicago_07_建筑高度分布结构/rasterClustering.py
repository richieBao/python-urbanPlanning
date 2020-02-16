# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 18:34:57 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import rasterio
import gdal,gdalnumeric
import numpy as np
import matplotlib.pyplot as plt
import copy,os,time,sys,pickle,re
from sklearn.cluster import DBSCAN
from tqdm import tqdm
from pylab import mpl


'''实现栅格聚类的方法'''    
def rasterCluster(rasterFn,val,eps,modelLoad=""):
    with rasterio.open(rasterFn) as src:
        r=src.read(1)
        profile=src.profile
    print(r)
        
    print("raster array shape:",r.shape)
    profile.update(
        count=1,
        compress='lzw',
        dtype=rasterio.int8
        )       
    
    relativeCellCoords=np.concatenate([v.reshape(-1,1) for v in np.where(r)],axis=1) #返回数组值索引（2 维度），作为坐标位置
    rCellCoordsMatrix=relativeCellCoords.reshape(r.shape+(2,))
    extractCoords=rCellCoordsMatrix[r==val] #仅保留待计算的类别索引值
    print("extractCoords.shape:",extractCoords.shape)
    
    # Compute DBSCAN
    if modelLoad:  #对于聚类加载保存的模型计算无意义，此条件可移除          
        loaded_model = pickle.load(open(modelLoad, 'rb'))
        print("model loaded")
        t1=time.time() 
        print("staring computing:",time.asctime())
        y_db=loaded_model.fit_predict(extractCoords)
        t2=time.time()
        print("end computing:",time.asctime())            
        tDiff_af=t2-t1 #用于计算聚类所需时间
        print("duration:",tDiff_af)
        print("cluster finished")
    else:          
        t1=time.time() 
        print("staring computing:",time.asctime())
        db=DBSCAN(eps=eps,min_samples=3,algorithm='ball_tree', metric='euclidean') #DBSCAN聚类
        y_db=db.fit_predict(extractCoords)
        t2=time.time()
        print("end computing:",time.asctime())
        tDiff_af=t2-t1 #用于计算聚类所需时间
        print("duration:",tDiff_af)
       
        #保存模型,因此类模型保存无意义，可移除
#            modelSaveName = os.path.join(modelSavePath,'rasterDBSCAN_%d.sav'%eps)
#            pickle.dump(db, open(modelSaveName, 'wb'))  
#            print("model saved:",modelSaveName)
        
        #保存数据
        dataSaveFn=os.path.join(resultsPath,"DBSCANResults_%d"%eps)
        np.save(dataSaveFn, y_db)
        print("predicted data saved:",dataSaveFn)
    
    #保存所有层聚类结果，以及所有层聚类频数
    #依据原栅格shape，存储聚类类标
    clusterArray=np.zeros(r.shape)
    y_db_plus=y_db+1
    n=0
    
    for idx in extractCoords:
        clusterArray[idx[0],idx[1]]=y_db_plus[n]
        n+=1
    print("n:",n)
    clusterArraySaveFn=os.path.join(resultsPath,"clusterArray_%d"%eps)
    np.save(clusterArraySaveFn,clusterArray)
    print("clusterArray saved:",clusterArraySaveFn)
    
    #计算聚类频数
    unique_elements, counts_elements = np.unique(clusterArray, return_counts=True)
    clusterFrequency=np.asarray(list(zip(unique_elements, counts_elements)), dtype=np.int)
    clusterFrequencyFn=os.path.join(resultsPath,"clusterFrequency_%d"%eps)
    np.save(clusterFrequencyFn,clusterFrequency)
    print("cluster frequency saved:",clusterFrequencyFn)
    
    #将每一层级计算聚类结果写入栅格数据
    # clusterRasterFn=r"clusterRaste_%d.tif"%eps
    with rasterio.open(os.path.join(resultsPath,r"clusterRaste_%d.tif"%eps), 'w', **profile) as dst:
        dst.write(clusterArray.astype(int))  

    
    return clusterArray,clusterFrequency
        

if __name__=="__main__":
    rasterFn=r"E:\spatialStructure_temp\BUildingHeight\mosaic\mosaic_39.tif"
    resultsPath=r"E:\spatialStructure_temp\BUildingHeight\clustering_height39" #配置保存结果数据的路径
    valExtraction=39
    eps=range(1,50,1)
    clusterArray,clusterFrequency=rasterCluster(rasterFn,valExtraction,eps)
    