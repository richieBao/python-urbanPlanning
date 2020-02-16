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

# memory_location=r"E:\memoryLocation"
# memory = Memory(memory_location, verbose=0)

#读取栅格，并查看属性值，返回需要的属性
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
# chunks from l. 
#递归分组列表数据
def divide_chunks(l,n):
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

#建立用于rasterio库分批读取一个较大Raster数据的windows列表（如果内存溢出，而要处理较大的单独raster数据时）
#关于rasterio的window数据格式可以查看其官方网站
def rasterio_windows(totalWidth,totalHeight,subWidth,subHeight):
    w_n=list(divide_chunks(list(range(totalWidth)), subWidth))
    h_n=list(divide_chunks(list(range(totalHeight)), subHeight))
    wins=[Window(w[0],h[0],len(w),len(h)) for h in h_n for w in w_n]
    # print(wins)
    '''之下的代码繁复，并无法处理边界高宽问题，弃之'''
    # if totalWidth%subWidth==0 and totalHeight%subHeight==0:
    #     w_n=[subWidth*i for i in range(totalWidth//subWidth)]
    #     h_n=[subHeight*i for i in range(totalHeight//subHeight)]
    #     wins=[Window(w,h,subWidth,subHeight) for h in h_n for w in w_n]
    
    # if totalWidth%subWidth==0 and totalHeight%subHeight!=0:
    #     w_n=[subWidth*i for i in range(totalWidth//subWidth)]
    #     h_n=[subHeight*i for i in range(totalHeight//subHeight+1)]
    #     wins=[Window(w,h,subWidth,subHeight) for h in h_n for w in w_n]
            
    # if totalWidth%subWidth!=0 and totalHeight%subHeight==0:
    #     w_n=[subWidth*i for i in range(totalWidth//subWidth+1)]
    #     h_n=[subHeight*i for i in range(totalHeight//subHeight)]
    #     wins=[Window(w,h,subWidth,subHeight) for h in h_n for w in w_n]    
        
    # if totalWidth%subWidth!=0 and totalHeight%subHeight!=0:
    #     w_n=[subWidth*i for i in range(totalWidth//subWidth+1)]
    #     h_n=[subHeight*i for i in range(totalHeight//subHeight+1)]
    #     wins=[Window(w,h,subWidth,subHeight) for h in h_n for w in w_n]            
        
    print("raster windows amount:",len(wins))
    return wins

#testing 测试部分，可丢弃
def readWriteRasterByBlock(rasterFp,saveRasterByBlock_fp):
    '''reading and writing single block by para Defination '''
    # win=Window(120, 145, 512, 256) # Window(col_off=10, row_off=10, width=80, height=80)
    # with rasterio.open(rasterFp) as src:
    #       w = src.read(1, window=win) 
    #       print(w.shape)
    #       profile=src.profile
    #       win_transform=src.window_transform(win)
    
    # profile.update(
    #     width=512, 
    #     height=256,
    #     count=1,
    #     transform=win_transform
    #     )
    # # with rasterio.open(os.path.join(saveRasterByBlock_fp,"testingBlock.tif"), 'w', driver='GTiff' width=512, height=256, count=1,dtype=w.dtype,**profile) as dst:
    # with rasterio.open(os.path.join(saveRasterByBlock_fp,"testingBlock.tif"), 'w', **profile) as dst:
    #     dst.write(w, window=Window(0, 0, 512, 256), indexes=1)
    
    '''reading row by row'''
    # with rasterio.open(rasterFp) as src:
    #       # for i, shape in enumerate(src.block_shapes, 1):
    #       #     print((i, shape))
    #     i=0
    #     for ji, window in src.block_windows(1):
    #         print((ji, window))
    #         i+=1
    #     print(i)

    with rasterio.open(rasterFp) as src:
        i=0
        for ji, window in src.block_windows(1):
            print((ji, window))
            r=src.read(1,window=window)
            i+=1
            print(r.shape)
            break
        print(i)

    '''multi bands'''
     # with rasterio.open('tests/data/RGB.byte.tif') as src:         
     #     assert len(set(src.block_shapes)) == 1
     #     for ji, window in src.block_windows(1):             
     #         b, g, r = (src.read(k, window=window) for k in (1, 2, 3))
     #         print((ji, r.shape, g.shape, b.shape))
     #         break

        
    '''read block by block'''    

