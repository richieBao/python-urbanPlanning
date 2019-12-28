# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:13:41 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import Subplot
from pylab import mpl
import os

'''from kneed import DataGenerator, KneeLocator
因为kneed库无法正常加载，因此单独读取文件函数
kneed库官方地址：https://github.com/arvkevi/kneed
'''
from data_generator import DataGenerator
from knee_locator import KneeLocator

mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式

def lineGraph(x,eps):
    #matplotlib的常规折线图
    font1 = {'family' : 'STXihei',
             'weight' : 'normal',
             'size'   : 50,
             }
    plt.figure(figsize=(8*3, 8*3))
    plt.plot(eps,x,'ro-',label="POI独立点总数")
    plt.xlabel('聚类距离',font1)
    plt.ylabel('独立点频数',font1)
    plt.tick_params(labelsize=40)
    plt.legend(prop=font1)  
    

    # plt.show()
    
    #如果调整图表样式，需调整knee_locator文件中的plot_knee（）函数相关参数
    kneedle = KneeLocator(eps, x, curve='convex', direction='decreasing')
    print(round(kneedle.knee, 3))
    print(round(kneedle.elbow, 3))
    kneedle.plot_knee()
    
def readingData(fp,fn):
    readedData=np.load(os.path.join(fp,fn+".npy"))
    return readedData    
    
    
if __name__=="__main__":  
    #读取第22次实验所保存的数据
    fp=r'D:\data\data_01_Chicago\results_data_save\OSMClusterDataSave'
    fn_a=r'POI__LineGraph'
    fn_eps=r'POI__eps'
    
    data=readingData(fp,fn_a)
    eps=readingData(fp,fn_eps)
    lineGraph(data,eps)