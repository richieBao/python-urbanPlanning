# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:06:05 2019

ref:https://howtoinqgis.wordpress.com/2016/12/17/how-to-split-a-raster-in-several-tiles-using-qgis-or-python-gdal/
"""

import os, gdal
 
in_path = r"D:/data/lidar/lidar_bundle/mosaic/mosaic_dtm/"
input_filename = r"Chicago_loop_dtm_mosaic.tif"
 
out_path = r'D:/data/lidar/pdal_data/'
output_filename = r'chicago_loop_tile_'
 
ds = gdal.Open(in_path + input_filename)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize
print(xsize,ysize)
 
tile_size_x = 20000
tile_size_y = 20000

for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)