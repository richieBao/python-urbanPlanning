# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 23:05:10 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""
import driverlessCityProject_spatialPointsPattern_association_basic as basic
import numpy as np
import pandas as pd
from tqdm import tqdm
import plotly.express as px
from plotly.offline import plot
import matplotlib.pyplot as plt
import seaborn as sns 
import copy,math,os
from statistics import mean 
from itertools import compress
from shapely.geometry import Point,MultiPoint,Polygon,MultiPolygon,LineString,MultiLineString
from shapely.affinity import rotate
from shapely.ops import linemerge,split
from sklearn import preprocessing
from numpy import convolve as npConv

import scipy.spatial
import libpysal as ps
from pointpats import PointPattern, PoissonPointProcess, as_window, G, F, J, K, L, Genv, Fenv, Jenv, Kenv, Lenv #you can also use R's spatstat spatial points pattern library  亦可以使用R的spatstat空间点格局模式库
import pointpats.quadrat_statistics as qs #apply Quadrat_statistics of PySAL 应用PySAL的Quadrat_statistics



'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]


def G_direction(dataPath,save_root):
    i=0
    indicator_df_list=[]
    distance_eachDirection_list=[]
    genv_dic={}
    distance_domain_quadrat=range(2,20,1)
    for dat in dataPath:
        '''A:basic'''
        landmarks_fn=dat["landmark"]
        phmi_fn=dat["phmi"]
        #01   
        LandmarkMap_dic=basic.readMatLabFig_LandmarkMap(landmarks_fn)
        try:
            PHMI_dic=basic.readMatLabFig_PHMI_A(phmi_fn,LandmarkMap_dic)
            print("applied type -A")
            PHMI_dic=basic.readMatLabFig_PHMI_B(phmi_fn,LandmarkMap_dic)
            Phmi=PHMI_dic[1][2] 
            print("applied type -B")    
        except:
            PHMI_dic=basic.readMatLabFig_PHMI_C(phmi_fn)
            Phmi=PHMI_dic
            print("applied type -C")              
        #-01    
                
        #04
        # locations=PHMI_dic[0] #the coordinates of AV
        locations=LandmarkMap_dic[0]
        landmarks=LandmarkMap_dic[1] #无distribution feature of landmarks
        
        radius=25 # scanning area of on_board lidar
        targetPts,locations_pts,targetPts_idx=basic.scanCircleBuffer(locations,landmarks,radius)
        
       
        i=0
        num=45 #segments of a circle 360/12=30    [12,18,24,36,45]
        lidarScanDis=25.0
        left_offset=15
        right_offset=10
        
        landmarks_direction=[]
        
        for i in tqdm(range(len(locations_pts)-1)):
            '''B-direction-related content'''            
            p=locations_pts[i]
            p_n=locations_pts[i+1]
            
            bufferCircle = p.buffer(lidarScanDis).boundary
            circleLen=bufferCircle.length                    
            divisionRange=np.arange(0.,circleLen,(circleLen-0)/num)
            interpolationPts=[bufferCircle.interpolate(i) for i in divisionRange]
            interpolationPtsPairs=list(zip(interpolationPts, interpolationPts[1:] + interpolationPts[:1]))         
            # segments=[Polygon([p,i[0],i[1]]) for i in interpolationPtsPairs]
            # multiSegs=MultiPolygon(segments)
            
            line_0=LineString([p,p_n])
            # endPts=line_0.interpolate(lidarScanDis,normalized=True)
            # forward_line=LineString([p,endPts])
            
            try:
                forward_line=LineString([p,Point(lidarScanDis*(p_n.x-p.x)/line_0.length,lidarScanDis*(p_n.y-p.y)/line_0.length)])
            except:
                print("data error")
            r=rotate(forward_line,250,origin=p)
            lines=[rotate(forward_line,deg,origin=p) for deg in range(0,360,num)]
            # M_lines=MultiLineString(lines)
            
            forward_line_180=rotate(forward_line,180,origin=p)
            center_line=LineString([forward_line.coords[1],forward_line_180.coords[1]])
            left_line=center_line.parallel_offset(left_offset,'left')
            right_line=center_line.parallel_offset(right_offset,'right')
            
            # M_RL_circle=MultiLineString([list(left_line.coords)]+[list(right_line.coords)]+[list(line.coords) for line in lines])
            M_RL=MultiLineString([list(left_line.coords)]+[list(right_line.coords)])
            
            
            polyogn_lines=[lines[i] for i in range(len(lines)) if i%2==0]
            inters_lines=[lines[i] for i in range(len(lines)) if i%2!=0]            
            
            inter_pts=[line.intersection(M_RL) for line in inters_lines if line.crosses(M_RL)]
            # M_inter_pts=MultiPoint(inter_pts)
            
            endPts_polyogn_lines=[line.coords[1] for line in polyogn_lines]
            polyton_pts=list(zip(endPts_polyogn_lines, endPts_polyogn_lines[1:] + endPts_polyogn_lines[:1]))       
            segments=[Polygon([p,i[0],i[1]]) for i in polyton_pts]
            # multiSegs=MultiPolygon(segments)

            if landmarks_direction:
                # print("_"*50)
                # print(landmarks_direction)
                temp_seg_opposite=[seg for pt in landmarks_direction for seg in segments if seg.contains(pt)]
                # b=[seg.contains(pt) for pt in landmarks_direction for seg in segments]
                temp_seg=[seg for seg in segments if seg not in temp_seg_opposite]
                
            
            else:
                temp_seg=segments
            
            temp_landmarks=[pt for pt in inter_pts for seg in temp_seg if seg.contains(pt)]
            landmarks_direction.append(temp_landmarks)
            landmarks_direction=flatten_lst(landmarks_direction)
            
           
            
            # if i==50:break
            # i+=1
                
        M_landmarks_direction=MultiPoint(landmarks_direction)     
        
        G_landmarks_df=pd.DataFrame(data=np.array([[pts.x,pts.y] for pts in landmarks_direction]), columns=["landmark_x", "landmark_y",])
        
        save_name=r"G_Direction_landmarks_%d.csv"%num
        G_landmarks_df.to_csv(os.path.join(save_root,save_name),index=False) 


