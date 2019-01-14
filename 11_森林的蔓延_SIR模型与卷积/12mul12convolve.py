# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:12:13 2017
@author:richieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from scipy import misc
#from sklearn.preprocessing import MinMaxScaler

from scipy.ndimage.filters import correlate,convolve #nd卷积
from scipy.signal import convolve2d   #2d卷积
from numpy import convolve as npConvolve #1d卷积

imagePath=r'D:\MUBENAcademy\pythonSystem\dataB\12mul12Pixal.bmp'  #.jpg格式文件因为压缩而使得数据不为预期值，因此使用.bmp格式文件
#imagePath=r'D:\MUBENAcademy\pythonSystem\dataB\da01.bmp' #根据图像调整参数，xyticksRange=(100,100);miscImage=misc.imresize(imageData,0.3);nColumn=1;width=10

'''读取图像文件'''
def readImage(imagePath):
    imageData=plt.imread(imagePath)
    miscImage=misc.imresize(imageData,0.3)  #如果读取的图像较大，需要压缩图像，缩短计算量
    return imageData  #默认时返回值未压缩，需要压缩的图像需返回miscImage变量

'''显示图像'''
def imgShow(imges,titleName,xyticksRange=False): #imges参数为元组，可以传入多个图像；titleName对应imges参数设置名称字符串元组；xyticksRange参数用于设置轴坐标间距
    axNum=len(imges)
    print(int(axNum/2))
    nColumn=3  #可以自行根据图数量，调整排布数量
    width=15
    figsize=(width, width/nColumn)
    fig,axes=plt.subplots(math.ceil(axNum/nColumn),nColumn,sharex=True,sharey=True,figsize=figsize)
    ax=axes.flatten()
    for i in range(axNum): #循环设置子图 
#        print(imges[i])
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

'''图像卷积。使用了convolve，convolve2d两种方法，比较二者计算时间。并比较convolve和correlate关系'''
def imgConvolve(img):
    kernel_edge=np.array([[-1,-1,-1],
                          [-1,8,-1],
                          [-1,-1,-1]])  #边缘检测卷积核/滤波器。统一称为卷积核
    kernel_dispertion=np.array([[0.5, 1 , 0.5],
                                [1  , -6, 1],
                                [0.5, 1, 0.5]]) #用于SIR模型的卷积核
    kernel=kernel_dispertion
    imgRed=img[...,0].astype(np.int32)  #有时图像默认值为'int8'，如果不修改数据类型，convolve计算结果会出错
    print(imgRed,'\n',imgRed.shape,kernel.shape)  #检测图像和卷积核维度是否相同
    t0=time.time()
    img_convolve2d=convolve2d(imgRed,kernel,mode='same') #convolve2d(in1, in2, mode='full', boundary='fill', fillvalue=0)
    t1=time.time()
    t_convolve2d=t1-t0  #convolve2d所花费时间
    
    t2=time.time()
    img_convolve=convolve(imgRed,kernel,mode='constant',cval=0.0) #convolve(input, weights, output=None, mode='reflect', cval=0.0, origin=0)
    t3=time.time()
    t_convolve=t3-t2 #convolve所花费时间
#    img_correlate=correlate(imgRed,kernel)  
#    print(img_convolve2d,"\n",img_convolve,"\n",img_correlate)
    print(img_convolve2d,"\n",img_convolve)
    imgShow(imges=(img,img_convolve,img_convolve2d,),titleName=("img","img_convolve:%s"%t_convolve,"img_convolve2d:%s"%t_convolve2d,),xyticksRange=(1,1))
    print(t_convolve2d,t_convolve)

if __name__=="__main__":
    imageData=readImage(imagePath)
#    imgShow((imageData,),"X",xyticksRange=(5,5))    
#    print(imageData)
    imgConvolve(imageData)
    


