# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 09:36:24 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import rasterio,os,gc,h5py,datetime,scipy
from rasterio.windows import Window
from tqdm import tqdm
import numpy as np
from numba import jit, cuda,njit
import datetime
import numba 
from joblib import Memory
import tables
from numba import jit,cuda,njit
from tempfile import mkdtemp
import os.path as path
import scipy.ndimage


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
    print("raster windows amount:",len(wins))
    return wins


# @njit(parallel=True)
# @cuda.jit(debug=True)
def ArrayCoordi(rasterArray):
    relativeCellCoords=np.indices(rasterArray.shape)
    relativeCellCoords2D=np.stack(relativeCellCoords,axis=2).reshape(-1,2)
    del relativeCellCoords
    # print(relativeCellCoords2D_O)                              
    return relativeCellCoords2D


#计算首尾坐标，用到三角函数
# @profile #内存监测所标识的函数
# @cuda.jit(debug=True)
# @njit(parallel=True)
#计算首尾坐标，用到三角函数
# @profile #内存监测所标识的函数
def equalCircleDivide(originalCoordiArray,radious,lineProfileAmount):
    # print(originalCoordiArray.shape)
    angle_s=360/lineProfileAmount
    angle_array=np.array([i*angle_s for i in range(lineProfileAmount)],dtype=np.float32)
    #.astype(np.float16)
    opposite=np.sin(np.radians(angle_array),dtype=np.float16)*radious
    opposite=opposite.astype(np.float32)
    # print(opposite.dtype)
    yCoordi=np.add(opposite,originalCoordiArray[:,1].reshape(-1,1),dtype=np.float32)
    del opposite
    # print(yCoordi.dtype)
    
    adjacent=np.cos(np.radians(angle_array),dtype=np.float16)*radious
    xCoordi=np.add(adjacent,originalCoordiArray[:,0].reshape(-1,1),dtype=np.float32)
    del adjacent,angle_array
    # print(xCoordi.dtype)
    
    CoordiArray=np.stack((xCoordi,yCoordi),axis=-1)
    # print(CoordiArray.dtype)
    # del xCoordi,yCoordi
    return CoordiArray

#计算障碍角度和高度,以及SVF值。参考文献：城区复杂下垫面天空视域因子参数化方法——以北京鸟巢周边地区为例
# @profile #内存监测所标识的函数
# @cuda.jit(debug=True)
# @njit(parallel=True)    
def SVF(radious,equalDistance,ziList,j):
    segment=radious/equalDistance
    distanceList=np.array([i*segment for i in range(equalDistance+1)],dtype=np.float32)
    distanceList=distanceList[1:]

    ziListSub=ziList[:,:,1:]
    ziListOrigin=ziList[:,:,0]
    
    sinValues=np.true_divide(np.subtract(ziListSub,np.expand_dims(ziListOrigin, axis=2)),np.sqrt(np.add(np.power(distanceList,2),np.power(np.subtract(ziListSub,np.expand_dims(ziListOrigin, axis=2)),2))))
    
    sinMaxValue=np.amax(sinValues,axis=2)
    del sinValues
    SVFValue=1-np.true_divide(np.sum(sinMaxValue, axis=1),sinMaxValue.shape[-1])
    
    # SVFValueFn=os.path.join(saveFp,"SVFValue_%d"%(j))            
    # np.save(SVFValueFn, SVFValue)    
    # del SVFValue
    # print("SVF Value saved:%d"%i)    
    # with open(os.path.join(saveFp,"SVFValue_filenames.txt"), "a") as text_file:
    #     text_file.write("%s\n"%SVFValueFn)
        
    return SVFValue.astype(np.float32)


#数组延直线截面提取单元值
# @profile #内存监测所标识的函数
# @cuda.jit(debug=True)
# @njit(parallel=True)
def lineProfile(zValue,originalPoint,endPoint): 
    num=equalDistance+1
    
    x0=originalPoint[:,0].reshape(-1,1)
    x1=endPoint[:,:,0]
    # print(x0.dtype)
    # print(x1.dtype)
    x=np.linspace(x0, x1, num,dtype=np.int) #可以不用修改数组类型。出于内存优化考虑,会加快后续np.stack计算速度
    del x0,x1
    # fp[:]=np.linspace(x0, x1, num,dtype=np.int)[:]
    
    
    y0=originalPoint[:,1].reshape(-1,1)  
    y1=endPoint[:,:,1]
    y=np.linspace(y0, y1, num,dtype=np.int)
    del y0,y1
    
    xStack=np.stack(x,axis=-1)
    # xStackSplit=np.array_split(xStack,saveN) #为减缓单次数组计算量，切分数组为saveN个单个数组，切分量越大，单个数组越小，计算所占用内存越小
    # del xStack #清空该变量，释放内存.关于numpy array占据内存的大小，查找确认
    # print("xStack finished!")
    
    yStack=np.stack(y,axis=-1)
    # yStackSplit=np.array_split(yStack,saveN)
    # del yStack
    del x,y

    zi = scipy.ndimage.map_coordinates(zValue,[xStack,yStack],cval=0,mode="nearest",order=0) #根据数组索引值，提取实际值
    del xStack,yStack
    

    # #记录每次存储的数据路径为.txt文件，最后通过该文件读取所有数据，组合与写入raster格式文件
    # with open(os.path.join(saveFp,"SVFValue_filenames.txt"), "a") as text_file:
    #     text_file.write("%s\n"%SVFValueFn)
    return zi

