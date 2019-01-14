# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 10:29:12 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import json  #json数据格式库
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree
from pykml.factory import KML_ElementMaker as KML  #定义.kml文件的库，可以在Google Earth中夹中，或者在GIS平台下加载
import conversionofCoordi as cc  #之前课程中阐述的百度坐标系和GPS84坐标系转换程序
import codecs  #在写入文件时，定义存储类型为"UTF-8"
from scipy import stats
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']

'''将采集的百度POI数据中经纬度坐标，散点图显示，查看其位置关系。注意，该函数中为百度坐标系'''
def coordiScatter(jsonFilePath):  
    f=open(jsonFilePath,'r')
    jsonDecodes=json.load(f) #读取json数据格式文件  
    #print(jsonDecodes)
    coordi=[]
    for value in jsonDecodes:  #从json数据据格式中提取经纬度
        #print(value)
        coordi.append((value['location']['lat'],value['location']['lng']))
    #print(coordi)
    f.close()
    coordiArray=np.array(coordi)
    #print(coordiArray[:,0])
    fig=plt.figure(figsize=(8,8))
    ax=fig.add_subplot(111)
    ax.plot(coordiArray[:,0],coordiArray[:,1],'ro',markersize=5)
    ax.set_xlabel('lng')
    ax.set_ylabel('lat')
    plt.show()    

'''将采集的poi中经纬度信息另存为.kml格式文件，方便在Google Earth或者GIS平台中加载查看'''
def placemark_KML(jsonFilePath,kmlPath):
    f=open(jsonFilePath,'r')
    jsonDecodes=json.load(f)   
    coordi=[]
    for value in jsonDecodes: #提取poi经纬度和name信息，并将百度坐标系转换为GPS84坐标系
        converCoordiGCJ=cc.bd09togcj02(value['location']['lng'],value['location']['lat'])
        converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
        coordi.append((converCoordiGPS84[0],converCoordiGPS84[1],value['name']))
    f.close()    
    #print(coordi)
    folderKML=KML.Folder(KML.Placemark(KML.name(coordi[0][2]),KML.Point(KML.coordinates(str(coordi[0][0])+','+str(coordi[0][1])+',0'))))  #使用pykml库建立<Folder></Folder>跟标签，并追加第一个地标
    for i in range(1,len(coordi)):
        folderKML.append(KML.Placemark(KML.name(coordi[i][2]),KML.Point(KML.coordinates(str(coordi[i][0])+','+str(coordi[i][1])+',0'))))  #在Folder标签下追加剩余的所有地标
    content=etree.tostring(etree.ElementTree(folderKML),encoding='unicode',pretty_print=True)  #将元素序列化为编码字符串
    print(content)
    with codecs.open(kmlPath,'w',"UTF-8") as kp: #指定文件编码格式为"UTF-8"，写入地标文件
        kp.write(content)
        
'''描述性统计'''
def basicStatistics(jsonFilePath):
    f=open(jsonFilePath,'r')
    jsonDecodes=json.load(f) 
    #print(jsonDecodes)
    poiInfo={}
    for value in jsonDecodes:
        keys=value['detail_info'].keys()
