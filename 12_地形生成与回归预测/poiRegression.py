# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 11:43:44 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import re
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import pandas as pd
import json
import numpy as np
from sklearn.datasets import base
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import RANSACRegressor,LinearRegression,Ridge,RidgeCV,Lasso,ElasticNet
#from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
#from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import manifold

dataPath=r'D:\MUBENAcademy\pythonSystem\code\poiXianOldTown\poi_1_hotel.json'

explanatoryVariable=r'D:\MUBENAcademy\pythonSystem\dataB\explanatoryVariable.txt'
targetVariable=r'D:\MUBENAcademy\pythonSystem\dataB\targetVariable.txt'
predictedFeatures=r'D:\MUBENAcademy\pythonSystem\dataB\predictedFeatures.txt'

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
    dataArray=np.array(dataList) #数据输出为数组形式
    return dataArray

'''提取分析所需数据，并转换为skleran的bunch存储方式，统一格式，方便读取。'''
def json2bunch(fName):   #传入数据，面向不同的数据存储方式，需要调整函数内读取的代码
    infoDic=[]
    f=open(fName)
    jsonDecodes=json.load(f)
    j=0
    for info in jsonDecodes:
        condiKeys=info['detail_info'].keys()
        if 'price' in condiKeys and'overall_rating' in condiKeys and 'service_rating' in condiKeys and 'facility_rating' in condiKeys and 'hygiene_rating' in condiKeys and 'image_num' in condiKeys and 'comment_num' in condiKeys and 'favorite_num' in condiKeys: #提取的键都有数据时，才提取，否则忽略掉此数据
            if 50<float(info['detail_info']['price'])<1000: #设置价格区间，提取数据
                j+=1
                infoDic.append([info['location']['lat'],info['location']['lng'],info['detail_info']['price'],info['detail_info']['overall_rating'],info['detail_info']['service_rating'],info['detail_info']['facility_rating'],info['detail_info']['hygiene_rating'],info['detail_info']['image_num'],info['detail_info']['comment_num'],info['detail_info']['favorite_num'],info['detail_info']['checkin_num'],info['name']])
            else:pass
        else:pass
    print('.....................................',j)

    data=np.array([(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10]) for v in infoDic],dtype='float')  #解释变量(特征)数据部分
    targetInfo=np.array([v[11] for v in infoDic])  #目标变量(类标)部分
    dataBunch=base.Bunch(DESCR=r'info of poi',data=data,feature_names=['lat','lng','price','overall_rating','service_rating','facility_rating','hygiene_rating','image_num','comment_num','favorite_num','checkin_num'],target=targetInfo,target_names=['price','name'])  #建立sklearn的数据存储格式bunch
    return dataBunch #返回bunch格式的数据

'''描述性统计，分析解释变量之间及与目标变量之间的关系'''
def basicStat(dataBunch):
    sns.set(style='whitegrid',context='notebook')
    cols=['lat','lng','price','overall_rating','service_rating','facility_rating','hygiene_rating','image_num','comment_num','favorite_num','checkin_num']  #用于标识frame数据框的列索引
    frame=pd.DataFrame(dataBunch.data[:],columns=cols)  #转换为pandas库的frame数据框格式，方便数据观察和提取
#    print(frame)
    sns.pairplot(frame[cols],size=2.5)  #两两数据的散点图，用于观察数据间的关系
    plt.show()    
   
    cm=np.corrcoef(frame[cols].values.T)  #计算两两间的相关系数
    sns.set(font_scale=1.3)
    hm=sns.heatmap(cm,cbar=True,annot=True,square=True,fmt='.2f',annot_kws={'size':13},yticklabels=cols,xticklabels=cols) #热力图显示相关系数，方便直观查看
    plt.show

'''打印散点图'''
def lr_regPlot(X,y,model):
    plt.scatter(X,y,c='blue')
    plt.plot(X,model.predict(X),color='red')
    return None

