# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:03:49 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
reference:https://github.com/d2l-ai/d2l-zh  《动手学深度学习》(PyTorch版)
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import scipy.io as sio
import math
from decimal import *
from shapely.geometry import Point,MultiPoint
import networkx as nx
import operator
import torch
from sklearn import preprocessing
from tqdm import tqdm 
import pickle

getcontext().prec = 28
np.set_printoptions(precision=28)

'''LandmarkMap 读取MatLab的.fig数据'''
LandmarkMap_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\LandmarkMap.fig"
def readMatLabFig_LandmarkMap(LandmarkMap_fn):
    LandmarkMap=loadmat(LandmarkMap_fn, squeeze_me=True, struct_as_record=False)
    y=loadmat(LandmarkMap_fn)
    print(sorted(LandmarkMap.keys()))
    
    
    LandmarkMap_dic={} #提取.fig值
    for object_idx in range(LandmarkMap['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=LandmarkMap['hgS_070000'].children.children[object_idx].properties.XData #good
            Y=LandmarkMap['hgS_070000'].children.children[object_idx].properties.YData 
            LandmarkMap_dic[object_idx]=(X,Y)
        except:
            pass
    
    # print(LandmarkMap_dic)
    fig= plt.figure(figsize=(20,130))
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    i=0
    for key in LandmarkMap_dic.keys():
        plt.scatter(LandmarkMap_dic[key][0], LandmarkMap_dic[key][1],s=dotSizes[i],marker=markers[i], color=colors[i],linewidth=linewidths[i])
        i+=1
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    return LandmarkMap_dic


''''PHmi读取激光雷达导航评估值'''
PHMI_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\PHMI.fig"
def readMatLabFig_PHMI(PHMI_fn,LandmarkMap_dic):
    PHMI=loadmat(PHMI_fn, squeeze_me=True, struct_as_record=False)
    x=loadmat(PHMI_fn)
    print(sorted(PHMI.keys()))
    
    PHMI_dic={} #提取MatLab的.fig值
    for object_idx in range(PHMI['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=PHMI['hgS_070000'].children.children[object_idx].properties.XData #good
            Y=PHMI['hgS_070000'].children.children[object_idx].properties.YData 
            Z=PHMI['hgS_070000'].children.children[object_idx].properties.ZData
            PHMI_dic[object_idx]=(X,Y,Z)
        except:
            pass
    
    # print(PHMI2_dic)
    fig= plt.figure(figsize=(20,130)) #figsize=(20,130)
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    
    ScalePhmi=math.pow(10,1)
    
    plt.plot(PHMI_dic[0][0], PHMI_dic[0][1],marker=markers[0], color=colors[0],linewidth=linewidths[0])
    
    
    ref=math.pow(10,-5)
    
    #for display clearly
    PHmiValue=PHMI_dic[1][2]
    # print(PHmiValue)
    # replaceValue=np.extract(PHmiValue<ref,PHmiValue)*-math.pow(10,5)
    # print(replaceValue)
    # PHmiValue[PHmiValue<ref]=replaceValue
    plt.plot(PHmiValue*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    
    # plt.plot(PHMI_dic[1][2]*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    plt.axvline(x=ref*ScalePhmi)
    
    
    plt.scatter(LandmarkMap_dic[1][0], LandmarkMap_dic[1][1],marker=markers[1], s=dotSizes[1],color=colors[2],linewidth=10)
    
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    
    return PHMI_dic

'''车载激光雷达导航的扫描区域影响landmarks提取 scanning circle buffer, extract the landmarks in the buffer at earch location'''
def scanCircleBuffer(locations,landmarks,radius):
    landmarks_pts=[Point(coordi[0],coordi[1]) for coordi in np.stack((landmarks[0], landmarks[1]), axis=-1)]
    # print(len(landmarks_pts))
    # print(landmarks_pts)
    locations_pts=[Point(coordi[0],coordi[1]) for coordi in np.stack((locations[0], locations[1]), axis=-1)]
    # print(len(locations_pts))
    scanCircleBuffer=[pt.buffer(radius) for pt in locations_pts]
    # print(scanCircleBuffer)
    targetPts={} #landmarks特征点
    targetPts_idx={} #建立location位置与其扫描范围内landmarks位置坐标的对应索引值
    for locBuffer_idx in range(len(scanCircleBuffer)):
        temp=[]
        temp_idx=[]
        for LM_idx in range(len(landmarks_pts)):
           if scanCircleBuffer[locBuffer_idx].contains(landmarks_pts[LM_idx]):
               temp.append(landmarks_pts[LM_idx])
               temp_idx.append(LM_idx)
        targetPts[locBuffer_idx]=temp
        targetPts_idx[locBuffer_idx]=temp_idx
    print("locations points:%d, target points:%d"%(len(locations_pts),len(targetPts.keys())))
    return targetPts,locations_pts,targetPts_idx
 
#展平函数
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]    

'''#建立无人车位置点及对应扫描区范围特征点的网络结构，使用Networkx库 build the location network'''  
def location_landmarks_network(targetPts_idx,locations,landmarks):   
    LMs=np.stack((landmarks[0], landmarks[1]), axis=-1)
    LCs=np.stack((locations[0], locations[1]), axis=-1)
    ptsMerge=np.vstack((LMs,LCs))
    print("LMs shape:%s, LCs shaoe:%s, ptsMerge shape:%s"%(LMs.shape, LCs.shape,ptsMerge.shape))
    targetPts_idx_adj={}
    for key in targetPts_idx.keys():
        targetPts_idx_adj[key+LMs.shape[0]]=targetPts_idx[key]
    edges=[[(key,i) for i in targetPts_idx_adj[key]] for key in targetPts_idx_adj.keys()]
    edges=flatten_lst(edges)
    
    G=nx.Graph()
    G.position={}
    # G.targetPtsNum={}    
    i=0
    for pts in ptsMerge:
        G.add_node(i)
        G.position[i]=(pts[0],pts[1])        
        # G.targetPtsNum[LM]=(len(targetPts[key]))
        i+=1
    
    G.add_edges_from(edges)
    
    plt.figure(figsize=(20,130))
    nx.draw(G,G.position,linewidths=1,edge_color='gray')
    plt.show()

    return G

#应用numpy.histogram2d转换位置点及对应扫描区特征点为图片栅格数据
def colorMesh_phmi(landmarks,locations,targetPts_idx,Phmi):
    patternValuesDic={}
    for key in targetPts_idx.keys():
        patternValuesDic[key]=[0.5]*len(targetPts_idx[key])
        patternValuesDic[key].append(0.9)
    
    patternDic={}
    for key in patternValuesDic.keys():
        patternDic[key]={"x":landmarks[0][targetPts_idx[key]],
                         "y":landmarks[1][targetPts_idx[key]],
                         "z":patternValuesDic[key]
                         }
        patternDic[key]["x"]=np.append(patternDic[key]["x"],locations[0][key])
        patternDic[key]["y"]=np.append(patternDic[key]["y"],locations[1][key])
        
    histogram2dDic={}
    binNumber=(25,25) #32
    for key in patternDic.keys():
        zi, yi, xi = np.histogram2d(patternDic[key]["y"], patternDic[key]["x"], bins=binNumber, weights=patternDic[key]["z"], normed=False)
        counts, _, _ = np.histogram2d(patternDic[key]["y"], patternDic[key]["x"],bins=binNumber)
        # print(counts)
        histogram2dDic[key]={"xi":xi,"yi":yi,"zi":zi,"count":counts,"ziCount":zi / counts,"ziMasked":np.ma.masked_invalid(zi)}
    
    
    for key in histogram2dDic.keys():
        xi=histogram2dDic[key]["xi"]
        yi=histogram2dDic[key]["yi"]
        zi=histogram2dDic[key]["ziMasked"]
        
        x=patternDic[key]["x"]
        y=patternDic[key]["y"]
        z=patternDic[key]["z"]
        # print(x,y,z)
        #plot it
        fig, ax = plt.subplots(figsize=(25,20))
        ax.pcolormesh(xi, yi, zi, edgecolors='black')
        scat = ax.scatter(x, y, c=z, s=30)
        fig.colorbar(scat)
        ax.margins(0.05)
        
        plt.title("PHmi_%d:%f"%(key,Phmi[key]))
        plt.show()        
        
        if key==20:
            break

    
    return histogram2dDic,patternDic

#显示评估值Phmi的数值分布
def singleBoxplot(array):
    import plotly.express as px
    import pandas as pd
    df=pd.DataFrame(array,columns=["value"])
    fig = px.box(df, y="value",points="all")
    fig.show()


# pyorth 深度学习 迭代数据集建立。迁移https://github.com/d2l-ai/d2l-zh  《动手学深度学习》(PyTorch版)
def data_iter(batch_size, features, labels):
    import random
    num_examples = len(features)
    indices = list(range(num_examples))
    random.shuffle(indices)  # 样本的读取顺序是随机的
    for i in range(0, num_examples, batch_size):
        j = torch.LongTensor(indices[i: min(i + batch_size, num_examples)]) # 最后一次可能不足一个batch
        yield  features.index_select(0, j), labels.index_select(0, j)

'''输出类别配置'''
# pytorch output值确定，用Percentile百分位数分类连续数值用作输出类别
def labelsPercentile(data):
    percentileNumber=[25,50,75]    
    percentileValue=[np.percentile(data,i) for i in percentileNumber]
    for i in range(len(percentileValue)):
        if pow(10,-5)<percentileValue[i]:
            percentileValue.insert(i,pow(10,-5))
            break
    
    data_label=["e","d","c","b","a"]
    labels=[]
    for i in data:
        if i<=percentileValue[0]:
            labels.append(0)
        elif percentileValue[0]<i<=percentileValue[1]:
            labels.append(1)
        elif percentileValue[1]<i<=percentileValue[2]:
            labels.append(2)
        elif percentileValue[2]<i<=percentileValue[3]:
            labels.append(3)
        elif i>percentileValue[3]:
            labels.append(4)
            
    return labels

#pytorch output值确定，用Percentile百分位数分类连续数值用作输出类别——升级版
def labelsPercentile_upgrade(data):
    percentileNumber=[0,1,10,20, 30, 40,50,60, 70, 80, 90,100] #可以设置任意百分位切分值
    percentileValue=[np.percentile(data,i) for i in percentileNumber]
    print(percentileValue)
    
    bunchRange=list(zip(percentileValue, percentileValue[1:] + percentileValue[:1]))   
    bunchIdx=list(range(len(bunchRange)))
    print(bunchRange,bunchIdx)
    valRange=[]

    i=0
    for val in data:        
        val_Idx=[bunchIdx[k] for k in range(len(bunchRange)) if val>=bunchRange[k][0] and val<=bunchRange[k][1]]
        valRange.append(val_Idx[0])
        # print(val,val_Idx)
        # if i==0:
        #     break

    # print(valRange)
    print("bunchIdx amount:",len(bunchIdx),"\n",bunchIdx)
    return valRange    

#输出类别设置，math.pow(10,-5)为评估标准值
def labels2Values(data):
    data[data>math.pow(10,-5)]=1
    data[data<=math.pow(10,-5)]=0
    print(data)

    return data 

#pytorch output值确定，均分方式分类连续数值用作输出类别
def labelsPercentile_extent(data):
    # print(min(data))
    diff=max(data)-min(data)
    bunch=50.
    bunchList=[]
    i=0
    while 1:
        val=min(data)+diff/bunch*i
        if val<=max(data)+diff/bunch:
            bunchList.append(val)
            i+=1
        else:
            break
    bunchRange=list(zip(bunchList, bunchList[1:] + bunchList[:1]))   
    bunchIdx=list(range(len(bunchRange)))
    # print(bunchRange,bunchIdx)
    valRange=[]

    i=0
    for val in data:
        
        val_Idx=[bunchIdx[k] for k in range(len(bunchRange)) if val>=bunchRange[k][0] and val<=bunchRange[k][1]]
        valRange.append(val_Idx[0])
        # print(val,val_Idx)
        # if i==0:
        #     break

    # print(valRange)
    print("bunchIdx amount:",len(bunchIdx),"\n",bunchIdx)
    return valRange

#提取返回值，以字典形式
def relationPts(landmarks,locations,targetPts_idx,Phmi):
    ptsVectors={}
    for key in targetPts_idx.keys():
        ptsVectors[key]={"vector":[(landmarks[0][i]-locations[0][key],landmarks[1][i]-locations[1][key]) for i in targetPts_idx[key]],
                         "distance":[math.sqrt((landmarks[0][i]-locations[0][key])**2+(landmarks[1][i]-locations[1][key])**2) for i in targetPts_idx[key]],
                         "quantity":len(targetPts_idx[key]),
                         "Phmi":Phmi[key]
                                   }
   
    return ptsVectors

#数据特征栅格——A。location无人车位置点与激光雷达扫描范围landmarks数据特征，将位置点作为栅格中心，图片栅格格式
def centricRaster(ptsCenter,radius,cellsize):
    pass
    Xi=list(np.arange(ptsCenter[0]-radius-cellsize/2,ptsCenter[0]+radius+cellsize,cellsize))
    Yi=list(np.arange(ptsCenter[1]-radius-cellsize/2,ptsCenter[1]+radius+cellsize,cellsize))
    XYi=np.array([(x,y) for x in Xi for y in Yi]).reshape(len(Xi),len(Yi),2)
    
    XRangei=list(zip(Xi, Xi[1:] + Xi[:1]))
    XRangei.pop(-1)
    
    YRangei=list(zip(Yi, Yi[1:] + Yi[:1]))
    YRangei.pop(-1)
    XYRangei=np.array([(x,y) for x in XRangei for y in  YRangei]).reshape(len( XRangei),len(YRangei),2,2)
    idxRange=np.array([1 for x in XRangei for y in  YRangei]).reshape(len( XRangei),len(YRangei),-1)
    
    z=idxRange
    featureLabel=np.array(range(z.shape[0]*z.shape[1])).reshape(z.shape[:-1])
    
    
    fig, ax = plt.subplots(figsize=(20,20))
    scat = ax.scatter(XYi[:,:,0], XYi[:,:,1], c="r", s=30)
    plt.show()     
    
    return XYi,XYRangei,idxRange,featureLabel
        
#数据特征栅格——A。接函数 centricRaster()。
def featureRaster(landmarks,locations,targetPts_idx,Phmi,radius,cellsize):
    featureDic={}    
    for key in tqdm(targetPts_idx.keys()):               
        XYi,XYRangei,idxRange,featureLabel=centricRaster([locations[0][key],locations[1][key]],radius,cellsize)
        # fearureMinusValue=np.full(featureLabel.shape,-1)
        # print(XYi.shape,XYRangei.shape)
        
 
        relativeCellCoords=np.concatenate([v.reshape(-1,1) for v in np.where(idxRange)],axis=1) #返回数组值索引（2 维度），作为坐标位置
        rCellCoordsMatrix=relativeCellCoords.reshape(idxRange.shape[:-1]+(3,))
        idxList=[]
        labelList=[]
        for i in targetPts_idx[key]:        
            valX=landmarks[0][i]
            valY=landmarks[1][i]
            a_bool=np.logical_and(XYRangei[:,:,0,0]<=valX,valX<=XYRangei[:,:,0,1])
            b_bool=np.logical_and(XYRangei[:,:,1,0]<=valY,valY<=XYRangei[:,:,1,1])
            c_bool=np.logical_and(a_bool,b_bool)
            idxList.append(rCellCoordsMatrix[c_bool].tolist()[0])
            labelList.append(featureLabel[c_bool].tolist()[0])
            
        # fearureMinusValueExtract=fearureMinusValue[]  
        featureDic[key]={"idx":idxList,
                         "label":labelList,
                         "Phmi":Phmi[key],
                         # "featureValue":
                         }

        if key==1:
            break

    return featureDic

'''栅格图像显示'''
from IPython import display
from matplotlib import pyplot as plt
def use_svg_display():
    """Use svg format to display plot in jupyter"""
    display.set_matplotlib_formats('svg')    
def colorMeshShow(histogram2dDic_part,patternDic_part,Phmi_part,condi):
    use_svg_display()
    xiArray=np.array([histogram2dDic_part[key]["xi"].tolist() for key in histogram2dDic_part.keys()])
    yiArray=np.array([histogram2dDic_part[key]["yi"].tolist() for key in histogram2dDic_part.keys()])
    ziArray=np.array([histogram2dDic_part[key]["ziMasked"].tolist() for key in histogram2dDic_part.keys()])
    
    xArray=np.array([patternDic_part[key]["x"].tolist() for key in patternDic_part.keys()])
    yArray=np.array([patternDic_part[key]["y"].tolist() for key in patternDic_part.keys()])
    zArray=np.array([patternDic_part[key]["z"] for key in patternDic_part.keys()])
    
    # print(xiArray)
    
    width=int(round(math.sqrt(len(xArray)),2))  
    # print("+"*50)
    # print(width)
    fig, axs = plt.subplots(width, width, figsize=(10, 10),constrained_layout=True)
    for ax, xi, yi, zi, x, y,z,titleV,key in zip(axs.flat, xiArray,yiArray,ziArray,xArray, yArray,zArray,Phmi_part,condi):

        ax.pcolormesh(xi, yi, zi, edgecolors='black')
        scat = ax.scatter(x, y, c=z, s=30)
        fig.colorbar(scat)
        ax.margins(0.05)
        
        ax.set_title("PHmi_%d:%f"%(key,titleV))
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    plt.show() 


if __name__ == "__main__":
    LandmarkMap_dic=readMatLabFig_LandmarkMap(LandmarkMap_fn)    
    PHMI_dic=readMatLabFig_PHMI(PHMI_fn,LandmarkMap_dic)
    
    locations=PHMI_dic[0]
    landmarks=LandmarkMap_dic[1]
    radius=25
    targetPts,locations_pts,targetPts_idx=scanCircleBuffer(locations,landmarks,radius)
    Phmi=PHMI_dic[1][2]
    singleBoxplot(Phmi)
    # G=location_landmarks_network(targetPts_idx,locations,landmarks)

    #b = (f >= 1.0 ? 255 : (f <= 0.0 ? 0 : (int)floor(f * 256.0)))
    # data=colorMesh_phmi(landmarks,locations,targetPts_idx,Phmi)
    
    histogram2dDic,patternDic=colorMesh_phmi(landmarks,locations,targetPts_idx,Phmi)
    condi={i for i in range(20)}
    histogram2dDic_part={key: histogram2dDic[key] for key in histogram2dDic.keys() & condi} 
    patternDic_part={key:patternDic[key] for key in patternDic.keys() & condi} 
    Phmi_part=[Phmi[i] for i in condi]
    colorMeshShow(histogram2dDic_part,patternDic_part,Phmi_part,condi)
    
    
    
    # features=torch.tensor(np.asarray([data[val]["zi"] for val in data.keys()]).reshape(len(data.keys()),-1))
    # LE=preprocessing.LabelEncoder()
    # lables=torch.tensor(LE.fit_transform(labelsPercentile(Phmi)))
    
    # features=torch.tensor(np.asarray([data[val]["zi"] for val in data.keys()]))
    # labels=torch.tensor(labelsPercentile(Phmi))
    # valRange=labelsPercentile_extent(Phmi)
    # labelsExtent=torch.tensor(labelsPercentile_extent(Phmi))
    
    # labelsUpgrade=labelsPercentile_upgrade(Phmi)
    # label2V=labels2Values(Phmi)
    # (unique, counts) = np.unique(label2V, return_counts=True)
    # print((unique, counts))
    # batch_size=100
    # data_iter(batch_size, features, labels)
    # for X, y in data_iter(batch_size, features, labels):
    #     print(X.shape, y.shape)
    #     break


    # ptsVectors=relationPts(landmarks,locations,targetPts_idx,Phmi)
    # ptsVectorsFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\ptsVectors.pkl"
    # with open(ptsVectorsFn, 'wb') as handle:
    #     pickle.dump(ptsVectors, handle, protocol=pickle.HIGHEST_PROTOCOL)
          
    
    
    # ptsCenter=[0,0]
    # cellsize=1
    # XYi,XYRangei,idxRange,featureLabel=centricRaster(ptsCenter,radius,cellsize)
    # featureDic=featureRaster(landmarks,locations,targetPts_idx,Phmi,radius,cellsize)
    
    
    
    # featureDicFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmiFeature.pkl"
    # with open(featureDicFn, 'wb') as handle:
    #     pickle.dump(featureDic, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # with open(featureDicFn, 'rb') as handle:
    #     b = pickle.load(handle)    
        
    # phmi_labelFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmi_label.pkl"
    # with open(phmi_labelFn, 'wb') as handle:
    #     pickle.dump(featureLabel, handle, protocol=pickle.HIGHEST_PROTOCOL)    
    