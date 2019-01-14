# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 16:11:03 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import arcpy
from arcpy import env
import os
from arcpy.sa import *
 
#设置工作环境
worksapce_path=r"D:\project\gisData\design"
env.overwriteOutput=True
env.workspace=worksapce_path
env.overwriteOutput=True

in_raster=r'D:\project\gisData\data_A\LC81260322016210LGN00\16flash.tif' #原始的landsat8 OLI的数据

in_boundary=r'D:\project\gisData\ecoRecovery\ecoPreBoundary.shp' #外围边界
outClipRaster=r'outclipraster.tif'

preBoundary=r'D:\project\gisData\ecoRecovery\ecoRecovery.shp' #内层，预测范围边界
preClipRaster=r'preclipraster.tif'

clipRas=arcpy.Clip_management(in_raster,"#",os.path.join(worksapce_path,outClipRaster),in_boundary ,"#", "#", "NO_MAINTAIN_EXTENT")

'''查看栅格基本信息，查看栅格大小和行列数量，用于预测程序'''                              
rasterInfoName=["CELLSIZEX","CELLSIZEY","COLUMNCOUNT","ROWCOUNT"]        
rasterInfo={}      
for info in rasterInfoName:          
    rasterSTDResult=arcpy.GetRasterProperties_management(clipRas, info)                              
    rasterInfo[info]=rasterSTDResult.getOutput(0)                           
print(rasterInfo)

'''提取预测数据，并设置mask，其值为0和1'''
preRas=arcpy.Clip_management(clipRas,"#",os.path.join(worksapce_path,preClipRaster),preBoundary ,"#", True, "NO_MAINTAIN_EXTENT")
                             
arcpy.env.extent=os.path.join(worksapce_path,outClipRaster) #设置计算(Processing)范围，方便不同大小栅格的计算
preClipRasterExtent=Con(IsNull(preClipRaster),1,preClipRaster)
ecoOuter=arcpy.Raster(clipRas)-preClipRasterExtent  
ecoMask=Con(ecoOuter,0,1,"Value=0")

ecoMask.save(os.path.join(worksapce_path,r'ecoMake.tif'))  #保存mask
arcpy.env.extent="MAXOF"


                         
                                           