# @njit(parallel=True)
#比较使用numba库并行计算结果，原始numpy布尔值计算方法，较之np.where采用numba并行计算更快
def computing(w,z):
    w[w<z]=-1
    w[w>=z]=z #numba do not support this type of array
    
    # wBool=np.where(w>=z,z,-1) #可用于numba库，并行计算的numpy数据函数
    # unique, counts = np.unique(w, return_counts=True)
    # uniqueCounts=dict(zip(unique, counts))   
    temp_count=np.count_nonzero(w==z)
    return w.astype(np.int8),temp_count
    
    
#read raster blocks 分批读取较大栅格数据，并计算
def RWRasterBlocks(rasterFp,dataSave_fp, windowsList):
    zList=list(range(0,100,3)) #450
    # zList=zList[:1]
    buildingAmount={}
    for zValue in zList:   
        
        newPath=os.path.join(saveRasterByBlock_fp,"%s"%zValue )
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
            # print("_"*50)
            # print(win)
            with rasterio.open(rasterFp,"r+") as src:                
                src.nodata=-1
                w = src.read(1, window=win) 
                # print("_"*50)
                # print(w.shape)
                profile=src.profile
                win_transform=src.window_transform(win)    
            # print(w)            
            #to split building Height by successive Z value            
            # from math import isclose
            # a = 1.0
            # b = 1.00000001
            # assert isclose(a, b, abs_tol=1e-8)
            #isclose(a, b, rel_tol=1e-9, abs_tol=0.0)
            z=zValue
            # print("+"*50)
            # w[w<z]=-3.4028235e+38
            # w[w>=z]=z
            # print(w.dtype)
            '''计算部分'''
            w,temp_count=computing(w,z)
            
            # unique, counts = np.unique(w, return_counts=True)
            # uniqueCounts=dict(zip(unique, counts))
            # print("%d---unique:counts"%i,uniqueCounts)   
            
            # buildingAmount_epochMultiple+=np.count_nonzero(w==z)
            buildingAmount_epochMultiple+=temp_count
            # print("%d---z:"%i,buildingAmount_epochMultiple)
            #更新栅格属性值，尤其compress栅格压缩，及dtype数据类型的配置，可以大幅度降低栅格数据量
            profile.update(
                width=win.width, 
                height=win.height,
                count=1,
                transform=win_transform,
                compress='lzw',
                dtype=rasterio.int8
                )
            # with rasterio.open(os.path.join(saveRasterByBlock_fp,"testingBlock.tif"), 'w', driver='GTiff' width=512, height=256, count=1,dtype=w.dtype,**profile) as dst:
            with rasterio.open(os.path.join(newPath,"buildingHeight_%d.tif"%i), 'w', **profile) as dst:
                dst.write(w, window=Window(0,0,win.width,win.height), indexes=1)              
                  
            i+=1     
            #在正式计算前，通过break，仅对部分数据编写与调整代码
            # if i ==2:
            #     break    
        np.save(os.path.join(dataSave_fp,"data_%d.npy"%zValue),buildingAmount_epochMultiple) 
        buildingAmount[zValue]=buildingAmount_epochMultiple
        print("_"*50)
        print("%d---zValue has completed!!!"%zValue)
        b_T= datetime.datetime.now()
        print("time span:", b_T-a_T)
    print("_"*50)      
    print("total amount:",buildingAmount)
    np.save(os.path.join(dataSave_fp,"buildingFrequency.npy"),buildingAmount)
    
    return buildingAmount
    
if __name__=="__main__":  
    rasterFp=r"E:\spatialStructure_temp\transfer\buidingHeightRaseter.tif"
    saveRasterByBlock_fp=r"E:\spatialStructure_temp\BUildingHeight\output"
    dataSave_fp=r"E:\spatialStructure_temp\BUildingHeight\output_data"
    
    totalWidth,totalHeight=rasterProperties(rasterFp)
    # readWriteRasterByBlock(rasterFp,saveRasterByBlock_fp)

    
    # rasterio_wins=rasterio_windows(21,15,5,3)
    #根据不同的栅格大小，自行调整subWidth和subHeight，满足内存要求
    subWidth=60000
    subHeight=60000
    rasterio_wins=rasterio_windows(totalWidth,totalHeight,subWidth,subHeight)
    buildingAmount=RWRasterBlocks(rasterFp, dataSave_fp,rasterio_wins)
    
    buildingAmount_load=np.load(os.path.join(dataSave_fp,"buildingFrequency.npy"),allow_pickle=True)