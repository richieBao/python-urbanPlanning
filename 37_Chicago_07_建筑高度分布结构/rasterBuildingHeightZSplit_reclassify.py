# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 22:28:03 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import rasterio,os
from rasterio.windows import Window
from tqdm import tqdm
import numpy as np
from numba import jit, cuda,njit
import datetime
import numba 
from joblib import Memory

#读取栅格，提取属性值
def rasterProperties(rasterFp):
    raster=rasterio.open(rasterFp)
    print("type:",type(raster))
    print("transform:",raster.transform)
    print("[width,height]:", raster.width, raster.height)
    print("number of bands:",raster.count)
    print("bounds:",raster.bounds)
    print("driver:", raster.driver)
    print("no data values:",raster.nodatavals)    
    print("_"*50)
    # print("meta:",raster.meta)        
    # print("_"*50)
    # print("profile:",raster.profile)
    return raster.width, raster.height

# Yield successive n-sized 
def divide_chunks(l,n):
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

#建立用于rasterio分区读取较大raster的window数据
def rasterio_windows(totalWidth,totalHeight,subWidth,subHeight):
    w_n=list(divide_chunks(list(range(totalWidth)), subWidth))
    h_n=list(divide_chunks(list(range(totalHeight)), subHeight))
    wins=[Window(w[0],h[0],len(w),len(h)) for h in h_n for w in w_n]
    # print(wins)
        
    print("raster windows amount:",len(wins))
    return wins

# @njit(parallel=True)
#栅格重分类计算。如果栅格数据很大，采用rasterio的window读取数据，并计算，可以避免内存溢出
def computing(w):
    zList=list(range(0,100,3)) #450
    # zList=zList[:1]    
    z_domain=[(zList[i],zList[i+1]) for i in range(len(zList)-1)]
    for z in z_domain:
        w[np.logical_and(w>=z[0], w<z[1])]=z[0]
        # w=np.where((w>=z[0]) & (w<z[1]),z[0],w)
    
    w[w<0]=-1
    w[w>=100]=100 #numba do not support this type of array    
    # w=np.where(w<0,-1,w)
    # w=np.where(w>100,100,w)
    # unique, counts = np.unique(w, return_counts=True)
    # uniqueCounts=dict(zip(unique, counts))  
    return w.astype(np.int8)
    
#read raster blocks 分区读取单独raster数据，并计算
def RWRasterBlocks(rasterFp,dataSave_fp, windowsList):
    newPath=os.path.join(saveRasterByBlock_fp,"reclassify")
    try:
        os.mkdir(newPath)
    except OSError:
        print ("Creation of the directory %s failed" % newPath)
    else:
        print ("Successfully created the directory %s " % newPath)  
    a_T = datetime.datetime.now()
    i=0    
    buildingAmount_epochMultiple=0
    for win in tqdm(windowsList):
        with rasterio.open(rasterFp,"r+") as src:                
            src.nodata=-1
            w = src.read(1, window=win) 
            # print("_"*50)
            # print(w.shape)
            profile=src.profile
            win_transform=src.window_transform(win)  
        #计算部分
        w=computing(w)
        #配置raster属性值，尤其compress和dtype参数部分，可以大幅度降低栅格大小
        profile.update(
            width=win.width, 
            height=win.height,
            count=1,
            transform=win_transform,
            compress='lzw',
            dtype=rasterio.int8
            )
        # with rasterio.open(os.path.join(saveRasterByBlock_fp,"testingBlock.tif"), 'w', driver='GTiff' width=512, height=256, count=1,dtype=w.dtype,**profile) as dst:
        with rasterio.open(os.path.join(newPath,"buildingHeight_reclassify_%d.tif"%i), 'w', **profile) as dst:
            dst.write(w, window=Window(0,0,win.width,win.height), indexes=1)             
              
        i+=1     
        # if i ==2:
        #     break    
        # np.save(os.path.join(dataSave_fp,"data_%d.npy"%zValue),buildingAmount_epochMultiple) 
        # buildingAmount[zValue]=buildingAmount_epochMultiple
        # print("_"*50)
        # print("%d---zValue has completed!!!"%zValue)
    b_T= datetime.datetime.now()
    print("time span:", b_T-a_T)
    print("_"*50)      
    # print("total amount:",buildingAmount)
    # np.save(os.path.join(dataSave_fp,"buildingFrequency.npy"),buildingAmount)    
    # return buildingAmount
    
if __name__=="__main__":  
    rasterFp=r"E:\spatialStructure_temp\transfer\buidingHeightRaseter.tif"
    saveRasterByBlock_fp=r"E:\spatialStructure_temp\BUildingHeight\reclassify"
    dataSave_fp=r"E:\spatialStructure_temp\BUildingHeight\output_data"
    
    totalWidth,totalHeight=rasterProperties(rasterFp)
    # readWriteRasterByBlock(rasterFp,saveRasterByBlock_fp)   
    # rasterio_wins=rasterio_windows(21,15,5,3)
    subWidth=60000
    subHeight=60000
    rasterio_wins=rasterio_windows(totalWidth,totalHeight,subWidth,subHeight)
    buildingAmount=RWRasterBlocks(rasterFp, dataSave_fp,rasterio_wins)
    
    # buildingAmount_load=np.load(os.path.join(dataSave_fp,"buildingFrequency.npy"),allow_pickle=True)