#        if 'overall_rating' in keys and 'comment_num' in keys :
#            poiInfo[value['name']]=(value['detail_info']['overall_rating'],value['detail_info']['comment_num'])
        if 'overall_rating' in keys and 'price' in keys :
            poiInfo[value['name']]=(value['detail_info']['overall_rating'],value['detail_info']['price'])
            
    #print(poiInfo)
    poiArray=np.array(list(poiInfo.values()),dtype='float')
    #print(poiArray)
    
    '''中心位置(均值、中位数、众数)'''
    rating=poiArray[...,0]
    print(rating)
    poiMean=np.mean(rating)
    poiMedian=np.median(rating)
    poiMode=stats.mode(rating)
    #print(poiMean,poiMedian,poiMode[1])
    print("均值=%.2f;中位数=%.2f;众数值=%.2f,众数次数=%d"%(poiMean,poiMedian,poiMode[0][0],poiMode[1][0]))
    
    '''发散程度(极差、方差、标准差、变异系数)'''
    poiPtp=np.ptp(rating)
    poiVar=np.var(rating)
    poiStd=np.std(rating)
    poiCV=np.mean(rating)/np.std(rating)
    print("极差=%.2f;方差=%.2f;标准差=%.2f;变异系数=%.2f"%(poiPtp,poiVar,poiStd,poiCV))
    
    '''偏差程度(Z-Score/z-分数)，为测量值距均值相差的标准差的数目,通常其绝对值大于3将视为异常'''
    zScore=(rating-np.mean(rating))/np.std(rating)
    print("Z-Score:\n",zScore,'\n')
    
    '''相关程度(协方差、相关系数),实验评分与评论数量之间是否存在相关关系'''
    #poiCOV=np.cov(poiArray[...,0],poiArray[...,1],bias=1)
    poiCOV=np.cov(poiArray.transpose(),bias=1)
    #poiCorrcoef=np.corrcoef(poiArray[...,0],poiArray[...,1])   
    poiCorrcoef=np.corrcoef(poiArray.transpose()) 
    print("协方差:\n",poiCOV,'\n','相关系数:\n',poiCorrcoef)
    
    '''利用matplotlib进行图分析'''    
    fig, axes= plt.subplots(ncols=4,nrows=2, figsize=(18, 9))
    ax=axes.flatten()
    
    '''频数分析'''
    grades=[]
    for score in rating:
        if score>=0 and score <=5:
            grade='E' if score < 2 else ('D' if score < 3 else ('C' if score < 4 else ('B' if score < 5 else 'A')))
            grades.append(grade)
    print("########")
    print(grades)
    xticks=['A', 'B', 'C', 'D', 'E']
    gradeGroup={}
    for grade in grades:
        gradeGroup[grade] = gradeGroup.get(grade, 0) + 1    
    
    print(gradeGroup)
    '''
    countA=0
    for i in grades:
        if i=='A':countA+=1
    print(countA)
    '''    
    #bar/柱状图    
    titleName=r"美食"
    ax[0].bar(range(5),[gradeGroup.get(xtick,0) for xtick in xticks],align='center',color='y')
    ax[0].set_title(titleName+'评分的频数柱状图')
    ax[0].set_xlabel('Grade')

    ax[1].pie([gradeGroup.get(xtick,0) for xtick in xticks],labels=xticks,autopct='%1.1f%%')
    ax[1].set_title(titleName+'评分的频数饼形图')
    
    poiMax=poiArray.max(axis=0)
    poiMin=poiArray.min(axis=0)
    min_maxNormalization=(poiArray-poiMin)/(poiMax-poiMin)  #min-max标准化（Min-Max Normalization）,结果映射到[0,1]之间
    #print(min_maxNormalization)
    ax2Legend=ax[2].plot(min_maxNormalization[...,0],'r--',min_maxNormalization[...,1],'y--')
    ax[2].set_title(titleName+'评分与价格折线图')
    ax[2].legend([ax2Legend[0],ax2Legend[1]],['评分','价格'],bbox_to_anchor=(0.35,0.25))

    ax[3].hist(rating, 10, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)
    ax[3].set_title(titleName+'评分直方图')

    ax[4].hist(rating,10,normed=True,histtype='step',cumulative=True)
    ax[4].set_title(titleName+'评分累计曲线')
    
    ax[5].scatter(rating,poiArray[...,1],c='y',alpha=0.6)
    ax[5].set_title(titleName+'评分(x轴)与价格(y轴)散点图关系分析')
    
    ax[6].boxplot([min_maxNormalization[...,0],min_maxNormalization[...,1]],labels=['评分','价格'])
    ax[6].set_title(titleName+'评分/价格箱形图')
    
    fig.tight_layout()
    plt.show()
    
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
    

if __name__=="__main__":
#    jsonFilePath=r"D:/MUBENAcademy/pythonSystem/code/poi_01_delicacy.json"
#    kmlPath=r"D:/MUBENAcademy/pythonSystem/code/poi_01_delicacy.kml"
#    jsonFilePath=r'D:\project\gisData\poi\poi_0_delicacy.json'
#    kmlPath=r'D:\project\gisData\poi\poi_0_delicacy.kml'
    
    dirpath=r'D:\project\gisData\poi'
    fileType=["json"]
    fileinfo=filePath(dirpath,fileType)
    print(fileinfo)
    for key in fileinfo:
        for pathName in fileinfo[key]:
            jsonFilePath=os.path.join(key,pathName)
            kmlPath=os.path.join(key,pathName[:-4]+r'kml')
            coordiScatter(jsonFilePath)
            placemark_KML(jsonFilePath,kmlPath)
        
#    coordiScatter(jsonFilePath)
#    placemark_KML(jsonFilePath,kmlPath)
#    basicStatistics(jsonFilePath)
    