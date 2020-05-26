# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:11:24 2020

@author: :Richie Bao-caDesign设计(cadesign.cn).Chicago
ref:esda-http://pysal.org/notebooks/explore/esda/intro.html
"""
import os,shapely,esda,ogr,gdal
import pandas as pd
from shapely.geometry import Point,Polygon
import geopandas as gpd
import pysal as ps
import numpy as np
import libpysal as lps
import mapclassify as mc
import matplotlib.pylab as plt
import seaborn as sns
from rasterstats import zonal_stats
import contextily as ctx
from sklearn.metrics import silhouette_samples
from sklearn.cluster import KMeans


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


    
#Spatial_Autocorrelation_for_Areal_Unit_Data
def spatialAutocorrelation_G(data_df,zipPolygon):
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
    data_df_zipGPD_bfill=data_df_zipGPD.fillna(method='bfill',axis=1)    
    data_df_zipGPD_bfill[weeks]=data_df_zipGPD_bfill[weeks].fillna(0)
    # print(data_df_zipGPD_bfill.isna().sum())
    # data_df_zipGPD_bfill["idxPlus"]=data_df_zipGPD_bfill["idx"].apply(lambda x: str(x[0])+"-"+str(x[1]))
    # print(data_df_zipGPD_bfill)


    df=data_df_zipGPD_bfill
    wq =  lps.weights.Queen.from_dataframe(df)
    wq.transform = 'r'
    
    #01_Attribute Similarity
    finalWeek=19
    y = df[finalWeek]
    ylag = lps.weights.lag_spatial(wq, y)

    ylagq5 = mc.Quantiles(ylag, k=5)
    
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=ylagq5.yb).plot(column='cl', categorical=True, \
        k=5, cmap='GnBu', linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.title("Spatial Lag Median Covid-19(Quintiles)")    
    plt.show()
    
    #A_Global Spatial Autocorrelation
    #02-Binary Case
    print("value median",y.median())
    yb = y > y.median()
    print(sum(yb))
    yb = y > y.median()
    labels = ["0 Low", "1 High"]
    yb = [labels[i] for i in 1*yb] 
    df['yb'] = yb
    
    plt.figure()
    fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
    df.plot(column='yb', cmap='binary', edgecolor='grey', legend=True, ax=ax)
    
    #03_Join counts
    yb = 1 * (y > y.median()) # convert back to binary
    wq =  lps.weights.Queen.from_dataframe(df)
    wq.transform = 'b'
    np.random.seed(12345)
    jc = esda.join_counts.Join_Counts(yb, wq)
    print("bb:",jc.bb,"ww:",jc.ww,"bw:",jc.bw,"bb+ww+bw:",jc.bb + jc.ww + jc.bw,"wq.so:",wq.s0/2,"mean_bb:",jc.mean_bb)
    
    plt.figure()
    sns.kdeplot(jc.sim_bb, shade=True)
    plt.vlines(jc.bb, 0, 0.075, color='r')
    plt.vlines(jc.mean_bb, 0,0.075)
    plt.xlabel('BB Counts')
    
    # 04_Continuous Case
    # print(df,df.columns)
    wq.transform = 'r'
    y = df[finalWeek]  
    # print(y)
    np.random.seed(12345)
    mi = esda.moran.Moran(y, wq)
    print(mi.I)
        
    plt.figure()
    sns.kdeplot(mi.sim, shade=True)
    plt.vlines(mi.I, 0, 1, color='r')
    plt.vlines(mi.EI, 0,1)
    plt.xlabel("Moran's I")
    print("p_sim:",mi.p_sim)
    
    
    #B_Local Autocorrelation: Hot Spots, Cold Spots, and Spatial Outliers
    #05_Moran Scatterplot
    np.random.seed(12345)
    wq.transform = 'r'
    lag_fw = lps.weights.lag_spatial(wq, df[finalWeek])
    
    fw = df[finalWeek]
    b, a = np.polyfit(fw, lag_fw, 1)
    f, ax = plt.subplots(1, figsize=(9, 9))
    
    plt.plot(fw, lag_fw, '.', color='firebrick')
    
     # dashed vert at mean of the fw
    plt.vlines(fw.mean(), lag_fw.min(), lag_fw.max(), linestyle='--')
     # dashed horizontal at mean of lagged price 
    plt.hlines(lag_fw.mean(), fw.min(), fw.max(), linestyle='--')
    
    # red line of best fit using global I as slope
    plt.plot(fw, a + b*fw, 'r')
    plt.title('Moran Scatterplot')
    plt.ylabel('Spatial Lag of finalweek_Covid-19')
    plt.xlabel('final week value')
    plt.show()
    
    li = esda.moran.Moran_Local(y, wq)
    print("quadrant:",li.q)
    print("p_value<0.05",(li.p_sim < 0.05).sum())
    
    #06_hot spot
    sig = li.p_sim < 0.05
    hotspot = sig * li.q==1
    coldspot = sig * li.q==3
    doughnut = sig * li.q==2
    diamond = sig * li.q==4
    
    spots = ['n.sig.', 'hot spot']
    labels = [spots[i] for i in hotspot*1]
    
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['red', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()
    
    #07_cold spot
    spots = ['n.sig.', 'cold spot']
    labels = [spots[i] for i in coldspot*1]
    
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['blue', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()
    
    #08_sig    
    spots = ['n.sig.', 'doughnut']
    labels = [spots[i] for i in doughnut*1]
    
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['lightblue', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()
            
    #09_diamond
    spots = ['n.sig.', 'diamond']
    labels = [spots[i] for i in diamond*1]
    
    df = df
    from matplotlib import colors
    hmap = colors.ListedColormap(['pink', 'lightgrey'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()
        
    #10_composite
    sig = 1 * (li.p_sim < 0.05)
    hotspot = 1 * (sig * li.q==1)
    coldspot = 3 * (sig * li.q==3)
    doughnut = 2 * (sig * li.q==2)
    diamond = 4 * (sig * li.q==4)
    spots = hotspot + coldspot + doughnut + diamond
    
    spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
    labels = [spot_labels[i] for i in spots]
    from matplotlib import colors
    hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
    f, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.show()


#ref:https://www.programcreek.com/python/example/101827/gdal.RasterizeLayer
def Feature_to_Raster(input_shp, output_tiff, cellsize, field_name=False, NoData_value=-9999):
    """
    Converts a shapefile into a raster
    """

    # Input
    inp_driver = ogr.GetDriverByName('ESRI Shapefile')
    inp_source = inp_driver.Open(input_shp, 0)
    inp_lyr = inp_source.GetLayer()
    inp_srs = inp_lyr.GetSpatialRef()

    # Extent
    x_min, x_max, y_min, y_max = inp_lyr.GetExtent()
    x_ncells = int((x_max - x_min) / cellsize)
    y_ncells = int((y_max - y_min) / cellsize)

    # Output
    out_driver = gdal.GetDriverByName('GTiff')
    if os.path.exists(output_tiff):
        out_driver.Delete(output_tiff)
    out_source = out_driver.Create(output_tiff, x_ncells, y_ncells,1, gdal.GDT_Int16)
    print("+"*50)
    print(x_ncells, y_ncells,1, gdal.GDT_Int16)

    out_source.SetGeoTransform((x_min, cellsize, 0, y_max, 0, -cellsize))
    out_source.SetProjection(inp_srs.ExportToWkt())
    out_lyr = out_source.GetRasterBand(1)
    out_lyr.SetNoDataValue(NoData_value)

    # Rasterize
    # print(inp_lyr)
    if field_name:
        gdal.RasterizeLayer(out_source, [1], inp_lyr,options=["ATTRIBUTE={0}".format(field_name)])
    else:
        gdal.RasterizeLayer(out_source, [1], inp_lyr, burn_values=[1])

    # Save and/or close the data sources
    inp_source = None
    out_source = None

    # Return
    return output_tiff 

#geo_silhouettes
def geo_silhouettes(data_df,zipPolygon,communityAreaPolygon):
    caseWeekly_unstack=data_df['CasesWeekly'].unstack(level=0)
    
    zip_codes= gpd.read_file(zipPolygon)
    # zip_codes=zipPolygon
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
    data_df_zipGPD_bfill=data_df_zipGPD.fillna(method='bfill',axis=1)    
    data_df_zipGPD_bfill[weeks]=data_df_zipGPD_bfill[weeks].fillna(0)
    # print(data_df_zipGPD_bfill.isna().sum())
    # data_df_zipGPD_bfill["idxPlus"]=data_df_zipGPD_bfill["idx"].apply(lambda x: str(x[0])+"-"+str(x[1]))
    # print(data_df_zipGPD_bfill)    
    
    #using one Polygon samples another Polygon values(first convert Polygon to raster)
    communityArea=gpd.read_file(communityAreaPolygon)
    print(communityArea.crs,communityArea.shape)
    print(data_df_zipGPD_bfill.crs)
    
    temp_4sample=data_df_zipGPD_bfill[["geometry",19]]
    print(temp_4sample.crs)
    if temp_4sample.crs["init"]!=communityArea.crs["init"]:
        temp_4sample=temp_4sample.to_crs(communityArea.crs)
    else:print("data_df_zipGPD_bfill crs is the same as reference crs")  
    print(temp_4sample.crs)
    temp_4sample.columns=temp_4sample.columns.map(str)
    temp_4sample.to_file(os.path.join(dataRoot,r"temp_4sample.shp"))
    Feature_to_Raster(os.path.join(dataRoot,r"temp_4sample.shp"), os.path.join(dataRoot,"temp_4sample.tif"), 20, field_name="19", NoData_value=-9999)
    communityArea_sample=zonal_stats(communityAreaPolygon,os.path.join(dataRoot,"temp_4sample.tif"),stats="count min mean max median")
    communityArea_sample_df=pd.DataFrame(communityArea_sample)
    communityArea_sample_df.rename(columns={"count":"finalCount", "min":"finalMin", "mean":"finalMean", "max":"finalMax", "median":"finalMedian"},inplace=True)
    communityArea_merge=communityArea.merge(communityArea_sample_df,left_on=communityArea.index, right_on=communityArea_sample_df.index)
    # showVector(communityArea_merge,"finalMean")
    communityArea_merge.plot('finalMean',legend=True,figsize=(20,10))
    # showVector(communityArea_merge,"sides")
    communityArea_merge.plot('sides',legend=True,figsize=(20,10))
    communityArea_merge.plot('community',legend=True,figsize=(20*2,10*2))

    plt.figure()
    plt.rcParams.update({'font.size': 10})
    ax=communityArea_merge.plot(column="community",figsize=(20,20))
    plt.title("community area")
    # ax=showVector(zs_zip,'quantile')
    communityArea_merge.apply(lambda x: ax.annotate(s=x["community"], xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
    
    #This is done using the contextily package, which expects our data in a specific coordinate projection system
    communityArea_merge=communityArea_merge.to_crs(epsg=3857)
    basemap, extent = ctx.bounds2img(*communityArea_merge.total_bounds, zoom=11,url=ctx.tile_providers.ST_TONER_LITE)

    f,ax = plt.subplots(1,2, figsize=(20,10), sharex=True, sharey=True)
    communityArea_merge.plot('sides', ax=ax[0], alpha=.6)
    communityArea_merge.plot('finalMean', ax=ax[1], cmap='plasma', alpha=.6)

    for ax_ in ax:
        ax_.imshow(basemap, extent=extent, interpolation='bilinear')        
        ax_.axis(communityArea_merge.total_bounds[[0,2,1,3]])        
    f.tight_layout()
    plt.show()
    
    #Geosilhouettes: geographical measures of cluster fit
    # Path Silhouettes, which characterize the joint geographical and feature similarity in a clustering.
    # Boundary Silhouettes, which characterize how well-defined a geographical boundary is in a clustering.
    #01-The Silhouette Score
    silhouettes = silhouette_samples(communityArea_merge[['finalMean']].values, communityArea_merge.sides)
    
    f,ax = plt.subplots(1,2,figsize=(12,3))
    ax[0].hist(silhouettes)
    communityArea_merge.plot(silhouettes, ax=ax[1], cmap='bwr', vmin=-.5, vmax=.5, alpha=.6)
    ax[1].imshow(basemap, extent=extent, interpolation='bilinear')
    ax[1].axis(communityArea_merge.total_bounds[[0,2,1,3]])
    f.tight_layout()
    plt.show()    
    
    #02-KMeans
    communitySide=np.unique(communityArea_merge.sides)
    data_driven_clustering = KMeans(n_clusters=len(communitySide)).fit(communityArea_merge[['finalMean']].values)
    data_labels = data_driven_clustering.labels_
    data_silhouettes = silhouette_samples(communityArea_merge[['finalMean']].values, data_labels)
    communityArea_merge.plot(data_labels, categorical=True, legend=True,figsize=(12,10))
    plt.show()
    
    #03-as comparison with KMeans cluster results  /in this geography of inequality, each cluster is very well fit to its group
    f,ax = plt.subplots(1,2,figsize=(12,3))
    ax[0].hist(data_silhouettes)
    communityArea_merge.plot(data_silhouettes, ax=ax[1], cmap='bwr', vmin=-.5, vmax=.5, alpha=.6)
    ax[1].imshow(basemap, extent=extent, interpolation='bilinear')
    ax[1].axis(communityArea_merge.total_bounds[[0,2,1,3]])
    f.tight_layout()
    plt.show()
    
    #04-Nearest Label
    sidesMapping={'Central':0, 
                  'Far North Side':1, 
                  'Far Southeast Side':2,
                  'Far Southwest Side':3, 
                  'North Side':4, 
                  'Northwest Side':5, 
                  'South Side':6,
                  'Southwest Side':7, 
                  'West Side':8}
    communityArea_merge["sidesNum"]=communityArea_merge["sides"].to_frame().applymap(lambda s: sidesMapping.get(s) if s in sidesMapping else s)
    nearest_label = esda.nearest_label(communityArea_merge[['finalMean']].values, communityArea_merge.sidesNum)
    # print(nearest_label )
    nearest_outside_state = np.asarray(communitySide)[nearest_label]
    f, ax = plt.subplots(1,2,figsize=(12*2,4*2), sharex=True, sharey=True)
    communityArea_merge.plot('sides', ax=ax[0], categorical=True)
    communityArea_merge.plot(nearest_outside_state, ax=ax[1],legend=True, categorical=True, legend_kwds=dict(loc='lower right', ncol=2))
    ax[1].set_title('Most similar *other* state to county ($\hat{k}_i$)')
    for ax_ in ax:
        ax_.imshow(basemap, extent=extent, interpolation='bilinear')

    #05-single Nearest Label
    nearest_label = esda.nearest_label(communityArea_merge[['finalMean']].values,communityArea_merge.sidesNum, keep_self=True)
    nearest_state = np.asarray(communitySide)[nearest_label]
    plt.figure()
    f, ax = plt.subplots(1,2,figsize=(12*3,4*3), sharex=True, sharey=True)
    communityArea_merge.plot('sides', ax=ax[0], categorical=True)
    communityArea_merge.plot(nearest_state, ax=ax[1],legend=True, categorical=True,legend_kwds=dict(loc='lower right', ncol=2))
    ax[1].set_title('Most similar *other* state to county ($\hat{k}_i$)')
    for ax_ in ax:
        ax_.imshow(basemap, extent=extent, interpolation='bilinear')

    #06-Geographical Structure
    w = lps.weights.Rook.from_dataframe(communityArea_merge)
    f,ax = w.plot(communityArea_merge, edge_kws=dict(linewidth=.5), node_kws=dict(s=0))
    communityArea_merge.plot('sides', ax=ax, alpha=.6)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    plt.show()

    #07-Path Silhouettes
    path_silhouette = esda.path_silhouette(communityArea_merge[['finalMean']].values,communityArea_merge.sidesNum, w)
    f,ax = plt.subplots(1,2,figsize=(12*3,3*3))
    ax[0].hist(path_silhouette)
    communityArea_merge.plot(path_silhouette, ax=ax[1], cmap='bwr', vmin=-.5, vmax=.5)
    ax[1].imshow(basemap, extent=extent, interpolation='bilinear')
    ax[1].axis(communityArea_merge.total_bounds[[0,2,1,3]])
    f.tight_layout()
    plt.show()

    #08- path equivalent of nearest_label
    path_silhouette, next_best_path = esda.path_silhouette(communityArea_merge[['finalMean']].values, communityArea_merge.sidesNum, w,return_nbfc=True)

    next_best_path_state = np.asarray(communitySide)[next_best_path]
    f, ax = plt.subplots(1,2,figsize=(12*3,4*3), sharex=True, sharey=True)
    communityArea_merge.plot(path_silhouette, ax=ax[0], cmap='bwr', vmin=-.5, vmax=.5)
    communityArea_merge.plot(next_best_path_state, ax=ax[1],legend=True, categorical=True, legend_kwds=dict(loc='lower right', ncol=2))
    ax[1].set_title('Most path-similar other state')
    for ax_ in ax:
        ax_.imshow(basemap, extent=extent, interpolation='bilinear')
    f.tight_layout()
    plt.show()

    #09-Boundary Silhouettes
    boundary_silhouette = esda.boundary_silhouette(communityArea_merge[['finalMean']].values, communityArea_merge.sidesNum, w)
    communityArea_merge['boundary_silhouette'] = boundary_silhouette
    communityArea_merge.boundary_silhouette.hist()
    plt.figure()
    communityArea_merge.query('boundary_silhouette != 0').boundary_silhouette.hist()

    f,ax = plt.subplots(1,2,figsize=(12*3,3*3))
    ax[0].hist(communityArea_merge.query('boundary_silhouette != 0').boundary_silhouette)
    communityArea_merge.plot('sides', ax=ax[1], alpha=.5)
    communityArea_merge.query('boundary_silhouette != 0')\
        .plot('boundary_silhouette', ax=ax[1], cmap='bwr',vmin=-.5, vmax=.5, legend=True)
    ax[1].imshow(basemap, extent=extent, interpolation='bilinear')
    ax[1].axis(communityArea_merge.total_bounds[[0,2,1,3]])
    f.tight_layout()
    plt.show()


if __name__=="__main__": 
    dataRoot=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\Chicago Health_spatioTemporalAnalysis\data"
    dataFpDic={
            "Covid-19_CasesByZipCode":os.path.join(dataRoot,r"COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv"),
           
            "zip_codes":os.path.join(dataRoot,r"Boundaries - ZIP Codes\geo_export_1a9a53ff-8090-4a1a-85ce-ac92bd036028.shp"),
            "communityArea":os.path.join(dataRoot,r"community_project.shp"),
       }
    # np.set_printoptions(threshold=sys.maxsize) #threshold=False print full array, without trucation
    # np.set_printoptions(threshold=False)
    
    # main()
    '''basis'''
    covid19_gpd,covid19_df,covid19_zip,covid19_df_byZip=covid_19_csv2gpd(dataFpDic) 
    # publicHealth_communityArea=publicHealth_csv2gpd(dataFpDic)
    # communityArea_merge=communityAreaMerge(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"],dataFpDic["communityArea"])
    # communityArea_CRS=gpd.read_file(dataFpDic["communityArea"]).crs
    # population_quantile=populationNeighborhood(dataFpDic["populationCensus"],dataFpDic["zip_codes"],dataFpDic["populationCensusTif"])

    '''B-Exploratory Spatial Data Analysis in PySAL '''
    #http://pysal.org/notebooks/explore/esda/intro.html
    #Spatial_Autocorrelation_for_Areal_Unit_Data  http://pysal.org/notebooks/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data.html
    #*Covid-19_final time
    #11-Exploratory Analysis of Spatial Data: Spatial Autocorrelation
    # spatialAutocorrelation_G(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"])
    #12-geo_silhouettes
    geo_silhouettes(covid19_df[['CasesWeekly','WeekStart','zipBak']],dataFpDic["zip_codes"],dataFpDic["communityArea"])
