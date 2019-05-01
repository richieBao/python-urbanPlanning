# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:21:35 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pylab import mpl
from mpl_toolkits.axisartist.axislines import Subplot

mpl.rcParams['font.sans-serif']=['STXihei'] #设置图表文字样式

def boxplot(data):
    all_data=data
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9*5, 4*5))
    # plot violin plot
    axes[0].violinplot(all_data, showmeans=False,showmedians=True)
    axes[0].set_title('Violin plot')
    
    # plot box plot
    axes[1].boxplot(all_data)
    axes[1].set_title('Box plot',fontsize=40)
    
    # adding horizontal grid lines
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data))])
        ax.set_xlabel('聚类距离',fontsize=30)
        ax.set_ylabel('聚类数量',fontsize=30)    
        
    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data)) if y%2==0],xticklabels=all_data.index[::2])
    plt.tick_params(labelsize=25)
    fig.autofmt_xdate()
    plt.show()    


if __name__=="__main__":    
    fn=r'C:\Users\Richi\sf_richiebao\sf_paper\data\poiStatistics.xlsx'
    #读取excel文件数据
    data= pd.read_excel(fn,index_col=0,header=0,sheet_name='Sheet2')
#    print(data)
    boxplot(data.T)