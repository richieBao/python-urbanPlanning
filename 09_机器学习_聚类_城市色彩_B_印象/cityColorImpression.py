# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 09:28:41 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
print(__doc__)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.random import rand
from scipy import misc

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler

import os
import time
import warnings
from itertools import cycle, islice
import json

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

'''读取图像为RGB数组，并调整图像大小，减少计算时间。调整图像数组形状为2维，用于下一步骤的聚类计算'''
def getPixData(img):
        lum_img=mpimg.imread(img)  #读取图像为数组，值为RGB格式0-255
        lum_imgSmall=misc.imresize(lum_img, 0.3)  #传入图像的数组，调整图片大小
        h, w, d=lum_imgSmall.shape
        pixData=np.reshape(lum_imgSmall, (h*w, d))  #调整数组形状为2维
        return lum_imgSmall,pixData
#        return pixData

'''聚类的方法提取图像主题色，并打印图像、聚类预测类的二维显示和主题色带'''
def cityColorThemes(imgInfo):    
    #设置聚类参数，本实验中仅使用了KMeans算法，其它算法可以自行尝试
    default_base = {'quantile': .3,
                    'eps': .3,
                    'damping': .9,
                    'preference': -200,
                    'n_neighbors': 10,
                    'n_clusters': 7}    
    datasets=[((i[1],None),{}) for i in imgInfo] #基于pixData的图像数据，用于聚类计算
#    datasets=[((i,None),{}) for i in imgInfo]
    imgList=[i[0] for i in imgInfo]  #基于lum_imgSmall的图像数据，用于图像显示
#    print(datasets[0])
    #官方聚类案例中对于datasets的配置，此处保留记录，可以查看对官方案例调整的痕迹
#    datasets = [
#        (noisy_circles, {'damping': .77, 'preference': -240,'quantile': .2, 'n_clusters': 2}),
#        (noisy_moons, {'damping': .75, 'preference': -220, 'n_clusters': 2}),
#        (varied, {'eps': .18, 'n_neighbors': 2}),
#        (aniso, {'eps': .15, 'n_neighbors': 2}),
#        (blobs, {}),
#        (no_structure, {})
#        ]
    themes=np.zeros((default_base['n_clusters'], 3))  #建立0占位的数组，用于后面主题数据的追加。'n_clusters'为提取主题色的聚类数量，此处为7，轴2为3，是色彩的RGB数值
    (img,pix)=imgInfo[0]  #可以1次性提取元组索引值相同的值，img就是lum_imgSmall，而pix是pixData
#    pix=imgInfo[0]
    pixV,pixH=pix.shape  #获取pixData数据的形状，用于pred预测初始数组的建立
    pred=np.zeros((pixV))  #建立0占位的pred预测数组，用于后面预测结果数据的追加，即图像中每一个像素点属于设置的7个聚类中的哪一组，预测给定类标
#    print(pred,pred.shape)
#    print(ok)
    plt.figure(figsize=(6*3+3, len(imgInfo)*2))  #图表大小的设置，根据图像的数量来设置高度，宽度为3组9个子图，每组包括图像、预测值散点图和主题色
    plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.3,hspace=.3)  #调整图，避免横纵向坐标重叠    
    plot_num=1  #子图的计数    
    
    for i_dataset, (dataset, algo_params) in enumerate(datasets):  #循环pixData数据，即待预测的每个图像数据。enumerate()函数将可迭代对象组成一个索引序列，可以同时获取索引和值，其中i_dataset为索引，从整数0开始
        print(i_dataset)  #打印索引，在程序运行时，可以查看计算进度，为图像的数量
        params=default_base.copy()  #备份参数设置，此次实验未用
        #print(params)
        params.update(algo_params)  #更新参数，此次实验未更新。采用字典存储参数，并通过更新获取最新值的编程思路，值得学习，有C语言结构体的特点
        #print(params)
#        print(dataset)
        X, y = dataset  #用于机器学习的数据一般包括特征值和类标，此次实验为无监督分类的聚类实验，没有类标，并将其在前文中设置为None对象
