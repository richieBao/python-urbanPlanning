# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 18:38:15 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import matplotlib.pyplot as plt

from pylab import mpl #解决matplotlib中文显示问题，matplotlib提供的pylab的模块
mpl.rcParams['font.sans-serif'] = ['SimHei']  #可在交互式解释中，直接输入mpl.rcParams查看参数

filePath='D:\MUBENAcademy\pythonSystem\code\\5月25日早动线2\positions_9_34二十五日动线二.txt'
f=open(filePath,'r')
dataList=[]
while True:
    line=f.readline().split()
    if len(line)!=0:
        dataList.append(line)   
    if not line:break
print(dataList)
itemName=dataList.pop(0)
#print(itemName)

temp_A=[i[1] for i in dataList]
humi_A=[i[2] for i in dataList]
lightItem_A=[i[3] for i in dataList]
timeline=[int(i[-3])*3600+int(i[-2])*60+int(i[-1]) for i in dataList] #将时间转化为秒
relativeTimeline=[i-timeline[0] for i in timeline] #将时间转化为相对时间

#print(temp_A,humi_A,lightItem_A,relativeTimeline)

legend=plt.plot(relativeTimeline,temp_A,'r--',relativeTimeline,humi_A,'b--',relativeTimeline,lightItem_A,'y--')
print(legend)
plt.xlabel(r'时间线')
plt.ylabel(r'测量值')
plt.legend([legend[0],legend[1],legend[2]],["temp_A","humi_A","lightItem_A"],bbox_to_anchor=(0.15, 0.75))
plt.show()

f.close()

