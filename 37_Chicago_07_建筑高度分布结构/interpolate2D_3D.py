# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 18:24:25 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""

import geopandas as gp
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
from rasterio.fill import fillnodata
import glob
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tqdm import tqdm

# def interpolateRaster(preRaster):
#     preData=gp.read_file(preRaster)
#     print(preData)
    
#栅格插值，不全数据
def interpolateRaster(dirpath,out_fp):
    search_criteria = "*.tif"
    q = os.path.join(dirpath, search_criteria)
   
    # glob function can be used to list files from a directory with specific criteria
    dem_fps = glob.glob(q)
    print(len(dem_fps))
    
    for fp in tqdm(dem_fps): 
        # print(fp)
        # print("interplate_dtm_%s"%os.path.basename(fp))
        with rasterio.open(fp,'r') as src:
            data = src.read(1, masked=True)
            msk = src.read_masks(1) 
            #配置max_search_distance参数，或者多次执行插值，补全较大数据缺失区域
            fill_raster=fillnodata(data,msk,max_search_distance=400.0,smoothing_iterations=0) #reference:https://rasterio.readthedocs.io/en/latest/api/rasterio.fill.html
            # scaler=MinMaxScaler()
            # plt.imshow(scaler.fit_transform(fill_raster))
            # plt.imshow(scaler.fit_transform(data))
            
            out_meta = src.meta.copy()         
            arr = np.random.randint(5, size=(100,100)).astype(np.float) 
            with rasterio.open(os.path.join(out_fp,"interplate_dtm_%s"%os.path.basename(fp)), "w", **out_meta) as dest:            
                dest.write(fill_raster, 1)
   

if __name__ == "__main__":
    # preRaster=r"D:\data\data_01_Chicago\lidar\lidar_bundle\mosaic\mosaic_dtm\01_JACKSON PARK_Tdtm_mosaic.tif"
    dirpath=r"D:\data\data_01_Chicago\lidar\lidar_bundle\mosaic\mosaic_dtm_interplate"
    out_fp=r"D:\data\data_01_Chicago\lidar\lidar_bundle\mosaic\mosaic_dtm_interplate\demInterplate_2th"
    interpolateRaster(dirpath,out_fp)

