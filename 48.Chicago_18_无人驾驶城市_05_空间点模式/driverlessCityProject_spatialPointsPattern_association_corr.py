# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:10:12 2020

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
import copy,math
from statistics import mean 
from itertools import compress
from shapely.geometry import Point,MultiPoint,Polygon,MultiPolygon
from sklearn import preprocessing
from numpy import convolve as npConv

import scipy.spatial
import libpysal as ps
from pointpats import PointPattern, PoissonPointProcess, as_window, G, F, J, K, L, Genv, Fenv, Jenv, Kenv, Lenv #you can also use R's spatstat spatial points pattern library  亦可以使用R的spatstat空间点格局模式库
import pointpats.quadrat_statistics as qs #apply Quadrat_statistics of PySAL 应用PySAL的Quadrat_statistics

#01-classify PHMI with percentile
def labelsPercentile_upgrade(data):
    percentileNumber=[0,1,10,20, 30, 40,50,60, 70, 80, 90,100] #可以设置任意百分位切分值    
    percentileValue=[np.percentile(data,i) for i in percentileNumber]
    #print(percentileValue)
    
    bunchRange=list(zip(percentileValue, percentileValue[1:] + percentileValue[:1]))   
    bunchIdx=list(range(len(bunchRange)))
    #print(bunchRange,bunchIdx)
    valRange=[]

    i=0
    for val in data:        
        val_Idx=[bunchIdx[k] for k in range(len(bunchRange)) if val>=bunchRange[k][0] and val<=bunchRange[k][1]]
        valRange.append(val_Idx[0])
        # print(val,val_Idx)
        # if i==0:
        #     break

    # print(valRange)
    # print("bunchIdx amount:",len(bunchIdx),"\n",bunchIdx)
    return valRange   

#auxiliary tool
def Average(lst): 
    return sum(lst) / len(lst) 
#auxiliary tool
def getIndexPositions_2(listOfElements, element):
    ''' Returns the indexes of all occurrences of give element in the list- listOfElements '''
    indexPosList = []
    for i in range(len(listOfElements)): 
        if listOfElements[i] == element:
            indexPosList.append(i)
    return indexPosList 
