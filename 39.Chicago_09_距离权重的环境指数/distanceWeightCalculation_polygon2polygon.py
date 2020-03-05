# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 13:57:28 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import datetime,math
import geopandas as gpd
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import numpy as np
import os

#查看DataFrame信息
def dataFrameInfoPrint(df):
    print("info:\n",df.info(verbose=False),
      "head:\n",df.head(),
      "columns:\n",df.columns,
      )
    
#显示vector数据
def showVector(df,columnName):
    # print(df.columns)
    #可以显示vecter（polygon,point）数据。show vector
    multi=2
    fig, ax = plt.subplots(figsize=(14*multi, 8*multi))
    df.plot(column=columnName,
            categorical=True,
            legend=True,
            scheme='QUANTILES',
            cmap='RdBu', #'OrRd'
            ax=ax)
    # df.plot()
    # adjust legend location
    leg = ax.get_legend()
    # leg.set_bbox_to_anchor((1.15,0.5))
    ax.set_axis_off()    
    plt.show()      

#计算polygon的中心点，然后计算中心点到polygon的距离    
def polygon2polygonInverseDestanceWeight(location,target):
    epsg={'init': 'epsg:2028'}
    locationPD=gpd.read_file(location)
    targetPD=gpd.read_file(target)
    locationPDReproject=locationPD.to_crs(epsg)
    targetPDReproject=targetPD.to_crs(epsg)
    # print("location fields:",locationPD.columns)
    # print("target fields:",targetPD.columns)
    # showVector(targetPDReproject,'TOTAL POPU')
    # showVector(locationPD,'park_class')
    
    targetPDReproject["centroid"]=targetPDReproject.geometry.centroid
    geo_pts=gpd.GeoDataFrame(targetPDReproject['TOTAL POPU'],crs=epsg,geometry=targetPDReproject.centroid)
    
    locationPDReprojectGeometry=locationPDReproject.geometry
    valueWeightedDescribe=[]
    for i in tqdm(range(len(locationPDReprojectGeometry))):
        # print(locationPDReprojectGeometry[i])
        distances=geo_pts.geometry.distance(locationPDReprojectGeometry[i])
        distancesPD=pd.DataFrame(distances,columns=["distance"])
        distancesPD['IDW']=distancesPD.apply(lambda row:math.pow(row.distance+1,-1),axis=1)    
        distancesPD['value']=geo_pts["TOTAL POPU"]
        scale=10000
        distancesPD['IDWScale']=distancesPD.apply(lambda row:row.value*row.IDW*scale,axis=1)    
        valueWeightedDescribe.append(distancesPD.IDWScale.describe())

        # if i==1:
        #     break        
        
    weightValueDes=pd.DataFrame(data=valueWeightedDescribe,index=list(range(len(valueWeightedDescribe))),dtype=np.float32)   
    fp=r"F:\data_02_Chicago\parkNetwork\dataOutput"
    weightValueDes.to_pickle(os.path.join(fp,r'parkPopulationDistanceWeight.pkl')) 
    
    return weightValueDes


if __name__=="__main__": 
    data_Dic={"parkBoundaries":r"F:\data_02_Chicago\parkNetwork\Parks - Chicago Park District Park Boundaries (current).shp",
              "populationCensus":r"F:\data_02_Chicago\parkNetwork\populationCensus.shp"
            } 
    a_T = datetime.datetime.now()
    weightValueDes=polygon2polygonInverseDestanceWeight(data_Dic["parkBoundaries"],data_Dic["populationCensus"])                  
    b_T = datetime.datetime.now()
    print("reprojected time span:", b_T-a_T)                 
                  