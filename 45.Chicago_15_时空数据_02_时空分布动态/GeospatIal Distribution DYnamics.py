# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:01:03 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import os,shapely
import pandas as pd
from shapely.geometry import Point,Polygon
import geopandas as gpd
from rasterstats import zonal_stats
import matplotlib.pylab as plt
import numpy as np

from pylab import rcParams
from matplotlib.pylab import style
style.use('ggplot')   
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

import mapclassify as mc
import giddy

import math
import pysal as ps
from esda.moran import Moran

from scipy import stats
import seaborn as sns

from giddy.markov import FullRank_Markov,GeoRank_Markov,Markov
from giddy import markov,mobility

from giddy.directional import Rose

from libpysal.weights import block_weights

#pip install descartes  -is required for plotting polygons in geopandas 
#calculate the x and y coordinates of geopandas object-Point
def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    geom_val=row[geom]
    if isinstance(geom_val, str):
        P = shapely.wkt.loads(geom_val)
    else:P=geom_val    
    # print(type(P))  #P.is_empty
    # print(P.x)
    # print("+"*50)
    # if isinstance(P,float):
        # print(P)
        # P=Point()
    # print(P)
    if coord_type == 'x':
        if isinstance(P,float): return float('nan')
        else: return P.x
    elif coord_type == 'y':
        if isinstance(P,float): return float('nan')
        else: return P.y

def covid_19_csv2gpd(dataFpDic):
    Covid_19=pd.read_csv(dataFpDic["Covid-19_CasesByZipCode"])
    covid19_dfCopy=Covid_19.copy(deep=True)
    # print("-"*50)
    # print(Covid_19.head)
    # print(Covid_19.columns)
    # Covid_19_MultiIdx_weekZip=Covid_19
    Covid_19['zipBak']=Covid_19['ZIP Code']
    covid19_df_byZip=covid19_dfCopy.set_index(['ZIP Code','Week Number']).sort_index()
    
    Covid_19_MultiIdx_weekZip=Covid_19.set_index(['Week Number','ZIP Code']).sort_index()
    Covid_19_MultiIdx_weekZip=Covid_19_MultiIdx_weekZip.rename(columns={
    'Week Start':'WeekStart', 
    'Week End':'WeekEnd', 
    'Cases - Weekly':'CasesWeekly', 
    'Cases - Cumulative':'CasesCumulative',
    'Case Rate - Weekly':'CaseRateWeekly', 
    'Case Rate - Cumulative':'CaseRateCumulative', 
    'Tests - Weekly':'TestsWeekly',
    'Tests - Cumulative':'TestsCumulative', 
    'Test Rate - Weekly':'TestRateWeekly', 
    'Test Rate - Cumulative':'TestRateCumulative',
    'Percent Tested Positive - Weekly':'PercentTestedPositiveWeekly',
    'Percent Tested Positive - Cumulative':'PercentTestedPositiveCumulative', 
    'Deaths - Weekly':'DeathsWeekly',
    'Deaths - Cumulative':'DeathsCumulative',
    'Death Rate - Weekly':'DeathRateWeekly', 
    'Death Rate - Cumulative':'DeathRateCumulative',
    'Population':'Population', 
    'Row ID':'RowID',
    'x':'x', 
    'y':'y'      
    })  
    covid19_df=Covid_19_MultiIdx_weekZip.drop(['ZIP Code Location'], axis=1).copy()    
    Covid_19_MultiIdx_weekZip["geometry"]=Covid_19_MultiIdx_weekZip.apply(lambda row,x:shapely.wkt.loads(row[x]) if isinstance(row[x],str) else float('nan'),x='ZIP Code Location',axis=1)
    # print(Covid_19_MultiIdx_weekZip.xs(10,level=0,drop_level=False))
    # print(Covid_19_MultiIdx_weekZip.xs('60602',level=1,drop_level=False))
    
    Covid_19_MultiIdx_weekZip["x"]=Covid_19_MultiIdx_weekZip.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
    Covid_19_MultiIdx_weekZip["y"]=Covid_19_MultiIdx_weekZip.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)
    # print(Covid_19_MultiIdx_weekZip.head())
    # print(Covid_19_MultiIdx_weekZip.dtypes)
    # print(Covid_19_MultiIdx_weekZip.index.values)
    # print(Covid_19_MultiIdx_weekZip.index)
    zip_codes= gpd.read_file(dataFpDic["zip_codes"])
    # print("-"*50)
    # print(zip_codes.columns)
    # print(zip_codes.head())
    covid19_df_joinColumn=covid19_df.reset_index(level=['Week Number','ZIP Code']).rename(columns={'ZIP Code':'zip'})
    covid19_zip=zip_codes.merge(covid19_df_joinColumn,on='zip')
        
    return Covid_19_MultiIdx_weekZip,covid19_df,covid19_zip,covid19_df_byZip

