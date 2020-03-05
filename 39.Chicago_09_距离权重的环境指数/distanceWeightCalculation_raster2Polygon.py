# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:03:08 2020

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
from matplotlib import pyplot

#显示pandas DataFrame信息
def dataFrameInfoPrint(df):
    print("info:\n",df.info(verbose=False),
      "head:\n",df.head(),
      "columns:\n",df.columns,
      )

#显示向量vector
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

#合并数据到单一的DataFrame。（弃），参考valueWeightStatistic_merge.py
def parkInfoIntegration(data_Dic):
    ParkBoundaries=gpd.read_file(data_Dic["ParkBoundaries"])
    # dataFrameInfoPrint(ParkBoundaries)    
    '''
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

    parkFacility=gpd.read_file(data_Dic["ParkFacilities"],encoding="utf8")
    # dataFrameInfoPrint(parkFacility)
    '''
    [5 rows x 9 columns] columns:
    Index(['facility_n', 'facility_t', 'gisobjid', 'objectid', 'park', 'park_no',
       'x_coord', 'y_coord', 'geometry'],
      dtype='object')
    '''
    facilityFieldsExtractedList=['facility_n', 'facility_t','park', 'park_no','x_coord', 'y_coord', 'geometry']
    facility_fieldsExtracted=parkFacility[facilityFieldsExtractedList]    
    # dataFrameInfoPrint(facility_fieldsExtracted)
    parksInfo_linkFacility=gpd.sjoin(parks_fieldsExtracted, facility_fieldsExtracted, how='inner')
    # dataFrameInfoPrint(parksInfo_linkFacility)
    
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

    #变换投影，存储文件为EPSG:4326: WGS 84
    parks_fieldsExtracted=parks_fieldsExtracted.to_crs({'init': 'epsg:4326'})  
    parks_fieldsExtracted.to_file(os.path.join(data_outputFp,r"parkFieldExtracted.shp"))
    
    return parks_fieldsExtracted,parksInfo_linkFacility

#数据可视化。（弃），参考parkDataVisulization.py
def visualisationDF(df):    
    dataFrameInfoPrint(df)
    #graph-01
    # df['shapelyArea'].plot.hist(alpha=0.5)    
    #graph-02
    # df['shapelyArea'].plot.kde()    
    #graph-03
    # df[['shapelyLength','shapeIdx']].plot.scatter('shapelyLength','shapeIdx')    
    #normalize data in a range of columns
    cols_to_norm=['shapeIdx', 'FRAC']
    df[cols_to_norm]=df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    
    a='shapeIdx'
    b='FRAC'
    c='park_class'
    
    #graph-04
    # sns.jointplot(a,b,df,kind='hex')
    
    #graph-05
    # sns.jointplot(a, b, df, kind='kde')
    
    #graph-06
    # sns.catplot(x='park_class',y=a,data=df)
    
    #graph-07
    '''
    # Initialize the figure
    f, ax = plt.subplots()
    sns.despine(bottom=True, left=True)
    # Show each observation with a scatterplot
    sns.stripplot(x=a, y=c, hue=c,data=df, dodge=True, alpha=.25, zorder=1)    
    # Show the conditional means
    sns.pointplot(x=a, y=c, hue=c,data=df, dodge=.532, join=False, palette="dark",markers="d", scale=.75, ci=None)
    # Improve the legend 
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[3:], labels[3:], title=b,handletextpad=0, columnspacing=1,loc="lower right", ncol=3, frameon=True)
    '''
    
    #graph-08
    # sns.catplot(x=c,y=a,data=df,kind='box')
    
    #graph-09
    # sns.catplot(x=c,y=a,data=df,kind='violin')
    
    #graph-10
    '''
    f, axs = plt.subplots(1, 2, figsize=(12, 6))
    # First axis    
    df[b].plot.hist(ax=axs[0])
    # Second axis
    df[b].plot.kde(ax=axs[1])
    # Title
    f.suptitle(b)
    # Display
    plt.show()
    '''        

#从新定义栅格投影，参考投影为vector .shp文件
def reprojectedRaster(rasterFn,ref_vectorFn):
    dst_crs=gpd.read_file(ref_vectorFn).crs
    print(dst_crs) #{'init': 'epsg:4326'}
    dst_raster_projected=os.path.join(dataFp_1,r"svf_dstRasterProjected_b.tif")
    a_T = datetime.datetime.now()
    
    # dst_crs='EPSG:4326'
    with rasterio.open(rasterFn) as src:
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height,
        # 'compress': "LZW",
        'dtype':rasterio.float32,
        })
        # print(src.count)

        with rasterio.open(dst_raster_projected, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                    )     
    
    b_T = datetime.datetime.now()
    print("reprojected time span:", b_T-a_T)    
 

#根据Polgyon统计raster栅格信息
def polygonExtractRasterValue(polygonFn,rasterFn):    
    # parkBoundaries=gpd.read_file(polygonFn)
    # parkGeometry=ParkBoundaries.geometry.values
    # print(parkGeometry)
    # CVF=gpd.read_file(rasterFn)
    # print(CVF.head())
    # raster = rasterio.open(rasterFn)
    # rioShow(raster)
    
    #zonal_stats_stats: min,max,mean,count,sum,std,median,majority,minority,unique,range,nodata,percentile 
    # zs=zonal_stats(polygonFn, rasterFn,stats=['min', 'max', 'median', 'majority', 'sum']) #,geojson_out=True
    zs=zonal_stats(polygonFn, rasterFn,stats=['min','max','mean','count','sum','std','median','majority','minority','unique','range','nodata',])
    # print(zs)
        
    zsDataFrame=pd.DataFrame(zs)
    return zsDataFrame
    
'''polygon->buffer/difference->extract raster by mask->calculate distance->inverse distance weight->save to pickle'''
#读取栅格，并查看属性值，返回需要的属性
def rasterProperties(rasterFp):
    raster=rasterio.open(rasterFp)
    print("type:",type(raster))
    print("transform:",raster.transform)
    print("[width,height]:", raster.width, raster.height)
    print("number of bands:",raster.count)
    print("bounds:",raster.bounds)
    print("driver:", raster.driver)
    print("no data values:",raster.nodatavals)    
    print("_"*50)
    # print("meta:",raster.meta)        
    # print("_"*50)
    # print("profile:",raster.profile)
    return raster.width, raster.height

# Yield successive n-sized 
# chunks from l. 
#递归分组列表数据
def divide_chunks(l,n):
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
#建立用于rasterio库分批读取一个较大Raster数据的windows列表（如果内存溢出，而要处理较大的单独raster数据时）
#关于rasterio的window数据格式可以查看其官方网站
def rasterio_windows(totalWidth,totalHeight,subWidth,subHeight):
    w_n=list(divide_chunks(list(range(totalWidth)), subWidth))
    h_n=list(divide_chunks(list(range(totalHeight)), subHeight))
    wins=[Window(w[0],h[0],len(w),len(h)) for h in h_n for w in w_n]
    # print(wins)
    print("raster windows amount:",len(wins))
    return wins

#meter=degree*(2 * math.pi * 6378137.0)/ 360  degree=50/(2 * math.pi * 6378137.0) * 360
def rasterWeight2polygon(rasterFn,polygonFn):
    geo_polygons=gpd.read_file(polygonFn)
    polygons=geo_polygons.geometry
    print("01-get the .shp geometry:",len(polygons))
    
    # print(polygonsBuffer)
    # bufferPolygon=polygonsBuffer.difference(polygons)
    # print(geo_polygons)
    del geo_polygons
    polygonsConvexHull=polygons.convex_hull
    polygonsConvexHullBuffer=polygonsConvexHull.buffer(0.008983152841195214,cap_style=1, join_style=1) #mitre_limit=5  0.044915764205976066=5000m, 0.017966305682390427=2000m 0.008983152841195214=1000m
    # polygonsConvexHullBoundary=polygonsConvexHull.boundary
    # polygonsConvexHullBoundaryOffsetDiff=[Polygon(hull.parallel_offset(0.044915764205976066,resolution=16,join_style=2).coords).difference(Polygon(hull.coords)) for hull in polygonsConvexHullBoundary]
    # polygonsConvexHullBoundaryOffset=[element.parallel_offset(0.044915764205976066) for element in polygonsConvexHullBoundary]
    polygonsConvexHullBufferDiff=polygonsConvexHullBuffer.difference(polygonsConvexHull)
    print("02-get the polygon buffer difference:",len(polygonsConvexHullBufferDiff))
    del polygonsConvexHull
    # polygonsConvexHullBufferDiff.to_file(os.path.join(data_outputFp,"mask.shp"))
    # with fiona.open(os.path.join(data_outputFp,"mask.shp"), "r") as shapefile:
    #     shapes = [feature["geometry"] for feature in shapefile]
    # print(shapes)


    # print(polygonsConvexHullBufferDiff[0])
    # for i,v in polygonsConvexHullBufferDiff.iterrows():
    
    for i in tqdm(range(len(polygonsConvexHullBufferDiff))):
        mask=[polygonsConvexHullBufferDiff[i]]
        # print(mask)
        a_T = datetime.datetime.now()        
        with rasterio.open(rasterFn) as src:     
            out_image, out_transform = rasterio.mask.mask(src, mask, crop=True)     
            out_meta = src.meta
            
        fig, ax = pyplot.subplots(1, figsize=(12, 12))    
        rioShow(out_image)
        pyplot.show()
        fp=r"F:\data_02_Chicago\parkNetwork\SVFPics"
        pyplot.savefig(os.path.join(fp,"SVF_%d.jpg"%i),dpi=300)
        
        
#        if i ==2:
#            break         
        
        
        print("03-get the marked raster using each polygon buffer differnce:", out_image.shape)
        #转栅格为polygon,并同时提取栅格值
        w_shapes=pd.DataFrame([(Polygon(s['coordinates'][0]),v) for i,(s,v) in enumerate(shapes(out_image, mask=None, transform=out_transform))],columns=['polygon','value'])
        print("04-get the cell polygon and its value" )
        geo_wShapes=gpd.GeoDataFrame(w_shapes,crs=src.crs,geometry=w_shapes.polygon)
        geo_wShapes["centroid"]=geo_wShapes.geometry.centroid
        geo_pts=gpd.GeoDataFrame(geo_wShapes[['value']],crs=src.crs,geometry=geo_wShapes.centroid)
        geo_pts['distance']=geo_pts.geometry.distance(polygons[i])
        print("05-get the short distance from each centroid of cell to the polygon")
        geo_pts['IDW']=geo_pts.apply(lambda row:math.pow(row.distance*(2 * math.pi * 6378137.0)/ 360+1,-1),axis=1) #+1，避免pow()时，y值过大
        geo_pts["WeightedValue"]=geo_pts.value*geo_pts.IDW
        print("06-computed weight and weighted values")
        # geo_pts.to_file(os.path.join(data_outputFp,r'geoPtsDistance_%d.shp'%i)) 
        fp=r"F:\data_02_Chicago\parkNetwork\dataOutput\SVF_weighted"
        geo_pts.to_pickle(os.path.join(fp,r'svf_geoPtsDistance_%d.pkl'%i))
        print("07-save geopandas to_pickle")
        b_T = datetime.datetime.now()
        print("08-distance weight calculation time span,the whole time:", b_T-a_T)          
        
        # if i ==0:
        #     break           
        
    '''
    polysSingle=[]
    for index,poly in geo_polygons.iterrows():
        # print(poly)
        if poly.geometry.type == 'Polygon':
            polysSingle.append(poly.geometry.exterior.coords)
        elif poly.geometry.type == 'MultiPolygon':
            allparts = [p.buffer(0) for p in poly.geometry]
            poly.geometry = shapely.ops.cascaded_union(allparts)
            print(poly.geometry.type)
            polysSingle.append(poly.geometry.exterior.coords)
    print(polysSingle)
    ring_polygons=[LinearRing(poly.exterior.coords) for poly in polysSingle]
    '''
    
    '''
    totalWidth,totalHeight=rasterProperties(rasterFn)
    subWidth=1000
    subHeight=1000
    rasterio_wins=rasterio_windows(totalWidth,totalHeight,subWidth,subHeight)
    # print(rasterio_wins)
    
    i=0
    for win in tqdm(rasterio_wins):    
        c_T = datetime.datetime.now()        
        with rasterio.open(rasterFn,"r+") as src:                
            src.nodata=-1
            w = src.read(1, window=win) 
            # print("_"*50)
            # print(w.shape)
            profile=src.profile
            win_transform=src.window_transform(win) 
            
            # print("+"*50)
            # print(w.shape)
            mask =None
            # results=({'properties': {'raster_val': v}, 'geometry': s} for i,(s,v) in enumerate(shapes(w, mask=mask, transform=src.transform)))
            w_shapes=pd.DataFrame([(Polygon(s['coordinates'][0]),v) for i,(s,v) in enumerate(shapes(w, mask=mask, transform=win_transform))],columns=['polygon','value'])
            # print(dataFrameInfoPrint(w_shapes))
            
            # w_shapes["centroid"]=w_shapes.polygon.centroid
            geo_wShapes=gpd.GeoDataFrame(w_shapes,crs=src.crs,geometry=w_shapes.polygon)
            # geo_wShapes=geo_wShapes.drop('polygon',axis=1)
            geo_wShapes["centroid"]=geo_wShapes.geometry.centroid
            # geo_pts=geo_wShapes.drop(['geometry','polygon'],axis=1)
            # geo_pts=gpd.GeoDataFrame(pts,crs=src.crs,geometry=pts.centroid)
            geo_pts=gpd.GeoDataFrame(geo_wShapes[['value']],crs=src.crs,geometry=geo_wShapes.centroid)
            
            geo_pts['distance']=geo_pts.geometry.distance(polygons[0])
            
            geo_pts.to_file(os.path.join(data_outputFp,r'geoPtsValue_%d.shp'%i)) 
            

        # geo=geo_pts['distance'].tolist()
        # print(geo)
        # print(ok)
        #[{'type': 'Points','coordinates':geo_pts['distance'].tolist()}]

        # image=rasterio.features.rasterize(w_shapes,out_shape=src.shape,transform=src.transform)
        # print(geo_pts['distance'].to_numpy().shape)
        # profile.update(
        #     width=win.width, 
        #     height=win.height,
        #     count=1,
        #     transform=win_transform,
        #     compress='lzw',
        #     dtype=rasterio.float32
        #     )
        # with rasterio.open(os.path.join(data_outputFp,"rasterWeight_%d.tif"%i), 'w', **profile) as dst:
        #     dst.write(image, window=Window(0,0,win.width,win.height), indexes=1)  

        i+=1     
        #在正式计算前，通过break，仅对部分数据编写与调整代码
        # if i ==1:
        #     break       
    
        d_T = datetime.datetime.now()
        print("distance weight calculation time span:", d_T-c_T)  
        # '''
    # return  geo_pts

