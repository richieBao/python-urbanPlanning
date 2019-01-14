# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 11:11:26 2018

@author: richieBao-caDesign设计(cadesign.cn)
"""

'''DBSCAN基于密度空间的聚类，聚类所有种植点'''
print(__doc__)

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import re
from sklearn import cluster

'''DBSCAN基于密度空间的聚类，给定点坐标值数组'''
def affinityPropagationForPoints(data):
    t1=time.time()     
    db=cluster.DBSCAN(eps=16,min_samples=3,metric='euclidean') #调整eps参数，和min_sample参数，获得适宜的聚类结果
    y_db=db.fit_predict(data)  #获取聚类预测类标
    t2=time.time()    
    tDiff_af=t2-t1 #用于计算聚类所需时间
    print("模型训练持续时间:",tDiff_af)
    
    pred=y_db  
    print("预测类标，与簇数：",pred,len(np.unique(pred)))  #打印查看预测类标和计算聚类簇数
    
    t3=time.time()
    plt.close('all')
    plt.figure(1,figsize=(15,15))
    plt.clf()
    cm=plt.cm.get_cmap('nipy_spectral')  #获取内置色带
    sc=plt.scatter(data[...,0],data[...,1],s=10,alpha=0.8,c=pred,cmap=cm) #c参数设置为预测值，传入色带，根据c值显示颜色
    plt.show()
    t4=time.time()
    tDiff_plt=t4-t3  #计算图表显示时间
    print("图表显示持续时间：",tDiff_plt)
    return pred,np.unique(pred)  #返回DBSCAN聚类预测值。和簇类标

'''读取grasshopper写入的.txt点坐标文件'''
def txtReading(fn):
    f=open(fn,'r')
    dataList=[]
    pat=re.compile('{(.*?)}')
    while True:
        line=f.readline().strip()    
        if len(line)!=0:
            line=pat.findall(line)[0].split(',')
            line=[float(i) for i in line]
            dataList.append(line)
        if not line:break
    f.close()
    dataArray=np.array(dataList)
    return dataArray

if __name__ == "__main__":
    fnPath=r'D:\MUBENAcademy\pythonSystem\dataB'
    fn=r'vegetitionCluster.txt'
    txtArray=txtReading(os.path.join(fnPath,fn))
    pred,predUnique=affinityPropagationForPoints(txtArray)
    predTxt=r'vegetitionPred.txt'
    np.savetxt(os.path.join(fnPath,predTxt),pred.astype(int),delimiter=',') #写入类标预测数据
    predU=r'predUnique.txt'
    np.savetxt(os.path.join(fnPath,predU),predUnique.astype(int),delimiter=',')  #写入类标名称文件