#read raster blocks 分批读取较大栅格数据，并计算
def SVF_Wins(rasterFp,dataSave_fp, windowsList):
    i=0
    for win in tqdm(windowsList):            
        with rasterio.open(rasterFp,"r+") as src:                
            src.nodata=-1
            w = src.read(1, window=win) 
            # print("_"*50)
            # print(w.shape)
            profile=src.profile
            win_transform=src.window_transform(win)    
        # print("_"*50)    
        # print(w.shape)
        # print(ok)
        '''计算部分'''
        # coordiArray=equalCircleDivide(T,radious,lineProfileAmount)  
        relativeCellCoords2D=ArrayCoordi(w)
        # print(relativeCellCoords2D)
        # print("+"*50)
        a_T = datetime.datetime.now()
        coordiArray=equalCircleDivide(relativeCellCoords2D,radious,lineProfileAmount)  
        b_T= datetime.datetime.now()
        print("qualCircleDivide time span:", b_T-a_T)
        # print(coordiArray)
        gc.collect()
        
        # print(coordiArray.shape)
        # print(relativeCellCoords2D.shape)
        c_T=datetime.datetime.now()
        zi=lineProfile(w,relativeCellCoords2D,coordiArray)
        d_T=datetime.datetime.now()
        print("lineProfile time span:",d_T-c_T)
        gc.collect()
        del coordiArray
        
        e_T=datetime.datetime.now()
        SVFValue=SVF(radious,equalDistance,zi,i)
        f_T=datetime.datetime.now()
        print("SVF time span:",d_T-c_T)
        # print(SVFValue.shape)
        gc.collect()
        del zi

        profile.update(
            width=win.width, 
            height=win.height,
            count=1,
            transform=win_transform,
            compress='lzw',
            dtype=rasterio.float32
            )
        # with rasterio.open(os.path.join(saveRasterByBlock_fp,"testingBlock.tif"), 'w', driver='GTiff' width=512, height=256, count=1,dtype=w.dtype,**profile) as dst:
       
        with rasterio.open(os.path.join(saveFp,"SVF3_%d.tif"%i), 'w', **profile) as dst:
            dst.write(SVFValue.reshape(w.shape), window=Window(0,0,win.width,win.height), indexes=1)              
              
        del SVFValue
        
        g_T=datetime.datetime.now()
        print("total time span:",g_T-a_T)
        
        i+=1     
        #在正式计算前，通过break，仅对部分数据编写与调整代码
        # if i ==1:
        #     break      


if __name__=="__main__":  
    tables.file._open_files.close_all() #关闭文件。该程序可忽略
    gc.collect() #释放缓存，IPython console 命令：%reset -f
    # rasterFp=r"D:\data\lidar\pdal_data\d.tif" #待计算SVF的栅格
    # rasterFp=r"D:\data\data_01_Chicago\pdal_data\chicago_loop_tile_0_0.tif"
    # rasterFp=r"F:\data_02_Chicago\parkNetwork\height_DSM-DTMInter.tif"
    rasterFp=r"F:\data_02_Chicago\ArcGisPro\parkNetwork\height_DSMDTMInter_3_a.tif"
    saveFp=r"F:\data_02_Chicago\parkNetwork\SVF"
    rasterFn=r"F:\data_02_Chicago\parkNetwork\SVF"    

    
    # mem_filename = path.join(saveFp, 'newfile.dat')
    # if os.path.exists(mem_filename):
    #     os.remove(mem_filename)
    # else:
    #     print("Can not delete the file as it doesn't exists,built new one!")
    # fp = np.memmap(mem_filename, dtype='float16', mode='w+', shape=(51, 25000000, 36))
    # print(fp.filename == path.abspath(mem_filename))
    
    totalWidth,totalHeight=rasterProperties(rasterFp)
    #根据不同的栅格大小，自行调整subWidth和subHeight，满足内存要求
    subWidth=3000
    subHeight=3000
    rasterio_wins=rasterio_windows(totalWidth,totalHeight,subWidth,subHeight)
    # print(ok)
    
    # hdf5Fn=os.path.join(saveFp,"cacheSVF.hdf5")
    # if os.path.exists(hdf5Fn):
    #     os.remove(hdf5Fn)
    # else:
    #     print("Can not delete the file as it doesn't exists,built new one!")
    # f=h5py.File(hdf5Fn, "a")

    
    #参数配置        
    rasterResolution=3 #计算栅格的分辨率    
    radious=100*rasterResolution #扫描半径
    lineProfileAmount=8#扫描截面数量36
    equalDistance=30 #每条扫描线的等分数量  50
    # saveN=12 #配置每块计算时，numpy数组一次性计算量，数值越大，单次数组计算量越小，单次计算占用内存越小。numpy 数组大小在1，000，000量时，内存16G，测试达到最大，如果超过该量值，则需要增加该参数值，即降低单次数组的大小。
    
    SVF=SVF_Wins(rasterFp, saveFp,rasterio_wins[:100])