# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 11:23:43 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import re
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

fn=r'D:\MUBENAcademy\pythonSystem\dataB\paraPolyline.txt'
pred_fn=r'D:\MUBENAcademy\pythonSystem\dataB\paraPolylinePred.txt'

'''读取文本数据'''
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

dataArray=txtReading(fn)
X=dataArray[...,0:2] #解释变量(X,Y值)
y=dataArray[...,2] #目标变量(Z值)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=1)

forest=RandomForestRegressor(n_estimators=1000,criterion='mse',random_state=1,n_jobs=-1)
forest.fit(X_train,y_train)
y_train_pred=forest.predict(X_train)
y_test_pred=forest.predict(X_test)

print('MSE train:%.3f,test:%.3f'%(mean_squared_error(y_train,y_train_pred),mean_squared_error(y_test,y_test_pred)))
print('R^2 train:%.3f,test:%.3f'%(r2_score(y_train,y_train_pred),r2_score(y_test,y_test_pred)))

#plt.figure(figsize=(20, 15)) 
plt.scatter(y_train_pred,y_train_pred-y_train,c='blue',marker='o',label='Training data')
plt.scatter(y_test_pred,y_test_pred-y_test,c='lightgreen',marker='s',label='Test data')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0,xmin=-10,xmax=30,lw=2,color='red')
plt.xlim([-10,30])
plt.show()

'''预测值(高程Z值)，并写入.txt文件，用于grasshopper读取'''
dataPred=txtReading(pred_fn) #读取预测解释变量
dataX=dataPred[...,0:2]
predValue=forest.predict(dataX)
prd_w_fn=r'D:\MUBENAcademy\pythonSystem\dataB\paraPolylineY.txt'
wf=open(prd_w_fn,'w')
for i in range(len(predValue)):
    if i==len(predValue)-1:
        wf.write(str(predValue[i]))
    else:
        wf.write(str(predValue[i])+',')    

wf.close()