#        print(X.shape,X)
#        print(X.shape)
        Xstd = StandardScaler().fit_transform(X)  #标准化数据仅用于二维图表的散点，可视化预测值，而不用于聚类，聚类数据保持色彩的0-255值范围
#        print(X)

        '''官网案例，用于不同聚类算法相关参数计算，此次实验使用KMeans算法，参数为'n_clusters'一项'''       
#        estimate bandwidth for mean shift    
#        bandwidth = cluster.estimate_bandwidth(X, quantile=params['quantile'])    
#        print(bandwidth)
#        connectivity matrix for structured Ward
#        connectivity = kneighbors_graph(X, n_neighbors=params['n_neighbors'], include_self=False)
#        make connectivity symmetric
#        print(connectivity.toarray())
#        connectivity = 0.5 * (connectivity + connectivity.T)   
#        print(connectivity.toarray())
#        ms = cluster.MeanShift(bandwidth=bandwidth, bin_seeding=True)
        
        '''scikit-learning所提供的聚类算法，可以自行常思不同算法下的计算结果，以及比较计算速度，此次实验使用KMeans算法。注意，部分算法计算时间较长。MiniBatchKMeans和KMeans算法计算较快'''        
        two_means = cluster.MiniBatchKMeans(n_clusters=params['n_clusters'])
#        ward = cluster.AgglomerativeClustering(n_clusters=params['n_clusters'], linkage='ward',connectivity=connectivity)
        spectral = cluster.SpectralClustering(n_clusters=params['n_clusters'], eigen_solver='arpack',affinity="nearest_neighbors")
        dbscan = cluster.DBSCAN(eps=params['eps'])
        affinity_propagation = cluster.AffinityPropagation(damping=params['damping'], preference=params['preference'])
#        average_linkage = cluster.AgglomerativeClustering(linkage="average", affinity="cityblock",n_clusters=params['n_clusters'], connectivity=connectivity)
        birch = cluster.Birch(n_clusters=params['n_clusters'])
        gmm = mixture.GaussianMixture(n_components=params['n_clusters'], covariance_type='full')
        km=cluster.KMeans(n_clusters=params['n_clusters'])
#        print('ok01')
        
        '''将所有算法及其别名存储与元组中，如果想尝试其它聚类算法，可以直接取消注释'''        
        clustering_algorithms = (
#            ('MiniBatchKMeans', two_means),
            ('KMeans',km),
    #        ('AffinityPropagation', affinity_propagation),
    #        ('MeanShift', ms),
    #        ('SpectralClustering', spectral),
    #        ('Ward', ward),
    #        ('AgglomerativeClustering', average_linkage),
    #        ('DBSCAN', dbscan),
    #        ('Birch', birch),
    #        ('GaussianMixture', gmm)
        )

        '''循环算法'''        
        for name, algorithm in clustering_algorithms:
            t0 = time.time()    
            #警告错误，使用warning库
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="the number of connected components of the " +"connectivity matrix is [0-9]{1,2}" +" > 1. Completing it to avoid stopping the tree early.",
                    category=UserWarning)
                warnings.filterwarnings(
                    "ignore",
                    message="Graph is not fully connected, spectral embedding" +" may not work as expected.",
                    category=UserWarning)

                print(X.shape,'...............\n')
                algorithm.fit(X)  #通过fit函数执行聚类算法
#                print(algorithm)
            quantize=np.array(algorithm.cluster_centers_, dtype=np.uint8) #返回聚类的中心，为主题色
            themes=np.vstack((themes,quantize))  #将计算获取的每一图像主题色追加到themes数组中
#            print(themes.shape,themes)
            t1 = time.time()  #计算聚类算法所需时间
            '''获取预测值/分类类标'''   
            if hasattr(algorithm, 'labels_'):
                y_pred = algorithm.labels_.astype(np.int)
#                print(algorithm.predict(X))
                print(algorithm.labels_)
            else:
                y_pred = algorithm.predict(X)
#                print(y_pred)     
#                print('111111')
            print(y_pred.shape,pred.shape)
            print(y_pred)
            pred=np.hstack((pred,y_pred))  #将计算获取的每一图像聚类预测结果追加到pred数组中
