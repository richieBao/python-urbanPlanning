# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:38:31 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import gdal,math,sys,time,os,copy,math
import numpy as np
from scipy.signal import convolve2d   #2d卷积
from sklearn.cluster import DBSCAN
from tqdm import tqdm
import matplotlib.pyplot as plt
from pylab import mpl

'''from kneed import DataGenerator, KneeLocator
因为kneed库无法正常加载，因此单独读取文件函数
kneed库官方地址：https://github.com/arvkevi/kneed
'''
from data_generator import DataGenerator
from knee_locator import KneeLocator

clusterRasterMax_6=r"D:\dataProcessing\codeResults\clusterRasteMax\clusterRasteMax_5.tif"
resultsPath=r"D:\dataProcessing\dataResults"

mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码/针对gdal
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码/针对gdal

'''连接度计算'''
class connectivityRaster():
    def __int__(self):
        pass
    
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
    
    '''基于卷积计算连接度'''
    def connectivity(self,array2D,distance=3): #输入参数需要为奇数，并>=3
        #配置卷积核，卷积核需为奇数，并大于等于3
        if distance>=3 and distance%2!=0:
            kernel=np.ones((distance,distance),dtype=int)
        else:
            print("-"*50)
            print("the value of distance must be odd number and equal or greater than 3!")
            print("-"*50)
            sys.exit() #卷积核不满足要求，系统退出
        kernel[math.floor(distance/2),math.floor(distance/2)]=0 #配置卷积核，形式为(中心值为0，其余为1):
#        array([[1, 1, 1],
#               [1, 0, 1],
#               [1, 1, 1]])
        print("kernel setting:\n",kernel)

        t0=time.time()
        array_convolve2d=convolve2d(array2D,kernel,mode='same')
        array_convolve2d[array2D==0]=0
        print("the max value:{}, the min value:{}".format(array_convolve2d.max(),array_convolve2d.min()))
      
        t1=time.time()
        t_convolve2d=t1-t0
        print("lasting time:",t_convolve2d)
        
        return array_convolve2d
       
    '''保存栅格数据，1个波段'''      
    def rasterRW(self, rasterArray,resultsPath,resultsFn,para):
        gdal.UseExceptions()    
    #    '''打开栅格数据'''
    #    try:
    #        src_ds=gdal.Open(os.path.join(resultsPath,resultsFn))
    #    except RuntimeError as e:
    #        print( 'Unable to open %s'% os.path.join(resultsPath,resultsFn))
    #        print(e)
    #        sys.exit(1)
    #    print("metadata:",src_ds.GetMetadata())   
      
        '''初始化输出栅格'''
        driver=gdal.GetDriverByName('GTiff')
        print(para['RasterXSize'],para['RasterYSize'])
        out_raster=driver.Create(os.path.join(resultsPath,resultsFn),para['RasterXSize'],para['RasterYSize'],1,gdal.GDT_Float64)
        out_raster.SetProjection(para['RasterProjection']) #设置投影与参考栅格同
        out_raster.SetGeoTransform(para['GeoTransform']) #配置地理转换与参考栅格同
        
        '''将数组传给栅格波段，为栅格值'''
        out_band=out_raster.GetRasterBand(1)
        out_band.WriteArray(rasterArray)
        
    #    '''设置overview'''
    #    overviews = pb.compute_overview_levels(out_raster.GetRasterBand(1))
    #    out_raster.BuildOverviews('average', overviews)
        
        '''清理缓存与移除数据源'''
        out_band.FlushCache()
        out_band.ComputeStatistics(False)
    #    del src_ds,out_raster,out_band    
        print("raster saved successfully!")    
        del out_raster,out_band

    '''实现栅格聚类的方法'''    
    def rasterCluster(self,rasterArray,val,eps,kernalDistance):
        relativeCellCoords=np.concatenate([v.reshape(-1,1) for v in np.where(rasterArray)],axis=1) #返回数组值索引（2 维度），作为坐标位置
#        print(relativeCellCoords)
#        print(relativeCellCoords.shape)
        
        rCellCoordsMatrix=relativeCellCoords.reshape(rasterArray.shape+(2,))
        extractCoords=rCellCoordsMatrix[rasterArray==val] #仅保留待计算的类别索引值
