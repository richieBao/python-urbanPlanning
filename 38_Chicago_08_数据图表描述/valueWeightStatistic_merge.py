# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 17:02:29 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import os,pysal,fiona,shapely,sympy,math,contextily,rasterio,datetime,geojson 
# print(fiona.supported_drivers) #a full list of supported formats, type
import pandas as pd
import seaborn as sns
import geopandas as gpd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from shapely.geometry import shape,mapping, Point,MultiPoint, Polygon, MultiPolygon,LineString
from shapely.geometry.polygon import LinearRing
from pylab import figure, scatter, show
from sklearn.preprocessing import minmax_scale
import contextily as ctx
from rasterio.mask import mask
# from eobox.raster import extraction
from rasterstats import zonal_stats
from rasterio import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.plot import show as rioShow
from rasterio.windows import Window
from rasterio.features import shapes

#打印pandas DataFrame数据信息
def dataFrameInfoPrint(df):
    print("info:\n",df.info(verbose=False),
      "head:\n",df.head(),
      "columns:\n",df.columns,
      )

#可视化vector数据
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

#合并分散的数据，整合到一个DataFrame中    
def valueMerge(data_Dic):
# def parkInfoIntegration(data_Dic):
    ParkBoundaries=gpd.read_file(data_Dic["parkBoundaries"])
    # dataFrameInfoPrint(ParkBoundaries)    
    '''所计算的内容
    [614 rows x 81 columns]> columns:
     Index(['acres', 'archery_ra', 'artificial', 'band_shell', 'baseball_b',
           'baseball_j', 'baseball_s', 'basketba_1', 'basketball', 'beach',
           'boat_lau_1', 'boat_launc', 'boat_slips', 'bocce_cour', 'bowling_gr',
           'boxing_cen', 'carousel', 'casting_pi', 'climbing_w', 'community',
           'conservato', 'cricket_fi', 'croquet', 'cultural_c', 'dog_friend',
           'fitness_ce', 'fitness_co', 'football_s', 'gallery', 'game_table',
           'garden', 'gisobjid', 'golf_cours', 'golf_drivi', 'golf_putti',
           'gymnasium', 'gymnastic', 'handball_i', 'handball_r', 'harbor',
           'horseshoe', 'iceskating', 'label', 'lagoon', 'location', 'minigolf',
           'modeltrain', 'modelyacht', 'mountain_b', 'nature_bir', 'nature_cen',
           'objectid_1', 'park', 'park_class', 'park_no', 'perimeter',
           'playgrou_1', 'playground', 'pool_indoo', 'pool_outdo', 'rowing_clu',
           'senior_cen', 'shape_area', 'shape_leng', 'shuffleboa', 'skate_park',
           'sled_hill', 'sport_roll', 'spray_feat', 'tennis_cou', 'track',
           'volleyba_1', 'volleyball', 'ward', 'water_play', 'water_slid',
           'wetland_ar', 'wheelchr_a', 'zip', 'zoo', 'geometry'],
          dtype='object')
    '''

    #仅提取需要的字段 clear data fields
    parksFieldsExtractedList=['park_no','label','park_class','location','acres','shape_area', 'shape_leng','perimeter','geometry']
    parks_fieldsExtracted=ParkBoundaries[parksFieldsExtractedList]
    # dataFrameInfoPrint(parks_fieldsExtracted)

    parkFacility=gpd.read_file(data_Dic["parkFacilities"],encoding="utf8")
    # dataFrameInfoPrint(parkFacility)
    '''
    [5 rows x 9 columns] columns:
    Index(['facility_n', 'facility_t', 'gisobjid', 'objectid', 'park', 'park_no',
       'x_coord', 'y_coord', 'geometry'],
      dtype='object')
    '''
    facilityFieldsExtractedList=['facility_n', 'facility_t','park', 'park_no','x_coord', 'y_coord', 'geometry']
    '''park facility'''
    facility_fieldsExtracted=parkFacility[facilityFieldsExtractedList]    
    # dataFrameInfoPrint(facility_fieldsExtracted)
    parksInfo_linkFacility=gpd.sjoin(parks_fieldsExtracted, facility_fieldsExtracted, how='inner')
    # dataFrameInfoPrint(parksInfo_linkFacility)
    facilityFrequency=parksInfo_linkFacility.index.value_counts()
    facilityFrequencyDf=pd.DataFrame(facilityFrequency,columns=["facilityFre"])
    facilityFrequencyDf["facilityID"]=facilityFrequencyDf.index
    
    #projection。因为要计算面积和长度等信息，因此需要定义投影
    # print(parks_fieldsExtracted.crs) #{'init': 'epsg:4326'}
    parks_fieldsExtracted=parks_fieldsExtracted.to_crs({'init': 'epsg:2028'}) #投影参考：https://spatialreference.org/ref/epsg/?search=&srtext=Search   https://epsg.io/  
    # print(parks_fieldsExtracted.crs)
    
    #calculation and add new fields
    parks_fieldsExtracted["shapelyArea"]=parks_fieldsExtracted.geometry.area
    parks_fieldsExtracted["shapelyLength"]=parks_fieldsExtracted.geometry.length

    #使用sympy库建立计算面公式，清晰方便
    #shape index
    #pij = perimeter (m) of patch ij.   aij = area (m2) of patch ij. 
    pij=sympy.Symbol('pij')
    aij =sympy.Symbol('aij ')
    expr_shapeIdx=0.25*pij/sympy.root(aij,2)    
    # result=fx.evalf(subs={x:3,y:4})
    fx_shapeIdx = sympy.lambdify((pij,aij), expr_shapeIdx, 'numpy')
    parks_fieldsExtracted["shapeIdx"]=fx_shapeIdx(parks_fieldsExtracted.shapelyLength,parks_fieldsExtracted.shapelyArea)
    
    validation_result=expr_shapeIdx.evalf(subs={pij:1093.47,aij:72084.9}) #仅用于验证。validate the first patch
    # print(validation_result)  

    #Fractal Dimension Index(FRAC)
    expr_FRAC=2*sympy.log(0.25*pij)/sympy.log(aij,2)
    fx_FRAC= sympy.lambdify((pij,aij), expr_FRAC, 'numpy')
    parks_fieldsExtracted["FRAC"]=fx_FRAC(parks_fieldsExtracted.shapelyLength,parks_fieldsExtracted.shapelyArea)
    
    ChicagoBoudnary=gpd.read_file(data_Dic["ChicagoBoudnary"])
    dataFrameInfoPrint(ChicagoBoudnary)
    
    showVector(parks_fieldsExtracted,'shapeIdx')
    
    parkPopulationDistanceWeight=pd.read_pickle(data_Dic["parkPopulationDistanceWeight"])
    parkSVFDistanceWeight=pd.read_pickle(data_Dic["parkSVFDistanceWeight"])
    popu_rename={origion:target for origion, target in zip(list(parkPopulationDistanceWeight.columns),["popu_"+name for name in list(parkPopulationDistanceWeight.columns)])}
    parkPopulationDistanceWeight=parkPopulationDistanceWeight.rename(columns=popu_rename)
    
    #columns rename部分可以单独编写为一个函数，方便调用，此处未编写。
    SVF_rename={origion:target for origion, target in zip(list(parkSVFDistanceWeight.columns),["SVFW_"+name for name in list(parkSVFDistanceWeight.columns)])}
    parkSVFDistanceWeight=parkSVFDistanceWeight.rename(columns=SVF_rename)

    parks_fieldsExtracted=parks_fieldsExtracted.join(parkPopulationDistanceWeight)
    parks_fieldsExtracted=parks_fieldsExtracted.join(parkSVFDistanceWeight)
    parks_fieldsExtracted["polyID"]=parks_fieldsExtracted.index
    
    parkSVFEp=pd.read_pickle(data_Dic["parkSVFEp"])
    parkSVFEp_rename={origion:target for origion, target in zip(list(parkSVFEp.columns),["SVFep_"+name for name in list(parkSVFEp.columns)])}
    parkSVFEp=parkSVFEp.rename(columns=parkSVFEp_rename)    
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, parkSVFEp], axis=1, sort=False)    
    
    heightVegetationS=pd.read_pickle(data_Dic["heightVegetationS"])
    heightVegetationS_rename={origion:target for origion, target in zip(list(heightVegetationS.columns),["HVege_"+name for name in list(heightVegetationS.columns)])}
    heightVegetationS=heightVegetationS.rename(columns=heightVegetationS_rename)    
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, heightVegetationS], axis=1, sort=False)
    
    mediVegetationS=pd.read_pickle(data_Dic["mediVegetationS"])
    mediVegetationS_rename={origion:target for origion, target in zip(list(mediVegetationS.columns),["MVege_"+name for name in list(mediVegetationS.columns)])}
    mediVegetationS=mediVegetationS.rename(columns=mediVegetationS_rename)    
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, mediVegetationS], axis=1, sort=False)   
    
    lowVegetationS=pd.read_pickle(data_Dic["lowVegetationS"])
    lowVegetationS_rename={origion:target for origion, target in zip(list(lowVegetationS.columns),["LVege_"+name for name in list(lowVegetationS.columns)])}
    lowVegetationS=lowVegetationS.rename(columns=lowVegetationS_rename)    
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, lowVegetationS], axis=1, sort=False)    
    
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, facilityFrequencyDf], axis=1, sort=False)
    
    classification=pd.read_pickle(data_Dic["classification"])
    classification_rename={origion:target for origion, target in zip(list(classification.columns),["cla_"+name for name in list(classification.columns)])}
    classification=classification.rename(columns=classification_rename)   
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, classification], axis=1, sort=False)
    
    classificationCount=pd.read_pickle(data_Dic["classificationCount"])
    classificationCount_rename={origion:target for origion, target in zip(list(classificationCount.columns),["classi_"+name for name in list(classificationCount.columns)])}
    classificationCount=classificationCount.rename(columns=classificationCount_rename)  
    parks_fieldsExtracted=pd.concat([parks_fieldsExtracted, classificationCount], axis=1, sort=False)
    
    #变换投影，存储文件为EPSG:4326: WGS 84
    parks_fieldsExtracted=parks_fieldsExtracted.to_crs({'init': 'epsg:4326'})  
    fp=r"F:\data_02_Chicago\parkNetwork\dataOutput"
    parks_fieldsExtracted.to_file(os.path.join(fp,r"parkFieldExtracted.shp"))
    
    return parks_fieldsExtracted,parksInfo_linkFacility