'''Ordinary Least Squares普通最小二乘法LinearRegression线性回归''' 
def LR_m(X_lr,y_lr,predFeat=False):
     lr=LinearRegression()
     lr.fit(X_lr,y_lr)
     print('Slope:%.3f;Intercept:%.3f'%(lr.coef_[0],lr.intercept_))  
     lr_regPlot(X_lr,y_lr,lr)
     plt.xlabel('hygiene_num')
     plt.ylabel('service_rating')
     plt.show()
     
     if type(predFeat).__module__=='numpy':  #判断是否有空间几何数据输入
         return lr.predict(predFeat)

'''RANSAC(RANDom SAmple Consensus)随机抽样一致性算法，robustness回归模型'''   
def RANSAC_m(X_ransac,y_ransac,predFeat=False):
    ransac=RANSACRegressor(LinearRegression(),max_trials=100,min_samples=10,residual_metric=lambda x:np.sum(np.abs(x),axis=1),residual_threshold=1.0,random_state=0) #max_trials为最大迭代次数，min_samples随机抽取作为内点的最小样本数量,residual_metric传递了一个lambda函数，拟合曲线与样本点间垂直距离的绝对值，residual_threshold残差阈值，只有小于该值的样本点从加入内点inliers中，否则为外电outliers中，默认使用MAD(Median Absolute Deviation中位数决定偏差)估计内点阈值
    ransac.fit(X_ransac,y_ransac)
    print('Slope:%.3f;Intercept:%.3f'%(ransac.estimator_.coef_[0],ransac.estimator_.intercept_))  
    
    X=X_ransac
    y=y_ransac
    inlier_mask=ransac.inlier_mask_  #内点掩码
#    print(inlier_mask)
    outlier_mask=np.logical_not(inlier_mask) #外点掩码
    line_X=np.arange(0,5,0.5)
    line_y_ransac=ransac.predict(line_X[:,np.newaxis])
    plt.scatter(X[inlier_mask],y[inlier_mask],c='blue',marker='o',label='Inliers')
    plt.scatter(X[outlier_mask],y[outlier_mask],c='lightgreen',marker='s',label='OutLiers')
    plt.plot(line_X,line_y_ransac,color='red')
    plt.xlabel('hygiene_num')
    plt.ylabel('Price in $1000')
    plt.legend(loc='upper left')
    plt.show()
    
    if type(predFeat).__module__=='numpy': #判断是否有空间几何数据输入
        return ransac.predict(predFeat)

'''多元(回归)，LinearRegression线性回归'''
def LR_multiRegression(X_lrm,y_lrm,predFeat=False):    
    X=X_lrm
    y=y_lrm
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=0)
    slr=LinearRegression()
    slr.fit(X_train,y_train)
    y_train_pred=slr.predict(X_train)
    y_test_pred=slr.predict(X_test)
    
    plt.scatter(y_train_pred,y_train_pred-y_train,c='blue',marker='o',label='Training data')
    plt.scatter(y_test_pred,y_test_pred-y_test,c='lightgreen',marker='s',label='Test data')
    plt.xlabel('Predicted values')
    plt.ylabel('Residuals')
    plt.legend(loc='upper left')
    plt.hlines(y=0,xmin=-10,xmax=7,lw=2,color='red')
    plt.xlim([0,7])
    plt.show()
      
    print(slr.coef_,slr.intercept_)
    print('MSE train:%.3f,test:%.3f'%(mean_squared_error(y_train,y_train_pred),mean_squared_error(y_test,y_test_pred))) #MSE， float or ndarray of floats,A non-negative floating point value (the best value is 0.0), or an array of floating point values, one for each individual target.
    print('R^2 train:%.3f,test:%.3f'%(r2_score(y_train,y_train_pred),r2_score(y_test,y_test_pred)))

    if type(predFeat).__module__=='numpy':
        return slr.predict(predFeat)

'''回归中的正则化方法Ridge|RidgeCV,Lasso,ElasticNet'''
def regularization_m(X_re,y_re,predFeat=False):
    n_alphas=200
    alphas=np.logspace(1, 8, n_alphas)
    coefs=[]
    n=0
    for a in alphas:
        n+=1
        ridge=Ridge(alpha=a, fit_intercept=False)
        ridge.fit(X_re,y_re)
        coefs.append(ridge.coef_)
