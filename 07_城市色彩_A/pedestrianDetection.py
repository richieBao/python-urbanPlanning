# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:14:24 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mpc
from mpl_toolkits.mplot3d import Axes3D
import math
from scipy import misc
import numpy as np

from PIL import ImageFile  
ImageFile.LOAD_TRUNCATED_IMAGES = True  #出现“IOError: image file is truncated (n bytes not processed)”错误的解决办法

'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
def filePath(dirpath,fileType):
    fileInfo={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       #print(i,'\n')
       #print(dirpath,'\n',dirNames,'\n',fileNames,'\n')
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           #if not tempList :
               #print(i,"NULL")
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               fileInfo.setdefault(dirpath,tempList)
    return fileInfo  

'''显示一个文件夹下所有图片，便于查看。并作为进一步图片处理分析的基础，关注后续相关实验'''
def imgShow(imgPath,imgList,nrows):    
    ncols=math.ceil(len(imgList)/nrows)
    fig,axes=plt.subplots(ncols,nrows,sharex=True,sharey=True,figsize=(15,20))   #布局多个子图，每个子图显示一幅图像
    ax=axes.flatten()  #降至1维，便于循环操作子图
    #print(ax)
    for i in range(len(imgList)):
        img=os.path.join(imgPath,imgList[i])  #获取图像的路径
        lum_img=mpimg.imread(img)  #读取图像为数组，值为RGB格式0-255
        lum_imgSmall=misc.imresize(lum_img, 0.3)  #传入图像的数组，调整图片大小
        #print(lum_img.shape,lum_imgSmall.shape)
        #lum_img=lum_img[:,:,]
        #print(lum_img.shape,lum_img)
        ax[i].imshow(lum_imgSmall)  #显示图像
        ax[i].set_title(i+1)
    fig.tight_layout() #自动调整子图参数，使之填充整个图像区域
    fig.suptitle("images show",fontsize=14,fontweight='bold',y=1.02)
    plt.show()

'''将像素RGB颜色投射到色彩空间中，直观感受图像颜色的分布'''
def imageColorPoints(imgPath,imgList,nrows):
    ncols=math.ceil(len(imgList)/nrows)
    fig = plt.figure()
    for i in range(len(imgList)):
    #for i in range(24):
        #print(i)
        ax=fig.add_subplot(nrows,ncols,i+1, projection='3d')  #不断增加子图，并设置投影为3d模式，可以显示三维坐标空间 
        #for j in range(len(imgList)):  #循环0轴
        img=os.path.join(imgPath,imgList[i])
        lum_img=mpimg.imread(img)
        lum_imgSmall=misc.imresize(lum_img, 0.01)
        #print(lum_imgSmall.shape)
        #print(lum_imgSmall[:,:,0],lum_imgSmall[:,:,1],lum_imgSmall[:,:,2])
        ax.scatter(lum_imgSmall[:,:,0],lum_imgSmall[:,:,1],lum_imgSmall[:,:,2], c=(lum_imgSmall/255).reshape(-1,3), marker='+') #用RGB的三个分量值作为颜色的空间坐标，并显示其颜色。设置颜色时，需要将0-255缩放至0-1区间
        ax.set_xlabel('r',labelpad=1)
        ax.set_ylabel('g')
        ax.set_zlabel('b',labelpad=2)
        ax.set_title(i+1)
        fig.set_figheight(20)
        fig.set_figwidth(35)
    #plt.subplots_adjust(wspace=0.4, hspace=0.2,top=0.9,bottom=0.1)
    fig.tight_layout()
    plt.show() 

'''建立图像颜色HSV各分量的直方图，分析颜色分布情况'''
def imageColorHist(imgPath,imgList,nrows):
    ncols=math.ceil(len(imgList)/nrows)
    fig,axes=plt.subplots(ncols,nrows,sharex=True,sharey=True,figsize=(15,20))
    ax=axes.flatten()
    #print(ax)
    num_bins = 50  #设置直方图的bin参数，及柱数量
    totalH=np.array([])
    totalS=np.array([])
    totalV=np.array([])
    
    for i in range(len(imgList)):
    #for i in range(3):
        #print(i)
        img=os.path.join(imgPath,imgList[i])
        lum_img=mpimg.imread(img)
        lum_imgSmall=misc.imresize(lum_img, 0.3)
        lum_imgSmallHSV=mpc.rgb_to_hsv(lum_imgSmall/255) #RGB空间结构不符合人们对颜色相似性的主观判断，因此将其转换为HSV空间、更接近于人们对颜色的主观认识。色调（H），饱和度（S），明度（V）
        #print(lum_imgSmallHSV[...,0].reshape(-1))
        ax[i].hist(lum_imgSmallHSV[...,0].reshape(-1), num_bins, normed=1)  #提取H色调分量
        #print(totalH.shape,lum_imgSmallHSV[...,0].reshape(-1).shape)
        totalH=np.append(totalH,lum_imgSmallHSV[...,0].reshape(-1))
        totalS=np.append(totalS,lum_imgSmallHSV[...,1].reshape(-1))
        totalV=np.append(totalV,lum_imgSmallHSV[...,2].reshape(-1))
        ax[i].set_title(i+1)
    fig.tight_layout()
    fig.suptitle("images show",fontsize=14,fontweight='bold',y=1.02)
    
    totalStat,(totalAXH,totalAXS,totalAXV)=plt.subplots(ncols=3,figsize=(20, 6))  #建立新图表，用于显示总体HSV的直方图统计
    totalAXH.hist(totalH*360,num_bins,normed=1,facecolor='y')    
    totalAXS.hist(totalS*100,num_bins,normed=1,facecolor='k')
    totalAXV.hist(totalV*100,num_bins,normed=1,facecolor='g')
   
    plt.show()
    
if __name__ == "__main__":
    dirpath=r"D:\digit-x\southernInternship"
    fileType=["jpg","png"] 
    fileInfo=filePath(dirpath,fileType)
    
    filePathKeys=list(fileInfo.keys())
    imgPath=filePathKeys[0]
    imgList=fileInfo[filePathKeys[0]]
    print(len(imgList))
    nrows=6
    imgShow(imgPath,imgList,nrows)
    #imageColorPoints(imgPath,imgList,nrows)
    #imageColorHist(imgPath,imgList,nrows)
