# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 21:49:09 2018

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import gdal,ogr,os,osr,gdalnumeric
import sys
import ospybook as pb
from ospybook.vectorplotter import VectorPlotter 
import numpy as np
from pandas import DataFrame
import pandas as pd
from dbfread import DBF
import cv2
import matplotlib.pyplot as plt 
import math
import colorsys

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码

fn=r'C:\Users\Richi\sf_richiebao\sf_monograph\21_jpgValueExtraction\Heatmap' 

#hsv2rgb和 rgb2hsv 的代码来自于网络查询，本例中并未使用，而是直接调用colorsys模块
def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

'''色彩值的提取与写入raster栅格数据'''
def rasterR(fn,raster_lyr,raster_lyr_w,bandNum):
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
    for band_num in range(1,bandNum+1):
        try:
            srcband.append(src_ds.GetRasterBand(band_num))
        except RuntimeError as e:
            print('Band ( %i ) not found' % band_num)
            print(e)
            sys.exit(1)
    print(srcband)

    '''获取RGB并图表打印查看'''
    rsData={}
    for key in range(bandNum):
        rsData[key]=srcband[key].ReadAsArray().astype(np.int32)
    for key in range(bandNum):
        print(rsData[key].shape)    
        print(DataFrame(rsData[key].flatten()).describe()) #count数量/mean均值/std标准差/min最小值/25%下四分位/50%中位数/75%上四分位/max最大值
    
    rgb=np.stack((rsData[0],rsData[1],rsData[2]),axis=2)
#    rgb[rgb==256]=100 #如果有些值不正确，或者需调整某些值时，可以进行替换
#    print(rgb)

    fig=plt.figure(figsize=(20, 12))
    ax=fig.add_subplot(111)
    ax.imshow(rgb)
    plt.show()
    print(rgb)
    print(rgb.shape)
    
    '''将RGB转换为HSV,并图表打印查看'''
    vfunc=np.vectorize(colorsys.rgb_to_hsv)  # HSV代表色调(Hue)，饱和度(Saturation)和值(Value)
#    vfunc=np.vectorize(colorsys.rgb_to_hls)  # HSL代表色调(Hue)，饱和度(Saturation)和亮度(Lightness)
    H,S,V=vfunc(rsData[0],rsData[1],rsData[2])    
    HSV=np.stack((H,S,V),axis=2)
    print(HSV)
    print(HSV.shape)
    #HSV = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
#    print(HSV.T.shape)
    print(DataFrame(H.flatten()).describe())
    
    fig=plt.figure(figsize=(20, 12))
    ax=fig.add_subplot(111)
    ax.imshow(HSV)
    plt.show()    

    '''将单独的色彩向量写入栅格，此次写入的是H色调值'''
    '''初始化输出栅格'''
    driver=gdal.GetDriverByName('GTiff')
    out_raster=driver.Create(os.path.join(fn,raster_lyr_w),src_ds.RasterXSize,src_ds.RasterYSize,1,gdal.GDT_Float64)
    out_raster.SetProjection(src_ds.GetProjection()) #设置投影与参考栅格同
    out_raster.SetGeoTransform(src_ds.GetGeoTransform()) #配置地理转换与参考栅格同
    
    '''将数组传给栅格波段，为栅格值'''
    out_band=out_raster.GetRasterBand(1)
    H[H>0.9]=0.01 #根据情况调整色调值，或进行标识
    H[H==0]=1 #特殊值处理，例如空白的值
    out_band.WriteArray(1-H)
#    out_band.WriteArray(V) #也可自行尝试写入其它值
    
    '''设置overview，本部分未使用'''
    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    overviews = pb.compute_overview_levels(srcband[0])
    src_ds.BuildOverviews('average', overviews)
    
    '''清理缓存与移除数据源'''
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    del src_ds,out_raster,out_band

    return rsData

if __name__=="__main__":
    raster_lyr=r'13.tif'
    raster_lyr_w=r'didi13mu.tif'
    rasterR(fn,raster_lyr,raster_lyr_w,4) 
    
