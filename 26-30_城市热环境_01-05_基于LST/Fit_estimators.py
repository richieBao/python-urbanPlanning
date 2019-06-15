# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 16:54:02 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
参考：scikit-learn案例-基于多模型人脸补全 Face completion with a multi-output estimators
"""
print(__doc__)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from pylab import mpl
from skimage import measure
#import seaborn as sns

from sklearn.datasets import fetch_olivetti_faces
from sklearn.utils.validation import check_random_state

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV

from LST import main
from sklearn import preprocessing
from sklearn.externals import joblib
import os

from sklearn.metrics import precision_score,recall_score,f1_score
from sklearn.metrics import explained_variance_score

NDVIClassifyBlockStack,LSTBlockStack,_,_=main() 
#OHEncoder=preprocessing.OneHotEncoder()
#NDVIClassifyOHEncoder=OHEncoder.fit_transform(NDVIClassifyBlockStack.reshape((NDVIClassifyBlockStack.shape[0],NDVIClassifyBlockStack.shape[1]*NDVIClassifyBlockStack.shape[2])))

min_max_scaler = preprocessing.MinMaxScaler()
LSTBlockStackScale=min_max_scaler.fit_transform(LSTBlockStack.reshape((LSTBlockStack.shape[0],LSTBlockStack.shape[1]*LSTBlockStack.shape[2])))

#NDVIClassifyScale=min_max_scaler.fit_transform(NDVIClassifyBlockStack.reshape((NDVIClassifyBlockStack.shape[0],NDVIClassifyBlockStack.shape[1]*NDVIClassifyBlockStack.shape[2])))
NDVIClassifyScale=NDVIClassifyBlockStack.reshape((NDVIClassifyBlockStack.shape[0],NDVIClassifyBlockStack.shape[1]*NDVIClassifyBlockStack.shape[2]))

dataLen=NDVIClassifyScale.shape[0]
msk=np.random.rand(dataLen)<0.85
X_train=NDVIClassifyScale[msk]
y_train=LSTBlockStackScale[msk]

X_test=NDVIClassifyScale[~msk]
y_test=LSTBlockStackScale[~msk]

#num = 20 #5
num=len(y_test)
# Fit estimators
ESTIMATORS = {
    "Extra trees": ExtraTreesRegressor(n_estimators=10, max_features=32,random_state=0),
    "K-nn": KNeighborsRegressor(),
    "Linear regression": LinearRegression(),
    "Ridge": RidgeCV(),
}
    
y_test_predict = dict()
fp=r'C:\Users\Richi\sf_richiebao\sf_code\pythonSYS\pix2pix\saved_model'

for name, estimator in ESTIMATORS.items():
    estimator.fit(X_train, y_train)
    joblib.dump(estimator,os.path.join(fp,'LST_NDVI.pkl'))  #如果数据量大，模型训练将会花费较多时间，因此保存训练好的模型到硬盘空间，方便之后直接调用
    y_test_predict[name] = estimator.predict(X_test)
# Plot the completed faces
image_shape = (100, 100)
n_cols =2 + len(ESTIMATORS)
plt.figure(figsize=(2. * n_cols*3, 2.26 * num*3))
plt.suptitle("Face completion with multi-output estimators", size=16)
    
MultiDataDic={}
for i in range(num):    
    MultiData=[]
    true_LST = y_test[i]   
    MultiData.append(true_LST)
    if i:
        sub = plt.subplot(num, n_cols, i * n_cols + 1)
    else:
        sub = plt.subplot(num, n_cols, i * n_cols + 1,title="original")
    sub.axis("off")
    sub.imshow(true_LST.reshape(image_shape),
               cmap=plt.cm.gray,
               interpolation="nearest")
    contours = measure.find_contours(true_LST.reshape(image_shape), true_LST.mean())
    for n, contour in enumerate(contours):
        sub.plot(contour[:, 1], contour[:, 0], linewidth=2)
    true_NDVI = X_test[i]    
    if i:
        sub = plt.subplot(num, n_cols, i * n_cols + 2)
    else:
        sub = plt.subplot(num, n_cols, i * n_cols + 2,title="condition")

    sub.axis("off")
    true_NDVIReshape=true_NDVI.reshape(image_shape)
    cmap=plt.cm.Pastel2
    sub.imshow(true_NDVIReshape, cmap=cmap)    
    for j, est in enumerate(sorted(ESTIMATORS)):
        completed_pre = y_test_predict[est][i]   
        if i:
            sub = plt.subplot(num, n_cols, i * n_cols + 3 + j)
        else:
            sub = plt.subplot(num, n_cols, i * n_cols + 3 + j,title=est)
        sub.axis("off")
        sub.imshow(completed_pre.reshape(image_shape),
                   cmap=plt.cm.gray,
                   interpolation="nearest")
        contours = measure.find_contours(completed_pre.reshape(image_shape), completed_pre.mean())
        for n, contour in enumerate(contours):
            sub.plot(contour[:, 1], contour[:, 0], linewidth=2)
        MultiData.append(completed_pre)
#        print("$"*30)
#        print("estimator:%s:"%j,explained_variance_score(true_LST.reshape(image_shape), completed_pre.reshape(image_shape)))
    MultiDataDic[i]=np.array(MultiData)
plt.show()

## 计算F1_score,以及召回率recall_score, 准确率precision_score
def ACCuracy_mean(data):
    for i in range(data.shape[0]):
        data[i]=data[i]>data[i].mean()
#    print(data)
#    print(data.shape)
    LST_score={}
    F1_score=[]
    for i in range(1,data.shape[0]):
        LST_score[i]=[precision_score(y_true=data[0],y_pred=data[i]),recall_score(y_true=data[0],y_pred=data[i]),f1_score(y_true=data[0],y_pred=data[i])]
#    print(LST_score)
        F1_score.append(f1_score(y_true=data[0],y_pred=data[i]))
    return LST_score,F1_score

## 折线图
mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式
def lineGraph(array,estimators):
    #matplotlib的常规折线图
    font1 = {'family' : 'STXihei',
             'weight' : 'normal',
             'size'   : 50,
             }
#    estimators = ["Extra trees","K-nn","Linear regression","Ridge"]
#    experimentsNum=["1","2","3","4","5"]
#    experimentsNum=["1","2","3","4","5","6","7","8","9","10"]
    experimentsNum=[str(i+1) for i in range(len(array.T))]
    plt.figure(figsize=(8*10, 8*2))
#    color=['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78']
    for i in range(len(estimators)):
        plt.plot(experimentsNum,array[i],label=estimators[i])
    plt.xlabel('测试数据集-LC08_L1TP_127036_20190525',font1)
    plt.ylabel('F1_score',font1)
    plt.tick_params(labelsize=40)
    plt.legend(prop=font1,loc = 1)  
    plt.show()
    
##箱型图和小提琴图
def violinPlot(all_data,estimators):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8*4, 8*2))
    # plot violin plot
    axes[0].violinplot(all_data,showmeans=False,showmedians=True)
    axes[0].set_title('Violin plot',fontsize=30)
    # plot box plot
    axes[1].boxplot(all_data,flierprops={'marker':'o','markerfacecolor':'red','color':'black'})
    axes[1].set_title('Box plot',fontsize=30)
    # adding horizontal grid lines
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data.T))])
        ax.set_xlabel('回归模型',fontsize=30)
        ax.set_ylabel('F1_score',fontsize=30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data.T)) if y%1==0],xticklabels=[estimators[i] for i in range(len(estimators)) if i%1==0])
#    plt.setp(axes)
    fig.autofmt_xdate()
    plt.rcParams['font.sans-serif']=['STXihei']
    plt.tick_params(labelsize=20)
    plt.show()  

if __name__=="__main__":  
    print("#"*30)
    finalScore={}
    finalF1Score=[]
    for idx in range(num):
        LST_score,F1_score=ACCuracy_mean(MultiDataDic[idx])
        finalScore[idx]=LST_score
        finalF1Score.append(F1_score)
    
    estimators = ["Extra trees","K-nn","Linear regression","Ridge"] 
    lineGraph(np.array(finalF1Score).T,estimators) #观察F1_Score折线图变化
    violinPlot(np.array(finalF1Score),estimators) #观察F1_Score箱型图变化