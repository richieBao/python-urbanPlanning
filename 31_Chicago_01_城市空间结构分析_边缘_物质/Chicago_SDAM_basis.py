# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 20:21:48 2019

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
"""

import gdal,gdalnumeric
import numpy as np
import matplotlib.pyplot as plt
import copy,os,time,sys,pickle,re
from sklearn.cluster import DBSCAN
from tqdm import tqdm
from pylab import mpl

'''from kneed import DataGenerator, KneeLocator
因为kneed库无法正常加载，因此单独读取文件函数
kneed库官方地址：https://github.com/arvkevi/kneed
'''
from data_generator import DataGenerator
from knee_locator import KneeLocator

mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码/针对gdal
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码/针对gdal


landsat8Path=r"D:\data\RSImages\LC08_L1TP_023031_20180310_20180320_01_T1" #数据来源于美国地质勘探局（United States Geological Survey, USGS）下载Landsat OLI 8
resultsPath=r"D:\dataProcessing\codeResults" #配置保存结果数据的路径
modelSavePath=r"D:\dataProcessing\modelSave" #用于保存计算的模型

#待读取的分类数据，.tif格式
rasterDataPending={
        "rD_CL180310":r"D:\dataProcessing\dataResults\classification_LC08_201803103_clip.tif", #冬季
        "rD_CL190820":r"D:\dataProcessing\dataResults\classification_LC08_201808201_clip.tif", #夏季
        "rD_CL191018":r"D:\dataProcessing\dataResults\classification_LC08_201810181_clip.tif" #秋季   
        }

#！基础类
class baseClass:
##配置工作环境
    def __init__(self,landsat8Path='',resultsPath=''):
        self.landsat8Path=landsat8Path
        self.resultsPath=resultsPath    

'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
    def filePath(self,dirpath,fileType):
        fileInfo={}
        i=0
        for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
           i+=1
           #print(i,'\n')
           #print(dirpath,'\n',dirNames,'\n',fileNames,'\n')
           if fileNames: #仅当文件夹中有文件时才提取
               tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
               #if not tempList :
                   #print(i,"NULL")
               if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
                   fileInfo.setdefault(dirpath,tempList)
        return fileInfo  

'''读取landsat *_MTL.txt文件，提取需要的信息'''
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
    
'''栅格数据读取程序，.tif,单波段。读取需要的波段数据并存储。未裁切影像方法'''
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

'''影像数据裁切'''
    def rasterClip(self,rasterFp,clipRange):
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
#        offset_x=3200 #行
#        offset_y=4400 #列
#        
#        #定义切图的大小
#        block_xsize=1800 #行
#        block_ysize=1800 #列
        offset_x=clipRange[0]
        offset_y=clipRange[1]
        block_xsize=clipRange[2]
        block_ysize=clipRange[3]
        
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

'''保存栅格数据，1个波段'''      
    def rasterRW(self, rasterValue,resultsPath,rasterSavingFn,para):
        gdal.UseExceptions()    
    #    '''打开栅格数据'''
    #    try:
    #        src_ds=gdal.Open(os.path.join(resultsPath,rasterSavingFn))
    #    except RuntimeError as e:
    #        print( 'Unable to open %s'% os.path.join(resultsPath,rasterSavingFn))
    #        print(e)
    #        sys.exit(1)
    #    print("metadata:",src_ds.GetMetadata())   
      
        '''初始化输出栅格'''
        driver=gdal.GetDriverByName('GTiff')
        print(para['RasterXSize'],para['RasterYSize'])
        out_raster=driver.Create(os.path.join(resultsPath,rasterSavingFn),para['RasterXSize'],para['RasterYSize'],1,gdal.GDT_Float64)
        out_raster.SetProjection(para['RasterProjection']) #设置投影与参考栅格同
        out_raster.SetGeoTransform(para['GeoTransform']) #配置地理转换与参考栅格同
        
        '''将数组传给栅格波段，为栅格值'''
        out_band=out_raster.GetRasterBand(1)
        out_band.WriteArray(rasterValue)
        
    #    '''设置overview'''
    #    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    #    out_raster.BuildOverviews('average', overviews)
        
        '''清理缓存与移除数据源'''
        out_band.FlushCache()
        out_band.ComputeStatistics(False)
    #    del src_ds,out_raster,out_band        
        del out_raster,out_band
  
'''栅格数据显示查看程序'''
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

'''计算数据(数组)显示'''
    def arrayShow(self,data):            
        multiple=2 #配置图像大小的倍数
        fig=plt.figure(figsize=(20*multiple, 12*multiple))
        ax=fig.add_subplot(111)
        plt.xticks([x for x in range(data.shape[0]) if x%200==0])
        plt.yticks([y for y in range(data.shape[0]) if y%200==0])
#        print("*"*20,data.shape)
        ax.imshow(data) 

      
'''显示图像'''
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

'''加载numpy 数组数据。可省略该函数，直接调用np.load()方法'''
    def npArrayLoad(self,dataLoadFn):
        return np.load(dataLoadFn)

'''读取多个numpy数组数据，并追加在一个数组中'''
    def npyRead(self,filePath):
        #读取文件路径并按照文件名中数字排序
        fileType=["npy"]
#        dirs_files=basis.filePath(filePath,fileType)           
        dirs_files = os.listdir(filePath)  #返回指定的文件夹包含的文件或文件夹的名字的列表，按字母-数字顺序
        dirs_files.sort()
        pattern=re.compile(r'[_](.*?)[.]', re.S)
        fn_numExtraction=[(int(re.findall(pattern, fName)[0]),fName) for fName in dirs_files] #提取文件名中的数字，即聚类距离。并对应文件名
        fn_sort=sorted(fn_numExtraction)
    #    print(fn_sort)
        fn_sorted=[i[1] for i in fn_sort]
    #    print(fn_sorted)        
    
        #读取数据与组合数组
        bundleArrayList=[np.load(os.path.join(filePath,arr)) for arr in fn_sorted]
        bundleArray=np.stack(bundleArrayList)       
        
        return bundleArray

'''读取Numpy数组数据，因为每一数组shape不同，因此最终追加在一个列表中'''    
    def npyReadMulti(self,filePath):
        #读取文件路径并按照文件名中数字排序
        fileType=["npy"]
#        dirs_files=basis.filePath(filePath,fileType)           
        dirs_files = os.listdir(filePath)  #返回指定的文件夹包含的文件或文件夹的名字的列表，按字母-数字顺序
        dirs_files.sort()
        pattern=re.compile(r'[_](.*?)[.]', re.S)
        fn_numExtraction=[(int(re.findall(pattern, fName)[0]),fName) for fName in dirs_files] #提取文件名中的数字，即聚类距离。并对应文件名
        fn_sort=sorted(fn_numExtraction)
    #    print(fn_sort)
        fn_sorted=[i[1] for i in fn_sort]
    #    print(fn_sorted)  
        
        bundleArrayList=[np.load(os.path.join(filePath,arr)) for arr in fn_sorted]
        
        return bundleArrayList
                
    
    


'''计算'''
class calculate:
    def __int__(self):
        pass

'''调整分类数据，合并夏季和秋季农田区域''' 
    def classificationAdjust(self,cl_a,cl_b):
        Copy_cl_a=copy.deepcopy(cl_a)
        Copy_cl_a[cl_b==2.]=2.
    #    basis.arrayShow(calGreen)
        classificationGreenAdj=r'classificationGreenAdj.tif'
        basis=baseClass(landsat8Path,resultsPath) #实例化类baseClass
        #因为为分类数据，因此可以调整为整数
        basis.rasterRW(Copy_cl_a.astype(int),resultsPath,classificationGreenAdj,rD_CL190820_info)        
        print("written raster")
        return Copy_cl_a

'''实现栅格聚类的方法'''    
    def rasterCluster(self,rasterArray,val,eps,modelLoad=""):
        relativeCellCoords=np.concatenate([v.reshape(-1,1) for v in np.where(rasterArray)],axis=1) #返回数组值索引（2 维度），作为坐标位置
        rCellCoordsMatrix=relativeCellCoords.reshape(rasterArray.shape+(2,))
        extractCoords=rCellCoordsMatrix[rasterArray==val] #仅保留待计算的类别索引值
        print("extractCoords.shape:",extractCoords.shape)
        
        # Compute DBSCAN
        if modelLoad:  #对于聚类加载保存的模型计算无意义，此条件可移除          
            loaded_model = pickle.load(open(modelLoad, 'rb'))
            print("model loaded")
            t1=time.time() 
            print("staring computing:",time.asctime())
            y_db=loaded_model.fit_predict(extractCoords)
            t2=time.time()
            print("end computing:",time.asctime())            
            tDiff_af=t2-t1 #用于计算聚类所需时间
            print("duration:",tDiff_af)
            print("cluster finished")
        else:          
            t1=time.time() 
            print("staring computing:",time.asctime())
            db=DBSCAN(eps=eps,min_samples=3,algorithm='ball_tree', metric='euclidean') #DBSCAN聚类
            y_db=db.fit_predict(extractCoords)
            t2=time.time()
            print("end computing:",time.asctime())
            tDiff_af=t2-t1 #用于计算聚类所需时间
            print("duration:",tDiff_af)
           
            #保存模型,因此类模型保存无意义，可移除
#            modelSaveName = os.path.join(modelSavePath,'rasterDBSCAN_%d.sav'%eps)
#            pickle.dump(db, open(modelSaveName, 'wb'))  
#            print("model saved:",modelSaveName)
            
            #保存数据
            dataSaveFn=os.path.join(resultsPath,"DBSCANResults_%d"%eps)
            np.save(dataSaveFn, y_db)
            print("predicted data saved:",dataSaveFn)
        
#保存所有层聚类结果，以及所有层聚类频数
        #依据原栅格shape，存储聚类类标
        clusterArray=np.zeros(rasterArray.shape)
        y_db_plus=y_db+1
        n=0
        
        for idx in extractCoords:
            clusterArray[idx[0],idx[1]]=y_db_plus[n]
            n+=1
        print("n:",n)
        clusterArraySaveFn=os.path.join(resultsPath,"clusterArray_%d"%eps)
        np.save(clusterArraySaveFn,clusterArray)
        print("clusterArray saved:",clusterArraySaveFn)
        
        #计算聚类频数
        unique_elements, counts_elements = np.unique(clusterArray, return_counts=True)
        clusterFrequency=np.asarray(list(zip(unique_elements, counts_elements)), dtype=np.int)
        clusterFrequencyFn=os.path.join(resultsPath,"clusterFrequency_%d"%eps)
        np.save(clusterFrequencyFn,clusterFrequency)
        print("cluster frequency saved:",clusterFrequencyFn)
        
        #将每一层级计算聚类结果写入栅格数据
        clusterRasterFn=r"clusterRaste_%d.tif"%eps
        basis.rasterRW(clusterArray.astype(int),resultsPath,clusterRasterFn,rD_CL190820_info)
        
        
        return clusterArray,clusterFrequency
        

'''折线图，及计算knee/inflection points拐点'''    
    def lineGraph(self,x,y):
        #matplotlib的常规折线图
        font1 = {'family' : 'STXihei',
                 'weight' : 'normal',
                 'size'   : 50,
                 }
        plt.figure(figsize=(8*3, 8*3))
        plt.plot(x,y,'ro-',label="最大聚类变化值")
        plt.xlabel('聚类距离',font1)
        plt.ylabel('最大聚类变化值',font1)
        plt.tick_params(labelsize=40)
        plt.legend(prop=font1)  
        for i, txt in enumerate(x):
            plt.annotate("%s_var"%txt, (x[i], y[i]),size=20)
        
        
        #如果调整图表样式，需调整knee_locator文件中的plot_knee（）函数相关参数
        kneedle = KneeLocator(x, y, curve='convex', direction='decreasing')
        print(round(kneedle.knee, 3))
        print(round(kneedle.elbow, 3))
        kneedle.plot_knee()    

'''箱型图统计'''
    def boxplot(self,data,labels):
        all_data=data
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9*5, 4*5))
        # plot violin plot
        axes[0].violinplot(all_data, showmeans=False,showmedians=True)
        axes[0].set_title('Violin plot')
        
        # plot box plot
        axes[1].boxplot(all_data)
        axes[1].set_title('Box plot',fontsize=40)
        
        # adding horizontal grid lines
        for ax in axes:
            ax.yaxis.grid(True)
            ax.set_xticks([y + 1 for y in range(len(all_data))])
            ax.set_xlabel('聚类距离',fontsize=30)
            ax.set_ylabel('聚类频数',fontsize=30)    
            
        # add x-tick labels
        plt.setp(axes, xticks=[y+1 for y in range(len(all_data)+1) if y%1==0],xticklabels=labels)
        plt.tick_params(labelsize=25)
        fig.autofmt_xdate()
        plt.show()     
    
        
#组合
class combo():
    def __int__(self):
        pass

'''设置聚类距离，批量计算聚类，并保存raster文件，及array数组'''
    def clusterBundleCal(self,epsList):
        #程序失败则重新加载已存数据
#        clusterArray_list_exists=os.path.join(resultsPath,"clusterArray_list_temp.npy")
#        clusterFrequency_list_exists=os.path.join(resultsPath,"clusterFrequency_list_temp.npy")
#        if os.path.isfile(clusterArray_list_exists):
#            clusterArray_list=np.load(clusterArray_list_exists)
#            print("have loaded clusterArray_list_temp!")
#        else:
#            clusterArray_list=[]
#        if os.path.isfile(clusterFrequency_list_exists):
#            clusterFrequency_list=np.load(clusterFrequency_list_exists)
#            print("have loaded lusterFrequency_list_temp!")
#        else:
#            clusterFrequency_list=[]
            
        clusterArray_list=[]   
        clusterFrequency_list=[]
        
        for eps in tqdm(epsList):
            print("the current calculation:", eps*30)
            clusterArray,clusterFrequency=cal.rasterCluster(calGreenClip,valExtraction,eps)
            clusterArray_list.append(clusterArray)
            clusterFrequency_list.append(clusterFrequency)
            
            #需保存每一组数据，因为计算量较大，容易内存溢出，建议每组保存
            clusterArray_listFn_temp=os.path.join(resultsPath,"clusterArray_list_temp")
            clusterFrequency_listFn_temp=os.path.join(resultsPath,"clusterFrequency_list_temp")
            np.save(clusterArray_listFn_temp,clusterArray_list)
            np.save(clusterFrequency_listFn_temp,clusterFrequency_list)            
        
        #一次保存所有数据，当前16组，每组.shape=(10426,10232,2),总共超过12G之多，可能溢出内存（16G）,可扩充内存，或不整体保存，将其注释掉，仅保留单独每层保存的文件
        clusterArray_listFn=os.path.join(resultsPath,"clusterArray_list")
        clusterFrequency_listFn=os.path.join(resultsPath,"clusterFrequency_list")
        np.save(clusterArray_listFn,clusterArray_list)
        np.save(clusterFrequency_listFn,clusterFrequency_list)
        print("^"*50)
        print("clusterArray_list and clusterFrequency_list saved!!!")
        return clusterArray_list, clusterFrequency_list 

'''批量图表统计'''
    def graphAnalysis(self):
    #聚类总数/聚类距离
        epsDistance=[i*30 for i in list(epsList)]
        FrequencyNum=[i.shape[0] for i in bundleFrequencyArray]
    #    cal.lineGraph(epsDistance,FrequencyNum)
    
        #独立cell/聚类距离_boxplot
        clusterFrequencyPClean=[np.delete(val,0,0)[:,1] for val in bundleFrequencyArray]
        
    #    cal.boxplot(clusterFrequencyPClean,epsDistance)
        
        #除最大值外频数boxplot
    #    clusterFrequencyPCleanSort=[i.sort() for i in clusterFrequencyPClean]
        clusterFrequencyBesidesMax=[np.sort(i)[:-1] for i in clusterFrequencyPClean]
    #    cal.boxplot(clusterFrequencyBesidesMax,epsDistance)
        
        #最大值的变化幅度
        clusterFrequencyMax=[max(i) for i in clusterFrequencyPClean]
        clusterFrequencyMaxReverse=[max(clusterFrequencyMax)-i for i in clusterFrequencyMax]
#        cal.lineGraph(epsDistance,clusterFrequencyMaxReverse)
#        print(clusterFrequencyMax)
        cluFreMaxVariation=[clusterFrequencyMax[i+1]-clusterFrequencyMax[i] for i in range(len(clusterFrequencyMax)-1)]
#        print(cluFreMaxVariation)
#        cal.lineGraph(epsDistance[1:],cluFreMaxVariation)
        
        
#        return clusterFrequencyMax
        
'''最大聚类提取并存储为raster'''   
    def maxClusterRaster(self,clusterArray,clusterFrequency):
        cluFreList=[]
        for i in clusterFrequency:
            cluFreIdx=np.argmax(i[1:],axis=0)[1] #返回聚类频数最大值的索引
            cluFreList.append(cluFreIdx+1)
        
        clusterArrayDc=copy.deepcopy(clusterArray)
        clusterArray=None
        #仅保留最大聚类频数位置的索引，其它位置赋值为0，即背景
        for i in tqdm(range(len(cluFreList))):
            clusterArrayDc[i][clusterArrayDc[i]!=cluFreList[i]]=0
            
        #将每一层级计算最大聚类结果写入栅格数据
        n=1
        for i in tqdm(clusterArrayDc):
            clusterRasterMaxFn=r"clusterRasteMax_%d.tif"%n
            basis.rasterRW(i.astype(int),resultsPath,clusterRasterMaxFn,rD_CL190820_info) 
            n+=1
        print("cluster max raster has converted")
           
        return clusterArrayDc
         

'''最大聚类变化区写入raster'''
    def clusterMaxVariaton(self,clusterArray,clusterFrequency):
        cluFreList=[]
        for i in clusterFrequency:
            cluFreIdx=np.argmax(i[1:],axis=0)[1] #返回聚类频数最大值的索引
            cluFreList.append(cluFreIdx+1)
        
        clusterArrayDc=copy.deepcopy(clusterArray)
#        clusterArray=None
        #仅保留最大聚类频数位置的索引，其它位置赋值为0，即背景
        for i in tqdm(range(len(cluFreList))):
            clusterArrayDc[i][clusterArrayDc[i]!=cluFreList[i]]=0        
        
        n=1
        #每两个层级做和，设置上一层级城市区域为1，下一层及城市区域为2，如果作和，则可能出现最后值为0,1,2,3等4种情况，
        #0代表两层均没有值，1代表仅上一层有值，2代表仅下一层有值，3代表两层均有值
        for i in tqdm(range(len(clusterArrayDc)-1)):
            upper=clusterArrayDc[i+1]
            under=clusterArrayDc[i]
            upper[upper!=0]=1
            under[under!=0]=2
            varVal=upper+under
            
            varValFn=r"clusterRasteMaxVar_%d.tif"%n
            basis.rasterRW(varVal.astype(int),resultsPath,varValFn,rD_CL190820_info)         
            n+=1
            
        print("cluster max raster variation has converted") 
#        return clusterArrayDc
        


if __name__=="__main__": 
    print("+"*50)
    basis=baseClass(landsat8Path,resultsPath)
    #读取三组分类栅格数据：18/03冬季， 19/08夏季（农田变化），19/10秋季（农田变化）
#    rD_CL180310_Val, rD_CL180310_info=basis.singleBand(rasterDataPending["rD_CL180310"])
#    rD_CL190820_Val, rD_CL190820_info=basis.singleBand(rasterDataPending["rD_CL190820"])
#    rD_CL191018_Val, rD_CL191018_info=basis.singleBand(rasterDataPending["rD_CL191018"])
    
#    basis.rasterShow(rasterDataPending["rD_CL180310"])
#    basis.arrayShow(rD_CL180310_Val)   
    
#调正绿地范围，由于不同季节农田的变化    
    cal=calculate()
#    calGreen=cal.classificationAdjust(rD_CL190820_Val,rD_CL191018_Val)
    
#栅格raster，DBSCAN聚类算法
#    clipRange=[3000,3000,1800,1800]  #(10232, 10426)
#    calGreen=basis.rasterClip(calGreen,clipRange)  #应为raster格式
#    calGreenClip=calGreen[4000:4800,4000:4800]
#    calGreenClip=calGreen
#        
    valExtraction=3 #3为建成区类别
#    eps=10  #需要根据栅格大小确定，如果栅格大小=30m, 预计算300m的聚类，则300/30=10，即eps=10
#    modelLoad=r"D:\dataProcessing\modelSave\rasterDBSCAN_1574908954.4651601.sav" #放弃该种方法
#    clusterArray,clusterFrequency=cal.rasterCluster(calGreenClip,valExtraction,eps)

#将聚类结果写入单波段栅格文件  
#    dataLoadFn=r"D:\dataProcessing\codeResults\clusterArray_1574958399.9721985.npy"
#    clusterArrayLoad=cal.npArrayLoad(dataLoadFn)
#    clusterRasterFn=r"clusterRaster.tif"
#    basis.rasterRW(clusterArrayLoad.astype(int),resultsPath,clusterRasterFn,rD_CL190820_info)
    
#批量计算
    clusterBundle=combo()
    epsList=range(1,17,1) #如果程序失败，需自行调整取值范围，从失败位置计算
#    clusterArray_list, clusterFrequency_list=clusterBundle.clusterBundleCal(epsList)
    
    #读取多个单独clusterArray文件并分析
    clusterArrayPath=r"D:\dataProcessing\codeResults\cluster_0-16\clusterArray"
#    bundleClusterArray=basis.npyRead(clusterArrayPath)
    clusterFrequencyPath=r"D:\dataProcessing\codeResults\cluster_0-16\clusterFrequency"
#    bundleFrequencyArray=basis.npyReadMulti(clusterFrequencyPath)
    
#统计分析
    clusterBundle.graphAnalysis()
    
#最大聚类提取并存储为raster 
#    rr=clusterBundle.maxClusterRaster(bundleClusterArray,bundleFrequencyArray)
    
#最大聚类变化区写入raster
    qq=clusterBundle.clusterMaxVariaton(bundleClusterArray,bundleFrequencyArray)
    
    
    