#            print(y_pred.shape,y_pred)
            figWidth=(len(clustering_algorithms)+2)*3  #水平向子图数
            plt.subplot(len(datasets), figWidth, plot_num)
            plt.imshow(imgList[i_dataset])  #图像显示子图
            
            plt.subplot(len(datasets),figWidth, plot_num+1)
            if i_dataset == 0:
                plt.title(name, size=18)
            colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']),int(max(y_pred) + 1))))  #设置预测类标分类颜色
            #print(colors)
            plt.scatter(Xstd[:, 0], Xstd[:, 1], s=10, color=colors[y_pred]) #预测类标子图
            plt.xlim(-2.5, 2.5)
            plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(.99, .01, ('%.2fs' % (t1 - t0)).lstrip('0'),transform=plt.gca().transAxes, size=15,horizontalalignment='right')  #子图中显示聚类计算时间长度，用于分析不同算法速度      
            '''图像主题色子图参数配置'''
            plt.subplot(len(datasets), figWidth, plot_num+2)
            t=1
            pale=np.zeros(imgList[i_dataset].shape, dtype=np.uint8)
            h, w,_=pale.shape
            ph=h/len(quantize)
            for y in range(h):
                pale[y,::] = np.array(quantize[int(y/ph)], dtype=np.uint8)
            plt.imshow(pale)    
            t+=1  
            plot_num+=3    
    plt.show()
    return themes,pred

'''显示所有图像主题色，获取总体印象'''
def cityColorImpression(themes):  
    n_samples=themes.shape[0]
    random_state=170  #可为默认，不设置该参数，获得随机图形  
    #利用scikit的datasets数据集构建有差异变化的斑点
    varied=datasets.make_blobs(n_samples=n_samples,cluster_std=[1.0, 2.5, 0.5],random_state=random_state)
    (x,y)=varied    
    fig, ax=plt.subplots(figsize=(10,10))
    scale=1000.0*rand(n_samples)  #设置斑点随机大小
    ax.scatter(x[...,0], x[...,1], c=themes/255,s=scale,alpha=0.7, edgecolors='none')  #将主题色赋予斑点
    ax.grid(True)       
    plt.show()

'''保存文件。因为对于大量数据聚类计算花费时间较长，因此建议将数据存储在文件中，以备之后调用。savingData()函数将文件存储为json数据格式''' 
def savingData(data,savingPath,name):
    jsonFile=open(os.path.join(savingPath,str(time.time())+r'_cityColorImpression_%s.json'%name),'w')
    json.dump(data.tolist(),jsonFile)  #将numpy数组转换为列表后存储为json数据格式
    jsonFile.close()
    
if __name__ == "__main__":
#    savingPath=r"D:\MUBENAcademy\pythonSystem\code"
    savingPath=r'D:\project\std\imagesA'
#    dirpath=r"D:\digit-x\southernInternship"
#    dirpath=r'D:\r_academiccommunication\GPSToolBox\export'
    dirpath=r'D:\project\std\imagesA'
#    fileType=["jpg","png","JPG"] 
    fileType=["jpg","JPG"] 
    fileInfo=filePath(dirpath,fileType)
#    print(fileInfo)
#    print(ok)
    filePathKeys=list(fileInfo.keys())
    selection=0 #选择待分析图像文件夹索引
    imgPath=filePathKeys[selection]  
#    print(imgPath)  #通过打印路径核实所选文件夹是否正确
    imgList=fileInfo[filePathKeys[selection]]
    imgPathList=[os.path.join(imgPath,i) for i in imgList]
#    print(imgPathList)
    imgInfo=[(getPixData(img)) for img in imgPathList]    
#    print(imgPathList)
#    print(imgInfo[0][1])
#    print(imgInfo)
#    print(ok)
    '''图像主题色显示与印象'''    
    themes,pred=cityColorThemes(imgInfo)
    cityColorImpression(themes)
    '''存储数据'''    
    nameThemes=r'themes'
    savingData(themes,savingPath,nameThemes)
    namePred=r'pred'
    savingData(pred,savingPath,namePred)