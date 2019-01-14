# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:20:59 2017

@author: RichieBao-caDesign设计(cadesign.cn)
"""
dataPath='D:/MUBENAcademy/pythonSystem/ref/data.txt'
def extractCoords(dataPath):
    f=open(dataPath,'r')
    try:
        allData=f.read()
    finally:
        f.close()
    dataDic=eval(allData)
    floorList=dataDic['list'][0]['tile']
    partitionFun=lambda lst:[lst[i:i+2] for i in range(0,len(lst),2)]
    coordsList=[(data['name'],partitionFun(data['coords'])) for data in floorList] #列表形式
    coordsDic=dict(coordsList)  #字典形式
    return coordsList,coordsDic

coordsList,coordsDic=extractCoords(dataPath)
print(coordsList,'\n',coordsDic)