#        print("extractCoords.shape:",extractCoords.shape)
#        print(extractCoords)        
#        print("_"*50)
#        print(extractCoords.dtype)
        
       
        t1=time.time() 
        print("staring computing:",time.asctime())
        db=DBSCAN(eps=eps,min_samples=3,algorithm='ball_tree', metric='euclidean') #DBSCAN聚类
        y_db=db.fit_predict(extractCoords)
        t2=time.time()
        print("end computing:",time.asctime())
        tDiff_af=t2-t1 #用于计算聚类所需时间
        print("duration:",tDiff_af)
#        
        #保存数据
        dataSaveFn=os.path.join(resultsPath,"connectivityClusterResults_%s_%s"%(kernalDistance,eps))
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
        clusterArraySaveFn=os.path.join(resultsPath,"connectivityClusterArray_%s_%s"%(kernalDistance,eps))
        np.save(clusterArraySaveFn,clusterArray)
        print("clusterArray saved:",clusterArraySaveFn)
        
        #计算聚类频数
        unique_elements, counts_elements = np.unique(clusterArray, return_counts=True)
        clusterFrequency=np.asarray(list(zip(unique_elements, counts_elements)), dtype=np.int)
        clusterFrequencyFn=os.path.join(resultsPath,"connectivityClusterFrequency_%s_%s"%(kernalDistance,eps))
        np.save(clusterFrequencyFn,clusterFrequency)
        print("cluster frequency saved:",clusterFrequencyFn)
        
        #将每一层级计算聚类结果写入栅格数据
        clusterRasterFn=r"connectivityClusterRaste_%s_%s.tif"%(kernalDistance,eps)
        self.rasterRW(clusterArray.astype(int),resultsPath,clusterRasterFn,rasterInfo)
        
        return clusterArray,clusterFrequency

    '''最大聚类提取并存储为raster'''   
    def maxClusterRaster(self,clusterArray,clusterFrequency,kernalDistance):
        cluFreList=[]
        for i in clusterFrequency:
            cluFreIdx=np.argmax(i[1:],axis=0)[1] #返回聚类频数最大值的索引
            cluFreList.append(cluFreIdx+1)

        print("_"*50)
        print(cluFreList)
        
        clusterArrayDc=copy.deepcopy(clusterArray)
        clusterArray=None
        #仅保留最大聚类频数位置的索引，其它位置赋值为0，即背景
        for i in tqdm(range(len(cluFreList))):
            clusterArrayDc[i][clusterArrayDc[i]!=cluFreList[i]]=0
#        print(clusterArrayDc)
            
        #将每一层级计算最大聚类结果写入栅格数据
        n=1
        for i in tqdm(clusterArrayDc):
#            print(i)
            clusterRasterMaxFn=r"connectivityClusterRasteMax_%s_%s.tif"%(kernalDistance,n)
            self.rasterRW(i.astype(int),resultsPath,clusterRasterMaxFn,rasterInfo) 
            n+=1
        print("cluster max raster has converted")
           
        return clusterRasterMaxFn

    '''按数量多少排序的前n个值，'''
    def N_maxClusterRaster(self,clusterArray,clusterFrequency,n,kernalDistance):
        cluFreList=[]
        for i in clusterFrequency:           
            n_maximum=i[1:,1].argsort()[-n:] #应用.argsort()函数，按大小提取前n个值的索引
            print(n_maximum)
            n_maximum=[i+1 for i in n_maximum]
            cluFreList.append(n_maximum)
        print("_"*50)
        
        clusterArrayDc=copy.deepcopy(clusterArray)
        clusterArray=None
        #仅保留最大n个聚类频数位置的索引，其它位置赋值为0，即背景       
        
        #其它前n大值
        for i in tqdm(range(len(cluFreList))):
            mask = np.in1d(clusterArrayDc[i], cluFreList[i]).reshape(clusterArrayDc[i].shape)
            clusterArrayDc[i][~mask]=0

        #写入栅格
        n=1
        for i in tqdm(clusterArrayDc):
