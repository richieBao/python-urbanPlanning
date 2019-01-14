# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 23:30:43 2017

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
filePath=r"D:/MUBENAcademy/pythonSystem/code/baiduMapPoiLandscape.csv"
f=open(filePath)
csvReader=csv.reader(f)
coordi=[]
for row in csvReader:
    if row:
        #coordi.append(eval(row[1]))
        #coordi.append(eval(row[2]))
        #coordi.append(row[0])
        coordi.append((eval(row[1]),eval(row[2])))
#print(coordi)
coordiArray=np.array(coordi)
print(coordiArray[:,0])
plt.plot(coordiArray[:,0],coordiArray[:,1],'ro',markersize=5)
plt.xlabel('lng')
plt.ylabel('lat')
plt.show()
f.close()