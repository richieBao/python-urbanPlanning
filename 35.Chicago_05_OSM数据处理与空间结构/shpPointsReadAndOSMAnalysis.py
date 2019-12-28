# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 14:28:05 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicagoo
"""
from osgeo import ogr
from ospybook.vectorplotter import VectorPlotter  #pip install https://github.com/cgarrard/osgeopy-code/raw/master/ospybook-latest.zip
import os,re,h5py,osr
import pandas as pd
import numpy as np
from tqdm import tqdm
import kneePts_LineGraph as kneeLine #调入kneePts_LineGraph.py文件

'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]

'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义。返回的文件名不包含后缀名 '''
def filePathBesidesSuffix(dirpath,fileType):
    fileInfo={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       #print(i,'\n')
       #print(dirpath,'\n',dirNames,'\n',fileNames,'\n')
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f.split('.')[0] for f in fileNames if f.split('.')[-1] in fileType] #不包含后缀名
           #if not tempList :
               #print(i,"NULL")
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               fileInfo.setdefault(dirpath,tempList)
    return fileInfo  

'''point的读与可视化'''
def pointReading(ptsShpFn,pt_lyrName):
    ds=ogr.Open(ptsShpFn,0) #0为只读模式，1为编辑模式
    if ds is None:
        sys.exit('Could not open{0}'.format(fn))
    pt_lyr=ds.GetLayer(pt_lyrName) #可以直接数据层(文件)名或者指定索引
    # vp = VectorPlotter(True)
    # vp.plot(pt_lyr,'bo')
    
    tempDic={'type':[],'tagkey':[],'tagvalue':[],'cluster':[],'lon':[],'lat':[]}
    i=0
    for feat in pt_lyr:
        pt=feat.geometry()
        # pt_x=pt.GetX()
        # pt_y=pt.GetY()
        # pt_type=feat.GetField('type')
        # pt_tagkey=feat.GetField('tagkey')
        # pt_tagvalue=feat.GetField('tagvalue')
        # pt_cluster=feat.GetField('cluster')
        # print(pt_type,pt_tagkey,pt_tagvalue,pt_cluster,(pt_x,pt_y,))
        tempDic['type'].append(feat.GetField('type'))
        tempDic['tagkey'].append(feat.GetField('tagkey'))
        tempDic['tagvalue'].append(feat.GetField('tagvalue'))
        tempDic['cluster'].append(feat.GetField('cluster'))
        tempDic['lon'].append(pt.GetX())
        tempDic['lat'].append(pt.GetY())     
        
        i+=1
        # if i==4:
        #     break
    del ds
    return tempDic

#读取文件夹文件，并按照文件所包含的数字排序
def fnListOrder(fnList):
    pattern=re.compile('\d+', re.S)
    fn_numExtraction=[(int(re.findall(pattern, fName)[0]),fName) for fName in fnList] #提取文件名中的数字，即聚类距离。并对应文件名
    fn_sort=sorted(fn_numExtraction)
    # print(fn_sort)
    fn_sorted=[i[1] for i in fn_sort]
    # print(fn_sorted)
    return fn_sorted

#批量读取.shp格式点文件指定字段值，并存储为dataframe格式文件及保存于硬盘为.hdf5文件    
def dfPtsInfoBundle(ptsShpFp,fns,datSaveFp,datSaveFn):  
    # print(fns)
    # iterablesLabels=[fns,['type', 'tagkey', 'tagvalue', 'cluster','lon','lat']]
    # multiIdx=pd.MultiIndex.from_product(iterablesLabels, names=['first', 'second'])
    # print(multiIdx)
    ptsValueDic={}
    for fn in tqdm(fns):
        tempDic=pointReading(ptsShpFp,fn)
        # print("_"*50,"\n")
        # print(tempDic)
        ptsValueDic.setdefault(fn,tempDic)
    
    # print(ptsValueDic)
    #multiindex dataframe 建立多层dataframe数据。以每层聚类文件名为第1层，以字段为第2层
    reformDic = {(outerKey, innerKey): values for outerKey, innerDict in ptsValueDic.items() for innerKey, values in innerDict.items()}
    # dfPtsFields=pd.DataFrame(ptsValueDic, index=multiIdx)
    dfPtsFields=pd.DataFrame(reformDic)
    # print(dfPtsFields['40_POI'])
    
    #用pandas自带的保存dataframe为hdf5工具保存数据
    hdf5Fn=os.path.join(datSaveFp,datSaveFn)
    if os.path.exists(hdf5Fn):
        os.remove(hdf5Fn)
    else:
        print("Can not delete the file as it doesn't exists,built new one!")
        
    # f=h5py.File(hdf5Fn, "a")
    # if "dfPtsVals" in f.keys(): #如果索引存在于h5py数据库中，则移除该数据，为下次循清空
    #     del f["dfPtsVals"]    
    # dfPtsFields_Hdf5=f.create_dataset("dfPtsVals",data=dfPtsFields)
    # print(dfPtsFields_Hdf5)
        
    dfPtsFields.to_hdf(hdf5Fn,key='dfPtsVals', mode='a') #.to_hdf()保存dataframe为hdf5
    print("\ndfPtsFields has been saved as hdf5 file!")
    # dfPtsHdf=pd.read_hdf(hdf5Fn, 'dfPtsVals')
    # print(dfPtsHdf)
    return dfPtsFields


#A/B/C_将聚类的POI数据，写入.shp文件，用于GIS调用,三部分可以调整为一个函数，需要弹性设计待写入.shp文件中字段的内容。
'''A_将聚类的POI数据，写入.shp文件，用于GIS调用。'''
def point2Shp(dfMax,fn,pt_lyrName_w,ref_lyr=False):
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
    # print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())    
   
#    idx=0
    
    for i in dfMax.index:  #循环feature         
#        print(key)
        '''设置几何体'''
        #pt_ref=feat.geometry().Clone()
        # converCoordiGCJ=cc.bd09togcj02(dataBunch.data[i][1],dataBunch.data[i][0])
        # converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
#        print(wdCoordiDicSingle[key][1],wdCoordiDicSingle[key][0])
#        print(converCoordiGPS84[0], converCoordiGPS84[1])
        wkt="POINT(%f %f)" %  (dfMax["lon"][i], dfMax["lat"][i])
#        wkt="POINT(%f %f)" %  (dataBunch.data[i][0], dataBunch.data[i][1])
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
#        for i_field in range(feat.GetFieldCount()):
#            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",dfMax["lat"][i])
        pt_feat.SetField("origiLong",dfMax["lon"][i])
        
        
#        print(wdDicComplete[key]['20140901190000'])
        pt_feat.SetField("type",dfMax["type"][i]) #
        pt_feat.SetField("tagkey",dfMax["tagkey"][i])
        pt_feat.SetField("tagvalue",dfMax["tagvalue"][i])
        pt_feat.SetField("cluster",int(dfMax['cluster'][i]))
#        print(idx,int(valueArray[idx]),pt_ref.GetX())
#        idx+=1
        
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds       

 
'''B_将聚类的POI数据，写入.shp文件，用于GIS调用。'''
def point2ShpMerger(dfMax,fn,pt_lyrName_w,ref_lyr=False):
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
    # preFd=ogr.FieldDefn("type",ogr.OFTString)
    # pt_lyr.CreateField(preFd)
    # preFd.SetName("tagkey")
    # pt_lyr.CreateField(preFd)
    # preFd.SetName("tagvalue")
    # pt_lyr.CreateField(preFd)
    
    preFd=ogr.FieldDefn("idx",ogr.OFTInteger)
    pt_lyr.CreateField(preFd)
    preFd.SetName("layer")
    pt_lyr.CreateField(preFd)    
    
    
    
    
#    stationName=ogr.FieldDefn("stationN",ogr.OFTString)
#    pt_lyr.CreateField(stationName)    
    
#    preFd.SetName("ObservTime")
#    pt_lyr.CreateField(preFd)  
#   
     
    '''建立feature空特征和设置geometry几何类型'''
    # print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())    
   
#    idx=0
    
    for i in dfMax.index:  #循环feature         
#        print(key)
        '''设置几何体'''
        #pt_ref=feat.geometry().Clone()
        # converCoordiGCJ=cc.bd09togcj02(dataBunch.data[i][1],dataBunch.data[i][0])
        # converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
#        print(wdCoordiDicSingle[key][1],wdCoordiDicSingle[key][0])
#        print(converCoordiGPS84[0], converCoordiGPS84[1])
        wkt="POINT(%f %f)" %  (dfMax["lon"][i], dfMax["lat"][i])
#        wkt="POINT(%f %f)" %  (dataBunch.data[i][0], dataBunch.data[i][1])
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
#        for i_field in range(feat.GetFieldCount()):
#            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",dfMax["lat"][i])
        pt_feat.SetField("origiLong",dfMax["lon"][i])
        
        
#        print(wdDicComplete[key]['20140901190000'])
        pt_feat.SetField("layer",int(dfMax["layer"][i])) #
        pt_feat.SetField("idx",int(dfMax["idx"][i]))
        # pt_feat.SetField("tagvalue",dfMax["tagvalue"][i])
        # pt_feat.SetField("cluster",int(dfMax['cluster'][i]))
#        print(idx,int(valueArray[idx]),pt_ref.GetX())
#        idx+=1
        
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds           
    

'''C_将聚类的POI数据，写入.shp文件，用于GIS调用。'''
def point2ShpNLargest(dfMax,fn,pt_lyrName_w,ref_lyr=False):
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
    preFd.SetName("frequency")
    pt_lyr.CreateField(preFd)    
    
#    stationName=ogr.FieldDefn("stationN",ogr.OFTString)
#    pt_lyr.CreateField(stationName)    
    
#    preFd.SetName("ObservTime")
#    pt_lyr.CreateField(preFd)  
#   
     
    '''建立feature空特征和设置geometry几何类型'''
    # print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())    
   
#    idx=0
    
    for i in dfMax.index:  #循环feature         
#        print(key)
        '''设置几何体'''
        #pt_ref=feat.geometry().Clone()
        # converCoordiGCJ=cc.bd09togcj02(dataBunch.data[i][1],dataBunch.data[i][0])
        # converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
#        print(wdCoordiDicSingle[key][1],wdCoordiDicSingle[key][0])
#        print(converCoordiGPS84[0], converCoordiGPS84[1])
        wkt="POINT(%f %f)" %  (dfMax["lon"][i], dfMax["lat"][i])
#        wkt="POINT(%f %f)" %  (dataBunch.data[i][0], dataBunch.data[i][1])
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
#        for i_field in range(feat.GetFieldCount()):
#            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",dfMax["lat"][i])
        pt_feat.SetField("origiLong",dfMax["lon"][i])
        
        
#        print(wdDicComplete[key]['20140901190000'])
        pt_feat.SetField("type",dfMax["type"][i]) #
        pt_feat.SetField("tagkey",dfMax["tagkey"][i])
        pt_feat.SetField("tagvalue",dfMax["tagvalue"][i])
        pt_feat.SetField("cluster",int(dfMax['cluster'][i]))
        pt_feat.SetField("frequency",int(dfMax['frequency'][i]))
#        print(idx,int(valueArray[idx]),pt_ref.GetX())
#        idx+=1
        
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds       


    
#提取最大频数区域,以及合并最大频数区域
def maximalFrequencyPts(dfPtsFields,fns_sorted):
    frequencyDic={}
    i=0
    j=1
    dfObj=pd.DataFrame() #用于追加每层级的聚类信息数据
    for fn in tqdm(fns_sorted):
        tempDf=dfPtsFields[fn]
        # print(tempDf)
        #根据条件，删除行
        idx = tempDf[ tempDf['cluster'] == -1 ].index  #删除字段“cluster”值为-1对应的行，即独立的OSM点数据，未形成聚类
        tempDf.drop(idx,inplace=True)    
        # print(tempDf)
        frequncyDf=tempDf["cluster"].value_counts() #计算cluster的频数，返回值格式为Series
        idxOfMaxValue=frequncyDf.idxmax() #返回最大值对应的索引
        # print(frequncyDf[idxOfMaxValue])
        #仅保留最大值对应的行
        idxMax = tempDf[ tempDf['cluster'] != idxOfMaxValue ].index
        tempDf.drop(idxMax,inplace=True)
        # print(tempDf['cluster'])
        
        pt_lyrName_w=r'%s_clusterMax'%fn #字符串格式化输出文件名
        fn=r"D:\data\data_01_Chicago\QGisDat\OSMPointsCluster\OSMClusterMax"
        # point2Shp(tempDf,fn,pt_lyrName_w)  #将最大值存储为.shp格式文件，执行时，打开该行
        # print("\n%s has been written to disk"%i)
        # print(tempDf)
        tempDf["layer"]=j #增加字段/column，标识（50个）层级
        dfObj=dfObj.append(tempDf)
        # print(dfObj)
        j+=1

        #下部分3行代码用于代码调试，仅执行小部分数据，加快编写/调试速度
        # i+=1
        # if i==3:
        #     break

    # print(frequencyDic)
    print("\n","_"*50,"\n")
    # print(dfObj["cluster"])
    # dfDuplicateSum=dfObj.groupby(['lon','lat'], as_index=False)['cluster'].sum()
    dfObj["idx"]=1 #增加新字段/column，求和之后，表示（50）层级叠加/重叠的次数
    #如果同时满足字段['lon','lat']相同的条件，则根据指定条件.agg({'layer':'first', 'idx':'sum'})根据计算要求，分别计算指定字段。‘first’为仅保留第一个值，'sum'为求和
    dfDuplicateSum=dfObj.groupby(['lon','lat'], as_index=False).agg({'layer':'first', 'idx':'sum'}).reset_index() 
    # print(dfDuplicateSum)

    pt_lyrName_w_merger=r'OSMclusterMaxMerge' #字符串格式化输出文件名
    fnMerger=r"D:\data\data_01_Chicago\QGisDat\OSMPointsCluster\OSMClusterMax\OSMClusterMaxMerge"
    point2ShpMerger(dfDuplicateSum,fnMerger,pt_lyrName_w_merger) #存储所有层的信息在一个单独.shp文件中，包含层级聚类点的变化和点叠合的数量
    print("OSM Cluster max Merger has been written to disk")

#独立点频数折线图与拐点
def frequencyMinusOneKnee(dfPtsFields,fns_sorted):
        frequencyDic={}
        i=0
        j=1
        frequencyMinusOneDic={}
        frequencyMinusOneList=[]
        for fn in tqdm(fns_sorted):
            tempDf=dfPtsFields[fn]
            # frequncyDf=tempDf["cluster"].value_counts().to_dict()
            frequncyDf=tempDf["cluster"].value_counts() #计算频数
            # print(frequncyDf)
            # print(frequncyDf[-1])
            frequencyMinusOneDic[fn]=frequncyDf[-1] #每一层级对应的独立点频数，为字典
            frequencyMinusOneList.append(frequncyDf[-1]) #仅按层级顺序存储独立点频数
                        
            # i+=1
            # if i==3:
            #     break            
        # print(frequencyMinusOneList)  
        kneeLine.lineGraph(frequencyMinusOneList, [int(i.split("_")[0]) for i in fns_sorted])

#前n最大聚类提取
def nMaximalCluster(dfPtsFields,fns_sorted,n=10):
    frequencyDic={}
    i=0
    dfObj=pd.DataFrame()
    
    # Define a function to map the values 
    def set_value(row_number, assigned_value): 
        return assigned_value[row_number] 
    
    for fn in tqdm(fns_sorted):
        tempDf=dfPtsFields[fn]
        # print(tempDf)
        idx = tempDf[ tempDf['cluster'] == -1 ].index 
        tempDf.drop(idx,inplace=True)    
        # print(tempDf)
        frequncyDf=tempDf["cluster"].value_counts()    

        #Get the rows of a DataFrame/ sorted by the n largest values of columns.
        nLargest=frequncyDf.nlargest(n) 
        # print(nLargest.keys())
        nLargestCluster=tempDf[tempDf['cluster'].isin(nLargest.keys())] 
        # print(nLargestCluster["cluster"])
        
        
        # print(nLargest.to_dict())
        # Add a new column named 'Price' 
        nLargestCluster['frequency'] = nLargestCluster['cluster'].apply(set_value, args =(nLargest.to_dict(), ))
        # print(nLargestCluster)

        
        pt_lyrName_w=r'%s_clusterNLargest'%fn #字符串格式化输出文件名
        fnNLargest=r"D:\data\data_01_Chicago\QGisDat\OSMPointsCluster\OSMNLargest"
        point2ShpNLargest(nLargestCluster,fnNLargest,pt_lyrName_w) #前n最大聚类存储为.shp文件
        
        # i+=1
        # if i==3:
        #     break  
    print("_"*50,"\n","n largest Cluster has been written to rasters!")

if __name__=="__main__":  
    ptsShpFp=r"D:\data\data_01_Chicago\QGisDat\OSMPointsCluster\OSMChicagoCluster"
    pt_lyrName=r"20_POI"
    
    fileType=["shp"] 
    fileInfo=flatten_lst(list(filePathBesidesSuffix(ptsShpFp,fileType).values()))
    fns_sorted=fnListOrder(fileInfo)
    datSaveFp=r"D:\data\data_01_Chicago\results_data_save\dfPtsValuesBundleDfSave"
    datSaveFn=r"dfPtsValue.hdf5"
    # dfPtsFields=dfPtsInfoBundle(ptsShpFp,fns_sorted[:3],datSaveFp,datSaveFn) #写与调试用
    #批量读取.shp格式点文件指定字段值，并存储为dataframe格式文件及保存于硬盘为.hdf5文件  
    # dfPtsFields=dfPtsInfoBundle(ptsShpFp,fns_sorted,datSaveFp,datSaveFn) #返回OSM Points（.shp格式）的指定字段值
    
    #提取最大频数区域,以及合并最大频数区域
    # maximalFrequencyPts(dfPtsFields,fns_sorted)
       
    #读取pandas存储的hdf5文件
    # hdf5Fn=os.path.join(datSaveFp,datSaveFn)
    # dfPtsHdf=pd.read_hdf(hdf5Fn, 'dfPtsVals')
    
    #独立点频数折线图与拐点
    # frequencyMinusOneKnee(dfPtsHdf,fns_sorted)

    #前n最大聚类提取
    nMaximalCluster(dfPtsHdf,fns_sorted)