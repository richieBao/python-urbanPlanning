# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:36:33 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
"""
#该部分的注释可以参考showMatLabFig.ipynb文件
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import scipy.io as sio
import math
from decimal import *
from shapely.geometry import Point,MultiPoint
import networkx as nx

getcontext().prec = 28
np.set_printoptions(precision=28)

'''LandmarkMap'''
LandmarkMap_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\LandmarkMap.fig"
def readMatLabFig_LandmarkMap(LandmarkMap_fn):
    LandmarkMap=loadmat(LandmarkMap_fn, squeeze_me=True, struct_as_record=False)
    y=loadmat(LandmarkMap_fn)
    print(sorted(LandmarkMap.keys()))
    
    
    LandmarkMap_dic={}
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


''''PHmi'''
PHMI_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\PHMI.fig"
def readMatLabFig_PHMI(PHMI_fn,LandmarkMap_dic):
    PHMI=loadmat(PHMI_fn, squeeze_me=True, struct_as_record=False)
    x=loadmat(PHMI_fn)
    print(sorted(PHMI.keys()))
    
    PHMI_dic={}
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
    replaceValue=np.extract(PHmiValue<ref,PHmiValue)*-math.pow(10,5)
    # print(replaceValue)
    PHmiValue[PHmiValue<ref]=replaceValue
    plt.plot(PHmiValue*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    
    # plt.plot(PHMI_dic[1][2]*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    plt.axvline(x=ref*ScalePhmi)
    
    
    plt.scatter(LandmarkMap_dic[1][0], LandmarkMap_dic[1][1],marker=markers[1], s=dotSizes[1],color=colors[2],linewidth=10)
    
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    
    return PHMI_dic

'''scanning circle buffer, extract the landmarks in the buffer at earch location'''
def scanCircleBuffer(locations,landmarks,dradius):
    landmarks_pts=[Point(coordi[0],coordi[1]) for coordi in np.stack((landmarks[0], landmarks[1]), axis=-1)]
    # print(len(landmarks_pts))
    # print(landmarks_pts)
    locations_pts=[Point(coordi[0],coordi[1]) for coordi in np.stack((locations[0], locations[1]), axis=-1)]
    # print(len(locations_pts))
    scanCircleBuffer=[pt.buffer(radius) for pt in locations_pts]
    # print(scanCircleBuffer)
    targetPts={}
    targetPts_idx={}
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
 
'''build the location network''' 
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]     
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



if __name__ == "__main__":
    LandmarkMap_dic=readMatLabFig_LandmarkMap(LandmarkMap_fn)    
    PHMI_dic=readMatLabFig_PHMI(PHMI_fn,LandmarkMap_dic)
    
    locations=PHMI_dic[0]
    landmarks=LandmarkMap_dic[1]
    radius=20
    targetPts,locations_pts,targetPts_idx=scanCircleBuffer(locations,landmarks,radius)

    G=location_landmarks_network(targetPts_idx,locations,landmarks)
    
    
    
    
    
'''
import scipy.io as sio
mat_contents = sio.loadmat(matLabFigFn)
sorted(mat_contents.keys())
mat_contents['hgS_070000'][0].shape
x = loadmat(matLabFigFn)
mat_contents = sio.loadmat(matLabFigFn)
'''