#auxiliary tool
def multiPolygonShow(lst):
    cmap = plt.cm.get_cmap('RdPu') #'Spectral'  https://matplotlib.org/2.0.1/users/colormaps.html
    fig, axs = plt.subplots(figsize=(20,20))
    axs.set_aspect('equal', 'datalim')
    i=0
    for geom in multiSegs.geoms:
        xs, ys = geom.exterior.xy 
        axs.fill(xs, ys, alpha=0.5, fc=cmap(lst[i]), ec='none')
        # axs.text(10)
        i+=1
        # if i==10:break
    # cax = plt.axes(lst)
    # plt.colorbar(cax=cax)    
    plt.show() 
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    values=lst
    values += values[:1]    
    print(len(values),len(lst))

    N=len(lst)-1
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)     
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], list(range(num)), color='grey', size=8)     
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0,0.5,1], ["0","0.5","1"], color="grey", size=7)
    plt.ylim(0,1)     
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')     
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
#auxiliary tool    
def quadratCount(targetPts_epoch,locationsPts_epoch,nx,ny):
    # corners=[Point(p.x+30,p.y+30),Point(p.x+30,p.y-30),Point(p.x-30,p.y-30),Point(p.x-30,p.y+30)]
    corners_coordi=[(locationsPts_epoch.x+30,locationsPts_epoch.y+30),(locationsPts_epoch.x+30,locationsPts_epoch.y-30),(locationsPts_epoch.x-30,locationsPts_epoch.y-30),(locationsPts_epoch.x-30,locationsPts_epoch.y+30)]
    target_pts=[coordinate.coords[:][0] for coordinate in targetPts_epoch]+corners_coordi
    pp = PointPattern(target_pts)
    # print("^"*50)
 
    #应用PySAL的Quadrat_statistics样方统计,亦可以替换用R的spatstat库实现，获取更多功能。参考：https://pointpats.readthedocs.io/en/latest/  https://pysal.org/notebooks/explore/pointpats/Quadrat_statistics.html
    #样方分析（Quadrat Analysis ，QA ）法是样方内点数均值变差的分析方法，是由Greig-Smith 于1964年提出的。其具体做法是用一组样方覆盖在研究区域上并作叠置分析，统计落在每一个样方上的样本数，通过统计不同的具有m 个点数的样方的个数及其频率，并与完全随机过程（Poisson 分布）对比来判断点模式的空间分布特征。其结果一般用方差均值比（V ariance-Mean Ratio ，VMR ）判断。
    #合理地确定样方的大小较为重要，一般地样方大小的确定采用符合“拇指规则（rule of thumb ）”，即样方大小应当是平均每个点所占面积的两倍. ref:《黄土丘陵沟壑区农村居民点分布模式空间统计分析——以甘谷县为例》
    q_r = qs.QStatistic(pp,shape= "rectangle",nx = nx, ny = ny)
    # q_r.plot()
    mr=q_r.mr    
    quadratCount=mr.point_location_sta()
    # print(quadratCount)
    chi2=q_r.chi2 #观察点模式的卡方检验统计量 chi-squared test statistic for the observed point pattern
    chi2_pvalue=q_r.chi2_pvalue
    df=q_r.df
    
    comparisonValue=1
    quadratNum=sum(np.array(list(quadratCount.values()))>=comparisonValue) #the amount of the occupied quadrat based on a value used for comparison 
    
    # print(sum(np.array(list(quadratCount.values()))>=1))
    numDivQuad=len(targetPts_epoch)/sum(np.array(list(quadratCount.values()))>=1) #amount_landmarks/amount_the occupied quadrat
    return chi2,quadratNum,numDivQuad    
    