#    print(n,coefs)
    ax = plt.gca()
    ax.plot(alphas, coefs)
    ax.set_xscale('log')
    ax.set_xlim(ax.get_xlim()[::-1])  # reverse axis
    plt.xlabel('alpha')
    plt.ylabel('weights')
    plt.title('Ridge coefficients as a function of the regularization')
    plt.axis('tight')
    plt.show()   
        
    ridge=Ridge(alpha=28.6)  #Ridge预先确定a值
    ridge.fit(X_re,y_re)
    print(ridge.coef_,ridge.intercept_,ridge.alpha)
    
    redgecv=RidgeCV(alphas=alphas) #输入多个a值，模型自行择优选取
    redgecv.fit(X_re,y_re)
    print(redgecv.coef_,redgecv.intercept_,redgecv.alpha_)
    
    lasso=Lasso(alpha=0.01)
    lasso.fit(X_re,y_re)
    print(lasso.coef_,lasso.intercept_ ,lasso.alpha)
    
    elasticnet=ElasticNet(alpha=1.0,l1_ratio=0.5)
    elasticnet.fit(X_re,y_re)
    print(elasticnet.coef_,elasticnet.intercept_ ,elasticnet.alpha)
    
    if type(predFeat).__module__=='numpy':
        return redgecv.predict(predFeat)

'''线性回归模型的曲线化，PolynomialFeatures多项式回归'''
def polynomialReg(X_pReg,y_pReg,predFeat=False):    
    X=X_pReg
    y=y_pReg
    lr=LinearRegression()
    pr=LinearRegression()
    quadratic=PolynomialFeatures(degree=2) #加入多项式项，degree为多项式的次数
    X_quad=quadratic.fit_transform(X)
    
    lr.fit(X,y)
    X_fit=np.arange(0,8,1)[:,np.newaxis]
    y_lin_fit=lr.predict(X_fit)
    
    pr.fit(X_quad,y)
    y_quad_fit=pr.predict(quadratic.fit_transform(X_fit))    
#    print(X_fit,y_quad_fit)
    
    plt.scatter(X,y,label='training points')
    plt.plot(X_fit,y_lin_fit,label='linear fit',linestyle='--')
    plt.plot(X_fit,y_quad_fit,label='quadratic fit')
    plt.legend(loc='upper left')
    plt.show()
    
    print(pr.coef_) #根据degree参数设置数，返回的coef_系数数量不同.
    
    if type(predFeat).__module__=='numpy':
        return pr.predict(quadratic.fit_transform(predFeat))
 
'''DecisionTreeRegressor决策树回归'''    
def decisionTree(X_dTr,y_dTr,predFeat=False):
    X=X_dTr
    y=y_dTr
    tree=DecisionTreeRegressor(max_depth=3)
    tree.fit(X,y)
    sort_idx=X.flatten().argsort()
    lr_regPlot(X[sort_idx],y[sort_idx],tree)
    plt.xlabel('%lower status of the population [LASTAT]')
    plt.ylabel('Price in $1000')
    plt.show()
    
    if type(predFeat).__module__=='numpy':
        return tree.predict(predFeat)

'''RandomForestRegressor随机森林回归'''    
def rfReg(X_rfReg,y_rfReg,predFeat=False):     
     X=X_rfReg
     y=y_rfReg
     X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4,random_state=1)
     forest=RandomForestRegressor(n_estimators=100,criterion='mse',random_state=1,n_jobs=-1)
     forest.fit(X_train,y_train)
     y_train_pred=forest.predict(X_train)
     y_test_pred=forest.predict(X_test)
     print('MSE train:%.3f,test:%.3f'%(mean_squared_error(y_train,y_train_pred),mean_squared_error(y_test,y_test_pred)))
     print('R^2 train:%.3f,test:%.3f'%(r2_score(y_train,y_train_pred),r2_score(y_test,y_test_pred)))
    
     plt.scatter(y_train_pred,y_train_pred-y_train,c='blue',marker='o',label='Training data')
     plt.scatter(y_test_pred,y_test_pred-y_test,c='lightgreen',marker='s',label='Test data')
     plt.xlabel('Predicted values')
     plt.ylabel('Residuals')
     plt.legend(loc='upper left')
     plt.hlines(y=0,xmin=0,xmax=6,lw=2,color='red')
     plt.xlim([0,6])
     plt.show()
     
     if type(predFeat).__module__=='numpy':
         return forest.predict(predFeat)

