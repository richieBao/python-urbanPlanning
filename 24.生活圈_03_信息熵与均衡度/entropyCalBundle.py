# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:44:34 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
"""
import gdal,ogr,os,osr,gdalnumeric
import sys
import numpy as np
from tqdm import tqdm
from collections import Counter
import math
from pandas import DataFrame
import re

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码

'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
def filePath(dirpath,fileType):
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

'''point的读与计算信息熵/均衡度
计算公式参考：陈彦光,刘继生.城市土地利用结构和形态的定量描述:从信息熵到分数维[J].地理研究,2001(02):146-152.
'''
def pointReading(fn,pt_lyrName_r):
    ds=ogr.Open(fn,0) #0为只读模式，1为编辑模式
    if ds is None:
        sys.exit('Could not open{0}'.format(fn))
    pt_lyr=ds.GetLayer(pt_lyrName_r) #可以直接数据层(文件)名或者指定索引
#    vp = VectorPlotter(True)  #显示vector数据
#    vp.plot(pt_lyr,'bo')

    dic={}
    target=[]
    categoryList=[]
    poiCoordi=[]
    #读取.shp地理信息数据，经纬度、'poi'行业类别以及'cluster'所属聚类簇
    for feat in tqdm(pt_lyr): #循环feature
        pt=feat.geometry()
        pt_x=pt.GetX()
        pt_y=pt.GetY()
        poiIndices=feat.GetField('poi')
        clusterIndices=feat.GetField('cluster')
#        fid=feat.GetField('FID')
        target.append(clusterIndices)
        categoryList.append(poiIndices)
        dic.setdefault(clusterIndices,[]).append(poiIndices)
        poiCoordi.append((pt_x,pt_y))
     
    dic_len={}
    for key in dic.keys():
        dic_len[key]=len(dic[key])
       
    category={}
    for key in dic.keys():
        category[key]=Counter(dic[key]) #使用collections库Counter对象，用于行业类频数计算

    entropy={}
    for key in category.keys():
        s_entropy=0.0
        sum_v=dic_len[key]
        for i in category[key].keys():
            prob=category[key][i]*1.000/sum_v #计算簇行业类频数占总数的百分比
            s_entropy-=prob*math.log(prob) #计算信息熵
        category_num=len(category[key].keys()) #获取行业类数量
        max_entropy=math.log(category_num) #logN即为最大熵值
        if max_entropy==0: #排除特殊情况，并给定一个固定值标识
            entropy[key]=0.01
        else:
            frank_e=s_entropy/max_entropy
#            frank_e=(s_entropy/max_entropy)* sum_v    
            entropy[key]=frank_e  
#调试代码
#    print(entropy)   
#        print(name,kind,(pt_x,pt_y,))
#        i+=1
#        if i==12:
#            break
    del ds
    
#    print(len(categoryList))
    entropySinglePt=[entropy[key] for key in target]
#    print(entropySinglePt)
#    print(len(entropySinglePt))
    #将待使用的数据存储到pandas的DataFrame数据结构中，方便调研
    poiDF=DataFrame([[i,poiCoordi[i][0],poiCoordi[i][1],categoryList[i],target[i],entropySinglePt[i]] for i in range(len(categoryList))],columns=["IDX","long","lati","POI分类","POI聚类","POI信息熵"])
#    print(poiDF) 
    return poiDF

'''point的写入'''
def pointWriting(val,fn,pt_lyrName_w,ref_lyrN=False):
    ds=ogr.Open(fn,1) #注意fn值，否则会出现错误提示：
    
    '''参考层，用于空间坐标投影，字段属性等参照'''
    print(ref_lyrN)
    ref_lyr=ds.GetLayer(ref_lyrN)
    ref_sr=ref_lyr.GetSpatialRef() #获取对应的.shp文件的投影参考作为新.shp文件的投影
    print(ref_sr)
    ref_schema=ref_lyr.schema #查看属性表字段名和类型
    for field in ref_schema:
        print(field.name,field.GetTypeName())   

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
    
#    spatialRef = osr.SpatialReference()
#    spatialRef.SetWellKnownGeogCS("WGS84")      
    
    pt_lyr=pt_ds.CreateLayer(pt_lyrName_w,ref_sr,ogr.wkbPoint)
    
#    pt_lyr.SetProjection(ref_lyr.GetProjection()) #设置投影与参考栅格同
#    pt_lyr.SetGeoTransform(ref_lyr.GetGeoTransform()) #配置地理转换与参考栅格同    
    
    '''配置字段，名称以及类型和相关参数'''
    pt_lyr.CreateFields(ref_schema)
    LatFd=ogr.FieldDefn("origiLat",ogr.OFTReal)
    LatFd.SetWidth(8)
    LatFd.SetPrecision(3)
    pt_lyr.CreateField(LatFd)
    LatFd.SetName("Lat")
    pt_lyr.CreateField(LatFd)
    LatFd.SetName("entropy")
    pt_lyr.CreateField(LatFd)
    
    #    pt_lyr.CreateFields(ref_schema)
    preFd=ogr.FieldDefn("poi",ogr.OFTInteger)
    pt_lyr.CreateField(preFd)
    preFd.SetName("cluster")
    pt_lyr.CreateField(preFd)
     
    '''建立feature空特征和设置geometry几何类型'''
    print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())   
    
    for indexs in tqdm(val.index):
#        a=val.loc[indexs].values[:]
#        print(a)
#        print(len(a))
#        print(ok)
        wkt="POINT(%f %f)" %  (float(val.loc[indexs].values[1]),float( val.loc[indexs].values[2]))
#        wkt="POINT(%f %f)" %  (dataBunch.data[i][0], dataBunch.data[i][1])
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
#        for i_field in range(feat.GetFieldCount()):
#            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",val.loc[indexs].values[1])
        pt_feat.SetField("origiLong",val.loc[indexs].values[2])
        
        
#        print(wdDicComplete[key]['20140901190000'])
        pt_feat.SetField("poi",val.loc[indexs].values[3]) #
        pt_feat.SetField("cluster",val.loc[indexs].values[4])
        pt_feat.SetField("entropy",val.loc[indexs].values[5])
#        print(idx,int(pred[idx]),pt_ref.GetX())
#        idx+=1
        
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds

'''批量处理'''
def batchProcessing(dirpath,fileInfoList,savingPath_data):
    pattern1=re.compile(r'(.*?)[_]', re.S)
    pattern2=re.compile(r'(.*?)[.]', re.S)
    ptInfoDic={}
    for fn in fileInfoList:        
        newName=re.findall(pattern1, fn)[0]+"_entropy"    
        fn2=re.findall(pattern2, fn)[0]   
        ptInfoDic[newName]=pointReading(dirpath,fn2)        
        print(ptInfoDic[newName].columns)
        pointWriting(ptInfoDic[newName],dirpath,newName,ref_lyrN=fn2)   #,ref_lyrN=os.path.join(dirpath,fn2)      
        
    np.savez(os.path.join(savingPath_data,r'poiEntropy'),dic=ptInfoDic) 
#    rData=readingDataz(savingFp,"poiEntropy")["dic"]
 
if __name__=="__main__":
    #此次实验是读取所有.shp格式的文件，在实际操作时，可以使用实验22时的数据来简化处理，以及缩短计算时间。
    dirpath=r'C:\Users\Richi\sf_richiebao\sf_monograph\24_socialAttribute_03_entropyCalculation\data\POIPtsProjection'
    fileType=["shp"] 
    fileInfo=filePath(dirpath,fileType)
    fileInfoList=list(fileInfo.values())[0]
    #存储地理信息数据的路径，与原始.shp文件应处于一个文件加下，因此路径保持相同，不需单独设置路径，否则无法正确读取元.shp文件的信息，因为需要读取其投影参考
    #存储基本数据，用于已后分析，避免重复计算的路径
    savingPath_data=r'C:\Users\Richi\sf_richiebao\sf_monograph\24_socialAttribute_03_entropyCalculation\results\result_data'
    batchProcessing(dirpath,fileInfoList,savingPath_data)
