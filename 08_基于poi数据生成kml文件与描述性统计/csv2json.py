# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 14:41:14 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""

import json  #json数据格式
import csv  #csv数据格式
import os
import time

'''展平包含多个子列表的程序，使用了列表推导式和递归'''
flatten_lam=lambda lst:[m for n_lst in lst for m in flatten_lam(n_lst)] if type(lst) is list else [lst]

'''将csv数据格式转存为json数据格式，已当前时间为部分文件名'''   
def csv2json(rootPath,csvFilePath):
    csvFile=open(os.path.join(rootPath,csvFilePath),'r')
    csvReader=csv.reader(csvFile)
    #print(csvReader)
    #csvRow=[]
    csvRow=[row for row in csvReader if len(row)!=0]  #len(row)!=0 判断值不为空
    csvRow=flatten_lam(csvRow)  #读取的csv数据后的列表包含子列表，需要将其展平
    csvRow=[eval(row) for row in csvRow]  #读取的数据为字典字符串，需要使用eval()函数转换为纯粹的字典
    #print(csvRow)
    jsonFile=open(os.path.join(rootPath,str(time.time())+r'_csv2json.json'),'w')    
    json.dump(csvRow,jsonFile)  #将列表数据直接存储为json数据
    #jsonFile.write('\n') 
    print('csv2json done!')
    csvFile.close()
    jsonFile.close()

'''将json数据格式转存为csv数据格式，已当前时间为部分文件名'''  
def json2csv(rootPath,jsonFilePath):
    jsonFile=open(os.path.join(rootPath,jsonFilePath),'r')
    jsonDecodes=json.load(jsonFile) 
    #print(jsonDecodes)
    #jsonRow=[row for row in jsonDecodes if(row)!=0]
    #print(jsonRow)
    csvFile=open(os.path.join(rootPath,str(time.time())+r'_json2csv.csv'),'w')
    writer=csv.writer(csvFile)
    for row in jsonDecodes:
        #print(row)
        if len(row)!=0:
             writer.writerow([row])  #逐行写入csv数据
    print('json2csv done!')
    csvFile.close()
    jsonFile.close()

'''在条件设置时，给定一个根目录rootPath，以及待转换的csv或者json数据格式文件，转化后的文件自动生成于给定的根目录下'''    
if __name__=='__main__':
    rootPath=r"D:/MUBENAcademy/pythonSystem/code/"
    csvFilePath=r"baiduMapPoiSpotCSV2JSON.csv"
    jsonFilePath=r"baiduMapPoiSpotCSV2JSON.json"
    csv2json(rootPath,csvFilePath)
    json2csv(rootPath,jsonFilePath)
    