#merge all indicators
def indicatorAssociation(targetPts_idx,locations_pts,Phmi,distance_domain_quadrat):
    indicator_df=pd.DataFrame()
    
    #01-PHMI
    indicator_df["PHMI"]=Phmi
    
    '''A-basic related content'''
    #02-the amount of landmarks at each epoch
    LM_numbers=list(zip([key for key in targetPts_idx.keys()],[len(vals) for vals in targetPts_idx.values()]))
    # print(LM_numbers)
    indicator_df["LM_amount"]=[num[1] for num in LM_numbers]
    #03-(x,y) of AV location
    indicator_df["loc_x"]=[p.x for p in locations_pts]
    indicator_df["loc_y"]=[p.y for p in locations_pts]
        
    # distance_mean=[]
    # distance_min=[]
    indicator_dic={
        "distance_mean":[],
        "distance_min":[],
        "distance_max":[],
        "direction_is":[],
        "direction_none":[],
        "direction_edge":[],
        "intensity_mbb":[],
        "intensity_hull":[],
        "nnd_max":[],
        "nnd_min":[],
        "nnd_mean":[],
        "nnd2_mean":[],
        "G":[],
        # "F":[],
        
        }
    containResults={} #store bool values of segments at each epoch to check if there is landmarks in each segment  存储无人车位置点划分视角，存储每一视角存在的landmark布尔值
    containsResults_num={} #store the amount of landmarks in each segemnt存储无人车位置点划分视角，存储每一视角存在的landmark数量
    trueIdx={}
    distanceContain={}
    distanceContainAdj={}
    i=0    
    genv_list=[]
    quadratCount_dic={}
    for key in tqdm(targetPts_idx.keys()):
        #distance between landmarks and each location
        distance_temp=[locations_pts[key].distance(pt) for pt in targetPts[key]]
        #00-mean distances between landamarks and each location of AV
        indicator_dic["distance_mean"].append(Average(distance_temp))
        #00-min distance
        indicator_dic["distance_min"].append(min(distance_temp))
        #00-max distance
        indicator_dic["distance_max"].append(max(distance_temp))
    
        '''B-direction-related content'''
        p=locations_pts[key]
        lidarScanDis=25
        bufferCircle = p.buffer(lidarScanDis).boundary
        circleLen=bufferCircle.length
                
        divisionRange=np.arange(0.,circleLen,(circleLen-0)/num)
        interpolationPts=[bufferCircle.interpolate(i) for i in divisionRange]
        interpolationPtsPairs=list(zip(interpolationPts, interpolationPts[1:] + interpolationPts[:1]))         
        segments=[Polygon([p,i[0],i[1]]) for i in interpolationPtsPairs]
        multiSegs=MultiPolygon(segments)
        
        containResults[key]=[([seg.contains(pt) for pt in targetPts[key]]) for seg in segments]
        containsResults_num[key]=[val.count(True) for val in containResults[key]] #have problem, due to count(True) only count the number 1
        indicator_dic["direction_is"].append(sum(i>0 for i in containsResults_num[key]))
        indicator_dic["direction_none"].append(sum(i==0 for i in containsResults_num[key]))
        
        #00-the nearest distance between the landmark and the location of AV in each direction 
        trueIdx[key]=[getIndexPositions_2(lst, True) for lst in containResults[key]]
        distanceContain[key]=[[distance_temp[idx] for idx in lst] for lst in trueIdx[key]]
        distanceContainAdj[key]=[min(lst) if lst!=[] else 9999 for lst in distanceContain[key]]
        
        #00-edge detection-extract the jump point as [-1,2,-1] and others are 0
        kernel_conv_even=[-1,2,-1]
        edge_detection=npConv([int(i) for i in containResults[key][0]],kernel_conv_even,'same')
        indicator_dic["direction_edge"].append(sum([abs(v) for v in edge_detection]))
        
        '''C-Intensity of landmarks''' 
        pp= PointPattern([coordinate.coords[:][0] for coordinate in targetPts[key]])
        #based on minimum bounding box 
        indicator_dic["intensity_mbb"].append(pp.lambda_mbb)
        #based on convex hull
        indicator_dic["intensity_hull"].append(pp.lambda_hull)
        
        '''D-distance statistics'''
        #distance based statistical method ref http://pysal.org/notebooks/explore/pointpats/distance_statistics.html
        indicator_dic["nnd_max"].append(pp.max_nnd)
        indicator_dic["nnd_min"].append(pp.min_nnd)
        indicator_dic["nnd_mean"].append(pp.mean_nnd)
        indicator_dic["nnd2_mean"].append(pp.knn(2)[1])

        #Nearest Neighbor Distance Functions/simulation envelopes---G  function - event-to-event / F  function - "point-event"
        #simulation envelopes
        realizations = PoissonPointProcess(pp.window, pp.n, 100, asPP=True) # simulate CSR 100 times
        genv = Genv(pp, intervals=20, realizations=realizations) # call Genv to generate simulation envelope
        genv_list.append(genv)
        plt.figure()
        genv.plot()

        #G
        gp1 = G(pp, intervals=20) #cumulative nearest neighbor distance distribution over d (corresponding to the y-axis))
        # plt.figure()
        # gp1.plot()
        G_mean=np.mean(gp1.G)  
        # print(G_mean)
        indicator_dic["G"].append(G_mean)
        #F
        # fp1 = F(pp, intervals=20) # The default is to randomly generate 100 points.
        # print(help(fp1))
        # F_mean=np.mean(np.diff(fp1.G)) #error-AttributeError: 'F' object has no attribute 'G'
        # indicator_dic["F"].append(F_mean)

        #quadrat statistics based on continuous distance
        nx_m=ny_m=list(distance_domain_quadrat)
        temp_quadratCount={}
        for nx,ny in zip(nx_m,ny_m):
            chi2,quadratNum,numDivQuad=quadratCount(targetPts[key],p,nx,ny)
            temp_quadratCount[str(nx)+"dis"]={"chi2":chi2,"quadratNum":quadratNum,"numDivQuad":numDivQuad}
        quadratCount_dic[key]=temp_quadratCount
        quadratCount_df=pd.concat({k: pd.DataFrame.from_dict(v, 'index') for k, v in quadratCount_dic.items()},axis=0)
        
        chi2_df=quadratCount_df.chi2.unstack(level=1)
        chi2_df.set_axis(["qdt_chi2_"+i for i in chi2_df.columns],axis=1, inplace=True)
        
        quadratNum_df=quadratCount_df.quadratNum.unstack(level=1)
        quadratNum_df.set_axis(["qdt_num_"+i for i in quadratNum_df.columns],axis=1, inplace=True)
        
        numDivQuad_df=quadratCount_df.numDivQuad.unstack(level=1)
        numDivQuad_df.set_axis(["qdt_n/Q_"+i for i in numDivQuad_df.columns],axis=1, inplace=True)
        
        #VMR(Variance/Mean Ratio) 

        # if i==5:break
        i+=1    
                
    #direction and distance
    distance_eachDirection=pd.DataFrame.from_dict(distanceContainAdj,orient='index',columns=list(range(num)))
    print(distance_eachDirection)
    distance_eachDirection["PHMI"]=Phmi  #[:11]
    distance_eachDirection["loc_x"]=[p.x for p in locations_pts]
    
    # print(indicator_dic)
    indicator_dic_df=pd.DataFrame.from_dict(indicator_dic)
    indicator_df_m=pd.concat([indicator_df,indicator_dic_df,chi2_df,quadratNum_df,numDivQuad_df], axis=1, sort=False)
    
    return indicator_df_m,distance_eachDirection,multiSegs,genv_list

