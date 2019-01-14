# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 09:54:20 2018

@author: richieBao-caDesign设计(cadesign.cn)
"""

import cv2
import numpy as np
import os

rootDirectory=r'D:\MUBENAcademy\pythonSystem\images03'
inputImg_edge=r'D:\MUBENAcademy\pythonSystem\code\imagesforLab\IMG_0407.JPG'
imgA=r'D:\MUBENAcademy\pythonSystem\code\imagesforLab\IMG_0407.JPG'
imgB=r'D:\MUBENAcademy\pythonSystem\code\imagesforLab\IMG_0405.JPG'
import matplotlib.pyplot as plt 

#检测边
def edgeDetection(inputImg_edge):    
    imgEdge=cv2.imread(inputImg_edge,cv2.IMREAD_GRAYSCALE)  #读取图像
    sobelHorizontal=cv2.Sobel(imgEdge,cv2.CV_64F,1,0,ksize=5) #索贝尔滤波器Sobel filter，横向。参数解释通过help(cv2.Sobel)查看
    """
    help(cv2.Sobel)
    Help on built-in function Sobel:
    .   @param src input image. 输入待处理的图像
    .   @param dst output image of the same size and the same number of channels as src . 输出图像，同大小，同通道数
    .   @param ddepth output image depth, see @ref filter_depths "combinations"; in the case of.  8-bit input images it will result in truncated derivatives. 
    图像深度，-1时与原图像深度同，目标图像的深度必须大于等于原图像深度。避免truncated derivatives而设置cv2.CV_64F数据类型
    .   @param dx order of the derivative x. x方向求导阶数，0表示这个方向没有求导，一般为0,1,2
    .   @param dy order of the derivative y. y方向求导阶数，同上
    .   @param ksize size of the extended Sobel kernel; it must be 1, 3, 5, or 7. 算子大小，必须为1、3、5、7
    .   @param scale optional scale factor for the computed derivative values; by default, no scaling is. applied (see cv::getDerivKernels for details).
    缩放导数的比例常数，默认情况五伸缩系数
    .   @param delta optional delta value that is added to the results prior to storing them in dst.
    可选增量，默认情况无额外值加到dst中
    .   @param borderType pixel extrapolation method, see cv::BorderTypes 图像边界模式
    .   @sa  Scharr, Laplacian, sepFilter2D, filter2D, GaussianBlur, cartToPolar      
    """
    sobelVertical=cv2.Sobel(imgEdge,cv2.CV_64F,0,1,ksize=5) #索贝尔滤波器Sobel filter，纵向
    laplacian=cv2.Laplacian(imgEdge,cv2.CV_64F) #拉普拉斯边检测器，Laplacian edge detector
    canny=cv2.Canny(imgEdge,50,240) #Canny边检测器Canny edge detector
    
#    print(imgEdge)
    cv2.namedWindow('img')
#    cv2.imshow('original',imgEdge)
#    cv2.imshow('sobel horizontal',sobelHorizontal) #输出显示图像
#    cv2.imwrite(os.path.join(rootDirectory,'sobel horizontal.jpg'),sobelHorizontal)
#    cv2.imshow('sobel vertical',sobelVertical)    
#    cv2.imwrite(os.path.join(rootDirectory,'sobel vertical.jpg'),sobelVertical)
    cv2.imshow('laplacian',laplacian)
    cv2.imwrite(os.path.join(rootDirectory,'laplacian.jpg'),laplacian)
#    cv2.imshow('canny',canny)
#    cv2.imwrite(os.path.join(rootDirectory,'canny.jpg'),canny)
    cv2.waitKey()

#检测棱角
def cornerDetection(inputImg_edge):
    imgCorners=cv2.imread(inputImg_edge)    
    imgGray=cv2.cvtColor(imgCorners,cv2.COLOR_BGR2GRAY) #将图像转换为灰度，为每一像素位置1个值，可理解为图像的强度(颜色，易受光照影响，难以提供关键信息，故将图像进行灰度化，同时也可以加快特征提取的速度。)
    imgGray=np.float32(imgGray) #强制转换为浮点值，用于棱角检测
    imgHarris=cv2.cornerHarris(imgGray,7,5,0.04) #哈里斯角检测器 Harris corner detector
    print(imgHarris.max(),imgHarris.shape)
    imgHarris=cv2.dilate(imgHarris,np.ones((1,1))) #放大棱角标记
    print(imgCorners[300:500,])
    imgCorners[imgHarris>0.01*imgHarris.max()]=[40,75,236] #定义阈值，显示重要的棱角
    cv2.imshow('harris corners',imgCorners)
    cv2.imwrite(os.path.join(rootDirectory,'harris corners.jpg'),imgCorners)
    cv2.waitKey()

#SIFT(scale invariant feature transform 尺度不变特征变换)特征点检测
def siftDetection(inputImg_edge):
    imgSift=cv2.imread(inputImg_edge)
    imgGray=cv2.cvtColor(imgSift,cv2.COLOR_BGR2GRAY)
    print(imgGray.shape)
    sift=cv2.xfeatures2d.SIFT_create() #SIFT特征实例化
    keypoints=sift.detect(imgGray,None)  #提取SIFT特征关键点detector
    print(keypoints[:3],len(keypoints))
    for k in keypoints[:3]:
        print(k.pt,k.size,k.octave,k.response,k.class_id,k.angle) 
        """
        关键点信息包含：
        k.pt关键点点的坐标(图像像素位置)
        k.size该点直径的大小
        k.octave从高斯金字塔的哪一层提取得到的数据
        k.response响应程度，代表该点强壮大小，即角点的程度。角点：极值点，某方面属性特别突出的点(最大或最小)。
        k.class_id对图像进行分类时，可以用class_id对每个特征点进行区分，未设置时为-1
        k.angle角度，关键点的方向。SIFT算法通过对邻域做梯度运算，求得该方向。-1为初始值        
        """
       
    des = sift.compute(imgGray,keypoints) #提取SIFT调整描述子descriptor
    print(type(keypoints),type(des))
    print(des[0][:2]) #关键点
    print(des[1][:2]) #描述子(关键点周围对其有贡献的像素点)
    print(des[1].shape)
    imgSift=np.copy(imgSift)
    cv2.drawKeypoints(imgSift,keypoints,imgSift,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
    """
    help(cv2.drawKeypoints)
    Help on built-in function drawKeypoints:

    drawKeypoints(...)
    drawKeypoints(image, keypoints, outImage[, color[, flags]]) -> outImage
    .   @brief Draws keypoints.
    .   
    .   @param image Source image. 原始图像(3通道或单通道)
    .   @param keypoints Keypoints from the source image. 关键点(特征点向量)，向量内每一个元素是一个keypoint对象，包含特征点的各种属性特征
    .   @param outImage Output image. Its content depends on the flags value defining what is drawn in the. output image. See possible flags bit values below.
    特征点绘制的画布图像(可以是原始图像)。标记类型，参看@note部分
    .   @param color Color of keypoints. 显示颜色，默认随机彩色
    .   @param flags Flags setting drawing features. Possible flags bit values are defined by.DrawMatchesFlags. See details above in drawMatches .
        .   
    .   @note 特征点的 绘制模式，即绘制特征点的哪些信息
    .   For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT,
    .   cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG,
    .   cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
    """
    cv2.imshow('sift features',imgSift)
    cv2.imwrite(os.path.join(rootDirectory,'sift features.jpg'),imgSift)
    cv2.waitKey()

#star特征检测器
def starDetection(inputImg_edge):
    imgStar=cv2.imread(inputImg_edge)
#    imgGray=cv2.cvtColor(imgStar,cv2.COLOR_BGR2GRAY)
    star=cv2.xfeatures2d.StarDetector_create()
    keypoints=star.detect(imgStar)
#    print(len(keypoints),keypoints)
    cv2.drawKeypoints(imgStar,keypoints,imgStar,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('star features',imgStar)
    cv2.imwrite(os.path.join(rootDirectory,'star features.jpg'),imgStar)
    cv2.waitKey()    
   
#sift图像匹配    
def matchSift(imgA,imgB):   
    img1 = cv2.imread(imgA, 0) 
    img2 = cv2.imread(imgB, 0)  
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)  #获取SIFT关键点和描述子
    kp2, des2 = sift.detectAndCompute(img2, None)  
    bf = cv2.BFMatcher()  
    matches = bf.knnMatch(des1, des2, k=2)  #根据描述子匹配图像,返回n个最佳匹配
    """
    .   @param k Count of best matches found per each query descriptor or less if a query descriptor has less than k possible matches in total.
    The result of matches = bf.match(des1,des2) line is a list of DMatch objects. This DMatch object has following attributes:
    DMatch.distance - Distance between descriptors. The lower, the better it is.
    DMatch.trainIdx - Index of the descriptor in train descriptors
    DMatch.queryIdx - Index of the descriptor in query descriptors
    DMatch.imgIdx - Index of the train image.
    参看：https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
    """
    print(type(matches),matches[:2],(matches[0][0].distance,matches[0][1].distance))
    good = []  
    for m, n in matches:  
        if m.distance < 0.75 * n.distance:  #因为k=2,因此返回距离最近和次近关键点，比较最近和次近，满足最近/次近<value，才被认为匹配。ratio test explained by D.Lowe in his paper
            good.append([m])  
    
    imgM = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good[0:int(1*len(good)):int(0.1*len(good))], None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  
    fig, ax=plt.subplots(figsize=(50,30))
    ax.imshow(imgM), plt.show()    
#    cv2.imshow('matchSift',imgM)
#    cv2.waitKey() 

if __name__ == "__main__":
#    edgeDetection(inputImg_edge)
#    cornerDetection(inputImg_edge)
#    siftDetection(inputImg_edge)
    starDetection(inputImg_edge)
#    matchSift(imgA,imgB)