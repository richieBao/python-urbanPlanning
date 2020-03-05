# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:07:28 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import os,pysal,fiona,shapely,sympy,math,contextily,rasterio,datetime,geojson 
# print(fiona.supported_drivers) #a full list of supported formats, type
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from shapely.geometry import shape,mapping, Point,MultiPoint, Polygon, MultiPolygon,LineString
from shapely.geometry.polygon import LinearRing
from pylab import figure, scatter, show
from sklearn.preprocessing import minmax_scale
import contextily as ctx
from rasterio.mask import mask
# from eobox.raster import extraction
from rasterstats import zonal_stats
from rasterio import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.plot import show as rioShow
from rasterio.windows import Window
from rasterio.features import shapes

#从新定义栅格投影，参考投影为vector .shp文件
def reprojectedRaster(rasterFn,ref_vectorFn,dst_raster_projected):
    dst_crs=gpd.read_file(ref_vectorFn).crs
    print(dst_crs) #{'init': 'epsg:4326'}    
    a_T = datetime.datetime.now()
    
    # dst_crs='EPSG:4326'
    with rasterio.open(rasterFn) as src:
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height,
        # 'compress': "LZW",
        'dtype':rasterio.uint8,  #rasterio.float32
        })
        # print(src.count)

        with rasterio.open(dst_raster_projected, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                    )     
    
    b_T = datetime.datetime.now()
    print("reprojected time span:", b_T-a_T)    
 
#根据Polgyon统计raster栅格信息
def polygonExtractRasterValue(polygonFn,rasterFn):    
    # parkBoundaries=gpd.read_file(polygonFn)
    # parkGeometry=parkBoundaries.geometry.values
    # print(parkGeometry)    
    raster = rasterio.open(rasterFn)
    # print(raster)
    # rioShow(raster)
    
    #A_数值数据
    #zonal_stats_stats: min,max,mean,count,sum,std,median,majority,minority,unique,range,nodata,percentile 
    zs=zonal_stats(polygonFn, rasterFn,stats=["count",'min', 'max', "mean",'median', "std",'majority', "minority",'sum',"nodata","range"]) #,geojson_out=True
    # # print(zs)
    
    #B_classification data
    # cmap={1: 'treeCanopy', 2: 'grassShrub', 3: 'bareSoil',4:"water",5:"buildings",6:"roadsRailraods",7:"otherPavedSurfaces"}
    # zs=zonal_stats(polygonFn, rasterFn,categorical=True, category_map=cmap)
    # zs=zonal_stats(polygonFn, rasterFn,stats=["count"]) #,geojson_out=True
    
    zsDataFrame=pd.DataFrame(zs)
    return zsDataFrame


if __name__=="__main__": 
    data_Dic={"parkBoundaries":r"F:\data_02_Chicago\parkNetwork\Parks - Chicago Park District Park Boundaries (current).shp",
              
              "height_highVegetation":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\HighVegetationHeight_c3_f32.tif",
              "height_highVegetation_reprojected":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\height_highVegetation_reprojected.tif",
              "low_highVegetation_reprojected":r"F:\data_02_Chicago\ArcGisPro\temp\LVeg_c3Proj.tif",
              "medi_lowVegetation_reprojected":r"F:\data_02_Chicago\ArcGisPro\temp\MVeg_c3Proj.tif",
               
              "classification":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\LandCover_2010_ChicagoRegion\landcover_2010_chicagoregion.img",
              "classification_reprojected":r"F:\data_02_Chicago\ArcGisPro\temp\landcover_2010_chicagoreg_c3_r.tif",       
            } 
    # dst_raster_projected_height_highVegetation=r"F:\data_02_Chicago\ArcGisPro\parkNetwork\height_highVegetation_reprojected.tif"
    # reprojectedRaster(data_Dic["height_highVegetation"],data_Dic["parkBoundaries"],dst_raster_projected_height_highVegetation)
    
    # dst_raster_projected=r"F:\data_02_Chicago\ArcGisPro\parkNetwork\classification_reprojected.tif"
    # reprojectedRaster(data_Dic["classification"],data_Dic["parkBoundaries"],dst_raster_projected)
    
    # z=polygonExtractRasterValue(data_Dic["parkBoundaries"],data_Dic["height_highVegetation_reprojected"])
    # classificationPolygonStatistics=polygonExtractRasterValue(data_Dic["parkBoundaries"],data_Dic["classification_reprojected"])
    # classificationPolygonStatistics.to_pickle(r"F:\data_02_Chicago\ArcGisPro\parkNetwork\classificationPolygonStatistics.pkl")
  
    # classificationPolygonStatistics_count=polygonExtractRasterValue(data_Dic["parkBoundaries"],data_Dic["classification_reprojected"])
    # classificationPolygonStatistics_count.to_pickle(r"F:\data_02_Chicago\ArcGisPro\parkNetwork\classificationPolygonStatistics_count.pkl")
    
    
    # height_highVegetation_reprojectedStatistics=polygonExtractRasterValue(data_Dic["parkBoundaries"],data_Dic["height_highVegetation_reprojected"])
    # height_highVegetation_reprojectedStatistics.to_pickle(r"F:\data_02_Chicago\ArcGisPro\parkNetwork\height_highVegetation_reprojectedStatistics.pkl")
    
    # low_highVegetation_reprojectedStatistics=polygonExtractRasterValue(data_Dic["parkBoundaries"],data_Dic["low_highVegetation_reprojected"])
    # low_highVegetation_reprojectedStatistics.to_pickle(r"F:\data_02_Chicago\ArcGisPro\parkNetwork\low_highVegetation_reprojectedStatistics.pkl")    
    
    medi_highVegetation_reprojectedStatistics=polygonExtractRasterValue(data_Dic["parkBoundaries"],data_Dic["medi_lowVegetation_reprojected"])
    medi_highVegetation_reprojectedStatistics.to_pickle(r"F:\data_02_Chicago\ArcGisPro\parkNetwork\medi_highVegetation_reprojectedStatistics.pkl")    
        

    '''
    0 - Background
    1 - Tree Canopy
    2 - Grass/Shrub
    3 - Bare Soil
    4 - Water
    5 - Buildings
    6 - Roads/Railroads
    7 - Other Paved Surfaces
    Class definitions and stand
    '''   