#post-processing
def indicatorAssociation_postProcessing(indicator_df_concat):
    #01-percentile
    percentilePhmi=labelsPercentile_upgrade(indicator_df_concat.PHMI)  
    indicator_df_concat["PHMI_percentile"]=percentilePhmi
    
    #02-jitter mean
    con_breakPtsNeg,phmi_breakPtsNeg,phmi_breakIdx,plot_x=basic.con_1_dim(indicator_df_concat.PHMI.to_list(),indicator_df_concat.loc_x.to_numpy())
    phmi_breakPtsNeg_pop=copy.deepcopy(phmi_breakPtsNeg)
    

    temp=[lst.pop(-1) for lst in phmi_breakPtsNeg_pop[:-1]] #had better find a new way to solve "ValueError: Length of values does not match length of index"
    # temp=[lst.pop(0) for lst in phmi_breakPtsNeg_pop[1:]]
    phmi_breakPtsNeg_mean=[[mean(lst)]*len(lst) for lst in phmi_breakPtsNeg_pop]
    phmi_breakPtsNeg_mean_flatten=basic.flatten_lst(phmi_breakPtsNeg_mean)
    indicator_df_concat['jitter_mean']=phmi_breakPtsNeg_mean_flatten

    # print(phmi_breakPtsNeg_pop[:3])
    # print(len(basic.flatten_lst(phmi_breakPtsNeg)),len(basic.flatten_lst(phmi_breakPtsNeg_pop)),indicator_df_concat.PHMI.shape)
    
    return indicator_df_concat


