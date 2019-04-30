# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 20:33:48 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import arcpy
from arcpy import env
import os
from arcpy.sa import *
import re
 
#设置工作环境
#worksapce_path=r"C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\results\POIPtsProjection"
worksapce_path=r"C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\results\POIPts2Raster"
#worksapce_path=r"C:\Users\Richi\Music\greenCluster\sf_projeciotn"
env.overwriteOutput=True
env.workspace=worksapce_path

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

'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]

'''提取分析所需数据，并转换为skleran的bunch存储方式，统一格式，方便读取。注意poi行业分类类标的设置'''
def points2Raster(fileInfo):   #传入数据，面向不同的数据存储方式，需要调整函数内读取的代码
    rootPath=list(fileInfo.keys())  #待读取数据文件的根目录
#    print(rootPath)
    dataName=flatten_lst(list(fileInfo.values()))  #待读取数据文件的文件名列表
#    print(dataName)
    coodiDic=[]
    pattern1=re.compile(r'(.*?)[_]', re.S)
    pattern2=re.compile(r'(.*?)[.]', re.S)
    
    for fName in dataName: 
        cell_size=int(re.findall(pattern1, fName)[0]) #按照文件名标识的数字作为单元大小，例如120_POI.shp，单元大小为120
        in_features=os.path.join(rootPath[0],fName)
#        value_field="entropy" #指定读取值的字段，作为栅格单元值
        value_field="cluster" #指定读取值的字段，作为栅格单元值
        out_raster=re.findall(pattern2, fName)[0]+".tif" #定义输出文件名
        
        print(cell_size, in_features, value_field, out_raster)        
        arcpy.PointToRaster_conversion(in_features, value_field, out_raster, "MOST_FREQUENT", "", cell_size) #将点转换为栅格数据
                    
'''如果没有投影，则定义投影'''
def defineFeatureProjection(fileInfo):
    rootPath=list(fileInfo.keys())  #待读取数据文件的根目录
#    print(rootPath)
    dataName=flatten_lst(list(fileInfo.values()))  #待读取数据文件的文件名列表
    outCS=arcpy.SpatialReference('WGS 1984 UTM Zone 49N') #定义投影
    for fName in dataName: 
        in_features=os.path.join(rootPath[0],fName)
        out_raster=fName+"_prj.shp"
        arcpy.Project_management(in_features, out_raster, outCS)
  
    
if __name__=="__main__":  
#    dirpath=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\results\sf' #待处理的数据位置，无投影
    dirpath=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\results\POIPtsProjection' #已定义投影的数据
    fileType=["shp"] 
    fileInfo=filePath(dirpath,fileType)
#    defineFeatureProjection(fileInfo)    
    points2Raster(fileInfo)
    
    
    