#            print(i)
            clusterRasterMaxFn=r"connectivityClusterRasteNMax_%s_%s.tif"%(kernalDistance,n)
            self.rasterRW(i.astype(int),resultsPath,clusterRasterMaxFn,rasterInfo) 
            n+=1
        print("cluster N max raster has converted")
           
        return clusterRasterMaxFn    

    '''折线图，及计算knee/inflection points拐点'''    
    def lineGraph(self,x,y,fields):
        #matplotlib的常规折线图
        font1 = {'family' : 'STXihei',
                 'weight' : 'normal',
                 'size'   : 50,
                 }
        plt.figure(figsize=(8*3, 8*3))
        plt.plot(x,y,'ro-',label=fields["title"])
        plt.xlabel(fields["xlabel"],font1)
        plt.ylabel(fields["ylabel"],font1)
        plt.tick_params(labelsize=40)
        plt.legend(prop=font1)  
        for i, txt in enumerate(x):
            plt.annotate("%s"%txt, (x[i], y[i]),size=20)
        
        
        #如果调整图表样式，需调整knee_locator文件中的plot_knee（）函数相关参数
        kneedle = KneeLocator(x, y, curve='convex', direction='decreasing')
        print(round(kneedle.knee, 3))
        print(round(kneedle.elbow, 3))
        kneedle.plot_knee()    
        
    '''箱型图统计'''
    def boxplot(self,data,labels,fields):
        all_data=data
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9*5, 4*5))
        # plot violin plot
        axes[0].violinplot(all_data, showmeans=False,showmedians=True)
        axes[0].set_title(fields["title"])
        
        # plot box plot
        axes[1].boxplot(all_data)
        axes[1].set_title(fields["title"],fontsize=40)
        
        # adding horizontal grid lines
        for ax in axes:
            ax.yaxis.grid(True)
            ax.set_xticks([y + 1 for y in range(len(all_data))])
            ax.set_xlabel(fields["xlabel"],fontsize=30)
            ax.set_ylabel(fields["ylabel"],fontsize=30)    
            
        # add x-tick labels
        plt.setp(axes, xticks=[y+1 for y in range(len(all_data)+1) if y%1==0],xticklabels=labels)
        plt.tick_params(labelsize=25)
        fig.autofmt_xdate()
        plt.show()

'''主程序'''        
def combo(rasterData,kernalDistanceList):
    connection=connectivityRaster()
    bandValue,rasterInfo=connection.singleBand(rasterData)
    bandValue[bandValue!=0]=1 #如果值不同则指定同一值
    connectivityClusterArray_list=[] #存储聚类后数组
    connectivityClusterFrequency_list=[] #存储聚类频数值
    for kernalDistance in tqdm(kernalDistanceList):
        print("start computing kernalDistance_%s"%kernalDistance)
        array_convolve2d=connection.connectivity(bandValue,kernalDistance) 
        #栅格写入所有距离
        resultsFn=r"conectivity_%s.tif"%kernalDistance
        connection.rasterRW(array_convolve2d,resultsPath,resultsFn,rasterInfo)
        #栅格写入最大距离
        array_convolve2dMax=copy.deepcopy(array_convolve2d)
        array_convolve2dMax[array_convolve2dMax!=array_convolve2dMax.max()]=0
        array_convolve2dMaxFn=r"array_convolve2dMax_%s.tif"%kernalDistance
        connection.rasterRW(array_convolve2dMax,resultsPath,array_convolve2dMaxFn,rasterInfo)
        
        #连接度聚类
        eps=1
        val=array_convolve2dMax.max()+1
        connectivityClusterArray,connectivityClusterFrequency=connection.rasterCluster(array_convolve2dMax+1,val,eps,kernalDistance) #输入的数组不可值为0，因此+1;如果不+1，亦可调整函数部分，不需再单独提取
        connectivityClusterArray_list.append(connectivityClusterArray)
        connectivityClusterFrequency_list.append(connectivityClusterFrequency)
           
        #连接度最大聚类    
        connection.maxClusterRaster(np.expand_dims(connectivityClusterArray, axis=0),[connectivityClusterFrequency],kernalDistance)
        
        #按数量多少排序的前n个值
        N_clusterFrequency=20
        cc=connection.N_maxClusterRaster(np.expand_dims(connectivityClusterArray, axis=0),[connectivityClusterFrequency],N_clusterFrequency,kernalDistance)
        print("finish computing kernalDistance_%s"%kernalDistance)
    #在循环外，计算所有值后，存储值，因为如果每次循环均存储，每次存储的时间较长
    connectivityClusterArray_list_fn=os.path.join(resultsPath,"connectivityClusterArray_list")
    connectivityClusterFrequency_list_fn=os.path.join(resultsPath,"connectivityClusterFrequency_list")
    np.save(connectivityClusterArray_list_fn,connectivityClusterArray_list)
    np.save(connectivityClusterFrequency_list_fn,connectivityClusterFrequency_list) 
    print("data saved!")    
     
    return connectivityClusterArray_list,connectivityClusterFrequency_list
            
