# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:22:47 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import os,re
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns

#读取文件，并排序
def filesDirectoryOrder(fp):
    dirs_files=os.listdir(fp)
    dirs_files.sort()
    fn_numExtraction=[(list(map(int, re.findall(r'\d+', s)))[0],s)for s in dirs_files] #提取文件名中的数字
    fn_sort=sorted(fn_numExtraction)
    fn_sorted=[i[1] for i in fn_sort]
    
    files_dir=[]
    for dir_file in fn_sorted:
        image_path = os.path.join(fp, dir_file)
        if image_path.endswith('.pkl'):
            files_dir.append(image_path)
      
    return files_dir 

#合并读取的数据。距离权重数据
def geoValueWeightedDescribe(geoDir):
    columnDescribeList=[]
    for item in tqdm(geoDir):
        # geoValues=pd.read_pickle(item)
        # print(geoValues)
        # print(ok)
        columnDescribeList.append(pd.read_pickle(item).WeightedValue.replace(-1.0,None).describe())
    weightValueDes=pd.DataFrame(data=columnDescribeList,index=list(range(len(columnDescribeList))),dtype=np.float32)    
    
    del columnDescribeList
    return weightValueDes

#弃之
def geoValueWeightedVisulization(valueDes):
    valueDes["ID"]=valueDes.index
    sns.set(style="whitegrid")
    # Make the PairGrid
    extractedColumns=["count","mean","std","max"]
    g=sns.PairGrid(valueDes.sort_values("count", ascending=False),x_vars=extractedColumns, y_vars=["ID"],height=10, aspect=.25)
    # Draw a dot plot using the stripplot function
    g.map(sns.stripplot, size=10, orient="h",palette="ch:s=1,r=-.1,h=1_r", linewidth=1, edgecolor="w")    
    # Use the same x axis limits on all columns and add better labels
    g.set(xlabel="value", ylabel="") #g.set(xlim=(0, 25), xlabel="Crashes", ylabel="")
    # Use semantically meaningful titles for the columns
    titles=valueDes.columns.tolist() 
    for ax, title in zip(g.axes.flat, titles):
        # Set a different title for each axes
        ax.set(title=title)
        # Make the grid horizontal instead of vertical
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)
    sns.despine(left=True, bottom=True)    


if __name__=="__main__": 
    #数据为distanceWeightCalculation_raster2Polygon.py计算获取的栅格单元到Polygon距离多个文件。
    valWeightedFp=r"F:\data_02_Chicago\parkNetwork\dataOutput\SVF_weighted"
    files_dir=filesDirectoryOrder(valWeightedFp)
    valueDes=geoValueWeightedDescribe(files_dir)
    # geoValueWeightedVisulization(valueDes)