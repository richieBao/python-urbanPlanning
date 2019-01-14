# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:12:13 2017
@author:richieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import misc
import time
#from sklearn.preprocessing import MinMaxScaler

from scipy.ndimage.filters import correlate,convolve #nd卷积
from scipy.signal import convolve2d   #2d卷积
from numpy import convolve as npConvolve #1d卷积

import moviepy.editor as mpy

imagePath=r'D:\MUBENAcademy\pythonSystem\dataB\12mul12Pixal.bmp'  #.jpg格式文件因为压缩而使得数据不为预期值，因此使用.bmp格式文件
dt=1
#hours_per_second=7*24
hours_per_second=20
dispersion_kernel = np.array([[0.5, 1 , 0.5],
                                [1  , -6, 1],
                                [0.5, 1, 0.5]]) #ISR模型卷积核

'''读取图像文件'''
def readImage(imagePath):
    imageData=plt.imread(imagePath)
    miscImage=misc.imresize(imageData,0.3) #如果读取的图像较大，需要压缩图像，缩短计算量
    return imageData #默认时返回值未压缩，需要压缩的图像需返回miscImage变量

'''显示图像'''
def imgShow(imges,titleName,xyticksRange=False): #imges参数为元组，可以传入多个图像；titleName对应imges参数设置名称字符串元组；xyticksRange参数用于设置轴坐标间距
    axNum=len(imges)
    print(int(axNum/2))
    nColumn=3  #可以自行根据图数量，调整排布数量
    width=15
    figsize=(width, width/nColumn)
    fig,axes=plt.subplots(math.ceil(axNum/nColumn),nColumn,sharex=True,sharey=True,figsize=figsize)
    ax=axes.flatten()
    for i in range(axNum):    
        ax[i].imshow(imges[i])
        if xyticksRange:
            ax[i].set_xticks([x for x in range(imges[i].shape[1]) if x%xyticksRange[0]==0])
            ax[i].set_yticks([y for y in range(imges[i].shape[0]) if y%xyticksRange[1]==0])
        else:
            ax[i].set_xticks([])  
            ax[i].set_yticks([])  
        ax[i].set_title(titleName[i])           
    fig.tight_layout()
    plt.show()

'''卷积扩散'''
def dispersion(SIR,dispersion_kernel):
    print(SIR)
    return np.array([convolve(SIR[0],dispersion_kernel,mode='constant',cval=0.0)]) #注意卷积核与待卷积数组的维度

'''更新数组，即基于前一步卷积结果的每一步卷积'''
def update(world):
    disperse=dispersion(world['SIR'], dispersion_kernel)
    world['SIR']=disperse 
    world['t']+=dt  #记录时间，用于循环终止条件

'''返回每一步卷积的数据到VideoClip中'''
def make_frame(t):
    while world['t']<hours_per_second*t:
        imageShow(world['SIR'][0],world['t'])
        update(world)  
        print('........................................................')
#        print(world['SIR'])
#        videoData=world['SIR'][0]
    return world['SIR'][0]

'''显示图像，观察数据变化'''
def imageShow(img,t):
    if t%1==0: #根据图像大小和待观察数据的变化程度调整图像显示步幅
        fig, axes = plt.subplots(nrows=1, ncols=2,facecolor='w', figsize=(10,5))
        ax0, ax1= axes.flatten()
        ax0.imshow(imageData.T[0])
        ax1.imshow(img)
        fig.tight_layout()
        plt.show()
    else:
        pass

if __name__=="__main__":
    imageData=readImage(imagePath)
    SIR=np.zeros((1,imageData.shape[0], imageData.shape[1]),dtype=np.int32)  #此次实验设置为后续基于SIR模型扩散实验作准备，因此部分程序结构基于后续代码
    print(SIR.shape)
    SIR[0]=imageData.T[0]  #将读取的图像数据中band1即red波段(通道)数据给SIR
    world={'SIR':SIR,'t':0}   #建立字典，方便数据更新
#    print(world['SIR'][0])
    animation=mpy.VideoClip(make_frame,duration=1) #通过动画库MoviePy的VideoClip记录扩散过程，执行函数中往往需要有循环语句
#    animation.write_videofile('testC.mp4', fps=20)  #存为video文件
    animation.write_gif("testE.gif", fps=15) #存为.gif文件