#地理数据可视化（弃）。转为单独的文件：parkDataVisulization.py
def geoValVisulization_a(geoPd):
    geoPd["ID"]=geoPd.index.astype(str)
    print(geoPd.columns)
    '''
Index(['park_no', 'label', 'park_class', 'location', 'acres', 'shape_area',
       'shape_leng', 'perimeter', 'geometry', 'shapelyArea', 'shapelyLength',
       'shapeIdx', 'FRAC', 'popu_count', 'popu_mean', 'popu_std', 'popu_min',
       'popu_25%', 'popu_50%', 'popu_75%', 'popu_max', 'SVFW_count',
       'SVFW_mean', 'SVFW_std', 'SVFW_min', 'SVFW_25%', 'SVFW_50%', 'SVFW_75%',
       'SVFW_max', 'polyID', 'SVFep_min', 'SVFep_max', 'SVFep_mean',
       'SVFep_count', 'SVFep_sum', 'SVFep_std', 'SVFep_median',
       'SVFep_majority', 'SVFep_minority', 'SVFep_unique', 'SVFep_range',
       'SVFep_nodata', 'HVege_min', 'HVege_max', 'HVege_mean', 'HVege_count',
       'HVege_sum', 'HVege_std', 'HVege_median', 'HVege_majority',
       'HVege_minority', 'HVege_range', 'HVege_nodata', 'MVege_min',
       'MVege_max', 'MVege_mean', 'MVege_count', 'MVege_sum', 'MVege_std',
       'MVege_median', 'MVege_majority', 'MVege_minority', 'MVege_range',
       'MVege_nodata', 'LVege_min', 'LVege_max', 'LVege_mean', 'LVege_count',
       'LVege_sum', 'LVege_std', 'LVege_median', 'LVege_majority',
       'LVege_minority', 'LVege_range', 'LVege_nodata', 'facilityFre',
       'facilityID', 'cla_treeCanopy', 'cla_grassShrub', 'cla_bareSoil',
       'cla_buildings', 'cla_roadsRailraods', 'cla_otherPavedSurfaces',
       'cla_water', 'classi_count', 'ID'],
      dtype='object')
    '''
    sns.set(style="whitegrid")
    
    # Make the PairGrid
    extractedColumns=['shapelyArea','shapelyLength',
                      'shapeIdx','FRAC',
                      'SVFW_mean','SVFW_std',
                      'SVFW_mean','SVFW_std',
                      'popu_std','popu_mean',                      
                      'facilityFre',
                      'classi_count','cla_treeCanopy', 'cla_grassShrub','cla_bareSoil', 'cla_buildings', 'cla_roadsRailraods', 'cla_otherPavedSurfaces','cla_water',
                      'HVege_count','HVege_mean',
                      'LVege_count','LVege_mean',
                      
                      ]
    # geoPdSort=geoPd.sort_values('shapelyArea', ascending=False)
    g=sns.PairGrid(geoPd.sort_values('shapelyArea', ascending=False),x_vars=extractedColumns, y_vars=["label"],height=20, aspect=.25)
    # g=sns.PairGrid(geoPd,x_vars=extractedColumns, y_vars=["ID"],height=20, aspect=.25)

    # Draw a dot plot using the stripplot function
    g.map(sns.stripplot, size=5, orient="h",palette="ch:s=1,r=-.1,h=1_r", linewidth=1, edgecolor="w")    
    # Use the same x axis limits on all columns and add better labels
    g.set(xlabel="value", ylabel="") #g.set(xlim=(0, 25), xlabel="Crashes", ylabel="")
    # Use semantically meaningful titles for the columns
    g.fig.set_figwidth(30)
    g.fig.set_figheight(80)
    
    titles=extractedColumns
    for ax, title in zip(g.axes.flat, titles):
        # Set a different title for each axes
        ax.set(title=title)
        # Make the grid horizontal instead of vertical
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)
    sns.despine(left=True, bottom=True)        

    return geoPd