def G_interval(dataPath,save_root):
    for dat in dataPath:
        '''A:basic'''
        landmarks_fn=dat["landmark"]
        phmi_fn=dat["phmi"]
        #01   
        LandmarkMap_dic=basic.readMatLabFig_LandmarkMap(landmarks_fn)
        try:
            PHMI_dic=basic.readMatLabFig_PHMI_A(phmi_fn,LandmarkMap_dic)
            print("applied type -A")
            PHMI_dic=basic.readMatLabFig_PHMI_B(phmi_fn,LandmarkMap_dic)
            Phmi=PHMI_dic[1][2] 
            print("applied type -B")    
        except:
            PHMI_dic=basic.readMatLabFig_PHMI_C(phmi_fn)
            Phmi=PHMI_dic
            print("applied type -C")              
        #-01    
                
        #04
        # locations=PHMI_dic[0] #the coordinates of AV
        locations=LandmarkMap_dic[0]
        landmarks=LandmarkMap_dic[1] #无distribution feature of landmarks
        
        radius=25 # scanning area of on_board lidar    
        targetPts,locations_pts,targetPts_idx=basic.scanCircleBuffer(locations,landmarks,radius)
        
        i=0
        lidarScanDis=25.0
        left_offset=15
        right_offset=10    
        landmarks_distance_pts=[]
        left_pts_all=[]
        right_pts_all=[]
        for i in tqdm(range(len(locations_pts)-1)):
            '''B-direction-related content'''            
            p=locations_pts[i]
            p_n=locations_pts[i+1]
            
            bufferCircle = p.buffer(lidarScanDis).boundary
            circleLen=bufferCircle.length 
            
            line_0=LineString([p,p_n])
            # endPts=line_0.interpolate(lidarScanDis,normalized=True)
            # forward_line=LineString([p,endPts])
            
            try:
                forward_line=LineString([p,Point(lidarScanDis*(p_n.x-p.x)/line_0.length,lidarScanDis*(p_n.y-p.y)/line_0.length)])
            except:
                print("data error")
            r=rotate(forward_line,250,origin=p)
            
            forward_line_180=rotate(forward_line,180,origin=p)
            center_line=LineString([forward_line.coords[1],forward_line_180.coords[1]])
            left_line=center_line.parallel_offset(left_offset,'left')
            right_line=center_line.parallel_offset(right_offset,'right')
            
            # M_RL_circle=MultiLineString([list(left_line.coords)]+[list(right_line.coords)]+[list(line.coords) for line in lines])
            M_RL=MultiLineString([list(left_line.coords)]+[list(right_line.coords)])       
           
            try:
                left_split=split(left_line,bufferCircle)[1]
                right_split=split(right_line,bufferCircle)[1]        
            except:
                left_split=split(left_line,bufferCircle)[0]
                right_split=split(right_line,bufferCircle)[0]
                
            M_RLC=MultiLineString([list(left_split.coords)]+[list(right_split.coords)]+[list(bufferCircle.coords)])
            left_split_coordi=np.array([(coordi[0],coordi[1]) for coordi in left_split.coords]).T
            right_split_coordi=np.array([(coordi[0],coordi[1]) for coordi in right_split.coords]).T
            
            if i==0:        
                division_num=50
                
                left_divide_x= np.linspace(left_split_coordi[0][0], left_split_coordi[0][1], division_num)
                left_divide_y=np.interp(left_divide_x,left_split_coordi[0],left_split_coordi[1])
                left_pts=MultiPoint([(x,y) for x , y in zip(left_divide_x,left_divide_y)])
                
                            
                right_divide_x= np.linspace(right_split_coordi[0][0], right_split_coordi[0][1], division_num)
                right_divide_y=np.interp(right_divide_x,right_split_coordi[0],right_split_coordi[1])
                right_pts=MultiPoint([(x,y) for x , y in zip(right_divide_x,right_divide_y)])
            
    
                temp_left_pts=[pt for pt in left_pts if Polygon(bufferCircle).contains(pt)]
                temp_right_pts=[pt for pt in right_pts if Polygon(bufferCircle).contains(pt)]
        
                left_num=len(temp_left_pts)
                right_num=len(temp_right_pts)
                
    
             
                left_pts_all.append(temp_left_pts)
                right_pts_all.append(temp_right_pts)
           
           
           
            temp_left_pts_=[pt for pt in flatten_lst(left_pts_all) if Polygon(bufferCircle).contains(pt)]
            temp_right_pts_=[pt for pt in flatten_lst(right_pts_all) if Polygon(bufferCircle).contains(pt)]
            if len(temp_left_pts_)<left_num:
                left_pts_all.append(Point(left_split_coordi.T[1]))
             
            if len(temp_right_pts_)<right_num:
                right_pts_all.append(Point(right_split_coordi.T[0]))        
         
             
    
            
            # if i==200:break
            # i+=1    
    
        landmarks_distance_pts.append(left_pts_all)
        landmarks_distance_pts.append(right_pts_all)        
        M_pts=MultiPoint(flatten_lst(landmarks_distance_pts))   
         
        G_landmarks_df=pd.DataFrame(data=np.array([[pts.x,pts.y] for pts in M_pts]), columns=["landmark_x", "landmark_y",])
        
        save_name=r"G_Distance_landmarks_%d.csv"%division_num
        G_landmarks_df.to_csv(os.path.join(save_root,save_name),index=False)     
    
                
            


if __name__ == "__main__":
    #merge data together
    dataPath=[
        # {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_LM.fig",
        #   "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_PHMI.fig" },
        # {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_LM.fig",
        #   "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_PHMI.fig"},
        # {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\LM.fig",
        #   "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\PHMI.fig"},
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-grasshopper\alexis_data\fwdsimulationresults\LMap_LinearConfig.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-grasshopper\alexis_data\fwdsimulationresults\PHMI_LinearConfig.fig"  },
        ]
    save_root=r"C:\Users\richi\omen-richiebao\omen-grasshopper\landmarksGeneration"
    #generate landmarks based on direction
    # G_direction(dataPath,save_root)
    
    G_interval(dataPath,save_root)
    

    
    
    
    
    
    