if __name__=="__main__": 
    data_outputFp=r"F:\data_02_Chicago\parkNetwork\dataOutput"
    dataFp_1=r"F:\data_02_Chicago\parkNetwork"   
    dataFp_2=r"F:\data_02_Chicago\ArcGisPro\parkNetwork"
    data_Dic={"ParkBoundaries":os.path.join(dataFp_1,r"Parks - Chicago Park District Park Boundaries (current).shp"),
            "ParkFacilities":os.path.join(dataFp_1,r"Parks - Chicago Park District Facilities (current).shp"),
            "ChicagoBoudnary":os.path.join(dataFp_1,r"Boundaries - Census Blocks - 2010.shp"),
            
            "population_CSV":os.path.join(dataFp_1,r"Population_by_2010_Census_Block.csv"),
            "CensusBlocks":os.path.join(dataFp_1,r"Boundaries - Census Blocks - 2010.shp"),
            
            "crimes":os.path.join(dataFp_1, r"Crimes_-_2001_to_present_-_Map.csv"),
            
            #相关栅格数据处理与分析
            "SVF":os.path.join(dataFp_1,r"SVF3_mosaic_c.tif"),
            "SVFReprojected":os.path.join(dataFp_1,r"svf_dstRasterProjected_a.tif"),
            }    
     
    # parks_fieldsExtracted,parksInfo_linkFacility=parkInfoIntegration(data_Dic)
    # visualisationDF(parks_fieldsExtracted)
    
#    # reprojectedRaster(data_Dic["SVF"],data_Dic["ParkBoundaries"]) #保持大地坐标，投影一致
#    zsDataFrame=polygonExtractRasterValue(data_Dic["ParkBoundaries"],data_Dic["SVFReprojected"])
#    zsDataFrame.to_pickle(r"F:\data_02_Chicago\parkNetwork\dataOutput\SVFEachPark.pkl")
    
    # visualisationDF(parks_fieldsExtracted)
    
    x=rasterWeight2polygon(data_Dic["SVFReprojected"],data_Dic["ParkBoundaries"])
    '''
    #读取rasterWeight2polygon（）函数保存的距离权重值，并计算['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'],保存数据为pickle
    import distanceWeightStatistic as dws
    valWeightedFp=r"F:\data_02_Chicago\parkNetwork\dataOutput\SVF_weighted"
    e_T = datetime.datetime.now()
    files_dir=dws.filesDirectoryOrder(valWeightedFp)
    valueDes=dws.geoValueWeightedDescribe(files_dir)
    valueDes.to_pickle(os.path.join(data_outputFp,r'parkSVFDistanceWeight.pkl'))
    f_T = datetime.datetime.now()
    print("distance weight calculation time span:", f_T-e_T)  
    '''