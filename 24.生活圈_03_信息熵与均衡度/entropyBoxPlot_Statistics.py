# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 23:46:43 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
"""
import os
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式

'''处理数据'''
def extractData(dataDic):
    dataKeys=list(dataDic.keys())
    pattern=re.compile(r'(.*?)[_]', re.S)
    fn_numExtraction=[(int(re.findall(pattern, fName)[0]),fName) for fName in dataKeys]
    fn_sort=sorted(fn_numExtraction) #按照文件名数字部分标识排序
    fn_sorted=[i[1] for i in fn_sort]
#    print(fn_sorted)
    
#    columnIndex=dataDic[fn_sorted[0]].columns.tolist() #['IDX', 'long', 'lati', 'POI分类', 'POI聚类', 'POI信息熵']
    clearData={}
    for i in fn_sorted:  #清理掉聚类簇为-1的行，即独立的POI点
        df=dataDic[i]
        clearData[i]=df[~(df['POI聚类']==-1)]
#        clearData[i]=df[~(df['POI信息熵']==1)]        
    poiEntropy={}
    for i in fn_sorted:
        poiEntropy[i]=dataDic[i]['POI信息熵']
    poiEntropyDF=pd.DataFrame(poiEntropy)    
    
    return poiEntropyDF,fn_sorted #返回信息熵，以及排序后的文件名

def violinPlot(all_data,eps):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18*2, 8*2))
    # plot violin plot
    axes[0].violinplot(all_data,showmeans=False,showmedians=True)
    axes[0].set_title('Violin plot',fontsize=30)
    
    # plot box plot
    axes[1].boxplot(all_data,flierprops={'marker':'o','markerfacecolor':'red','color':'black'})
    axes[1].set_title('Box plot',fontsize=30)
   
    # adding horizontal grid lines
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data))])
        ax.set_xlabel('聚类距离',fontsize=30)
        ax.set_ylabel('均衡度',fontsize=30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
     
    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data)) if y%2==0],xticklabels=[eps[i] for i in range(len(eps)) if i%2==0])
    fig.autofmt_xdate()
    plt.rcParams['font.sans-serif']=['STXihei']
    plt.tick_params(labelsize=20)
    plt.show()  


if __name__=="__main__":
    fp=r'C:\Users\Richi\sf_richiebao\sf_monograph\24_socialAttribute_03_entropyCalculation\results\result_data'
    fn=r'poiEntropy'
    readedData=np.load(os.path.join(fp,fn+".npz"))
    #读取使用numpy.savez()方式保存的.npz数据
    dataDic=readedData['dic'][()]  #加[()] ，不会出错
    poiEntropyDF,fn_sorted=extractData(dataDic)

    pattern=re.compile(r'(.*?)[_]', re.S)
    num=[int(re.findall(pattern, fName)[0]) for fName in fn_sorted] #提取数字，即聚类距离

    violinPlot(poiEntropyDF.T,num) #打印箱型图/小提琴图

    
    
    