#图表分析
def graphAnalysis_conectivity():  
    connection=connectivityRaster()    
    #聚类总数/聚类距离
#    fields_line={"title":"连接度聚类",
#            "xlabel":"kernel大小",
#            "ylabel":"连接度聚类数量"}
#    FrequencyNum=[i.shape[0] for i in connectivityClusterFrequency_list]
#    connection.lineGraph(kernalDistanceList,FrequencyNum,fields_line)
    
#    #除最大值外频数boxplot
    #给定fields字段，方便每次图表的label修改
    fields_box={"title":"连接度聚类频数分布",
            "xlabel":"kernel大小",
            "ylabel":"连接度聚类频数"}    
    clusterFrequencyBesidesMax=[np.sort(i[1:])[:-1] for i in connectivityClusterFrequency_list]
    connection.boxplot(clusterFrequencyBesidesMax,kernalDistanceList,fields_box)
   

if __name__=="__main__": 
    pass
'''不使用combo()函数一次性计算时，分别计算或测试
    connection=connectivityRaster()
#    bandValue,rasterInfo=connection.singleBand(clusterRasterMax_6)
    bandValue[bandValue!=0]=1
    kernalDistance=7
    array_convolve2d=connection.connectivity(bandValue,kernalDistance) 
    #栅格写入所有距离
    resultsFn=r"conectivity_%s.tif"%kernalDistance
    connection.rasterRW(array_convolve2d,resultsPath,resultsFn,rasterInfo)
    #栅格写入最大距离
    array_convolve2dMax=copy.deepcopy(array_convolve2d)
    array_convolve2dMax[array_convolve2dMax!=array_convolve2dMax.max()]=0
    array_convolve2dMaxFn=r"array_convolve2dMax_%s.tif"%kernalDistance
    connection.rasterRW(array_convolve2dMax,resultsPath,array_convolve2dMaxFn,rasterInfo)
    
    #连接度聚类
    eps=1
    val=array_convolve2dMax.max()+1
#    connection.rasterCluster(np.expand_dims(array_convolve2dMax,axis=0),val,epsList)
    connectivityClusterArray,connectivityClusterFrequency=connection.rasterCluster(array_convolve2dMax+1,val,eps,kernalDistance) #输入的数组不可值为0，因此+1;如果不+1，亦可调整函数部分，不需再单独提取
    #连接度最大聚类    
    connection.maxClusterRaster(np.expand_dims(connectivityClusterArray, axis=0),[connectivityClusterFrequency],kernalDistance)
    
    #按数量多少排序的前n个值
    N_clusterFrequency=10
    cc=connection.N_maxClusterRaster(np.expand_dims(connectivityClusterArray, axis=0),[connectivityClusterFrequency],N_clusterFrequency,kernalDistance)
'''   
#kernel列表，逐一计算    
#    rasterData=clusterRasterMax_6
#    kernalDistanceList=[i for i in range(50) if i%2!=0 and i>=3] #50
#    print("kernalDistanceList length:%d"%len(kernalDistanceList))
#    connectivityClusterArray_list,connectivityClusterFrequency_list=combo(rasterData,kernalDistanceList)
#图表计算
    graphAnalysis_conectivity()
  
    