# As provided in the answer by Divakar  https://stackoverflow.com/questions/41190852/most-efficient-way-to-forward-fill-nan-values-in-numpy-array
def ffill(arr):
    mask = np.isnan(arr)
    idx = np.where(~mask, np.arange(mask.shape[1]), 0)
    np.maximum.accumulate(idx, axis=1, out=idx)
    out = arr[np.arange(idx.shape[0])[:,None], idx]
    return out

# As provided in the answer by cchwala  
def bfill(arr):
    mask = np.isnan(arr)
    idx = np.where(~mask, np.arange(mask.shape[1]), mask.shape[1] - 1)
    idx = np.minimum.accumulate(idx[:, ::-1], axis=1)[:, ::-1]
    out = arr[np.arange(idx.shape[0])[:,None], idx]
    return out

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


#absolute dynamics and relative dynamics
def absoluteRelative_dynamics(data_df):
    print("-"*50)
    print(data_df.shape,data_df.columns)
    
    # data_df['CasesWeekly']=data_df['CasesWeekly'].fillna(method='ffill').fillna(method='bfill')
    # print(data_df.columns)
    #absolute
    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeksUnique=np.unique(weeks)
    print(weeksUnique)
    zipNum=data_df.index.get_level_values('ZIP Code')
    zipNumUnique=np.unique(zipNum)
    # print(zipNumUnique)
    valArray=data_df['CasesWeekly'].groupby(level='Week Number').apply(lambda x:x.values.tolist()).values
    valArray=np.array([np.array(i) for i in valArray])
    print(valArray.shape)
    # print(valArray[0])
    
    orderweek_0=np.argsort(valArray[0])
    # print(orderweek_0)
    orderweek_tailender=np.argsort(valArray[-1])
    # print(orderweek_tailender)
    print("+"*50)
    val_0=zipNumUnique[orderweek_0[::-1]]
    val_tailender=zipNumUnique[orderweek_tailender[::-1]]
    # print(val_tailender)
    first_last = np.vstack((val_0,val_tailender))

    plt.figure()
    rcParams['figure.figsize'] = 15,10
    
    plt.plot(weeksUnique,valArray)
    for i in range(len(zipNumUnique)):
        plt.text(9.7,630-(i*11), first_last[0][i],fontsize=9)
        plt.text(19.5,630-(i*11), first_last[1][i],fontsize=9)
    
    # plt.xlim((weeksUnique[0], weeksUnique[-1]))
    # plt.ylim((0, 54530))
    plt.ylabel(r"$y_{i,t}$",fontsize=14)
    plt.xlabel('weeks',fontsize=12)
    plt.title('Absolute Dynamics',fontsize=18)

    #relative
    # print(valArray)
    #pandas fill nan be waived
    # data_df_byZip=data_df.reorder_levels(['ZIP Code','Week Number']).sort_index()
    # data_df_byZip['CasesWeekly']=data_df_byZip['CasesWeekly'].fillna(method='ffill').fillna(method='bfill')
    # data_df_fillNan=data_df_byZip.reorder_levels(['Week Number','ZIP Code']).sort_index()
    # valArray_fillNan=data_df_fillNan['CasesWeekly'].groupby(level='Week Number').apply(lambda x:x.values.tolist()).values
    # valArray_fillNan=np.array([np.array(i) for i in valArray_fillNan])
    
    #numpy fill nan
    # print(valArray.T)
    valArray_fillNan=bfill(valArray.T).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0
    print("$"*50)
    print(valArray_fillNan.shape)

    # print(data_df_byZip)
    # print(valArray_fillNan)
    rvalArray=(valArray_fillNan.T / valArray_fillNan.mean(axis=1)).T
    print(rvalArray.shape)
    
    r_orderweek_0=np.argsort(rvalArray[0])
    # print(orderweek_0)
    r_orderweek_tailender=np.argsort(rvalArray[-1])
    # print(orderweek_tailender)
    print("+"*50)
    r_val_0=zipNumUnique[r_orderweek_0[::-1]]
    r_val_tailender=zipNumUnique[r_orderweek_tailender[::-1]]
    # print(val_tailender)
    r_first_last = np.vstack((r_val_0,r_val_tailender))

    plt.figure()
    rcParams['figure.figsize'] = 15,10
    
    plt.plot(weeksUnique,rvalArray)
    for i in range(len(zipNumUnique)):
        plt.text(8.7,5.7-(i*0.1), r_first_last[0][i],fontsize=9)
        plt.text(19.5,5.7-(i*0.1), r_first_last[1][i],fontsize=9)
    
    # plt.xlim((weeksUnique[0], weeksUnique[-1]))
    # plt.ylim((0, 54530))
    plt.ylabel(r"$y_{i,t}$",fontsize=14)
    plt.xlabel('weeks',fontsize=12)
    plt.title('Relative Dynamics',fontsize=18)    


