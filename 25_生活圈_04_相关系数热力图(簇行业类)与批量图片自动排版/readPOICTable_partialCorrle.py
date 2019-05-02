# -*- coding: utf-8 -*-
"""
Created on Wed May  1 23:28:40 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
"""
import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']

#POI行业类映射
class_mapping=[(0, 'poi_0_delicacy'),
                 (1, 'poi_10_medicalTreatment'),
                 (2, 'poi_11_carService'),
                 (3, 'poi_12_trafficFacilities'),
                 (4, 'poi_13_finance'),
                 (5, 'poi_14_realEstate'),
                 (6, 'poi_15_corporation'),
                 (7, 'poi_16_government'),
                 (8, 'poi_1_hotel'),
                 (9, 'poi_2_shopping'),
                 (10, 'poi_3_lifeService'),
                 (11, 'poi_4_beauty'),
                 (12, 'poi_5_spot'),
                 (13, 'poi_6_entertainment'),
                 (14, 'poi_7_sports'),
                 (15, 'poi_8_education'),
                 (16, 'poi_9_media')]

'''读取numpy.save()存储的数据'''
def readingData(fp,fn):
    readedData=np.load(os.path.join(fp,fn+".npy"))
    return readedData    

'''批量计算相关性，绘制热力图'''    
def snsBundleSavig(data,label,savingPath):
    for i in range(len(data)):
        currentData=data[i]
        sns.set()
        data_frame=pd.DataFrame(currentData,index=label, columns=label)
        f, ax = plt.subplots(figsize=(9*2, 6*2))
        sns.heatmap(data_frame, annot=True, fmt=".2f", linewidths=.5, ax=ax)
        plt.savefig(os.path.join(savingPath,"partialCorrle_%d.png"%i))
           
if __name__=="__main__":  
    fp=r'C:\Users\Richi\sf_richiebao\sf_monograph\25_socialAttribute_04_partialCorrle_picArranging\data'
    partialCorrleFn=r'POI__partialCorrelations'
    partialCorrle=readingData(fp,partialCorrleFn) #读取numpy.save()存储的聚类信息，参看实验22

    label=[i[1] for i in class_mapping] #读取行业类的映射标签

    savingPath=r'C:\Users\Richi\sf_richiebao\sf_monograph\25_socialAttribute_04_partialCorrle_picArranging\results\single' #图表保存位置
    snsBundleSavig(partialCorrle,label,savingPath)