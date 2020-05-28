# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:07:04 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
ref:http://pysal.org/notebooks/explore/segregation/intro.html
"""
import os,shapely,inequality,segregation
import pandas as pd
import numpy as np
from shapely.geometry import Point,Polygon
import shapely.wkt
import geopandas as gpd
import matplotlib.pylab as plt
from rasterstats import zonal_stats

import pysal as ps
import libpysal as lps

from segregation.decomposition import DecomposeSegregation
from segregation.inference import SingleValueTest, TwoValueTest
from segregation.spatial import RelativeConcentration,RelativeCentralization,SpatialDissim

from segregation.local import MultiLocationQuotient, MultiLocalDiversity, MultiLocalEntropy, MultiLocalSimpsonInteraction, MultiLocalSimpsonConcentration, LocalRelativeCentralization

from libpysal.weights.contiguity import Queen
from libpysal.weights import block_weights,Queen, Rook, Kernel
from splot.libpysal import plot_spatial_weights
from segregation.aspatial import MultiInformationTheory
from segregation.spatial import SpatialInformationTheory
from segregation.network import get_osm_network
from segregation.spatial import compute_segregation_profile
from pandana.network import Network

import contextily as ctx

import warnings                                  # 勿扰模式 do not disturbe` mode
warnings.filterwarnings('ignore')
from matplotlib.pylab import style
style.use('ggplot')   
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 



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
   
    
#gini
def inequlityGini(data_df,quantilePolygon):
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
    data_df_zipGPD_bfill["idxPlus"]=data_df_zipGPD_bfill["idx"].apply(lambda x: str(x[0])+"-"+str(x[1]))

    gdf=data_df_zipGPD_bfill
    
    plt.figure()
    plt.rcParams.update({'font.size': 10})
    ax = gdf.plot(column=19,k=5,scheme='Quantiles',legend=True,figsize=(12*4,3*4))
    ax.set_axis_off()
    plt.title("casesWeekly-19 quantiles-5,19 week")
    gdf.apply(lambda x: ax.annotate(s=x["zip"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    plt.savefig('19Case weekyly.png')
    print("*"*50)
    print(gdf.columns)

    #01-gini
    gini_19 = inequality.gini.Gini(gdf[19])
    print("gini_19-g:",gini_19.g)
    
    ginis = [ inequality.gini.Gini(gdf[week]).g for week in weeks]
    print("ginis:",ginis)

    #02-regimes
    regimes = gdf['idxPlus'] 
    w = lps.weights.block_weights(regimes) #values as string
    
    plt.figure()
    plt.rcParams.update({'font.size': 10,'text.color':'grey'})
    ax = gdf.plot(column="idxPlus", categorical=True,legend=True,figsize=(12*3,3*3),cmap='cubehelix') #'cubehelix', 'Greens',cmap='winter'
    plt.title("casesWeekly-19 regimes,19 week")
    gdf.apply(lambda x: ax.annotate(s=x["idxPlus"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    ax.set_axis_off()
    plt.savefig('regions.png')

    #03-gini spatial
    np.random.seed(12345)
    gs = inequality.gini.Gini_Spatial(gdf[19],w)    
    print("p_sim:",gs.p_sim)

    gs_all = [ inequality.gini.Gini_Spatial(gdf[week], w) for week in weeks]
    p_values = [gs.p_sim for gs in gs_all]
    print("p_values:",p_values)
    wgs = [gs.wcg_share for gs in gs_all]
    print("wgs:",wgs)
    bgs = [ 1 - wg for wg in wgs]
    print("bgs:",bgs)
    
    fig, ax1 = plt.subplots()
    t = weeks
    s1 = ginis
    ax1.plot(t, s1, 'b-')
    ax1.set_xlabel('weeks')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Gini', color='b')
    ax1.tick_params('y', colors='b')
    
    ax2 = ax1.twinx()
    s2 = bgs
    ax2.plot(t, s2, 'r-.')
    ax2.set_ylabel('Spatial Inequality Share', color='r')
    ax2.tick_params('y', colors='r')
    
    fig.tight_layout()    
    plt.savefig('share.png')


#segregation module for aspatial indexs
def segregationMisc(data_df,zipPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    caseWeekly_columnsReplace_dic={key:"case_"+str(key) for key in caseWeekly_unstack.columns}
    caseWeekly_unstack.rename(columns=caseWeekly_columnsReplace_dic,inplace=True)
    
    testWeekly_unstack=data_df['TestsWeekly'].unstack(level=0)
    testWeekly_columnsReplace_dic={key:"test_"+str(key) for key in testWeekly_unstack.columns}
    testWeekly_unstack.rename(columns=testWeekly_columnsReplace_dic,inplace=True)
    
    zip_codes= gpd.read_file(zipPolygon)
    data_df_zipGPD=zip_codes.merge(caseWeekly_unstack,left_on='zip', right_on=caseWeekly_unstack.index)
    data_df_zipGPD=data_df_zipGPD.merge(testWeekly_unstack,left_on='zip', right_on=testWeekly_unstack.index)
    # print(data_df_zipGPD)
    W=ps.lib.weights.Queen(data_df_zipGPD.geometry)
    W.transform = 'R'
    
    # weeks=idx_weekNumber=data_df.index.get_level_values('Week Number')
    # weeks=np.unique(weeks)
    columnsName=list(caseWeekly_columnsReplace_dic.values())+list(testWeekly_columnsReplace_dic.values())
    caseColumnsaName=list(caseWeekly_columnsReplace_dic.values())
    testColumnsName=list(testWeekly_columnsReplace_dic.values())
    
    # valArray=data_df_zipGPD[weeks].to_numpy()
    # valArray_fillNan=bfill(valArray).T
    # valArray_fillNan[np.isnan(valArray_fillNan)]=0  
    # # print(valArray_fillNan,valArray_fillNan.shape)  
    data_df_zipGPD_bfill=data_df_zipGPD.fillna(method='bfill',axis='columns')    
    data_df_zipGPD_bfill[columnsName]=data_df_zipGPD_bfill[columnsName].fillna(0)
    data_df_zipGPD_bfill[columnsName]=data_df_zipGPD_bfill[columnsName].astype('int32') #'int32'  float
    
    
    #A-aspatial indexes
    gdf=data_df_zipGPD_bfill[['case_19','test_19','case_15','test_15','geometry']]
    gdf=gdf[~(gdf==0).any(axis=1)]    
    
    #01-Dissimilarity
    from segregation.aspatial import Dissim
    index = Dissim(gdf, 'case_19','test_19')
    # print(type(index))
    print("dissimilarity:",index.statistic)
            
    #02-Gini
    from segregation.aspatial import GiniSeg
    index = GiniSeg(gdf, 'case_19','test_19')
    # type(index)
    print("Gini:",index.statistic)
    
    #03-Entropy
    from segregation.aspatial import Entropy
    index = Entropy(gdf, 'case_19','test_19')
    # type(index)
    print("Entropy:",index.statistic)
    
    #04-Atkinson
    from segregation.aspatial import Atkinson
    index = Atkinson(gdf, 'case_19','test_19', b = 0.5)
    # type(index)
    print("Atkinson:",index.statistic)
            
    
    #05-Concentration Profile
    from segregation.aspatial import ConProf
    index = ConProf(gdf, 'case_19','test_19')
    # type(index)
    print("Concentration Profile:",index.statistic)
    index.plot()
    
    #06-Isolation
    from segregation.aspatial import Isolation
    index = Isolation(gdf, 'case_19','test_19')
    # type(index)
    print("Isolation:",index.statistic)
    
    #07-Exposure
    from segregation.aspatial import Exposure
    index = Exposure(gdf, 'case_19','test_19')
    # type(index)
    print("Exposure:",index.statistic)
    
    #08-Correlation Ratio
    from segregation.aspatial import CorrelationR
    index = CorrelationR(gdf, 'case_19','test_19')
    # type(index)
    print("Correlation Ratio:",index.statistic)
    
    #09-Modified Dissimilarity
    from segregation.aspatial import ModifiedDissim
    index = ModifiedDissim(gdf, 'case_19','test_19', iterations = 500)
    # type(index)   
    print("Modified Dissimilarity:",index.statistic)
    
    #10-Modified Gini 
    from segregation.aspatial import ModifiedGiniSeg
    index = ModifiedGiniSeg(gdf, 'case_19','test_19', iterations = 500)
    # type(index)
    print("Modified Gini :",index.statistic)
    
    # #11-Bias-Corrected Dissimilarity
    # #FloatingPointError: invalid value encountered in true_divide
    # from segregation.aspatial import BiasCorrectedDissim
    # index = BiasCorrectedDissim(gdf, 'case_19','test_19', B = 500)
    # # type(index)
    # print("Bias-Corrected Dissimilarity:",index.statistic)
    
    #12-Density-Corrected Dissimilarity
    from segregation.aspatial import DensityCorrectedDissim
    index = DensityCorrectedDissim(gdf, 'case_19','test_19', xtol = 1e-5)
    # type(index)
    print("Density-Corrected Dissimilarity:",index.statistic)
    
    #13-Minimum-Maximum Index (MM)
    from segregation.aspatial import MinMax
    index = MinMax(gdf, 'case_19','test_19')
    # type(index)
    print("Minimum-Maximum Index (MM):",index.statistic)
    
    
    #B-Decomposition framework of the PySAL segregation module shapley值法 ref:于伟，张鹏._我国高校生均经费支出省际差异的再分析——基于shapley值分解的方法
    gdf["subtotal"]=gdf.case_19+gdf.case_15
    G_19=GiniSeg(gdf, 'case_19','subtotal')
    gdf_15=gdf[gdf.case_15<gdf.test_15]
    G_15=GiniSeg(gdf_15, 'case_15','subtotal')
    print("G19_gini:",G_19.statistic)
    print("G15_gini:",G_15.statistic)
    print("G_19-G_15:",G_19.statistic-G_15.statistic)
    
    # help(DecomposeSegregation)
    #14-Composition Approach (default)
    #Sergio J. Rey, Renan Cortes, and Elijah Knaap.Comparative Spatial Segregation Analytics[J].5.31.2019
    # help(DecomposeSegregation) #Decompose segregation differences into spatial and attribute components.
    #Shapley decomposition 
    DS_composition = DecomposeSegregation(G_15,G_19)
    print("Shapley's Spatial Component of the decomposition:",DS_composition.c_s) #Shapley's Spatial Component of the decomposition
    print("Shapley's Attribute Component of the decomposition:",DS_composition.c_a) #Shapley's Attribute Component of the decomposition
    plt.figure(figsize=(10,10))
    DS_composition.plot(plot_type = 'cdfs')
    # plt.figure(figsize=(50,50))
    DS_composition.plot(plot_type = 'maps')
    
    
    #15-Share Approach ref: Rey, S. et al "Comparative Spatial Segregation Analytics". 
    DS_share = DecomposeSegregation(G_19, G_15, counterfactual_approach = 'share')
    plt.figure(figsize=(10,10))
    DS_share.plot(plot_type = 'cdfs')
    plt.figure()
    DS_share.plot(plot_type = 'maps')

    #16-Dual Composition Approach
    DS_dual = DecomposeSegregation(G_19, G_15, counterfactual_approach = 'dual_composition')
    plt.figure(figsize=(10,10))
    DS_dual.plot(plot_type = 'cdfs')
    plt.figure()
    DS_dual.plot(plot_type = 'maps')
    
    #17-Inspecting a different index: Relative Concentration
    from segregation.spatial import RelativeConcentration
    RCO_19 = RelativeConcentration(gdf, 'case_19','subtotal')
    RCO_15= RelativeConcentration(gdf_15, 'case_15','subtotal')    
    print("RCO_19.statistic - RCO_15.statistic",RCO_19.statistic - RCO_15.statistic)
    RCO_DS_composition = DecomposeSegregation(RCO_19, RCO_15)
    print("RCO_DS_composition.c_s:",RCO_DS_composition.c_s)
    print("RCO_DS_composition.c_a:",RCO_DS_composition.c_a)
    
    
    #C-inference wrappers
    # single value
    #18-dissimilarity
    D= Dissim(gdf, 'case_19','subtotal')
    # print(type(index))
    print("dissimilarity:",D.statistic)
    #evenness
    infer_D_eve = SingleValueTest(D, iterations_under_null = 1000, null_approach = "evenness", two_tailed = True)
    plt.figure()
    infer_D_eve.plot()
    print("infer_D_eve.est_sim.mean:",infer_D_eve.est_sim.mean())
    print("infer_D_eve.p_value:",infer_D_eve.p_value)
    #systematic
    infer_D_sys = SingleValueTest(D, iterations_under_null = 5000, null_approach = "systematic", two_tailed = True)
    plt.figure()
    infer_D_sys.plot()
    
    # print("^"*50)
    #ValueError: 'Some estimates resulted in NaN or infinite values for estimations under null hypothesis.
    #19-relative concentration
    # RCO = RelativeConcentration(gdf, 'case_19','subtotal')
    # RCO=RCO_15
    # print(RCO)
    #permutation
    # infer_RCO_per = SingleValueTest(RCO, iterations_under_null = 1000, null_approach = "permutation", two_tailed = True)
    # plt.figure()
    # infer_RCO_per.plot()
    # print("infer_RCO_per.p_value:",infer_RCO_per.p_value)
    # #even_permutation
    # infer_RCO_eve_per = SingleValueTest(RCO, iterations_under_null = 1000, null_approach = "even_permutation", two_tailed = True)
    # plt.figure()
    # infer_RCO_eve_per.plot()
    
    #20-relative centralization
    #ValueError: It not possible to determine the center distance for, at least, one unit. This is probably due to the magnitude of the number of the centroids. We recommend to reproject the geopandas DataFrame.
    # print(gdf.crs)
    # RCE = RelativeCentralization(gdf.to_crs(communityArea_CRS), 'case_19','test_19')
    # infer_RCE_per = SingleValueTest(RCE, iterations_under_null = 1000, null_approach = "permutation", two_tailed = True)
    # plt.figure()
    # infer_RCE_per.plot()
    
    #D-comparative inference
    #21-compararive dissimilarity
    D_19=Dissim(gdf, 'case_19','subtotal')
    D_15=Dissim(gdf_15, 'case_15','subtotal')
    print("D_19-D_15:",D_19.statistic-D_15.statistic)
    
    compare_D_fit = TwoValueTest(D_19, D_15, iterations_under_null = 1000, null_approach = "random_label")
    plt.figure()
    compare_D_fit.plot()
    print("compare_D_fit.p_value:",compare_D_fit.p_value)
    
    #22-comparative Gini
    G_19=GiniSeg(gdf, 'case_19','subtotal')
    gdf_15=gdf[gdf.case_15<gdf.test_15]
    G_15=GiniSeg(gdf_15, 'case_15','subtotal')    
    compare_G_fit = TwoValueTest(G_19, G_15, iterations_under_null = 1000, null_approach = "random_label")
    plt.figure()
    compare_G_fit.plot()
    
    #23-comparative spatial dissimilarity
    SD_19 = SpatialDissim(gdf, 'case_19','subtotal')
    SD_15 = SpatialDissim(gdf_15, 'case_15','subtotal')
    compare_SD_fit = TwoValueTest(SD_19, SD_15, iterations_under_null = 500, null_approach = "counterfactual_composition")
    plt.figure()
    compare_SD_fit.plot()
    

def publicHealth_csv2gpd(dataFpDic):
    publicHealth=pd.read_csv(dataFpDic["public_healthStatistics"])
    columnsNameDic={'Community Area':'社区', 
                    'Community Area Name':'社区名',
                    'Birth Rate':'出生率',
                    'General Fertility Rate':'一般生育率',
                    'Low Birth Weight':'低出生体重',
                    'Prenatal Care Beginning in First Trimester':'产前3个月护理', 
                    'Preterm Births':'早产',
                    'Teen Birth Rate':'青少年生育率',
                    'Assault (Homicide)':'攻击（杀人）',
                    'Breast cancer in females':'女性乳腺癌',
                    'Cancer (All Sites)':'癌症', 
                    'Colorectal Cancer':'结肠直肠癌',
                    'Diabetes-related':'糖尿病相关',
                    'Firearm-related':'枪支相关',
                    'Infant Mortality Rate':'婴儿死亡率', 
                    'Lung Cancer':'肺癌',
                    'Prostate Cancer in Males':'男性前列腺癌',
                    'Stroke (Cerebrovascular Disease)':'中风(脑血管疾病)',
                    'Childhood Blood Lead Level Screening':'儿童血铅水平检查',
                    'Childhood Lead Poisoning':'儿童铅中毒',
                    'Gonorrhea in Females':'女性淋病', 
                    'Gonorrhea in Males':'男性淋病', 
                    'Tuberculosis':'肺结核',
                    'Below Poverty Level':'贫困水平以下', 
                    'Crowded Housing':'拥挤的住房', 
                    'Dependency':'依赖',
                    'No High School Diploma':'没有高中文凭', 
                    'Per Capita Income':'人均收入',
                    'Unemployment':'失业',
      }

    communityArea=gpd.read_file(dataFpDic['communityArea'])
    communityArea.area_numbe=communityArea.area_numbe.astype('int64')
    publicHealth_communityArea=communityArea.merge(publicHealth,left_on='area_numbe', right_on='Community Area')
    
    showVector(publicHealth_communityArea,'Lung Cancer')
    return publicHealth_communityArea

#local measure
def localMeasure_multigroup(geoDF,populationCensusTif):
    geoDF=geoDF.to_crs(communityArea_CRS)
    plt.figure()
    plt.rcParams.update({'font.size': 10})
    ax=geoDF.plot(column='Lung Cancer',cmap='OrRd',figsize=(15, 15),legend=True,scheme='quantiles') # scheme='quantiles'
    plt.title("lung cancer distribution")
    geoDF.apply(lambda x: ax.annotate(s=x["Community Area Name"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    
    # geoplot.polyplot(geoDF,figsize=(20, 20))
    # pc=gpd.read_file(populationCensus)
    # print(pc.columns)
    # print(pc.crs)
    # pc.to_file(os.path.join(dataRoot,"populationCensus_save.shp"))
    # Feature_to_Raster(os.path.join(dataRoot,"populationCensus_save.shp"), os.path.join(dataRoot,"popuC_1.tif"), 20, field_name=['CENSUS_BLO'], NoData_value=-9999)
    
    geoDF_sample=zonal_stats(geoDF,populationCensusTif,stats="count min mean max median")
    geoDF_sample_df=pd.DataFrame(geoDF_sample)
    geoDF_sample_df.rename(columns={"count":"popuCount", "min":"popuMin", "mean":"popuMean", "max":"popuMax", "median":"popuMedian"},inplace=True)
    geoDF_merge=geoDF.merge(geoDF_sample_df,left_on=geoDF.index, right_on=geoDF_sample_df.index)
    
    groups_list = ['Cancer (All Sites)','Lung Cancer','Tuberculosis','Gonorrhea in Females']
    geoDF_merge[groups_list]=geoDF_merge[groups_list].fillna(0)
    geoDF_merge["sumGroup"]=geoDF_merge[groups_list].sum(axis=1)
    input_df=geoDF_merge
    for i in range(len(groups_list)):
        input_df['comp_' + groups_list[i]] = input_df[groups_list[i]] / input_df["sumGroup"]  #input_df['popuMean']

    
    #A-Local Measures of segregation
    fig, axes = plt.subplots(ncols = 2, nrows = 2, figsize = (17, 10))
    input_df.plot(column = 'comp_' + groups_list[0],cmap = 'OrRd',legend = True, ax = axes[0,0])
    axes[0,0].set_title('Composition of ' + groups_list[0], fontsize = 18)
    axes[0,0].set_xticks([])
    axes[0,0].set_yticks([])
    axes[0,0].set_facecolor('white')
    
    input_df.plot(column = 'comp_' + groups_list[1], cmap = 'OrRd',legend = True, ax = axes[0,1])
    axes[0,1].set_title('Composition of ' + groups_list[1], fontsize = 18)
    axes[0,1].set_xticks([])
    axes[0,1].set_yticks([])
    axes[0,1].set_facecolor('white')
    
    input_df.plot(column = 'comp_' + groups_list[2],cmap = 'OrRd',legend = True, ax = axes[1,0])
    axes[1,0].set_title('Composition of ' + groups_list[2], fontsize = 18)
    axes[1,0].set_xticks([])
    axes[1,0].set_yticks([])
    axes[1,0].set_facecolor('white')
        
    input_df.plot(column = 'comp_' + groups_list[3],cmap = 'OrRd',legend = True, ax = axes[1,1])
    axes[1,1].set_title('Composition of ' + groups_list[3], fontsize = 18)
    axes[1,1].set_xticks([])
    axes[1,1].set_yticks([])
    axes[1,1].set_facecolor('white')   
    
    #B-Location Quotient (LQ)
    index = MultiLocationQuotient(input_df, groups_list)
    # print(index.statistics)
    
    for i in range(len(groups_list)):
        input_df['LQ_' + groups_list[i]] = index.statistics[:,i]
    fig, axes = plt.subplots(ncols = 2, nrows = 2, figsize = (17, 10))
    
    input_df.plot(column = 'LQ_' + groups_list[0],
                  cmap = 'inferno_r',
                  legend = True, ax = axes[0,0])
    axes[0,0].set_title('Location Quotient of ' + groups_list[0], fontsize = 18)
    axes[0,0].set_xticks([])
    axes[0,0].set_yticks([])
    axes[0,0].set_facecolor('white')
    
    input_df.plot(column = 'LQ_' + groups_list[1],
                  cmap = 'inferno_r',
                  legend = True, ax = axes[0,1])
    axes[0,1].set_title('Location Quotient of ' + groups_list[1], fontsize = 18)
    axes[0,1].set_xticks([])
    axes[0,1].set_yticks([])
    axes[0,1].set_facecolor('white')
    
    input_df.plot(column = 'LQ_' + groups_list[2],
                  cmap = 'inferno_r',
                  legend = True, ax = axes[1,0])
    axes[1,0].set_title('Location Quotient of ' + groups_list[2], fontsize = 18)
    axes[1,0].set_xticks([])
    axes[1,0].set_yticks([])
    axes[1,0].set_facecolor('white')
    
    input_df.plot(column = 'LQ_' + groups_list[3],
                  cmap = 'inferno_r',
                  legend = True, ax = axes[1,1])
    axes[1,1].set_title('Location Quotient of ' + groups_list[3], fontsize = 18)
    axes[1,1].set_xticks([])
    axes[1,1].set_yticks([])
    axes[1,1].set_facecolor('white')
    
    #C-Local Diversity
    print("-"*50)
    index = MultiLocalDiversity(input_df, groups_list)
    print(index.statistics[0:10]) # Values of first 10 units
    
    input_df['Local_Diversity'] = index.statistics
    input_df.head()
    ax = input_df.plot(column = 'Local_Diversity', cmap = 'inferno_r', legend = True, figsize = (15,7))
    ax.set_title("Local Diversity", fontsize = 25)
        
    #D-Local Entropy
    index = MultiLocalEntropy(input_df, groups_list)
    print(index.statistics[0:10]) # Values of first 10 units
    
    input_df['Local_Entropy'] = index.statistics
    input_df.head()
    ax = input_df.plot(column = 'Local_Entropy', cmap = 'inferno_r', legend = True, figsize = (15,7))
    ax.set_title("Local Entropy", fontsize = 25)
        
    #E-Local Simpson Interaction
    index = MultiLocalSimpsonInteraction(input_df, groups_list)
    print(index.statistics[0:10]) # Values of first 10 units
    input_df['Local_Simpson_Interaction'] = index.statistics
    input_df.head()
    ax = input_df.plot(column = 'Local_Simpson_Interaction', cmap = 'inferno_r', legend = True, figsize = (15,7))
    ax.set_title("Local Simpson Interaction", fontsize = 25)
        
    #F-Local Simpson Concentration
    index = MultiLocalSimpsonConcentration(input_df, groups_list)
    print(index.statistics[0:10]) # Values of first 10 units
    input_df['Local_Simpson_Concentration'] = index.statistics
    input_df.head()
    ax = input_df.plot(column = 'Local_Simpson_Concentration', cmap = 'inferno_r', legend = True, figsize = (15,7))
    ax.set_title("Local Simpson Concentration", fontsize = 25)
     
    #G-Local Centralization
    index = LocalRelativeCentralization(input_df, 'Lung Cancer', 'sumGroup')
    print(index.statistics[0:10]) # Values of first 10 units
    input_df['Local_Centralization'] = index.statistics
    input_df.head()
    ax = input_df.plot(column = 'Local_Centralization', cmap = 'inferno_r', legend = True, figsize = (15,7))
    ax.set_title("Local Centralization", fontsize = 25)    
    
    #H-multigroup aspatial
    #01-Multigroup Dissimilarity Index
    from segregation.aspatial import MultiDissim
    index = MultiDissim(input_df, groups_list)
    print(type(index))
    print("MultiDissim",index.statistic)
    
    #02-Multigroup Gini Index
    from segregation.aspatial import MultiGiniSeg
    index = MultiGiniSeg(input_df, groups_list)
    print(type(index))
    print("Multigroup Gini Index:",index.statistic)
    
    #03-Multigroup Normalized Exposure Index
    from segregation.aspatial import MultiNormalizedExposure
    index = MultiNormalizedExposure(input_df, groups_list)
    print(type(index))
    print("Multigroup Normalized Exposure Index:",index.statistic)
    
    #04-Multigroup Information Theory Index
    from segregation.aspatial import MultiInformationTheory
    index = MultiInformationTheory(input_df, groups_list)
    print(type(index))
    print("Multigroup Information Theory Index:",index.statistic)
    
    #05-Multigroup Relative Diversity Index
    from segregation.aspatial import MultiRelativeDiversity
    index = MultiRelativeDiversity(input_df, groups_list)
    print(type(index))
    print("Multigroup Relative Diversity Index:",index.statistic)
    
    #06-Multigroup Squared Coefficient of Variation Index
    from segregation.aspatial import MultiSquaredCoefficientVariation
    index = MultiSquaredCoefficientVariation(input_df, groups_list)
    print(type(index))
    print("Multigroup Squared Coefficient of Variation Index:",index.statistic)
    
    #07-Multigroup Diversity Index
    from segregation.aspatial import MultiDiversity
    index = MultiDiversity(input_df, groups_list)
    print(type(index))
    print("Multigroup Diversity Index:",index.statistic)
    
    #08-Simpson's Concentration Index (lambda)
    from segregation.aspatial import SimpsonsConcentration
    index = SimpsonsConcentration(input_df, groups_list)
    print(type(index))
    print("Simpson's Concentration Index (lambda):",index.statistic)
    
    #09-Simpson's Interaction Index (I)
    from segregation.aspatial import SimpsonsInteraction
    index = SimpsonsInteraction(input_df, groups_list)
    print(type(index))
    print("Simpson's Interaction Index (I)",index.statistic)
    
    #10-Multigroup Divergence Index
    from segregation.aspatial import MultiDivergence
    index = MultiDivergence(input_df, groups_list)
    print(type(index))
    print("Multigroup Divergence Index",index.statistic)
    
# multiscalar
def multiscalar(geoDF,populationCensusTif):
    geoDF=geoDF.to_crs(communityArea_CRS)
    plt.figure()
    geoDF.plot(column='Gonorrhea in Females',cmap='OrRd',figsize=(10, 10),legend=True,scheme='quantiles') # scheme='quantiles'
    # geoplot.polyplot(geoDF,figsize=(20, 20))
    # pc=gpd.read_file(populationCensus)
    # print(pc.columns)
    # print(pc.crs)
    # pc.to_file(os.path.join(dataRoot,"populationCensus_save.shp"))
    # Feature_to_Raster(os.path.join(dataRoot,"populationCensus_save.shp"), os.path.join(dataRoot,"popuC_1.tif"), 20, field_name=['CENSUS_BLO'], NoData_value=-9999)
    
    geoDF_sample=zonal_stats(geoDF,populationCensusTif,stats="count min mean max median")
    geoDF_sample_df=pd.DataFrame(geoDF_sample)
    geoDF_sample_df.rename(columns={"count":"popuCount", "min":"popuMin", "mean":"popuMean", "max":"popuMax", "median":"popuMedian"},inplace=True)
    geoDF_merge=geoDF.merge(geoDF_sample_df,left_on=geoDF.index, right_on=geoDF_sample_df.index)
    
    groups_list = ['Cancer (All Sites)','Lung Cancer','Tuberculosis','Gonorrhea in Females']
    geoDF_merge[groups_list]=geoDF_merge[groups_list].fillna(0)
    geoDF_merge["sumGroup"]=geoDF_merge[groups_list].sum(axis=1)
    for i in range(len(groups_list)):
        geoDF_merge['comp_' + groups_list[i]] = geoDF_merge[groups_list[i]] /geoDF_merge["sumGroup"]  #input_df['popuMean']
    df_pts=geoDF_merge.copy()
    df=df_pts
    
    w_queen = Queen.from_dataframe(df)
    w_rook = Rook.from_dataframe(df)
    w_kernel_1k = Kernel.from_dataframe(df_pts, bandwidth=2500)
    w_kernel_2k = Kernel.from_dataframe(df_pts, bandwidth=3000)

    #01-show spatial weights structure
    fig, ax = plt.subplots(1,4, figsize=(16,4))
    plot_spatial_weights(w_queen, df, ax=ax[0])
    ax[0].set_title('queen')
    
    plot_spatial_weights(w_rook, df, ax=ax[1])
    ax[1].set_title('rook')
    
    plot_spatial_weights(w_kernel_1k, df, ax=ax[2])
    ax[2].set_title('kernel 1k')
    
    plot_spatial_weights(w_kernel_2k, df, ax=ax[3])
    ax[3].set_title('kernel 2k')

    #02-show local environment
    def plot_local_environment(w, ax):
        from segregation.spatial.spatial_indexes import _build_local_environment
        d = _build_local_environment(df, groups_list, w)
        d['geometry'] = df.geometry
        d = gpd.GeoDataFrame(d)
        d.plot('Lung Cancer', k=6, scheme='quantiles', ax=ax)
        ax.axis('off')
    
    plt.figure()
    fig, axs = plt.subplots(1,4, figsize=(16,4))
    for i, wtype in enumerate([w_queen, w_rook, w_kernel_1k, w_kernel_2k]):
        plot_local_environment(w=wtype, ax=axs[i])

    #03-different local environments result in different segregation statistics
    #aspatial
    multiInfo=MultiInformationTheory(df, groups_list).statistic
    print("aspatial:",multiInfo)
    
    #rook neighborhood
    rookNeighborhood=SpatialInformationTheory(df, groups_list, w=w_rook).statistic
    print("rook neighborhood:",rookNeighborhood)

    #queen neighborhood
    queenNeighbor=SpatialInformationTheory(df, groups_list, w=w_queen).statistic
    print("queen neighborhood:",queenNeighbor)

    # 1 kilometer kernel distance neighborhood
    kernelDisNeighbor_a=SpatialInformationTheory(df, groups_list, w=w_kernel_1k).statistic
    print( "kernel distance neighborhood_A:",kernelDisNeighbor_a)
    
    # 2 kilometer kernel distance neighborhood
    kernelDisNeighbor_b=SpatialInformationTheory(df, groups_list, w=w_kernel_2k).statistic
    print("kernel distance neighborhood_B:",kernelDisNeighbor_b)
    
    distances = [1000.,2000.,3000.,4000.,5000.] # note these are floats [1000.,2000.,3000.,4000.,5000.]
    euclidian_profile = compute_segregation_profile(df_pts, groups=groups_list, distances=distances)
    print("euclidian_profile",euclidian_profile)
    
    #04-local street network can have a big impact on -
    df = df.to_crs(epsg=4326)
    # net = get_osm_network(df)
    # net.save_hdf5('dc_network.h5') #it can take awhile to download a street network, so you can save and read it back in using pandana
    dc_networkPath=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\Chicago Health_spatioTemporalAnalysis\data\dc_network.h5"
    net = Network.from_hdf5(dc_networkPath)
    # net = Network.from_hdf5('dc_network.h5')
    #three different segregation profiles
    network_linear_profile = compute_segregation_profile(df_pts, groups=groups_list, network=net, distances=distances)
    network_exponential_profile = compute_segregation_profile(df_pts, groups=groups_list, network=net, distances=distances, decay='exp', precompute=False)
  
    plt.figure()
    fig, ax = plt.subplots(figsize=(12,8))
    ax.scatter(euclidian_profile.keys(), euclidian_profile.values(), c='green', label='euclidian exp')
    ax.plot(list(euclidian_profile.keys()), list(euclidian_profile.values()), c='green') #TypeError: float() argument must be a string or a number, not 'dict_keys'
    
    ax.scatter(network_linear_profile.keys(), network_linear_profile.values(), c='red', label='net linear')
    ax.plot(list(network_linear_profile.keys()), list(network_linear_profile.values()), c='red')
    
    ax.scatter(network_exponential_profile.keys(), network_exponential_profile.values(), c='blue', label='net exp')
    ax.plot(list(network_exponential_profile.keys()), list(network_exponential_profile.values()), c='blue')
    
    plt.xlabel('meters')
    plt.ylabel('SIT')
    
    plt.legend()
    plt.show()
    
    #Multiscalar Segregation Profiles for Residential and Workplace areas
    #Workplace population and daytime population of council areas 
    #lack of data    


#network_measures
def networkMeasures(geoDF,populationCensusTif):
    geoDF=geoDF.to_crs(communityArea_CRS)
    plt.figure()
    geoDF.plot(column='Gonorrhea in Females',cmap='OrRd',figsize=(10, 10),legend=True,scheme='quantiles') # scheme='quantiles'
    # geoplot.polyplot(geoDF,figsize=(20, 20))
    # pc=gpd.read_file(populationCensus)
    # print(pc.columns)
    # print(pc.crs)
    # pc.to_file(os.path.join(dataRoot,"populationCensus_save.shp"))
    # Feature_to_Raster(os.path.join(dataRoot,"populationCensus_save.shp"), os.path.join(dataRoot,"popuC_1.tif"), 20, field_name=['CENSUS_BLO'], NoData_value=-9999)
    
    geoDF_sample=zonal_stats(geoDF,populationCensusTif,stats="count min mean max median")
    geoDF_sample_df=pd.DataFrame(geoDF_sample)
    geoDF_sample_df.rename(columns={"count":"popuCount", "min":"popuMin", "mean":"popuMean", "max":"popuMax", "median":"popuMedian"},inplace=True)
    geoDF_merge=geoDF.merge(geoDF_sample_df,left_on=geoDF.index, right_on=geoDF_sample_df.index)
    
    groups_list = ['Cancer (All Sites)','Lung Cancer','Tuberculosis','Gonorrhea in Females']
    geoDF_merge[groups_list]=geoDF_merge[groups_list].fillna(0)
    geoDF_merge["sumGroup"]=geoDF_merge[groups_list].sum(axis=1)
    for i in range(len(groups_list)):
        geoDF_merge['comp_' + groups_list[i]] = geoDF_merge[groups_list[i]] /geoDF_merge["sumGroup"]  #input_df['popuMean']
    
    
    fig, ax = plt.subplots(1,1, figsize=(12,12))
    geoDF_merge.plot(column='Lung Cancer', ax=ax)
    ax.axis('off')    
    
    geoDF_merge = geoDF_merge.to_crs({'init': 'epsg:4326'})
    net = Network.from_hdf5(dataFpDic["Chicago_osm_network"])
    factor_access = segregation.network.calc_access(geoDF_merge, network=net, distance=5000, decay='exp', variables=groups_list) #5000
    print(factor_access.head()) #Index(['acc_Cancer (All Sites)', 'acc_Lung Cancer', 'acc_Tuberculosis','acc_Gonorrhea in Females', 'geometry'],
    
    net_points =gpd.GeoDataFrame(factor_access, geometry=gpd.points_from_xy(net.nodes_df['x'],net.nodes_df['y']))
    net_points.crs = {'init': 'epsg:4326'}
    
    fig, ax = plt.subplots(1,2,figsize=(30,15))

    # tracts
    geoDF_merge.to_crs({'init': 'epsg:3857'}).plot('Lung Cancer', ax=ax[0], cmap='magma')
    ctx.add_basemap(ax[0],url=ctx.sources.ST_TONER_LITE)
    ax[0].axis('off')
    ax[0].set_title('Original Tract-Level Data',fontsize=24)
    
    print("net points columns:",net_points.columns)
    net_points[net_points["acc_Lung Cancer"] > 0].to_crs({'init': 'epsg:3857'}).plot('acc_Lung Cancer', alpha=0.01, ax=ax[1], cmap='magma', s=20)
    ctx.add_basemap(ax[1],url=ctx.sources.ST_TONER_LITE )
    ax[1].axis('off')
    ax[1].set_title('Intersection-Level Accessibility Surface ', fontsize=24)
    
    plt.suptitle('Non-Hispanic Black Population')
    plt.tight_layout()
    
    #represent distance-weighted densities
    plt.figure()
    fig, ax = plt.subplots(2,2, figsize=(16,16))
    ax = ax.flatten()  
    net_points[net_points["acc_Lung Cancer"] > 0].to_crs({'init': 'epsg:3857'}).plot("acc_Lung Cancer", ax=ax[0], cmap='magma', s=20)
    #ctx.add_basemap(ax[1],url=ctx.sources.ST_TONER_LITE )
    ax[0].axis('off')
    ax[0].set_title('acc_Lung Cancer Accessibility Surface ')
    
    net_points[net_points['acc_Tuberculosis'] > 0].to_crs({'init': 'epsg:3857'}).plot('acc_Tuberculosis', ax=ax[1], cmap='magma', s=20)
    #ctx.add_basemap(ax[1],url=ctx.sources.ST_TONER_LITE )
    ax[1].axis('off')
    ax[1].set_title('uberculosis Accessibility Surface ')
    
    net_points[net_points['acc_Gonorrhea in Females'] > 0].to_crs({'init': 'epsg:3857'}).plot('acc_Gonorrhea in Females', ax=ax[2], cmap='magma', s=20)
    #ctx.add_basemap(ax[1],url=ctx.sources.ST_TONER_LITE )
    ax[2].axis('off')
    ax[2].set_title('Gonorrhea  Accessibility Surface ')
    
    net_points[net_points['acc_Cancer (All Sites)'] > 0].to_crs({'init': 'epsg:3857'}).plot('acc_Cancer (All Sites)', ax=ax[3], cmap='magma', s=20)
    #ctx.add_basemap(ax[1],url=ctx.sources.ST_TONER_LITE )
    ax[3].axis('off')
    ax[3].set_title('Cancer (All Sites) Accessibility Surface ')
    
    
    #use these surfaces to calculate the multi-group network-based spatial information theory index
    accvars = ['acc_'+variable for variable in groups_list]
    #spatial information theory using the network kernel
    multiInfo_networkBased=MultiInformationTheory(factor_access, accvars).statistic
    print("multiInfo_networkBased:",multiInfo_networkBased)
    #aspatial information theory
    multiInfo=MultiInformationTheory(geoDF_merge, groups_list).statistic
    print("multiInfo:",multiInfo)
                                       

if __name__=="__main__": 
    dataRoot=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\Chicago Health_spatioTemporalAnalysis\data"
    dataFpDic={
            "Covid-19_CasesByZipCode":os.path.join(dataRoot,r"COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv"),
            "Covid-19_dailyCases":os.path.join(dataRoot,r"COVID-19_Daily_Cases_and_Deaths.csv"),
            
            "public_healthStatistics":os.path.join(dataRoot,r"Public_Health_Statistics-_Selected_public_health_indicators_by_Chicago_community_area.csv"),
            
            "zip_codes":os.path.join(dataRoot,r"Boundaries - ZIP Codes\geo_export_1a9a53ff-8090-4a1a-85ce-ac92bd036028.shp"),
            "communityArea":os.path.join(dataRoot,r"community_project.shp"),
       
            "populationCensus":os.path.join(dataRoot,r"populationCensus_Project.shp"),
            "populationCensusTif":os.path.join(dataRoot,r"population.tif"),
            
            "Chicago_osm_network":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\Chicago Health_spatioTemporalAnalysis\data\dc_network.h5"
       }
    # np.set_printoptions(threshold=sys.maxsize) #threshold=False print full array, without trucation
    # np.set_printoptions(threshold=False)
    
    '''basis'''
    covid19_gpd,covid19_df,covid19_zip,covid19_df_byZip=covid_19_csv2gpd(dataFpDic) 
    publicHealth_communityArea=publicHealth_csv2gpd(dataFpDic)
    communityArea_CRS=gpd.read_file(dataFpDic["communityArea"]).crs
    population_quantile=populationNeighborhood(dataFpDic["populationCensus"],dataFpDic["zip_codes"],dataFpDic["populationCensusTif"])

    '''C-inequality/equlity gini'''
    #13-gini Gini coefficient  https://en.wikipedia.org/wiki/Gini_coefficient  https://www.jianshu.com/p/95a4f076513c
    #0表示完全均衡，1表示完全不均衡
    # inequlityGini(covid19_df[['CasesWeekly','WeekStart','zipBak']],population_quantile[['zip','idx', 'geometry']])
     
    
    '''D-segregation'''    
    #14-aspatial indexes  http://pysal.org/notebooks/explore/segregation/aspatial_examples.html      
    # segregationMisc(covid19_df[['CasesWeekly','TestsWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])
    
    #**public health statistics
    # 15-local measure+multigroup  http://pysal.org/notebooks/explore/segregation/local_measures_example.html
    # localMeasure_multigroup(publicHealth_communityArea,dataFpDic['populationCensusTif'])
    #16-multiscalar
    # multiscalar(publicHealth_communityArea,dataFpDic['populationCensusTif'])
    #17-network_measures
    networkMeasures(publicHealth_communityArea,dataFpDic['populationCensusTif'])