#compute correlation(multiple) and show 
def correlation_graph(df,xlabel_str,title_str):
    plt.clf()
    corr =df.corr() 
    # print("_"*50,"correlation:")
    # print(corr)
    
    #01-correlation heatmap
    sns.set()
    f, ax = plt.subplots(figsize=(10*4.5, 10*4.5))
    sns.heatmap(corr, annot=True, fmt=".2f", linewidths=.5, ax=ax)
    
    #02-bar plot
    indicatorName=corr.columns.to_numpy()
    # plt.clf()
    plt.rcdefaults()
    plt.rcParams.update({'font.size':14})
    fig, ax = plt.subplots(figsize=(10*2, 10*2))  
    y_pos = np.arange(len(indicatorName))
    error = np.random.rand(len(indicatorName))
    
    ax.barh(y_pos, corr.PHMI.to_numpy(), align='center') #xerr=error, 
    ax.set_yticks(y_pos)
    ax.set_yticklabels(indicatorName)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(xlabel_str)
    ax.set_title(title_str)
    for index, value in enumerate(corr.PHMI.to_numpy()):
        plt.text(value, index, str(round(value,2)))
    plt.show()
    
    return corr

#plot multiple curve 
def multi_curve_plot(multi_df):
    xScale=multi_df.shape[0]
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    ax.set_prop_cycle(color=[
        '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a',
        '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94',
        '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d',
        '#17becf', '#9edae5'])
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    fig.subplots_adjust(left=.06, right=.75, bottom=.02, top=.94)
    ax.set_xlim(0,xScale+1)
    ax.set_ylim(-0.2, 0.6)
    ax.set_xticks(range(xScale))
    ax.set_yticks(np.arange(0,0.6,0.1))
    ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.2f}'.format))
    ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    ax.tick_params(axis='both', which='both', labelsize=14,
                   bottom=False, top=False, labelbottom=True,
                   left=False, right=False, labelleft=True)
    majors = ["PHMI_chi2","PHMI_qdtN","PHMI_nQ"] 
    y_offsets = {
        "PHMI_chi2":-0.02,
        }
    for column in majors:
        line, = ax.plot(list(range(xScale)), column, data=multi_df,lw=2.5)
        y_pos =multi_df[column].to_list()[-1]    
        if column in y_offsets:
            y_pos += y_offsets[column]        
        ax.text(xScale-0.8, y_pos, column, fontsize=14, color=line.get_color())
        fig.suptitle("correlation data curve", fontsize=18, ha="left")
    plt.show()