def showGpd_zipPolygon(dataFpDic):
    zip_codes= gpd.read_file(dataFpDic["zip_codes"])
    print("-"*50)
    print(zip_codes.columns)
    print(zip_codes.head())
     # base = world.plot(color='white', figsize=(20,10))
    plt.rcParams.update({'font.size': 10})
    ax=zip_codes.plot(figsize=(20,20))
    plt.title("zip_codes")
    zip_codes.apply(lambda x: ax.annotate(s=x.zip, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)


#Discrete Markov Chains (DMC)
def DMC(data_df):
    print("-"*50)
    print(data_df.shape,data_df.columns)        
    valArray=data_df['CasesWeekly'].groupby(level='Week Number').apply(lambda x:x.values.tolist()).values
    valArray=np.array([np.array(i) for i in valArray])
    # valArray=np.array([np.array(i) for i in valArray])
    # print(valArray.shape)
    valArray_fillNan=bfill(valArray.T).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0
    # print(valArray_fillNan.shape)
    q5 = np.array([mc.Quantiles(y,k=5).yb for y in valArray_fillNan]).transpose()
    # print(q5.shape)
    # print(q5)    
    m5 = giddy.markov.Markov(q5)
    print('DMC-transitions:\n',m5.transitions)
    print('DMC-p:\n',m5.p)
    print('DMC-steady state\n',m5.steady_state)
    print('DMC-fmpt',giddy.ergodic.fmpt(m5.p))

#Regional context and Moran’s Is-01-quantiles
#Regional context and Moran’s Is-02-Moran's Is
def quantiles_MoranI_Plot(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    # print(data_df_zipGPD.head())
    # print(data_df_zipGPD.describe())
    print(data_df_zipGPD.columns)

    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)

    nrows=2
    ncols=math.ceil(len(weeks)/nrows)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols,figsize = (30,15))
    for i in range(nrows):
        for j in range(ncols):
            # print("_"*50)
            # print(str(weeks[i*ncols+j]))
            try:
                plt.rcParams.update({'font.size': 5})
                ax = axes[i,j]
                data_df_zipGPD.plot(ax=ax, column=weeks[i*ncols+j], cmap='OrRd', scheme='quantiles', legend=True,)
                ax.set_title('daily cases %s Quintiles'%weeks[i*ncols+j])
                ax.axis('off')
                leg = ax.get_legend()
                leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
                data_df_zipGPD.apply(lambda x: ax.annotate(s=x.zip, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
                leg = ax.get_legend()
                leg.set_bbox_to_anchor((0., 0., 0.2, 0.2))
            except:
                pass
    plt.tight_layout()
    
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0
    # print(valArray_fillNan,valArray_fillNan.shape)

    mits=[Moran(cs,W) for cs in valArray_fillNan]
    res = np.array([(mi.I, mi.EI, mi.seI_norm, mi.sim[974]) for mi in mits])
    # print(res)
    
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize = (10,5) )
    ax.plot(weeks, res[:,0], label='Moran\'s I')
    #plot(years, res[:,1], label='E[I]')
    ax.plot(weeks, res[:,1]+1.96*res[:,2], label='Upper bound',linestyle='dashed')
    ax.plot(weeks, res[:,1]-1.96*res[:,2], label='Lower bound',linestyle='dashed')
    ax.set_title("Global spatial autocorrelation for Covid-19-cases",fontdict={'fontsize':15})
    # ax.set_xlim(weeks)
    # plt.axhline(y=0, color='gray', linestyle='--',)
    ax.legend()
    #Moran's I >0表示空间正相关性，其值越大，空间相关性越明显，Moran's I <0表示空间负相关性，其值越小，空间差异越大，否则，Moran's I = 0，空间呈随机性。
    
#spatial markov about the explanation ref:蒲英霞,马荣华,葛莹,黄杏元.基于空间马尔可夫链的江苏区域趋同时空演变[J]. 地理学报.2005-09-23	
#ref:https://pysal.org/pysal/generated/pysal.explore.giddy.markov.Spatial_Markov.html
def spatialMarkov(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    # print(data_df_zipGPD.head())
    # print(data_df_zipGPD.describe())
    # print(data_df_zipGPD.columns)

    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)
    # print()
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0
    # print(valArray_fillNan,valArray_fillNan.shape)
    rvalArray= (valArray_fillNan.T / valArray_fillNan.mean(axis=1)).T
    sm = giddy.markov.Spatial_Markov(rvalArray.T, W, fixed = True, k = 5,m=5) # spatial_markov instance o
    print("p:\n",sm.p)
    print("\nsummary:\n") #似然比(likelihood ratio, LR)
    print(sm.summary())
    print("DOF:",sm.dof_hom)
    samples = stats.chi2.rvs(size=10000, df=sm.dof_hom)
    plt.figure()
    sns.distplot(samples)
    plt.title('$\chi^2$,df=%s'%sm.dof_hom)
    plt.show()
    
    plt.figure()
    fig, axes = plt.subplots(2,3,figsize = (15,10))
    for i in range(2):
        for j in range(3):
            ax = axes[i,j]
            if i==0 and j==0:
                p_temp = sm.p
                im = ax.imshow(p_temp,cmap = "coolwarm",vmin=0, vmax=1)
                ax.set_title("Pooled",fontsize=18)
            else:
                p_temp = sm.P[i*3+j-1]
                im = ax.imshow(p_temp,cmap = "coolwarm",vmin=0, vmax=1)
                ax.set_title("Spatial Lag %d"%(i*3+j),fontsize=18)
            for x in range(len(p_temp)):
                for y in range(len(p_temp)):
                    text = ax.text(y, x, round(p_temp[x, y], 2),
                                   ha="center", va="center", color="w")
    
    fig.subplots_adjust(right=0.92)
    cbar_ax = fig.add_axes([0.95, 0.228, 0.01, 0.5])
    fig.colorbar(im, cax=cbar_ax)
    #fig.savefig('spatial_markov_us.png', dpi = 300)

    print("S:\n",sm.S)
    print("F:\n",sm.F)
    print("\nmarkov homogeneity test:\n")
    print(giddy.markov.Homogeneity_Results(sm.T).summary())    
    print("kullback:\n",giddy.markov.kullback(sm.T))
    print("cutoffs:\n",sm.cutoffs)
    print("lag_cutoffs:\n",sm.lag_cutoffs)

#LISA Markov
def LISAMarkov(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0   
    print(valArray_fillNan.shape)    
    
    lm = giddy.markov.LISA_Markov(valArray_fillNan.T, W)
    print("LISA transitions:]\n",lm.transitions)
    print("estimated transition probability matrix:\n",lm.p)
    print("steady state distribution of the chain:\n",lm.steady_state)
    print("the first mean passage time for the LISAs:\n",giddy.ergodic.fmpt(lm.p))
    print("chi-2:\n",lm.chi_2)

#full rank markov: Full Rank Markov in which ranks are considered as Markov states rather than quantiles or other discretized classes. This is one way to avoid issues associated with discretization.
def fullGeoRankMarkov(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    # print(data_df_zipGPD)
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray)
    valArray_fillNan[np.isnan(valArray_fillNan)]=0   
    # print(valArray_fillNan,valArray_fillNan.shape)  
    
    #Full Rank Markov
    m = FullRank_Markov(valArray_fillNan)
    print("ranks\n",m.ranks)
    print("transitions:\n",m.transitions)
    print("transition probability:\n",m.p)
    print("full rank first mean passage times:\n",m.fmpt)
    print("sojourn time:\n",m.sojourn_time)
    df_fullrank = pd.DataFrame(np.c_[m.p.diagonal(),m.sojourn_time], columns=["Staying Probability","Sojourn Time"], index = np.arange(m.p.shape[0])+1)
    print(df_fullrank.head())
    df_fullrank.plot(subplots=True, layout=(1,2), figsize=(15,5))
    
    plt.figure(figsize=(20,10)) 
    fmpt=m.fmpt.flatten()
    fmpt[np.isinf(fmpt)]=400
    sns.distplot(fmpt,kde=False)

    #Geographic Rank Markov
    gm = GeoRank_Markov(valArray_fillNan)
    print("gm-transitions:\n",gm.transitions)
    print("gm-p:\n",gm.p)
    print("gm-sojourn time:\n",gm.sojourn_time)
    print("gm-fmpt:\n",gm.fmpt)
    data_df_zipGPD["geo_sojourn_time"] = gm.sojourn_time
    i = 0
    for state in data_df_zipGPD["zip"]:
        data_df_zipGPD["geo_fmpt_to_" + state] = gm.fmpt[:,i]
        data_df_zipGPD["geo_fmpt_from_" + state] = gm.fmpt[i,:]
        i = i + 1
    # print(data_df_zipGPD.head(),data_df_zipGPD.columns.tolist())
    

    fig, axes = plt.subplots(nrows=2, ncols=2,figsize = (15*2,7*2))
    target_states = ["60655","60603"]
    directions = ["from","to"]
    for i, direction in enumerate(directions):
        for j, target in enumerate(target_states):
            ax = axes[i,j]
            col = direction+"_"+target
            data_df_zipGPD.plot(ax=ax,column = "geo_fmpt_"+ col,cmap='OrRd',scheme='quantiles', legend=True)
            ax.set_title("First Mean Passage Time "+direction+" "+target)
            ax.axis('off')
            leg = ax.get_legend()
            leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
    plt.tight_layout()


    # plt.figure()
    fig, axes = plt.subplots(nrows=1, ncols=2,figsize = (15,7))
    schemes = ["Quantiles",] #"Equal_Interval"
    for i, scheme in enumerate(schemes):
        ax = axes[i]
        data_df_zipGPD.plot(ax=ax,column = "geo_sojourn_time",cmap='OrRd',scheme=scheme, legend=True)
        ax.set_title("Rank Sojourn Time ("+scheme+")")
        ax.axis('off')
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
    plt.tight_layout()

#mobility https://giddy.readthedocs.io/en/latest/notebooks/MobilityMeasures.html
def mobilityOf_Values(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    # print(data_df_zipGPD)
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0   
    # print(valArray_fillNan,valArray_fillNan.shape)  
    
    q5 = np.array([mc.Quantiles(y).yb for y in valArray_fillNan]).transpose() #each row represents an state's income time series 1929-2010
    m= markov.Markov(q5)
    print(m.p)
    #1. Shorrock1’s mobility measure
    print("Shorrock1’s mobility measure:",mobility.markov_mobility(m.p, measure="P"))
    #2. Shorroks2’s mobility measure
    print("Shorroks2’s mobility measure:",mobility.markov_mobility(m.p, measure="D"))
    #3. Sommers and Conlisk’s mobility measure
    print("Sommers and Conlisk’s mobility measure:",mobility.markov_mobility(m.p, measure = "L2"))
    #4. Bartholomew1’s mobility measure
    pi = np.array([0.1,0.2,0.2,0.4,0.1])
    print("Bartholomew1’s mobility measure:",mobility.markov_mobility(m.p, measure = "B1", ini=pi))
    #5. Bartholomew2’s mobility measure    
    pi = np.array([0.1,0.2,0.2,0.4,0.1])
    print("Bartholomew2’s mobility measure:",mobility.markov_mobility(m.p, measure = "B2", ini=pi))

    # all of these mobility measures take values on [0,1]. 0 means immobility and 1 perfect mobility. 

#Directional Analysis of Dynamic LISAs
def dirAnalyofDynLISAs(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    # print(data_df_zipGPD)
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0  
    # print(valArray_fillNan,valArray_fillNan.shape)  
    
    rvalArray=(valArray_fillNan.T / valArray_fillNan.mean(axis=1))
    # print(rvalArray.shape)    
    Y= rvalArray[:, [0, -1]]
    # print(Y.shape)
    np.random.seed(100)
    r4 = Rose(Y, W, k=4)
    plt.figure()
    
    r4.plot() #plt.scatter(Y[:,0],r4.lag[:,0],)  the location of each point is the coordinates of starting relative income as x and the spatial lag of starting relative value as y
    r4.plot(Y[:,0]) # condition on starting relative income
    r4.plot(attribute=r4.lag[:,0]) # condition on the spatial lag of starting relative income
    r4.plot_vectors() # lisa vectors  r4.plot_vectors(arrows=False)  r4.plot_origin() # origin standardized
    # did not understand the following part
    print("cuts:",r4.cuts)
    print("counts:",r4.counts)
    np.random.seed(1234)
    r4.permute(permutations=999)
    print("p:",r4.p)
    r4.permute(alternative='positive', permutations=999)
    print("alter-positive:",r4.p)
    print("expected-positive:",r4.expected_perm)
    r4.permute(alternative='negative', permutations=999)
    print("alter-negative:",r4.p)
    
    # help(r4)
    # print(help(r4.plot()))

#population quantile
def populationNeighborhood(populationPolygon_P,zipPolygon,populationRaster_P):
    population=gpd.read_file(populationPolygon_P)
    print("population crs:",population.crs)
    print(population.columns)
    zip_codes= gpd.read_file(zipPolygon)
    print("zip codes crs:",zip_codes.crs)    
    if population.crs["init"]!=zip_codes.crs["init"]:
        zip_codes=zip_codes.to_crs(population.crs)
    else:print("population crs is the same as zip_codes crs")
    print("population crs:",population.crs)
    print("zip codes crs:",zip_codes.crs)
    print(zip_codes.columns)
    print("_"*50)
    # showVector(population,'TOTAL_POPU')
    # showVector(zip_codes,'shape_area')

    zs = zonal_stats(zip_codes, populationRaster_P)
    # print(zs)
    zs_df=pd.DataFrame(zs)
    # print(zs_df.head())
    # print(zip_codes.head())
    zs_zip=zip_codes.merge(zs_df,left_on=zip_codes.index, right_on=zs_df.index)    
    # showVector(zs_zip,'mean')
    zs_zip['quantile']=pd.qcut(zs_zip['mean'],5,labels=False)
    # print(zs_zip.head(),zs_zip.columns)
    
    plt.figure()
    plt.rcParams.update({'font.size': 30})
    ax=zs_zip.plot(column="quantile",figsize=(20,20))
    plt.title("pop_quantile-5")
    # ax=showVector(zs_zip,'quantile')
    zs_zip.apply(lambda x: ax.annotate(s=x["quantile"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    # print(zs_zip["quantile"])
    
    zs_zip_dissolve=zs_zip.dissolve(by='quantile',aggfunc='mean') #https://geopandas.org/aggregation_with_dissolve.html
    # print(zs_zip_dissolve.iloc[0:2])
    # zs_zip_dissolve.iloc[0:2].plot(column="mean",figsize=(20,20))
    zs_zip_explode=zs_zip_dissolve.explode()
    zs_zip_explode["idx"]=zs_zip_explode.index

    zip_codes_Scale=zip_codes.scale(xfact=0.5, yfact=0.5, zfact=1.0, origin='center')
    zip_codes_drop=zip_codes.drop(["geometry"],axis=1)
    # print(zip_codes_Scale)
    zip_codes_drop['geometry']=zip_codes_Scale
    # print(zip_codes_drop)
    # print(zip_codes_Scale.)
    # zip_codes_drop.plot()

    zs_zip_overlay=gpd.overlay(zip_codes_drop,zs_zip_explode, how='intersection',make_valid=True)
    zs_merge_drop=zs_zip_overlay.drop(["geometry"],axis=1)
    zs_merge=zs_merge_drop.merge(zs_zip[["zip","geometry"]],on="zip")
    # zs_merge.loc[zs_merge.idx==(2, 3)].plot()
    
    plt.figure()
    plt.rcParams.update({'font.size': 20})
    ax=zs_merge.plot(column="idx",figsize=(20,20))
    plt.title("zip_merge by quantile")
    zs_merge.apply(lambda x: ax.annotate(s=x["idx"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    
    return zs_merge
    
#kendall's tao
def kendallTau(data_df,quantilePolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= quantilePolygon
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    # print(data_df_zipGPD)
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    weeks=np.unique(weeks)
    valArray=data_df_zipGPD[weeks].to_numpy()
    valArray_fillNan=bfill(valArray).T
    valArray_fillNan[np.isnan(valArray_fillNan)]=0

    data_df_zipGPD_bfill=data_df_zipGPD.fillna(method='bfill',axis=1)    
    data_df_zipGPD_bfill[weeks]=data_df_zipGPD_bfill[weeks].fillna(0)
    print(data_df_zipGPD_bfill.isna().sum())
    data_df_zipGPD_bfill["idxPlus"]=data_df_zipGPD_bfill["idx"].apply(lambda x: str(x[0])+"-"+str(x[1]))
    
    plt.figure()
    plt.rcParams.update({'font.size': 30})
    ax=data_df_zipGPD_bfill.plot(column="idxPlus",figsize=(20,20))
    plt.title("pop_quantile-5")
    # ax=showVector(zs_zip,'quantile')
    data_df_zipGPD_bfill.apply(lambda x: ax.annotate(s=x["idxPlus"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
   
    #Classic Kendall’s tau
    tau = giddy.rank.Tau(data_df_zipGPD_bfill[10],data_df_zipGPD_bfill[19])
    print("_"*50,"Classic Kendall’s tau")
    #−1≤τ≤1 . Smaller τ indicates higher exchange mobility
    print("tau.concordant:",tau.concordant)
    print("tau.discordant:",tau.discordant)
    print("tau.tau:",tau.tau)
    print("tau.tau_p:",tau.tau_p)


    #Spatial Kendall’s tau
    w_quantile=block_weights(data_df_zipGPD_bfill["idxPlus"])
    np.random.seed(12345)
    tau_w = giddy.rank.SpatialTau(data_df_zipGPD_bfill[10],data_df_zipGPD_bfill[19],w_quantile,999)
    print("_"*50,"Spatial Kendall’s tau")
    print("tau_w.concordant:",tau_w.concordant)
    print("tau_w.concordant_spatial:",tau_w.concordant_spatial)
    print("tau_w.discordant:",tau_w.discordant)
    print("tau_w.discordant_spatial:",tau_w.discordant_spatial)
    print("tau_w.tau_spatial:",tau_w.tau_spatial)
    print("tau_w.tau_spatial_psim:",tau_w.tau_spatial_psim)

    #Inter- and Intra-regional decomposition of Kendall’s tau    
    np.random.seed(12345)
    tau_w = giddy.rank.Tau_Regional(data_df_zipGPD_bfill[10],data_df_zipGPD_bfill[19],data_df_zipGPD_bfill["idxPlus"],999)
    print("_"*50,"Inter- and Intra-regional decomposition of Kendall’s tau")
    print("tau_w.tau_reg:",tau_w.tau_reg)
    print("tau_w.tau_reg_pvalues:",tau_w.tau_reg_pvalues)
    print("tau_w.tau_reg * (tau_w.tau_reg_pvalues<0.05):",tau_w.tau_reg * (tau_w.tau_reg_pvalues<0.05))

    #Local Kendall’s tau
    tau_r = giddy.rank.Tau_Local(data_df_zipGPD_bfill[10],data_df_zipGPD_bfill[19])
    LocalKendallTau=pd.DataFrame({"STATE_NAME":data_df_zipGPD_bfill['zip'].tolist(),"$\\tau_r$":tau_r.tau_local}).head()
    print("Local Kendall’s tau:",LocalKendallTau)

    #Local indicator of mobility association-LIMA
    #1-Neighbor set LIMA    
    data_df_zipGPD_bfill_dropZero=data_df_zipGPD_bfill.loc[~(data_df_zipGPD_bfill[weeks]==0).all(axis=1)]
    # w_quantile_dropZero=block_weights(data_df_zipGPD_bfill_dropZero["idxPlus"]) #prompt mistake divide by zero
    W_=ps.lib.weights.Queen(data_df_zipGPD_bfill_dropZero.geometry)
    W_.transform = 'R'
    print(data_df_zipGPD_bfill.shape,data_df_zipGPD_bfill_dropZero.shape)
    tau_wr = giddy.rank.Tau_Local_Neighbor(data_df_zipGPD_bfill_dropZero[10],data_df_zipGPD_bfill_dropZero[19],W_,999)
    # print("tau_wr.tau_ln:",tau_wr.tau_ln)
    
    plt.figure()
    data_df_zipGPD_bfill_dropZero["tau_ln"] =tau_wr.tau_ln
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize = (20,20))
    ln_map = data_df_zipGPD_bfill_dropZero.plot(ax=ax, column="tau_ln", cmap='coolwarm', scheme='equal_interval',legend=True)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
    ln_map.set_title("Neighbor set LIMA for Covid-19",fontdict={"fontsize":20})
    ax.set_axis_off()
    
    print("tau_wr.tau_ln_pvalues:",tau_wr.tau_ln_pvalues)
    sig_wr = tau_wr.tau_ln * (tau_wr.tau_ln_pvalues<0.05)
    print("sig_wr :",sig_wr)
    
    plt.figure()
    data_df_zipGPD_bfill_dropZero["sig_wr"] =sig_wr
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize = (20,20))
    data_df_zipGPD_bfill_dropZero[data_df_zipGPD_bfill_dropZero["sig_wr"] == 0].plot(ax=ax, color='white',edgecolor='black')
    sig_ln_map =data_df_zipGPD_bfill_dropZero[data_df_zipGPD_bfill_dropZero["sig_wr"] != 0].plot(ax=ax,column="sig_wr",cmap='coolwarm',scheme='equal_interval',legend=True)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
    sig_ln_map.set_title("Significant Neighbor set LIMA for Covid=-19",fontdict={"fontsize":20})
    ax.set_axis_off()
            
    #Neighborhood set LIMA
    tau_wwr = giddy.rank.Tau_Local_Neighborhood(data_df_zipGPD_bfill_dropZero[10],data_df_zipGPD_bfill_dropZero[19],W_,999)
    print("tau_wwr.tau_lnhood:",tau_wwr.tau_lnhood)
    
    plt.figure()
    data_df_zipGPD_bfill_dropZero["tau_lnhood"] =tau_wwr.tau_lnhood
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize = (20,20))
    ln_map = data_df_zipGPD_bfill_dropZero.plot(ax=ax, column="tau_lnhood", cmap='coolwarm', scheme='equal_interval',legend=True)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
    ln_map.set_title("Neighborhood set LIMA for Covid-19",fontdict={"fontsize":20})
    ax.set_axis_off()
            
    print("tau_wwr.tau_lnhood_pvalues:",tau_wwr.tau_lnhood_pvalues)   
    sig_lnhood = tau_wwr.tau_lnhood * (tau_wwr.tau_lnhood_pvalues<0.05)
    
    plt.figure()
    data_df_zipGPD_bfill_dropZero["sig_lnhood"] =sig_lnhood
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize = (20,20))
    data_df_zipGPD_bfill_dropZero[data_df_zipGPD_bfill_dropZero["sig_lnhood"] == 0].plot(ax=ax, color='white',edgecolor='black')
    sig_ln_map = data_df_zipGPD_bfill_dropZero[data_df_zipGPD_bfill_dropZero["sig_lnhood"] != 0].plot(ax=ax,column="sig_lnhood",categorical=True,legend=True)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
    sig_ln_map.set_title("Significant Neighborhood set LIMA for U.S. states 1929-2009",fontdict={"fontsize":20})
    ax.set_axis_off()    



if __name__=="__main__": 
    dataRoot=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\Chicago Health_spatioTemporalAnalysis\data"
    dataFpDic={
            "Covid-19_CasesByZipCode":os.path.join(dataRoot,r"COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv"),
            
            "zip_codes":os.path.join(dataRoot,r"Boundaries - ZIP Codes\geo_export_1a9a53ff-8090-4a1a-85ce-ac92bd036028.shp"),
       
            "populationCensus":os.path.join(dataRoot,r"populationCensus_Project.shp"),
            "populationCensusTif":os.path.join(dataRoot,r"population.tif"),
       }
    # np.set_printoptions(threshold=sys.maxsize) #threshold=False print full array, without trucation
    # np.set_printoptions(threshold=False)
    
    # main()
    '''basis'''
    covid19_gpd,covid19_df,covid19_zip,covid19_df_byZip=covid_19_csv2gpd(dataFpDic) 
    population_quantile=populationNeighborhood(dataFpDic["populationCensus"],dataFpDic["zip_codes"],dataFpDic["populationCensusTif"])

    
    '''A-GeospatIal Distribution Dynamics (GIDDY)'''
    #https://giddy.readthedocs.io/en/latest/
    #01-absolute dynamics and relative dynamics
    # absoluteRelative_dynamics(covid19_df[['CasesWeekly','WeekStart','zipBak']])    
    #02-show
    # showGpd_zipPolygon(dataFpDic)
    #03-Discrete Markov Chains (DMC)
    # DMC(covid19_df[['CasesWeekly','WeekStart','zipBak']])    
    #04-Regional context and Moran’s Is
    # quantiles_MoranI_Plot(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])    
    #05-spatial markov
    # spatialMarkov(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])    
    #06-LISA markov
    # LISAMarkov(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])     
    #07-full rank markov/Geographic Rank Markov
    # fullGeoRankMarkov(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])    
    #08-mobility of values
    # mobilityOf_Values(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])
    #09-directional analysis of dynamic LISAs  
    #https://giddy.readthedocs.io/en/latest/notebooks/directional.html
    # dirAnalyofDynLISAs(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])
    #10-kendall's tao https://giddy.readthedocs.io/en/latest/notebooks/RankbasedMethods.html
    # kendallTau(covid19_df[['CasesWeekly','WeekStart','zipBak']],population_quantile[['zip','idx', 'geometry']])
