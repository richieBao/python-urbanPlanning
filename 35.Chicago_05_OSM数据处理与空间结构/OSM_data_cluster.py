# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 17:27:01 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicagoo
"""
import osmium as osm
import pandas as pd
import os,math,time,ogr,osr,gdal
from tqdm import tqdm
import numpy as np
from sklearn import cluster
from collections import Counter #用于一些特殊数据统计，以及实现了些方便实用的数据结构
from sklearn import preprocessing
from pylab import mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import Subplot

mpl.rcParams['font.sans-serif']=['STXihei']

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码


#读取OSM的node数据，指定需要的字段信息。具体方法查询官网
class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        # self.count = [0, 0, 0]

    def tag_inventory(self, elem, elem_type):
        for tag in elem.tags:
            self.osm_data.append([elem_type, 
                                   elem.id, 
                                   elem.version,
                                   elem.visible,
                                   pd.Timestamp(elem.timestamp),
                                   elem.uid,
                                   elem.user,
                                   elem.changeset,
                                   len(elem.tags),                                   
                                   tag.k, 
                                   tag.v,
                                   elem.location.lon,
                                   elem.location.lat
                                    ])

    def node(self, n):
        self.tag_inventory(n, "node")

    # def way(self, w):
    #     self.tag_inventory(w, "way")

    # def relation(self, r):
    #     self.tag_inventory(r, "relation")
        
    # def node(self, n):
    #     self.count[0] += 1
    # def way(self, w):
    #     self.count[1] += 1
    # def relation(self, r):
    #     self.count[2] += 1
'''DBSCAN基于密度空间的聚类，聚类所有poi特征点'''
def affinityPropagationForPoints(dataArray,epsValue):
    print("--------------------Clustering")
    data=dataArray
    t1=time.time()     
    db=cluster.DBSCAN(eps=epsValue,min_samples=3,metric='euclidean') #meter=degree*(2 * math.pi * 6378137.0)/ 360  degree=50/(2 * math.pi * 6378137.0) * 360，在调参时，eps为邻域的距离阈值，而分析的数据为经纬度数据，为了便于调参，可依据上述公式可以在米和度之间互相转换，此时设置eps=0.0008，约为90m，如果poi的空间点之间距离在90m内则为一簇；min_samples为样本点要成为核心对象所需要的邻域样本数阈值。参数需要自行根据所分析的数据不断调试，直至达到较好聚类的结果。
    y_db=db.fit_predict(data)  #获取聚类预测类标
    t2=time.time()    
    tDiff_af=t2-t1 #用于计算聚类所需时间
    print(tDiff_af)
    
    pred=y_db  
    print(pred,len(np.unique(pred)))  #打印查看预测类标和计算聚类簇数
    
#    t3=time.time()
#    plt.close('all')
#    plt.figure(1,figsize=(20,20))
#    plt.clf()
#    cm=plt.cm.get_cmap('nipy_spectral')  #获取内置色带
#    plt.scatter(data[...,0],data[...,1],s=10,alpha=0.8,c=pred,cmap=cm) #c参数设置为预测值，传入色带，根据c值显示颜色
#    plt.show()
#    t4=time.time()
#    tDiff_plt=t4-t3  #计算图表显示时间
#    print(tDiff_plt)
    print("-------------------cluster Finishing")
    return pred,np.unique(pred)  #返回DBSCAN聚类预测值。和簇类标

'''将聚类的POI数据，写入.shp文件，用于GIS调用。'''
def point2Shp(df_osm,valueArray,fn,pt_lyrName_w,ref_lyr=False):
    ds=ogr.Open(fn,1)
#    '''参考层，用于空间坐标投影，字段属性等参照'''
#    ref_lyr=ds.GetLayer(ref_lyr)
#    ref_sr=ref_lyr.GetSpatialRef()
#    print(ref_sr)
#    ref_schema=ref_lyr.schema #查看属性表字段名和类型
#    for field in ref_schema:
#        print(field.name,field.GetTypeName())     
        
    '''建立新的datasource数据源'''
    sf_driver=ogr.GetDriverByName('ESRI Shapefile')
    sfDS=os.path.join(fn,r'sf')
#    if os.path.exists(sfDS):
#        sf_driver.DeleteDataSource(sfDS)
    pt_ds=sf_driver.CreateDataSource(sfDS)
    if pt_ds is None:
        sys.exit('Could not open{0}'.format(sfDS))
        
    '''建立新layer层'''    
    if pt_ds.GetLayer(pt_lyrName_w):
        pt_ds.DeleteLayer(pt_lyrName_w)    
       
    spatialRef = osr.SpatialReference()
    spatialRef.SetWellKnownGeogCS("WGS84") #需要注意直接定义大地坐标未"WGS84"，而未使用参考层提取的坐标投影系统
    
    pt_lyr=pt_ds.CreateLayer(pt_lyrName_w,spatialRef,ogr.wkbPoint)    
#    pt_lyr=pt_ds.CreateLayer(pt_lyrName_w,ref_sr,ogr.wkbPoint)  

    '''配置字段，名称以及类型和相关参数'''
#    pt_lyr.CreateFields(ref_schema)
    LatFd=ogr.FieldDefn("origiLat",ogr.OFTReal)
    LatFd.SetWidth(20)
    LatFd.SetPrecision(3)
    pt_lyr.CreateField(LatFd)
    LatFd.SetName("origiLong")
    pt_lyr.CreateField(LatFd)
    
#    pt_lyr.CreateFields(ref_schema)
    preFd=ogr.FieldDefn("type",ogr.OFTString)
    pt_lyr.CreateField(preFd)
    preFd.SetName("tagkey")
    pt_lyr.CreateField(preFd)
    preFd.SetName("tagvalue")
    pt_lyr.CreateField(preFd)
    
    preFd=ogr.FieldDefn("cluster",ogr.OFTInteger)
    pt_lyr.CreateField(preFd)
    # preFd.SetName("cluster")
    # pt_lyr.CreateField(preFd)    
    
#    stationName=ogr.FieldDefn("stationN",ogr.OFTString)
#    pt_lyr.CreateField(stationName)    
    
#    preFd.SetName("ObservTime")
#    pt_lyr.CreateField(preFd)  
#   
     
    '''建立feature空特征和设置geometry几何类型'''
    print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())    
   
#    idx=0
    for i in tqdm(range(valueArray.shape[0])):  #循环feature         
#        print(key)
        '''设置几何体'''
        #pt_ref=feat.geometry().Clone()
        # converCoordiGCJ=cc.bd09togcj02(dataBunch.data[i][1],dataBunch.data[i][0])
        # converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
#        print(wdCoordiDicSingle[key][1],wdCoordiDicSingle[key][0])
#        print(converCoordiGPS84[0], converCoordiGPS84[1])
        wkt="POINT(%f %f)" %  (df_osm["lon"][i], df_osm["lat"][i])
#        wkt="POINT(%f %f)" %  (dataBunch.data[i][0], dataBunch.data[i][1])
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
#        for i_field in range(feat.GetFieldCount()):
#            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",df_osm["lat"][i])
        pt_feat.SetField("origiLong",df_osm["lon"][i])
        
        
#        print(wdDicComplete[key]['20140901190000'])
        pt_feat.SetField("type",df_osm["type"][i]) #
        pt_feat.SetField("tagkey",df_osm["tagkey"][i])
        pt_feat.SetField("tagvalue",df_osm["tagvalue"][i])
        pt_feat.SetField("cluster",int(valueArray[i]))
#        print(idx,int(valueArray[idx]),pt_ref.GetX())
#        idx+=1
        
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds       

'''绘制箱型图和小提琴图'''
def violinPlot(all_data,eps):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18*2, 8*2))
    # plot violin plot
    axes[0].violinplot(all_data,showmeans=False,showmedians=True)
    axes[0].set_title('Violin plot',fontsize=30)
    
    # plot box plot
    axes[1].boxplot(all_data,flierprops={'marker':'o','markerfacecolor':'red','color':'black'})
    axes[1].set_title('Box plot',fontsize=30)
   
    # adding horizontal grid lines
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data))])
        ax.set_xlabel('聚类距离',fontsize=30)
        ax.set_ylabel('聚类频数(标准化)',fontsize=30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=20)
        
    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data)) if y%2==0],xticklabels=[eps[i] for i in range(len(eps)) if i%2==0])
    fig.autofmt_xdate()
#    plt.tick_params(labelsize=20)
#    plt.rcParams('font.sans-serif')=['STXihei'] #在开始已经设置mpl.rcParams['font.sans-serif']=['STXihei']，因此此处可忽略
    plt.savefig(os.path.join(savingFig,"violinPlot"))
    plt.show()

'''绘制折线图'''
def lineGraph(all_data,eps):
    fig = plt.figure(1, (18*2, 9*2))
    ax = Subplot(fig, 111)  
    fig.add_subplot(ax)

    ax.plot(eps,all_data, 'ro-',label='POI聚类总数')
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.set_xlabel('聚类距离',fontsize=30)
    ax.set_ylabel('聚类总数',fontsize=30)
    ax.tick_params(labelsize=20)
    
    plt.legend()
    plt.savefig(os.path.join(savingFig,"lineGraph"))
    plt.show()

'''使用numpy保存与读取数据'''
def savingData(fp,fn,data):
    np.save(os.path.join(fp,fn),data) #保存一个数组到一个二进制的文件中,保存格式是.npy
    
def savingDataZ(fp,fn,data):
    np.savez(os.path.join(fp,fn),dic=data)   #保存多个数组到同一个文件中,保存格式是.npz,可以同时保持字典

#读取numpy保存的数据    
def readingData(fp,fn):
    readedData=np.load(os.path.join(fp,fn+".npy"))
    return readedData
def readingDataz(fp,fn):
    readedData=np.load(os.path.join(fp,fn+".npz"))
    return readedData



'''批量计算'''
def loopCalculate(df_osm,epsDegree,fn,eps):
    xyzArray=pd.DataFrame({"lon": df_osm['lon'] , "lat": df_osm['lat'] }).to_numpy()
    robustScaleList=[]
    totalNumber=[]
    CTableDic={}
    partialCorrelationsList=[]
    counter=0
    
    #逐一计算所有距离的聚类
    for i in range(len(epsDegree)):        
        pred,predLable=affinityPropagationForPoints(xyzArray,epsDegree[i]) #聚类计算，返回预测值及簇类标

        pt_lyrName_w=r'%s_POI'%eps[i] #字符串格式化输出文件名
        point2Shp(df_osm,pred,fn,pt_lyrName_w) 
        print("\n%s has been written to disk"%i)
        
        counterData=Counter(pred)   #聚类簇类标频数统计
#        print(counterData)
        counterValue=np.array(list(counterData.values()))
        cvFloat=counterValue.astype(float)
        robustScale=preprocessing.robust_scale(cvFloat.reshape(-1,1))  #如果数据中含有异常值，那么使用均值和方差缩放数据的效果并不好，因此用preprocessing.robust_scale()缩放带有outlier的数据 
        cvF=robustScale.ravel() #展平，注意numpy的ravel() 和 flatten()函数的区别
        robustScaleList.append(cvF)        
        totalNumber.append(len(predLable)) #预测类标的数量       
        
    return robustScaleList,totalNumber
        

if __name__=="__main__": 
    # osmChicagoFn=r"D:\data\data_01_Chicago\osm\map_exercise.osm"
    osmChicagoFn=r"D:\data\data_01_Chicago\osm\ChicagoOSM.osm"
    osmhandler = OSMHandler()
    # scan the input file and fills the handler list accordingly
    osmhandler.apply_file(osmChicagoFn)
    
    # transform the list into a pandas DataFrame
    # # data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid','user', 'chgset', 'ntags', 'tagkey', 'tagvalue']
    # data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid','user', 'chgset', 'ntags', 'tagkey', 'tagvalue','lon','lat']
    data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid','user', 'chgset', 'ntags', 'tagkey', 'tagvalue','lon','lat']
    df_osm = pd.DataFrame(osmhandler.osm_data, columns=data_colnames) #指定字段，读取OSM数据，并存储为dataframe数据格式
    
    # eps=list(range(20,520,10)) #设置多个聚类距离，因为已经将经纬度转换为了米制距离单位，因此不用如下行代码处理
    eps=list(range(20,520,10)) #设置多个聚类距离，因为已经将经纬度转换为了米制距离单位，因此不用如下行代码处理

    epsDegree=np.array(eps)/(2 * math.pi * 6378137.0) * 360
    fn=r"D:\data\data_01_Chicago\QGisDat\OSMPointsCluster"    
    robustScaleList,totalNumber=loopCalculate(df_osm,epsDegree,fn,eps)
    #绘制图表，观察数据变化
    savingFig=r"D:\data\data_01_Chicago\results_figure"
    violinPlot(robustScaleList,eps) #绘制箱型图/小提琴图
    lineGraph(totalNumber,eps) #绘制折线图/曲线图    
    
    
    #saving data。该部分仅保存了用于图表分析的部分数据
    savingFp=r'D:\data\data_01_Chicago\results_data_save' #将数据保存到硬盘中，便于日后使用，减少重复计算时间
    
    savingFn=r'POI_violin'
    tempData=robustScaleList
    savingData(savingFp,savingFn,tempData)    
    # X=readingData(savingFp,savingFn)
   
    savingData(savingFp,"POI__LineGraph",totalNumber)  
    Y=readingData(savingFp,"POI__LineGraph")
    savingData(savingFp,"POI__eps",eps)  
    # Z=readingData(savingFp,"POI__eps")