if __name__=="__main__": 
    data_Dic={"parkBoundaries":r"F:\data_02_Chicago\parkNetwork\Parks - Chicago Park District Park Boundaries (current).shp",
              "parkFacilities":r"F:\data_02_Chicago\parkNetwork\parks - Chicago Park District Facilities (current).shp",
              "ChicagoBoudnary":r"F:\data_02_Chicago\parkNetwork\Boundaries - Census Blocks - 2010.shp",
              
              "parkPopulationDistanceWeight":r"F:\data_02_Chicago\parkNetwork\dataOutput\parkPopulationDistanceWeight.pkl",
              "parkSVFDistanceWeight":r"F:\data_02_Chicago\parkNetwork\dataOutput\parkSVFDistanceWeight.pkl",
              "parkSVFEp":r"F:\data_02_Chicago\parkNetwork\dataOutput\SVFEachPark.pkl",
              
              "classification":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\classificationPolygonStatistics.pkl",
              "classificationCount":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\classificationPolygonStatistics_count.pkl",
              
              "heightVegetationS":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\height_highVegetation_reprojectedStatistics.pkl",
              "lowVegetationS":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\low_highVegetation_reprojectedStatistics.pkl",
              "mediVegetationS":r"F:\data_02_Chicago\ArcGisPro\parkNetwork\medi_highVegetation_reprojectedStatistics.pkl",
            } 
    
    parks_fieldsExtracted,parksInfo_linkFacility=valueMerge(data_Dic)
    # parks_fieldsExtractedSort=parks_fieldsExtracted.sort_values('shapelyArea', ascending=False)
    geoPdSort=geoValVisulization_a(parks_fieldsExtracted)
    
    
    parks_fieldsExtracted.to_pickle(r"F:\data_02_Chicago\parkNetwork\dataOutput\parks_fieldsExtracted.pkl")
    parksInfo_linkFacility.to_pickle(r"F:\data_02_Chicago\parkNetwork\dataOutput\parksInfo_linkFacility.pkl")
    
    '''x.facility_n.unique()
    array(['BASEBALL SR', 'FOOTBALL/SOCCER COMBO FLD', 'BASEBALL JR/SOFTBALL',
       'TENNIS COURT', 'BASKETBALL COURT', 'BASKETBALL BACKBOARD',
       'HORSESHOE COURT', 'BOCCE COURT', 'COMMUNITY GARDEN',
       'FITNESS CENTER', 'GYMNASIUM', 'POOL (INDOOR)', 'PLAYGROUND',
       'SPRAY FEATURE', 'SPORT ROLLER COURT', 'VOLLEYBALL (SAND)',
       'POOL (OUTDOOR)', 'TRACK', 'BOXING CENTER',
       'ARTIFICIAL TURF FIELD', 'VOLLEYBALL', 'LAGOON', 'CASTING PIER',
       'HANDBALL/RACQUET (OUT)', 'GARDEN', 'CAROUSEL', 'ARCHERY RANGE',
       'CULTURAL CENTER', 'HARBOR', 'BEACH', 'GYMNASTIC CENTER',
       'MODEL TRAIN DISPLAY', 'BOAT LAUNCH MOTORIZED', 'WETLAND AREA',
       'GAME TABLES', 'WATER SLIDE', 'HANDBALL/RACQUET (IN)',
       'CRICKET FIELD', 'GOLF COURSE', 'NATURE/BIRD SANCTUARY',
       'FITNESS COURSE', 'GOLF DRIVING RANGE', 'GOLF PUTTING GREEN',
       'BOAT LAUNCH NON-MOTORIZED', 'BOWLING GREEN', 'CROQUET',
       'WATER PLAYGROUND', 'ICESKATING', 'DOG FRIENDLY AREA',
       'SKATE PARK', 'BAND SHELL', 'CLIMBING WALL', 'SLED HILL',
       'PLAYGROUND PARK', 'ROWING CLUB', 'CONSERVATORY',
       'ALFRED CALDWELL LILY POND', 'SHUFFLEBOARD', 'SENIOR CENTER',
       'NATURE CENTER', 'GALLERY', 'WHEELCHR ACCSSBLE BALLFLD',
       'GOLF COURSE MINIATURE', 'BASEBALL BATTING CAGE',
       'MOUNTAIN BIKE TRAIL', 'MODEL YACHT BASIN'], dtype=object)
    '''