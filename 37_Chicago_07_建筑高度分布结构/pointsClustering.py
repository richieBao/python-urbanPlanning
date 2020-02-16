# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 19:44:07 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import geopandas as gpd
import geoplot,os,ogr,gdal
import pandas as pd
import datetime,osr
from sklearn import cluster
import numpy as np
from rasterio.plot import show
import rasterio
from tqdm import tqdm

'''DBSCAN基于密度空间的聚类，聚类所有poi特征点'''
def affinityPropagationForPoints(dataArray,epsValue):
    # print("--------------------Clustering")
    data=dataArray
    a_T = datetime.datetime.now()    
    db=cluster.DBSCAN(eps=epsValue,min_samples=3,metric='euclidean') #meter=degree*(2 * math.pi * 6378137.0)/ 360  degree=50/(2 * math.pi * 6378137.0) * 360，在调参时，eps为邻域的距离阈值，而分析的数据为经纬度数据，为了便于调参，可依据上述公式可以在米和度之间互相转换，此时设置eps=0.0008，约为90m，如果poi的空间点之间距离在90m内则为一簇；min_samples为样本点要成为核心对象所需要的邻域样本数阈值。参数需要自行根据所分析的数据不断调试，直至达到较好聚类的结果。
    y_db=db.fit_predict(data)  #获取聚类预测类标
    
    b_T= datetime.datetime.now()
    # print("time span:", b_T-a_T)
    # print("_"*50) 
    
    pred=y_db  
    # print(pred,len(np.unique(pred)))  #打印查看预测类标和计算聚类簇数

    # print("-------------------cluster Finishing")
    return pred,np.unique(pred)  #返回DBSCAN聚类预测值。和簇类标

#convert points .shp to raster 将点数据写入为raster数据。使用raster.SetGeoTransform,栅格化数据。参考GDAL官方代码
def pts2raster(shapefile,RASTER_PATH,cellSize,field_name=False):
    from osgeo import gdal, ogr

    # Define pixel_size and NoData value of new raster
    pixel_size = cellSize
    NoData_value = -9999
    
    # Filename of input OGR file
    vector_ptsShp_fn = shapefile
    
    # Filename of the raster Tiff that will be created
    raster_ptsShp_fn = RASTER_PATH
    
    # Open the data source and read in the extent
    source_ds = ogr.Open(vector_ptsShp_fn)
    source_layer = source_ds.GetLayer()
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    
    # Create the destination data source
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    target_ds = gdal.GetDriverByName('GTiff').Create(raster_ptsShp_fn, x_res, y_res, 1, gdal.GDT_Int32 )
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)
    
    # Rasterize
    # gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0])
    # Rasterize
    if field_name:
        gdal.RasterizeLayer(target_ds,[1], source_layer,options=["ATTRIBUTE={0}".format(field_name)])
        # print("write:",field_name)
    else:
        gdal.RasterizeLayer(target_ds,[1], source_layer,burn_values=[-1])   
    return gdal.Open(RASTER_PATH).ReadAsArray() 

#批量计算
def combo_clustering(ptsShp_fn,resultsPath_ptsCluster,output_raster_fp,eps,dataSave):
    feature=gpd.read_file(ptsShp_fn)
    dataArray=pd.concat((feature.geometry.x,feature.geometry.y),axis=1)
    labelDic={}
    predDic={}
    for distance in tqdm(eps):
        pred,label=affinityPropagationForPoints(dataArray,distance)
        feature["pred"]=pred #the field name should be short, or ArcGis will cut it.
        pts_cluster_path=os.path.join(resultsPath_ptsCluster,"pts_cluster_%d.shp"%distance)
        feature.to_file(pts_cluster_path)
        
        cellSize=distance
        input_shp=pts_cluster_path
        
        output_raster_path=os.path.join(output_raster_fp,"ptsRasterCluster_%s.tif"%distance)
        rasterRead=pts2raster(input_shp,output_raster_path,cellSize,"pred")
        # with rasterio.open(output_raster_path) as src:
        #     # r=src.read(1)
        #     show(src)
        labelDic[distance]=label
        predDic[distance]=pred
    labelSaveFn=os.path.join(dataSave,"labelDic.npy")
    np.save(labelSaveFn,labelDic)
    predSaveFn=os.path.join(dataSave,"predDic.npy")
    np.save(predSaveFn,predDic)
    return predDic,labelDic

if __name__=="__main__": 
    pass
    ptsShp_fn=r"E:\spatialStructure_temp\BUildingHeight\39mBuildingHeight.shp"
    resultsPath_ptsCluster=r"E:\spatialStructure_temp\BUildingHeight\clustering_height39\shp_pts" 
    output_raster_fp=r"E:\spatialStructure_temp\BUildingHeight\clustering_height39\raster_clustering"
    dataSave=r"E:\spatialStructure_temp\BUildingHeight\clustering_height39\dataSave"
    eps=range(10,500,10)
    
    predDic,labelDic=combo_clustering(ptsShp_fn,resultsPath_ptsCluster,output_raster_fp,eps,dataSave)