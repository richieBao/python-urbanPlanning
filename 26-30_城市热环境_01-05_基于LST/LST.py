# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:31:58 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
"""
import gdal,os,re,sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import math
from skimage import exposure
from distutils.version import LooseVersion
from scipy.ndimage.filters import gaussian_filter
import skimage
from skimage.transform import rescale
from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering
from scipy.signal import convolve2d   #2d卷积
from matplotlib import cm
from matplotlib.colors import LightSource
from dbfread import DBF
from sklearn.metrics import precision_score,recall_score,f1_score,confusion_matrix
from sklearn.metrics import explained_variance_score
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码/针对gdal
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码/针对gdal

dataPath=r"C:\Users\Richi\sf_richiebao\sf_geodata\landsat_data\LC08_L1TP_127036_20180810_20180815_01_T1" #数据来源于美国地质勘探局（United States Geological Survey, USGS）下载Landsat OLI 8
resultsPath=r"C:\Users\Richi\sf_richiebao\sf_code\results\LST_results\20180815" #配置保存结果数据的路径

#dataPath=r"C:\Users\Richi\sf_richiebao\sf_geodata\landsat_data\LC08_L1TP_127036_20190117_20190131_01_T1"
#resultsPath=r"C:\Users\Richi\sf_richiebao\sf_code\results\LST_results\20190131"

#！基础类
class AUXILIARY:     
##配置工作环境
    def __init__(self,dataPath='',resultsPath=''):
        self.dataPath=dataPath
        self.resultsPath=resultsPath
 
##读取landsat *_MTL.txt文件，提取需要的信息
    def MTL_info(self):
        fp=[os.path.join(root,file) for root, dirs, files in os.walk(self.dataPath) for file in files] #提取文件夹下所有文件的路径
#        print(fp)
        MTLPattern=re.compile(r'_MTL.txt',re.S) #匹配对象模式，提取_MTL.txt遥感影像的元数据文件
#        print(re.findall(MTLPattern,fp[6]))
        MTLFn=[fn for fn in fp if re.findall(MTLPattern,fn)][0]
#        print(MTLFn)
        with open(MTLFn,'r') as f: #读取所有元数据文件信息
            MTLText=f.read()
#        print(MTLText)
        file_name_bandPattern=re.compile(r'FILE_NAME_BAND_[0-9]\d* = "(.*?)"\n',re.S)  #Landsat 波段文件
        file_name_band=re.findall(file_name_bandPattern,MTLText)
#        print(file_name_band)
#        file_name_bandFp=[[(fn, re.findall(r'.*?%s$'%fn,f)[0]) for f in fp if re.findall(r'.*?%s$'%fn,f)] for fn in file_name_band] #(文件名，文件路径)
#        print(file_name_bandFp)
        file_name_bandFp=[[(re.findall(r'B[0-9]\d*',fn)[0], re.findall(r'.*?%s$'%fn,f)[0]) for f in fp if re.findall(r'.*?%s$'%fn,f)] for fn in file_name_band] #(文件名，文件路径)
        file_name_bandFp={i[0][0]:i[0][1] for i in file_name_bandFp}
#        print(file_name_bandFp)
        
        #需要数据的提取标签/根据需要读取元数据信息
        values_fields=["RADIANCE_ADD_BAND_10",
                       "RADIANCE_ADD_BAND_11",
                       "RADIANCE_MULT_BAND_10",
                       "RADIANCE_MULT_BAND_11",
                       "K1_CONSTANT_BAND_10",
                       "K2_CONSTANT_BAND_10",
                       "K1_CONSTANT_BAND_11",
                       "K2_CONSTANT_BAND_11",
                       "DATE_ACQUIRED",
                       "SCENE_CENTER_TIME",
                       "MAP_PROJECTION",
                       "DATUM",
                       "UTM_ZONE"]
        
        parameterValues={field:re.findall(re.compile(r'%s = "*(.*?)"*\n'%field),MTLText)[0] for field in values_fields} #（参数名，参数值）
#        print(parameterValues)
        return file_name_bandFp,parameterValues #返回所有波段路径和需要的参数值
        
##栅格数据读取程序，.tif,单波段。读取需要的波段数据并存储。未裁切影像方法
    def singleBand(self, rasterFp):
        gdal.UseExceptions()        
        '''打开栅格数据'''
        try:
            src_ds=gdal.Open(rasterFp)
        except RuntimeError as e:
            print( 'Unable to open %s'% rasterFp)
            sys.exit(1)
        #获取栅格信息
        rasterInfo={"RasterXSize":src_ds.RasterXSize,
                    "RasterYSize":src_ds.RasterYSize,
                    "RasterProjection":src_ds.GetProjection(),
                    "GeoTransform":src_ds.GetGeoTransform()}
        
        '''获取单波段像元值'''
        bandValue=src_ds.GetRasterBand(1).ReadAsArray().astype(np.float)
        print("readed rasterDate!")
        return bandValue,rasterInfo #返回该波段，为数组形式

#影像数据裁切
    def rasterClip(self,rasterFp):
        gdal.UseExceptions()
        try:
            src_ds=gdal.Open(rasterFp)
        except RuntimeError as e:
            print( 'Unable to open %s'% rasterFp)
            sys.exit(1)            
        print( "[ RASTER BAND COUNT ]: ", src_ds.RasterCount)
        bands=[]
        for band in range( src_ds.RasterCount ):
            band += 1
            print( "[ GETTING BAND ]: ", band)
            srcband = src_ds.GetRasterBand(band)
            if srcband is None:
                continue        
            stats = srcband.GetStatistics(True,True) #计算统计值
            if stats is None:
                continue        
            print( "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % (stats[0], stats[1], stats[2], stats[3] )  )          
            bands.append(srcband)
#            print(bands)
        print(bands[0].ReadAsArray().shape)
#        self.arrayShow(bands[0].ReadAsArray())
        #定义切图的起始点坐标，相比原点的横纵坐标偏移量   
        offset_x=3200 #行
        offset_y=4400 #列
        
        #定义切图的大小
        block_xsize=1800 #行
        block_ysize=1800 #列
        
        #按照矩形区域提取每个波段的数据，设置的范围不能大于原始影像的区域，如果超出，则发生异常
        outBands=[band.ReadAsArray(offset_x, offset_y, block_xsize, block_ysize) for band in bands]
#        print(outBands)
        print(outBands[0].shape)
        self.arrayShow(outBands[0])

        #建立.tif驱动drive
        gtifDriver=gdal.GetDriverByName("GTiff")
        print("_________",bands[0].DataType)
        out_ds=gtifDriver.Create(os.path.join(resultsPath,"clip.tif"),block_xsize, block_ysize,src_ds.RasterCount,bands[0].DataType)
        print("Creating new .tif")
        
        #获取原影像的原点坐标信息
        ori_transform = src_ds.GetGeoTransform()
        if ori_transform:
            print (ori_transform)
            print("Origin = ({}, {})".format(ori_transform[0], ori_transform[3]))
            print("Pixel Size = ({}, {})".format(ori_transform[1], ori_transform[5]))        
        
        # 读取影像仿射变换参数值
        top_left_x = ori_transform[0]  # 左上角x坐标
        w_e_pixel_resolution = ori_transform[1] # 东西方向像素分辨率
        top_left_y = ori_transform[3] # 左上角y坐标
        n_s_pixel_resolution = ori_transform[5] # 南北方向像素分辨率   

        # 根据反射变换参数计算新图的原点坐标
        top_left_x = top_left_x + offset_x * w_e_pixel_resolution
        top_left_y = top_left_y + offset_y * n_s_pixel_resolution        
        
        # 将计算后的值组装为一个元组，以方便设置
        dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])
        
        # 设置裁剪出来图的原点坐标
        out_ds.SetGeoTransform(dst_transform)
        
        # 设置SRS属性（投影信息）
        out_ds.SetProjection(src_ds.GetProjection())  
        for band in range( src_ds.RasterCount ):
            band += 1
            out_ds.GetRasterBand(band).WriteArray(outBands[band-1])
            
        # 将缓存写入磁盘
        out_ds.FlushCache()
        print("FlushCache succeed")     
        
        del out_ds
        print("clipping succeed!!!")
        #获取栅格信息
        rasterInfo={"RasterXSize":block_xsize,
                    "RasterYSize":block_ysize,
                    "RasterProjection":src_ds.GetProjection(),
                    "GeoTransform":dst_transform}   
        
        return outBands[0],rasterInfo

##栅格数据显示查看程序
    def rasterShow(self, rasterFp):    
        try:
            rasterArray=gdalnumeric.LoadFile(rasterFp)  #加载栅格数据为gdal数组格式
        except RuntimeError:
            print("Unable to open %s"%rasterFp)
        multiple=2 #配置图像大小的倍数
        fig=plt.figure(figsize=(20*multiple, 12*multiple))
        ax=fig.add_subplot(111)
        plt.xticks([x for x in range(rasterArray.shape[0]) if x%200==0])
        plt.yticks([y for y in range(rasterArray.shape[0]) if y%200==0])
        ax.imshow(rasterArray)

##计算数据(数组)显示
    def arrayShow(self,data):            
        multiple=2 #配置图像大小的倍数
        fig=plt.figure(figsize=(20*multiple, 12*multiple))
        ax=fig.add_subplot(111)
        plt.xticks([x for x in range(data.shape[0]) if x%200==0])
        plt.yticks([y for y in range(data.shape[0]) if y%200==0])
#        print("*"*20,data.shape)
        ax.imshow(data) 

##保存栅格数据，1个波段      
    def rasterRW(self, LSTValue,resultsPath,LSTSavingFn,para):
        gdal.UseExceptions()    
    #    '''打开栅格数据'''
    #    try:
    #        src_ds=gdal.Open(os.path.join(resultsPath,LSTSavingFn))
    #    except RuntimeError as e:
    #        print( 'Unable to open %s'% os.path.join(resultsPath,LSTSavingFn))
    #        print(e)
    #        sys.exit(1)
    #    print("metadata:",src_ds.GetMetadata())   
      
        '''初始化输出栅格'''
        driver=gdal.GetDriverByName('GTiff')
        print(para['RasterXSize'],para['RasterYSize'])
        out_raster=driver.Create(os.path.join(resultsPath,LSTSavingFn),para['RasterXSize'],para['RasterYSize'],1,gdal.GDT_Float64)
        out_raster.SetProjection(para['RasterProjection']) #设置投影与参考栅格同
        out_raster.SetGeoTransform(para['GeoTransform']) #配置地理转换与参考栅格同
        
        '''将数组传给栅格波段，为栅格值'''
        out_band=out_raster.GetRasterBand(1)
        out_band.WriteArray(LSTValue)
        
    #    '''设置overview'''
    #    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    #    out_raster.BuildOverviews('average', overviews)
        
        '''清理缓存与移除数据源'''
        out_band.FlushCache()
        out_band.ComputeStatistics(False)
    #    del src_ds,out_raster,out_band        
        del out_raster,out_band

##解译精度评价。采样的数据是使用GIS平台人工判断提取，样例文件在Github中获取。
    def InterpretaionACCuracyEstimaton(self,InterAccuEstiFp):
        NDVITable=DBF(InterAccuEstiFp,load=True) #读取存储有采样数据的.dbf类型文件
#        print(NDVITable)
        fieldName=[name for name in NDVITable.field_names]
        print(fieldName)
        records=[[record[field] for field in record] for record in NDVITable]
        val=np.array(records).T
        val_true=val[1]
#        print(val_true)
        val_interpretation=val[2]
#        print(val_interpretation)
        
        b=0.3
        c=2.5 
        d=500
        #转换采样数据数值，保持与解译数据同，以用于计算混淆矩阵，进行精度评价
        val_interpre=np.copy(val_interpretation)
        val_interpre[val_interpre<b]=1000
        val_interpre[(val_interpre>=b)&(val_interpre<c)]=2000
        val_interpre[(val_interpre>=c)&(val_interpre<d)]=3000
        val_interpre[val_interpre==1000]=1
        val_interpre[val_interpre==2000]=2
        val_interpre[val_interpre==3000]=3
#        print(val_interpre)        
        val_true=np.array(val_true,dtype=np.int)
        val_interpre=np.array(val_interpre,dtype=np.int)
        print(val_true.shape,val_interpre.shape)
        print(val_true,"\n",val_interpre)
        
        confMat=confusion_matrix(y_true=val_true,y_pred=val_interpre)
        print(confMat)
        print(np.sum(confMat.diagonal())/150)     

##直方图与拟合曲线
    def histogramFig(self,x):
        sns.set_palette("hls") 
        f, ax= plt.subplots(figsize = (20, 20))
        sns.distplot(x, hist=False, color="r", kde_kws={"shade": True},ax=ax)
        ax.tick_params(labelsize=30) 
        plt.show()    

##箱型图        
    def boxplot_outlier(self,data):
        fig, ax = plt.subplots(figsize=(20,20))
        ax.boxplot(data)
        ax.set_title("don't show\noutlier points")
        plt.show()

#！定义LST计算类
class LST():
##初始化相关值
    def __init__(self,b10,b11,b4,b5,parameterValues):
        self.b10Value=b10
        self.b11Value=b11
        self.RED=b4
        self.NIR=b5
        self.paraVal=parameterValues
        
##计算TOA(top of atmosphere)，单窗算法结合Landsat OLI 8热红外数据反演。参考文献“Estimation of Land Surface Temperature using LANDSAT 8 Data”，类似阐述文章很多，建议翻墙Google搜索
    def TOARadiance(self,Qcal,ML,AL): #TOA spectral radiance (Watts/ (m2 * sr * μm))
        return ML*Qcal+AL #ML = Radiance multiplicative Band (No.);AL = Radiance Add Band (No.);Qcal = Quantized and calibrated standard product pixel values (DN)
    def TOABrightnessTemperature(self,TOARadianceVal,K1,K2): #Top of atmosphere brightness temperature (°C)
#        return K2/np.log(K1/TOARadianceVal+1.0)-272.15 
        return (K2/np.log(K1/TOARadianceVal+1.0))-272.15 #TOARadianceVal = TOA spectral radiance (Watts/( m2 * sr * μm));K1 = K1 Constant Band (No.);K2 = K2 Constant Band (No.)
                
    def TOAAverage(self):
        b10TOARadianceVal=self.TOARadiance(self.b10Value,float(self.paraVal["RADIANCE_MULT_BAND_10"]),float(self.paraVal["RADIANCE_ADD_BAND_10"]))
        b10TOABTemperature=self.TOABrightnessTemperature(b10TOARadianceVal,float(self.paraVal["K1_CONSTANT_BAND_10"]),float(self.paraVal["K2_CONSTANT_BAND_10"]))
        b11TOARadianceVal=self.TOARadiance(self.b11Value,float(self.paraVal["RADIANCE_MULT_BAND_11"]),float(self.paraVal["RADIANCE_ADD_BAND_11"]))
        b11TOABTemperature=self.TOABrightnessTemperature(b11TOARadianceVal,float(self.paraVal["K1_CONSTANT_BAND_11"]),float(self.paraVal["K2_CONSTANT_BAND_11"]))       
        
        TOA=(b10TOABTemperature+b11TOABTemperature)/2
        return TOA,b10TOABTemperature,b11TOABTemperature

#计算NDVI
    def NDVI(self,RED,NIR):
        RED=np.ma.masked_where(NIR+RED==0,RED)
        NDVI=(NIR-RED)/(NIR+RED)
        NDVI=NDVI.filled(-999)
#        print(NDVI)
        print("!"+"_min:%f,max:%f"%(NDVI.min(),NDVI.max()))
        return NDVI
    
# 计算 Land Surface Emissivity (LSE):  
    def LSE(self,NDVI):
        PV=np.power((NDVI-NDVI.min())/(NDVI.max()+NDVI.min()),2)
        E=0.004*PV+0.986
        return E

#计算LST
    def LST(self,BT,W,E):
        LST=(BT/1)+W*(BT/14380)*np.log(E)
        return LST
#计算B10，B11的LST的均值
    def LSTAverage(self):
        E=self.LSE(self.NDVI(self.RED,self.NIR))
        _,b10TOABTemperature,b11TOABTemperature=self.TOAAverage()
        LSTB10=self.LST(b10TOABTemperature,self.b10Value,E)
        LSTB11=self.LST(b11TOABTemperature,self.b11Value,E)
        return (LSTB10+LSTB11)/2
      
    
#！分析数据，并建立机器学习/深度学习模型类。地物/用地分类与LST的关系等
class DLModel_preprocessing():
    def __init__(self,NDVIVal,LSTVal):
        self.NDVIVal=NDVIVal
        self.LSTVal=LSTVal        

##基于NDVI 解译水体/绿地/裸地 
    def interpret_NDVI(self,NDVI):
        #20180810年影像的阈值配置。计算NDVI，通过人工判读确定3个分类的阈值区域分别为：NDVI建成区<0.3，0.3<=NDVI绿地<2.5，NDVI水体>=2.5 通常根据自己待分析的影像重新配置。一般在GIS平台观察NDVI阈值范围    
        b=0.3
        c=2.5 
        d=500
#        print(NDVI)
        print(NDVI.shape)
        NDVIClassify=np.copy(NDVI)
        NDVIClassify[NDVIClassify<b]=1000
        print(NDVIClassify.min())
        NDVIClassify[(NDVIClassify>=b)&(NDVIClassify<c)]=2000
        print(NDVIClassify.min())
        NDVIClassify[(NDVIClassify>=c)&(NDVIClassify<d)]=3000
        NDVIClassifyInt=NDVIClassify.astype(np.int)
        print(np.unique(NDVIClassifyInt))     
        
        return NDVIClassifyInt
    
##将栅格数据分为多个单元块，每一个单元块为一个样本(sample)数据，划分的单元数量越多，越有利于模型训练
    def trainBlock(self,array,row,col):
        arrayShape=array.shape
        print(arrayShape)
        rowPara=divmod(arrayShape[1],row)  #divmod(a,b)方法为除法取整，以及a对b的余数
        colPara=divmod(arrayShape[0],col)
        extractArray=array[:colPara[0]*col,:rowPara[0]*row]  #移除多余部分，规范数组，使其正好切分均匀
    #    print(extractArray.shape)
        hsplitArray=np.hsplit(extractArray,rowPara[0])
        flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]
        vsplitArray=flatten_lst([np.vsplit(subArray,colPara[0]) for subArray in hsplitArray])
        dataBlock=flatten_lst(vsplitArray)
        print("样本量：%s"%(len(dataBlock)))  #此时切分的块数据量，就为样本数据量
        
        '''显示查看其中一个样本'''     
        subShow=dataBlock[-2]
        print(subShow,'\n',subShow.max(),subShow.std())
        fig=plt.figure(figsize=(20, 12))
        ax=fig.add_subplot(111)
        plt.xticks([x for x in range(subShow.shape[0]) if x%400==0])
        plt.yticks([y for y in range(subShow.shape[1]) if y%200==0])
        ax.imshow(subShow)    
        
        dataBlockStack=np.append(dataBlock[:-1],[dataBlock[-1]],axis=0) #将列表转换为数组
        print(dataBlockStack.shape)
        return dataBlockStack    
    
#主程序：数据准备/预处理
def main():
    aux=AUXILIARY(dataPath,resultsPath)
#    print(aux.dataPath)
    file_name_bandFp,parameterValues=aux.MTL_info() #获取遥感影像元数据信息
#    bandFp=file_name_bandFp['B10']
#    aux.rasterClip(bandFp)

#    b10Value,b10rasterInfo=aux.singleBand(file_name_bandFp['B10'])
#    b11Value,b11rasterInfo=aux.singleBand(file_name_bandFp['B11'])
#    b4Value,b4rasterInfo=aux.singleBand(file_name_bandFp['B4'])
#    b5Value,b5rasterInfo=aux.singleBand(file_name_bandFp['B5'])
    #获取波段信息
    b10Value,b10rasterInfo=aux.rasterClip(file_name_bandFp['B10'])
    b11Value,b11rasterInfo=aux.rasterClip(file_name_bandFp['B11'])
    b4Value,b4rasterInfo=aux.rasterClip(file_name_bandFp['B4'])
    b5Value,b5rasterInfo=aux.rasterClip(file_name_bandFp['B5'])    
    
#    aux.rasterShow(bandFp)
      
    lst=LST(b10Value,b11Value,b4Value,b5Value,parameterValues,)
#    TOARadianceVal=lst.TOARadiance(b10Value,float(parameterValues["RADIANCE_MULT_BAND_10"]),float(parameterValues["RADIANCE_ADD_BAND_10"]))
#    TOABTemperature=lst.TOABrightnessTemperature(TOARadianceVal,float(parameterValues["K1_CONSTANT_BAND_10"]),float(parameterValues["K2_CONSTANT_BAND_10"]))
#    TOA=lst.TOAAverage()
    NDVI=lst.NDVI(b4Value,b5Value) #计算归一化植被指数NDVI
    aux.arrayShow(NDVI)
    LSTValue=lst.LSTAverage() #反演地表温度
    aux.arrayShow(LSTValue)
    
    LSTSavingFn=r'LST.tif' 
    aux.rasterRW(LSTValue,resultsPath,LSTSavingFn,b10rasterInfo) #将需要在GIS平台中加载进一步分析的数据，写入硬盘存储
    
    NDVISavingFn=r'NDVI.tif' 
    aux.rasterRW(NDVI,resultsPath,NDVISavingFn,b10rasterInfo)
    
    '''建立数据集，用于机器学习或深度学习计算'''
    Model_MLP=DLModel_preprocessing(NDVI,LSTValue)
    NDVIClassifyInt=Model_MLP.interpret_NDVI(NDVI)
    aux.arrayShow(NDVIClassifyInt)
    row=100 #500
    col=100 #500
    NDVIClassifyBlockStack=Model_MLP.trainBlock(NDVIClassifyInt,row,col)
    LSTBlockStack=Model_MLP.trainBlock(LSTValue,row,col)

    return NDVIClassifyBlockStack,LSTBlockStack,LSTValue,b10rasterInfo
    
##建立用于LST进一步分析的函数方法
class LSTAnalysis():
    def __init__(self,LST):
        self.LST=LST
##应用spectral_clustering（）聚类。此次实验中，深入分析时未使用该数据，可以自行解读所建立的区域反映LST数据的含义
    def LSTClustering(self):
        # 参考“Segmenting the picture of greek coins in regions”方法，Author: Gael Varoquaux <gael.varoquaux@normalesup.org>, Brian Cheung
        # License: BSD 3 clause
        orig_coins=self.LST
        # these were introduced in skimage-0.14
        if LooseVersion(skimage.__version__) >= '0.14':
            rescale_params = {'anti_aliasing': False, 'multichannel': False}
        else:
            rescale_params = {}
        smoothened_coins = gaussian_filter(orig_coins, sigma=2)
        rescaled_coins = rescale(smoothened_coins, 0.2, mode="reflect",**rescale_params)        
        # Convert the image into a graph with the value of the gradient on the
        # edges.
        graph = image.img_to_graph(rescaled_coins)        
        # Take a decreasing function of the gradient: an exponential
        # The smaller beta is, the more independent the segmentation is of the
        # actual image. For beta=1, the segmentation is close to a voronoi
        beta = 10
        eps = 1e-6
        graph.data = np.exp(-beta * graph.data / graph.data.std()) + eps        
        # Apply spectral clustering (this step goes much faster if you have pyamg
        # installed)
        N_REGIONS = 200        
        for assign_labels in ('discretize',):
#        for assign_labels in ('kmeans', 'discretize'):
            t0 = time.time()
            labels = spectral_clustering(graph, n_clusters=N_REGIONS,assign_labels=assign_labels, random_state=42)
            t1 = time.time()
            labels = labels.reshape(rescaled_coins.shape)
        
            plt.figure(figsize=(5*3, 5*3))
            plt.imshow(rescaled_coins, cmap=plt.cm.gray)
            for l in range(N_REGIONS):
                plt.contour(labels == l,
                            colors=[plt.cm.nipy_spectral(l / float(N_REGIONS))])
            plt.xticks(())
            plt.yticks(())
            title = 'Spectral clustering: %s, %.2fs' % (assign_labels, (t1 - t0))
            print(title)
            plt.title(title)
        plt.show()

##基于卷积温度梯度变化界定冷区和热区的空间分布结构
    def LSTConvolue(self):
        kernel_rate= np.array([[1/8, 1/8 , 1/8],
                              [1/8, -1, 1/8],
                              [1/8, 1/8, 1/8]])  #卷积核    
        kernel_id= np.array([[-1, -1 ,-1],
                                [-1 ,8, -1],
                                [-1, -1, -1]])  #卷积核        
        kernel=kernel_rate
        t0=time.time()
#        print(self.LST)
        array_convolve2d=convolve2d(self.LST,kernel,mode='same')*-1
#        print(array_convolve2d.max(),array_convolve2d.min())
#        array_convolve2d=exposure.equalize_hist(array_convolve2d)
        p2, p98 = np.percentile(array_convolve2d, (2,96))
        array_convolve2dRescale = exposure.rescale_intensity(array_convolve2d, in_range=(p2, p98))
#        print()
        array_convolve2dZero=np.copy(array_convolve2d)
        array_convolve2dZero[array_convolve2dZero>0]=1
        array_convolve2dZero[array_convolve2dZero<0]=-1
        array_convolve2dZero[array_convolve2dZero==0]=0
        
        
        t1=time.time()
        t_convolve2d=t1-t0
        print("lasting time:",t_convolve2d)
        
        self.imgShow(imges=(self.LST,array_convolve2dRescale,array_convolve2dZero),titleName=("array","array_convolve2d_rescale","0",),xyticksRange=(1,1))
      
        return array_convolve2d,array_convolve2dZero
        
##显示图像
    def imgShow(self,imges,titleName,xyticksRange=False): #imges参数为元组，可以传入多个图像；titleName对应imges参数设置名称字符串元组；xyticksRange参数用于设置轴坐标间距
        axNum=len(imges)
        print(int(axNum/2))
        nColumn=3  #可以自行根据图数量，调整排布数量
        width=15*3
        figsize=(width, width/nColumn)
        fig,axes=plt.subplots(math.ceil(axNum/nColumn),nColumn,sharex=True,sharey=True,figsize=figsize)
        ax=axes.flatten()
        for i in range(axNum): #循环设置子图             
            ax[i].imshow(imges[i])
            if xyticksRange:
                ax[i].set_xticks([x for x in range(imges[i].shape[1]) if x%xyticksRange[0]==0])
                ax[i].set_yticks([y for y in range(imges[i].shape[0]) if y%xyticksRange[1]==0])
            else:
                ax[i].set_xticks([])  
                ax[i].set_yticks([])  
            ax[i].set_title(titleName[i])           
        fig.tight_layout()
        plt.show()

##三维显示数据，并显示剖面线，可以分析数据三维空间的变化    
    def ThrShow(self,data):        
        font1 = {'family' : 'STXihei',
         'weight' : 'normal',
         'size'   : 50,
         }
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'),figsize=(50,20))
        ls = LightSource(data.shape[0], data.shape[1])
        rgb = ls.shade(data, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
        x=np.array([list(range(data.shape[0]))]*data.shape[1])
        print(x.shape,x.T.shape,data.shape)
        surf = ax.plot_surface(x, x.T, data, rstride=1, cstride=1, facecolors=rgb,linewidth=0, antialiased=False, shade=False,alpha=0.3)
        fig.colorbar(surf,shrink=0.5,aspect=5)
        cset = ax.contour(x, x.T, data, zdir='z', offset=37, cmap=cm.coolwarm)
        cset = ax.contour(x, x.T, data, zdir='x', offset=-30, cmap=cm.coolwarm)
        cset = ax.contour(x, x.T, data, zdir='y', offset=-30, cmap=cm.coolwarm)
        plt.show()
           

if __name__=="__main__":  
    pass
    NDVIBlockStack,LSTBlockStack,LSTValue,b10rasterInfo=main()
#    DL=DataLoader()
#    DL.dataSet()
#    DL.load_batch()
#    NDVIClassifyBlockStack,LSTBlockStack=main()
    
#    LSTA= LSTAnalysis(LSTBlockStack[5])
#    LSTA= LSTAnalysis(LSTValue)
#    LSTA.LSTClustering()
#    array_convolve2d,array_convolve2dZero=LSTA.LSTConvolue()
#    aux=AUXILIARY(dataPath,resultsPath)
    
#    InterAccuEstiFp=r'C:\Users\Richi\sf_richiebao\sf_code\results\LST_results\20180815\NDVI201808Cla.dbf'
#    aux.InterpretaionACCuracyEstimaton(InterAccuEstiFp)
    
#    convolve2dZeroSavingFn=r'convolve2dZero.tif'
#    aux.rasterRW(array_convolve2dZero,resultsPath,convolve2dZeroSavingFn,b10rasterInfo)
#    LSTA.ThrShow(LSTBlockStack[4])
#    LSTA.ThrShow(array_convolve2d[10:90,10:90])
#    
#    LSTDiffFp=r'C:\Users\Richi\sf_richiebao\sf_code\results\LST_results\LSTSDifferent.tif'
#    LSTDiffVal,LSTDiffInfo=aux.singleBand(LSTDiffFp)
#    LSTDiffFlatten=LSTDiffVal.flatten()
#    aux.histogramFig(LSTDiffFlatten)
#    aux.boxplot_outlier(LSTDiffFlatten)
    
#    aux.histogramFig(LSTValue.flatten())