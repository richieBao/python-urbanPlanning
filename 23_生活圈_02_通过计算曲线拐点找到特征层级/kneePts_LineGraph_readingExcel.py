# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:28:02 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pylab import mpl
from mpl_toolkits.axisartist.axislines import Subplot

'''from kneed import DataGenerator, KneeLocator
因为kneed库无法正常加载，因此单独读取文件函数
kneed库官方地址：https://github.com/arvkevi/kneed
'''
from data_generator import DataGenerator
from knee_locator import KneeLocator
mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式

def lineGraph_kneePt(x,y):    
    #matplotlib的常规折线图
    font1 = {'family' : 'STXihei',
             'weight' : 'normal',
             'size'   : 50,
             }
    plt.figure(figsize=(8*3, 8*3))
    plt.plot(x,y,'ro-',label="POI独立点总数")
    plt.xlabel('聚类距离',font1)
    plt.ylabel('POI独立点',font1)
    plt.tick_params(labelsize=40)
    plt.legend(prop=font1)   
     
    #如果调整图表样式，需调整knee_locator文件中的plot_knee（）函数相关参数
    kneedle = KneeLocator(x, y, curve='convex', direction='decreasing')
    print(round(kneedle.knee, 3))
    print(round(kneedle.elbow, 3))
    kneedle.plot_knee()
    
    
if __name__=="__main__":  
    #读取存储有独立点变化的.xlsx文件，数据于GIS中观察判断，独立点（值为-1）与最多簇数量变化为人工判读，亦可以在实验22中聚类时提取
    fn=r'C:\Users\Richi\sf_richiebao\sf_monograph\23_socialAttribute_02_findTheCharacteristicLevelByCalculatingKneePoints\data\singlePts.xlsx'
    data= pd.read_excel(fn,index_col=0,header=0,sheet_name='Sheet1') #读取excel数据
    print(data)
    y=dataList=data.loc["单独点"].tolist()
    print(y)
    x=data.columns.tolist()
    print(x)
    lineGraph_kneePt(x,y)