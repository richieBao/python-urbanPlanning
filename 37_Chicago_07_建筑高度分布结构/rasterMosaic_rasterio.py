# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
rasterio库与pdal等库冲突，如果存在冲突，可以重新建立新环境
参考迁移：https://automating-gis-processes.github.io/CSC/notebooks/L5/raster-mosaic.html
"""
#如果rasterio库与pdal等库冲突，可以建立单独环境。
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm
# %matplotlib inline

#将多个栅格数据拼接为一张
def rasterMosaic(dirpath,out_fp):
    # File and folder paths
    # out_fp = os.path.join(dirpath, "Helsinki_DEM2x2m_Mosaic.tif")
    
    # Make a search criteria to select the DEM files
    search_criteria = "*.tif"
    q = os.path.join(dirpath, search_criteria)
    print(q)
    
    # glob function can be used to list files from a directory with specific criteria
    dem_fps = glob.glob(q)
    print(len(dem_fps))

    # List for the source files
    src_files_to_mosaic = []
    
    # Iterate over raster files and add them to source -list in 'read mode'
    for fp in dem_fps:
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)
    

    # Merge function returns a single mosaic array and the transformation info
    mosaic, out_trans = merge(src_files_to_mosaic)
    
    # Plot the result
    # show(mosaic, cmap='terrain')
    

    # Copy the metadata
    out_meta = src.meta.copy()
    # print(out_meta)

    # Update the metadata
    out_meta.update({"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": out_trans,
                     # "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
                     "compress":'lzw',
                     "dtype":rasterio.int8 #configure the raster type
                     }
                    )    

    # Write the mosaic raster to disk
    with rasterio.open(out_fp, "w", **out_meta) as dest:
        dest.write(mosaic)        
    
    return mosaic, out_trans


if __name__=="__main__":  
    dirpath=r"E:\spatialStructure_temp\BUildingHeight\reclassify\reclassify"
    # dirpath=r"D:\data\data_01_Chicago\mosaic\mosaic_dtm"
    out_path=r"E:\spatialStructure_temp\BUildingHeight\reclassifyMosaic\buildingHeightMosaic.tif"    

    # #bundle
    # subfolders=[ f.path for f in os.scandir(dirpath) if f.is_dir() ]
    # for subFp in tqdm(subfolders):
    #     out_fp = os.path.join(out_path, "mosaic_%s.tif"%subFp.split("\\")[-1])
        
    #     # a_T = datetime.datetime.now()
    #     mosaic, out_trans=rasterMosaic(subFp,out_fp)
    #     # b_T= datetime.datetime.now()
    #     # print("time span:", b_T-a_T)
    #     # 
    
    #single
    mosaic, out_trans=rasterMosaic(dirpath,out_path)    
    
    
    
  
      