'''将预测的目标变量值写入.txt文本'''
def targetValJump(prd_w_fn,predValue):
    wf=open(prd_w_fn,'w')
    for i in range(len(predValue)):
    #    print(i)
        if i==len(predValue)-1:
            wf.write(str(predValue[i]))
        else:
            wf.write(str(predValue[i])+',')    
    wf.close()

'''简单(单个解释变量与多个解释变量)线性回归模型公式说明'''   
def simpleLR(X0,X1,w0,w1,w2):
    y=w0+w1*X0  #单解释变量
    plt.scatter(X0,y,c='r',marker='x')
    plt.plot(X0,y,label='linear fit',linestyle='--')
    plt.hlines(y=0,xmin=-10,xmax=60,lw=1,color='red')
    plt.vlines(x=0,ymin=-100,ymax=600,lw=1,color='red')    
#    plt.plot(,linestyle='-')
    plt.show()
    
    if X1.shape and w1 and w2:
        y=w0+w1*X0+w2*X1  #多解释变量
        fig=plt.figure()
        ax=Axes3D(fig)
        ax.scatter(X0, X1, y)
        plt.show()

if __name__ == "__main__":    
    '''poi数据与回归预测'''
#    dataBunch=json2bunch(dataPath)
#    basicStat(dataBunch)
    X_lr=dataBunch.data[:,6][:,np.newaxis] #仅包含一个解释变量
    y_lr=dataBunch.data[:,4]
#    LR_m(X_lr,y_lr)  #hygiene卫生评分(解释变量)与service服务评分(目标变量)建立回归模型
#    RANSAC_m(X_lr,y_lr) #RANSAC(RANDom SAmple Consensus)随机抽样一致性算法,拟合高robustness回归模型。避免异常值的干扰
    X_lrm=dataBunch.data[:,[5,6]] #包含2个解释变量
    y_lrm=dataBunch.data[:,4]
#    LR_multiRegression(X_lrm,y_lrm)
#    regularization_m(X_lrm,y_lrm)
#    polynomialReg(X_lr,y_lr)
    X_dTr=dataBunch.data[:,3][:,np.newaxis]
    y_dTr=dataBunch.data[:,2]
#    decisionTree(X_lr,y_lr)
#    decisionTree(X_lr,y_lr)
    rfReg(X_lrm,y_lrm)

    '''空间几何数据与回归预测'''    
    dataArray=txtReading(explanatoryVariable)
    
    explanatoryVal=dataArray[:,0][:,np.newaxis]    
    targetVal=dataArray[:,1]
    
    explanatoryVal_M=dataArray[:,[0,1]]
    targetVal_M=dataArray[:,2]
    
    preData=txtReading(predictedFeatures)
    preFeat=preData[:,0][:,np.newaxis]
    preFeat_M=preData[:,[0,1]]
    
#    preVal=LR_m(explanatoryVal,targetVal,predFeat=preFeat)
#    preVal=RANSAC_m(explanatoryVal,targetVal,predFeat=preFeat)
#    preVal=LR_multiRegression(explanatoryVal_M,targetVal_M,predFeat=preFeat_M)
#    preVal=regularization_m(explanatoryVal_M,targetVal_M,predFeat=preFeat_M)
#    preVal=polynomialReg(explanatoryVal,targetVal,predFeat=preFeat)
#    preVal=decisionTree(explanatoryVal,targetVal,predFeat=preFeat)
    preVal=rfReg(explanatoryVal_M,targetVal_M,predFeat=preFeat_M)
    
    targetValJump(targetVariable,preVal)
    '''简单的线性回归公式解释'''    
#    X0=np.arange(-8,60,3)
#    X1=np.arange(2,70,3)
#    w0=100
#    w1=9
#    w2=3
#    simpleLR(X0=X0,X1=X1,w0=w0,w1=w1,w2=w2)