# multi_curve_plot(multi_df) 

    
if __name__ == "__main__":
    #merge data together
    dataPath=[
        # {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_LM.fig",
        #   "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_PHMI.fig" },
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_LM.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_PHMI.fig"},
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\LM.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\PHMI.fig"},
        # {"landmark":,
        #  "phmi":  },
        ]

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
        except:
            PHMI_dic=basic.readMatLabFig_PHMI_B(phmi_fn,LandmarkMap_dic)
            print("applied type -B")    
        #-01    
        Phmi=PHMI_dic[1][2]         
        #04
        locations=PHMI_dic[0] #the coordinates of AV
        landmarks=LandmarkMap_dic[1] #无distribution feature of landmarks
        radius=25 # scanning area of on_board lidar
        targetPts,locations_pts,targetPts_idx=basic.scanCircleBuffer(locations,landmarks,radius)

        '''B:association_correlation'''
        num=36 #segments of a circle
        indicator_df,distance_eachDirection,multiSegs,genv_list=indicatorAssociation(targetPts_idx,locations_pts,Phmi,distance_domain_quadrat)
        indicator_df_list.append(indicator_df)
        distance_eachDirection_list.append(distance_eachDirection)
        genv_dic[i]=genv_list        
        
        # if i==0:break
        i+=1          
    #A-indicator correlation           
    indicator_df_concat= pd.concat(indicator_df_list)
    # indicator_df_concat.to_pickle("./indicator_df_concat.pkl")
    # indicator_df_concat=pd.read_pickle("./indicator_df_concat.pkl")
    indicator_final=indicatorAssociation_postProcessing(indicator_df_concat) #indicator_df_postProcessing
    
    cols=indicator_final.columns.tolist()
    cols.remove("PHMI")
    cols.append("PHMI")
    indicator_final=indicator_final[cols]
    corr_indicator=correlation_graph(indicator_final,xlabel_str="indicator",title_str="indicators correlation")    
    
    #B-direction distance correlation
    distance_eachDirection_df=pd.concat(distance_eachDirection_list)
    # distance_eachDirection_df.to_pickle("./distance_eachDirection_df.pkl")
    # distance_eachDirection_df=pd.read_pickle("./distance_eachDirection_df.pkl")
    corr_disDirection=correlation_graph(distance_eachDirection_df,xlabel_str="direction distance",title_str="direction distance correlation")
    #if there is one or more landmarks in each direction
    distance_eachDirection_isOrNone=distance_eachDirection_df[list(range(36))].apply(lambda x:[1 if y==9999 else 0 for y in x])
    distance_eachDirection_isOrNone[["PHMI","loc_x"]]=distance_eachDirection_df[["PHMI","loc_x"]]
    corr_disDirection=correlation_graph(distance_eachDirection_isOrNone,xlabel_str="direction distance",title_str="direction distance correlation_isOrNone")
   
    #show radar plot
    corr_phmi=abs(corr_disDirection.corr().PHMI[:-2]).fillna(0)
    min_max_scaler = preprocessing.MinMaxScaler()
    scaled_array = min_max_scaler.fit_transform(corr_phmi.to_numpy().reshape(-1,1))
    corr_phmi_scale=scaled_array.reshape(-1).tolist()
    multiPolygonShow(corr_phmi_scale)        
    
    #C-curve plot
    rows_chi2=["qdt_chi2_"+str(i)+"dis" for i in list(distance_domain_quadrat)]
    columns=["PHMI"]
    multi_df_chi2=corr_indicator.loc[rows_chi2,columns]
    multi_df_chi2.reset_index(inplace=True)
    multi_df_chi2.rename(columns={"PHMI":"PHMI_chi2","index":"idx_chi2"},inplace=True)
    
    rows_qdtN=["qdt_num_"+str(i)+"dis" for i in list(distance_domain_quadrat)]
    multi_df_qdtN=corr_indicator.loc[rows_qdtN,columns]
    multi_df_qdtN.reset_index(inplace=True)
    multi_df_qdtN.rename(columns={"PHMI":"PHMI_qdtN","index":"idx_qdtN"},inplace=True)

    rows_qdtN=["qdt_n/Q_"+str(i)+"dis" for i in list(distance_domain_quadrat)]
    multi_df_nq=corr_indicator.loc[rows_qdtN,columns]
    multi_df_nq.reset_index(inplace=True)
    multi_df_nq.rename(columns={"PHMI":"PHMI_nQ","index":"idx_nQ"},inplace=True)

    
    multi_df=pd.concat([multi_df_chi2,multi_df_qdtN,multi_df_nq],axis=1, sort=False)             #[multi_df_chi2,multi_df_qdtN]
    multi_curve_plot(multi_df)
    
    multi_df_abs=multi_df.copy()
    colsName=["PHMI_chi2","PHMI_qdtN","PHMI_nQ"]
    multi_df_abs[colsName]=multi_df_abs[colsName].abs()
    multi_curve_plot(multi_df_abs)
    
    #D-change of position
    distance_eachDirection_change_before=distance_eachDirection_isOrNone[list(range(36))].copy()
    distance_eachDirection_change_after=distance_eachDirection_change_b.shift(periods=-1, fill_value=0)
    distance_eachDirection_change_before=distance_eachDirection_change_before.astype(str) 
    distance_eachDirection_change_after=distance_eachDirection_change_after.astype(str)
    direction_change=distance_eachDirection_change_before+distance_eachDirection_change_after
    direction_change.replace({"00":0,"01":1,"10":2,"11":3},inplace=True)
    direction_change[["PHMI","loc_x"]]=distance_eachDirection_df[["PHMI","loc_x"]]
    
    corr_direction_change=correlation_graph(direction_change,xlabel_str="direction landmarks change",title_str="direction landmarks correlation_change")
