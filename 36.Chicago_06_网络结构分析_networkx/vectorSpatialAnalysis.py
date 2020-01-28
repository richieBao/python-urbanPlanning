# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 20:56:57 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import geopandas as gpd
import os,pysal
import pandas as pd
import numpy as np
import fiona
import shapely #vector 分析工具
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from shapely.geometry import shape,mapping, Point,MultiPoint, Polygon, MultiPolygon,LineString
# print(fiona.supported_drivers) #a full list of supported formats, type

from pylab import figure, scatter, show
import sympy,math
from sklearn.preprocessing import minmax_scale


#基于networkx库的网络分析 network analysis_A 参考案例：Knuth Miles：https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_knuth_miles.html#sphx-glr-auto-examples-drawing-plot-knuth-miles-py
def networkAnalysis_A(dataFrame):
    # print(pd.concat((ChicagoParkBoundaries_Pd.centroid.x, ChicagoParkBoundaries_Pd.centroid.y),axis=1))
    coordi=pd.concat((dataFrame.centroid.x, dataFrame.centroid.y),axis=1) #提取patch中心点坐标，并合并
    #build weights 
    #1.distance gravity weights
    minDistance=pysal.lib.weights.min_threshold_distance(coordi.to_numpy()) #使用pysal库计算最小距离
    # print(minDistance)
    weights=pysal.lib.weights.DistanceBand(coordi,threshold=minDistance*3,binary=False,alpha=-2.) #使用pysal库计算距离权重
    # print(list(weights))
    # print(dataFrame.columns)
    G=nx.Graph() #建立网络图
    G.position={} #存储点位置
    G.perimeter={} #存储patch周长
    G.FRAC={} #存储patch的FRAC景观指数 Fractal Dimension Index
    G.shapeIdx={} #存储patch的形状指数 
    G.shape_area={} #存储patch的面积
    i=0 #用于计数循环一个点到多个点，构建的边edge
    for (index_label, row_series) in dataFrame.iterrows(): #循环dataFrame数据，逐行读取与存储到网络图graph中
        # print(index_label,"______\n",row_series["perimeter"])
        # print("_"*50)
        #add nodes
        node_parkLabel=row_series["label"] #以“label”字段作为点的ID标识
        G.add_node(node_parkLabel)
        #根据计算需要，加入属性值
        G.position[node_parkLabel]=(row_series["centroid"].x,row_series["centroid"].y)
        G.perimeter[node_parkLabel]=row_series["shapelyLength"]
        G.FRAC[node_parkLabel]=row_series["FRAC"]
        G.shapeIdx[node_parkLabel]=row_series["shapeIdx"]
        G.shape_area[node_parkLabel]=row_series["shape_area"]

        #add edges with weights
        # print(weights[i])
        #循环加入边
        for w in weights[i]:
            # print(node_parkLabel)
            # print(w)
            # print(ChicagoParkBoundaries_Pd)
            # print(ChicagoParkBoundaries_Pd.iloc[w]["label"])
            # print(weights[i][w])
            G.add_edge(node_parkLabel, dataFrame.iloc[w]["label"], weight=weights[i][w])
        #     print(w)
            
        i+=1
            
    print("_"*50)
    print("Loaded vector containing network info.")
    print("digraph has %d nodes with %d edges"% (nx.number_of_nodes(G), nx.number_of_edges(G)))
    print("_"*50)
    
    return G


#基于networkx库的网络分析 network analysis_B。 参考案例：Giant Component https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_giant_component.html#sphx-glr-auto-examples-drawing-plot-giant-component-py
def networkAnalysis_B(G):
    #本次实验中未使用该部分，但保留在该代码文件中，已备查看
    try:
        import pygraphviz  # conda install -c alubbock pygraphviz   用此方法安装pygraphviz库，能正常安装
        from networkx.drawing.nx_agraph import graphviz_layout
        layout = graphviz_layout 
    except ImportError:
        try:
            import pydot
            from networkx.drawing.nx_pydot import graphviz_layout
            layout = graphviz_layout
        except ImportError:
            print("PyGraphviz and pydot not found;\n"
                  "drawing with spring layout;\n"
                  "will be slow.")
            layout = nx.spring_layout

    # 建立新网络图，复制G，make new graph
    H = nx.Graph()
    for v in G:
        # print(v)
        H.add_node(v)
    weightValue=list(nx.get_edge_attributes(G,'weight').values()) #提取权重值
    # weightsForWidth=[G[u][v]['weight'] for u,v in G.edges()] #another way
    # print(weightValue)
    import pysal.viz.mapclassify as mc
    q=mc.Quantiles(weightValue,k=50).bins #计算分位数，用于显示值的提取
    # print(q)
    #复制G到H
    for (u, v, d) in G.edges(data=True):
        # print(u,v,d)
        # print()
        # print(d['weight'])
        if d['weight'] > q[48]: #根据权重选择较为紧密的部分提取
            H.add_edge(u, v)
    
    print("H_digraph has %d nodes with %d edges"% (nx.number_of_nodes(H), nx.number_of_edges(H)))             
    weightsForWidthScale=np.interp(weightValue, (min(weightValue), max(weightValue)), (1, 3000)) #缩放值到新区间，用于强化显示数据，setting the edge width  
    # print(weightsForWidthScale)     
    node_color = [float(H.degree(v)) for v in H]   
    scaleNode=1
    
            
    # the following range of p values should be close to the threshold
    plt.figure(figsize=(100,100))
    plt.subplots_adjust(left=0, right=1, bottom=0, top=0.95, wspace=0.01, hspace=0.01)
    # nx.draw(H, G.position, with_labels=False, node_size=800)
    #打印图_node部分
    nx.draw(H, G.position,node_size=minmax_scale([G.shape_area[v]*scaleNode for v in H],feature_range=(100, 8200)), node_color=node_color,with_labels=True,font_size=60,edge_cmap=plt.cm.Blues,width=weightsForWidthScale) #edge_cmap=plt.cm.Blues
    
    #根据edge长度排序node identify largest connected component
    Gcc = sorted(nx.connected_components(H), key=len, reverse=True)
    # print(Gcc)
    G0 = H.subgraph(Gcc[0]) #为最长的边
    nx.draw_networkx_edges(G0, G.position, with_labels=False,edge_color='r',width=9.0)

    #设置条件，显示其它长度的边 show other connected components
    for Gi in Gcc[1:]:
        if len(Gi) > 10: 
            nx.draw_networkx_edges(H.subgraph(Gi), G.position,with_labels=False,edge_color='r',alpha=0.3,width=7.0)

    plt.show()
 

#vector读取关键信息与分析,network; discard. 该部分丢弃
def vectorSpatialAnalysis_basis(fp, fnDic):
    #读取vector/.shp数据
    ChicagoParkBoundariesFn=fnDic["ChicagoParkBoundaries"]
    ChicagoParkBoundaries_Pd=gpd.read_file(ChicagoParkBoundariesFn)
    ChicagoParkBoundaries_Pd_fields=ChicagoParkBoundaries_Pd.columns  
    
    ChicaoParkFacilityFn=fnDic["ChicagoParkFacilities"]
    ChicaoParkFacility_Pd=gpd.read_file(ChicaoParkFacilityFn,encoding="utf8")
    # print(ChicaoParkFacility_Pd,ChicaoParkFacility_Pd.columns)
    
    #基本统计分析部分+network网络分析
    ChicagoParkBoundaries_Pd["centroid"]=ChicagoParkBoundaries_Pd.geometry.centroid
    # a=vectorGeoPd.geometry.centroid
    # print(a)    
    # print(vectorGeoPd)
    Boundary_Facility_join=gpd.sjoin(ChicagoParkBoundaries_Pd, ChicaoParkFacility_Pd, how='inner')
    # print("Boundaries info:",ChicagoParkBoundaries_Pd.info())
    # print("Facilities info:",ChicaoParkFacility_Pd.info())
    # print("inner info:",Boundary_Facility_join.info())
    # print(ChicagoParkBoundaries_Pd.columns)
    # print(ChicagoParkBoundaries_Pd.geometry[0])
    # print(ChicagoParkBoundaries_Pd.centroid[0].x)
    
    # print(Boundary_Facility_join.iloc[0])
    # print(Boundary_Facility_join.info())
    # print(Boundary_Facility_join)

    # print(pd.concat((ChicagoParkBoundaries_Pd.centroid.x, ChicagoParkBoundaries_Pd.centroid.y),axis=1))
    coordi=pd.concat((ChicagoParkBoundaries_Pd.centroid.x, ChicagoParkBoundaries_Pd.centroid.y),axis=1)
    #build weights 
    #1.distance gravity weights
    minDistance=pysal.lib.weights.min_threshold_distance(coordi.to_numpy())
    # print(minDistance)
    weights=pysal.lib.weights.DistanceBand(coordi,threshold=minDistance*3,binary=False,alpha=-2.)
    # print(list(weights))
   
    G=nx.Graph()
    G.position={}
    G.perimeter={}
    i=0
    for (index_label, row_series) in ChicagoParkBoundaries_Pd.iterrows():
        # print(index_label,"______\n",row_series["perimeter"])
        # print("_"*50)
        #add nodes
        node_parkLabel=row_series["label"]
        G.add_node(node_parkLabel)
        G.position[node_parkLabel]=(row_series["centroid"].x,row_series["centroid"].y)
        G.perimeter[node_parkLabel]=row_series["perimeter"]

        #add edges with weights
        # print(weights[i])
        for w in weights[i]:
            # print(node_parkLabel)
            # print(w)
            # print(ChicagoParkBoundaries_Pd)
            # print(ChicagoParkBoundaries_Pd.iloc[w]["label"])
            # print(weights[i][w])
            G.add_edge(node_parkLabel, ChicagoParkBoundaries_Pd.iloc[w]["label"], weight=weights[i][w])
        #     print(w)
            
        i+=1
            
    print("_"*50)
    print("Loaded vector containing network info.")
    print("digraph has %d nodes with %d edges"% (nx.number_of_nodes(G), nx.number_of_edges(G)))
    print("_"*50)
    
    return G

#打印显示网络图G   
def G_display(G):
    # make new graph
    H = nx.Graph()
    for v in G:
        # print(v)
        H.add_node(v)
    weightValue=list(nx.get_edge_attributes(G,'weight').values()) #提取权重
    # weightsForWidth=[G[u][v]['weight'] for u,v in G.edges()] #another way
    # print(weightValue)
    import pysal.viz.mapclassify as mc
    q=mc.Quantiles(weightValue,k=30).bins #计算分位数，用于显示值的提取
    # print(q)
  
    for (u, v, d) in tqdm(G.edges(data=True)):
        # print(u,v,d)
        # print()
        # print(d['weight'])
        if d['weight'] > q[28]:
            H.add_edge(u, v)

    print("H_digraph has %d nodes with %d edges"% (nx.number_of_nodes(H), nx.number_of_edges(H)))
    # draw with matplotlib/pylab
    plt.figure(figsize=(18, 18))
    # m=2
    # fig = figure(figsize=(9*m,9*m)
    # with nodes colored by degree sized by value elected
    node_color = [float(H.degree(v)) for v in H]
    # print(node_color)
    # nx.draw(H, G.position,node_size=[G.perimeter[v] for v in H],node_color=node_color, with_labels=True)
    
    weightsForWidthScale=np.interp(weightValue, (min(weightValue), max(weightValue)), (1, 3000)) #setting the edge width
    scaleNode=1
    
    # sklearn.preprocessing.minmax_scale(X, feature_range=(0, 1), axis=0, copy=True)
    nx.draw(H, G.position,node_size=minmax_scale([G.shape_area[v]*scaleNode for v in H],feature_range=(10, 2200)), node_color=node_color,with_labels=True,edge_cmap=plt.cm.Blues,width=weightsForWidthScale) #edge_cmap=plt.cm.Blues
    # scale the axes equally
    # plt.xlim(-5000, 500)
    # plt.ylim(-2000, 3500)

    plt.show()


#CSV文件转.shp格式，并返回关键信息。使用geopandas库实现
def CSV2SHP(dataFp,dataCSV,outFn): #传入文件路径，文件名和输出文件名
    csvPath=os.path.join(dataFp,dataCSV)
    csvPd=pd.read_csv(csvPath)
    csvPd_fields=csvPd.columns

    # newColumns：['X Coordinate', 'Y Coordinate','Year','Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description',
    #    'Location Description', 'Arrest', 'Domestic', 'Beat', 'Ward','FBI Code',  'Latitude','Longitude', 'Location']
    # convert to GeoDataFrame
    crimesDropNan=csvPd.dropna(subset=['Location']) #根据需要删除column字段
    crimesDropNan_con=crimesDropNan.loc[crimesDropNan['Year'] >=2015] #提取满足条件的rows
    # csvPdTest=crimesDropNan[:10]
    crimesDropNan_con['geometry'] =crimesDropNan_con.apply(lambda row: Point(row.Longitude,row.Latitude,0),axis=1) #自行确定[x,y,z]。使用shapely.geometry库的Point建立点数据
  
    # df = df.drop(['x', 'y', 'z'], axis=1)
    # crimesDropNan=crimes_pd.dropna(subset=['Location'])
    
    crs={'init': 'epsg:4326'} #坐标系统值参考：https://spatialreference.org/  Find your references in any number of formats!
    gdf=gpd.GeoDataFrame(crimesDropNan_con,crs=crs, geometry=crimesDropNan_con.geometry)
    gdf.to_file(driver = 'ESRI Shapefile', filename=os.path.join(dataFp,outFn))

    return crimesDropNan_con, csvPd_fields


#CSV数据读取与分析。discard
def CSVSpatialAnalysis_basis(dataFp,dataCSV):
    csvPath=os.path.join(dataFp,dataCSV)
    csvPd=pd.read_csv(csvPath)
    csvPd_fields=csvPd.columns
    crimesDropNan=csvPd.dropna(subset=['Location'])
    crimesDropNan_con=crimesDropNan.loc[crimesDropNan['Year'] >=2015] #提取满足条件的rows
    
    
    return crimesDropNan_con,csvPd_fields

#dataArray数据均打印在一张图中，可用于同一数据不同情况的比较，print boxplot graph, all classes lie in single graph
def boxplot_single(dataArray):    
    # dataArray=dataFrame.to_numpy()
    arrayShape=dataArray.shape
    # print(dataArray)
    # print(arrayShape)
    # print(ok)
    fig_n=2
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9*fig_n, 4*fig_n))
    
    # plot violin plot
    axes[0].violinplot(dataArray,
                       showmeans=False,
                       showmedians=True)
    axes[0].set_title('Violin plot')
    
    # plot box plot
    axes[1].boxplot(dataArray)
    axes[1].set_title('Box plot')
    
    # adding horizontal grid lines
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(arrayShape[1])])
        ax.set_xlabel('Four separate samples')
        ax.set_ylabel('Observed values')
    
    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(arrayShape[1])],xticklabels=['x1', 'x2', 'x3', 'x4'])
    plt.show()

#dataArray数据打印在各自单独的图中，避免单位，数值大小的影响。print boxplot graph, each class lies in each graph
def boxplot_multi(dataFrame):
    dataArray=dataFrame.to_numpy()
    arrayShape=dataArray.shape
    # print(dataArray)
    print(arrayShape)
    # print(ok)
    fig_n=2
    fig, axs = plt.subplots(1, arrayShape[1],figsize=(9*fig_n, 4*fig_n))
    titleList=dataFrame.columns
    
    # basic plot
    # print(dataArray.T)
    for sub in range(arrayShape[1]):
        # print(sub)
        # print(dataArray.T[sub,:].shape)
        axs[sub].boxplot(dataArray.T[sub,:])
        axs[sub].set_title('%s'%titleList[sub])
    
    fig.subplots_adjust(left=0.18, right=1.28, bottom=0.05, top=1.9,hspace=0.4, wspace=0.3)

    plt.show()
    
#.shp数据读取，组织，计算与统计部分。basic statistics, including landscape metrics
def basicStatistics(fp, fnDic):
    #读取vector/.shp数据
    ChicagoParkBoundariesFn=fnDic["ChicagoParkBoundaries"]
    ChicagoParkBoundaries_Pd=gpd.read_file(ChicagoParkBoundariesFn)
    ChicagoParkBoundaries_Pd_fields=ChicagoParkBoundaries_Pd.columns  
    # print(ChicagoParkBoundaries_Pd_fields)
    '''
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
    parksFieldsExtracted=['park_no','label','park_class','location','acres','shape_area', 'shape_leng','perimeter','geometry']
    ChicagoParks_fieldsExtracted=ChicagoParkBoundaries_Pd[parksFieldsExtracted]
    # ChicagoParks_fieldsExtracted["centroid"]=ChicagoParks_fieldsExtracted.geometry.centroid
    # print(ChicagoParks_fieldsExtracted.columns)
    # print(ChicagoParks_fieldsExtracted.head())  
    
    #link other data(facility points based on the parameter "within")
    ChicaoParkFacilityFn=fnDic["ChicagoParkFacilities"]
    ChicaoParkFacility_Pd=gpd.read_file(ChicaoParkFacilityFn,encoding="utf8")
    # print(ChicaoParkFacility_Pd.columns)
    '''
    Index(['facility_n', 'facility_t', 'gisobjid', 'objectid', 'park', 'park_no',
       'x_coord', 'y_coord', 'geometry'],
      dtype='object')    
    '''
    facilityFieldsExtracted=['facility_n', 'facility_t','park', 'park_no','x_coord', 'y_coord', 'geometry']
    facility_fieldsExtracted=ChicaoParkFacility_Pd[facilityFieldsExtracted]  
    Boundary_Facility_join=gpd.sjoin(ChicagoParks_fieldsExtracted, ChicaoParkFacility_Pd, how='inner') #数据连接，根据polygon是否包含point,此次实验未进一步数据分析
    # print(Boundary_Facility_join.head())
    # print(Boundary_Facility_join.iloc[0])
    # print(Boundary_Facility_join)
    
    
    #projection。因为要计算面积和长度等信息，因此需要定义投影
    print(ChicagoParks_fieldsExtracted.crs)
    ChicagoParks_fieldsExtracted=ChicagoParks_fieldsExtracted.to_crs({'init': 'epsg:2028'}) #投影参考：https://spatialreference.org/ref/epsg/?search=&srtext=Search   https://epsg.io/  
    
    #calculation and add new fields
    ChicagoParks_fieldsExtracted["shapelyArea"]=ChicagoParks_fieldsExtracted.geometry.area
    ChicagoParks_fieldsExtracted["shapelyLength"]=ChicagoParks_fieldsExtracted.geometry.length
    
    # print(ChicagoParks_fieldsExtracted.iloc[0])
    
    #使用sympy库建立计算面公式，清晰方便
    #shape index
    #pij = perimeter (m) of patch ij.   aij = area (m2) of patch ij. 
    pij=sympy.Symbol('pij')
    aij =sympy.Symbol('aij ')
    expr_shapeIdx=0.25*pij/sympy.root(aij,2)    
    # result=fx.evalf(subs={x:3,y:4})
    fx_shapeIdx = sympy.lambdify((pij,aij), expr_shapeIdx, 'numpy')
    ChicagoParks_fieldsExtracted["shapeIdx"]=fx_shapeIdx(ChicagoParks_fieldsExtracted.shapelyLength,ChicagoParks_fieldsExtracted.shapelyArea)

   
    # print(ChicagoParks_fieldsExtracted.iloc[0])
    # print(ChicagoParks_fieldsExtracted.shapelyArea)    
    validation_result=expr_shapeIdx.evalf(subs={pij:1093.47,aij:72084.9}) #仅用于验证。validate the first patch
    # print(validation_result)    
    # print(ChicagoParks_fieldsExtracted.shapeIdx)
    
    #Fractal Dimension Index(FRAC)
    expr_FRAC=2*sympy.log(0.25*pij)/sympy.log(aij,2)
    fx_FRAC= sympy.lambdify((pij,aij), expr_FRAC, 'numpy')
    ChicagoParks_fieldsExtracted["FRAC"]=fx_FRAC(ChicagoParks_fieldsExtracted.shapelyLength,ChicagoParks_fieldsExtracted.shapelyArea)
    

    #可以显示vecter（polygon,point）数据。show vector
    multi=10
    fig, ax = plt.subplots(figsize=(14*multi, 8*multi))
    ChicagoParks_fieldsExtracted.plot(column='shapeIdx',
                    categorical=True,
                    legend=False,
                    ax=ax)
    
    # adjust legend location
    leg = ax.get_legend()
    # leg.set_bbox_to_anchor((1.15,0.5))
    ax.set_axis_off()    
    plt.show()    
    
    # geometry=ChicagoParks_fieldsExtracted.pop("geometry")
    # ChicagoParks_fieldsExtracted["geometry"]=geometry
    #变换投影，存储文件为EPSG:4326: WGS 84
    ChicagoParks_fieldsExtracted=ChicagoParks_fieldsExtracted.to_crs({'init': 'epsg:4326'})    
    # ChicagoParks_fieldsExtracted.pop("centroid")
    # print(ChicagoParks_fieldsExtracted.iloc[0])    
    ChicagoParks_fieldsExtracted.to_file(os.path.join(dataFp,r"xx\xx.shp"))
    #如果dataFrame中包含的字段中有多类shape几何字段，则无法存储为.shp格式文件，因此在存储之后，再次计算centroid将其添加到字段中
    ChicagoParks_fieldsExtracted["centroid"]=ChicagoParks_fieldsExtracted.geometry.centroid
        
    #boxplot
    # print(ChicagoParks_fieldsExtracted.columns)
    '''
    Index(['park_no', 'label', 'park_class', 'location', 'acres', 'shape_area',
       'shape_leng', 'perimeter', 'geometry', 'shapelyArea', 'shapelyLength',
       'shapeIdx','FRAC'],
      dtype='object')    
    '''
    printDataList=['shapelyArea', 'shapelyLength', 'shapeIdx','FRAC']
    ChicagoParks_boxplot=ChicagoParks_fieldsExtracted[printDataList] #提取使用boxplot统计数据的字段
    
    # boxplot_single(ChicagoParks_boxplot.to_numpy())
    boxplot_multi(ChicagoParks_boxplot) #使用boxplot统计数据
    
    return ChicagoParks_fieldsExtracted


if __name__=="__main__": 
    #读取vector(.shp)并统计分析
    #文件："Parks - Chicago Park District Park Boundaries .shp"
    dataFp=r"D:\data\data_01_Chicago\data.city of chicago"    
    fnDic={"ChicagoParkBoundaries":os.path.join(dataFp,r"Parks - Chicago Park District Park Boundaries.shp"),
            "ChicagoParkFacilities":os.path.join(dataFp,r"Parks - Chicago Park District Facilities .shp")}    
 
    #——————————————————————————————————————————————————————————————————————————
    #basic statistics
    ChicagoParks_fieldsExtracted=basicStatistics(dataFp, fnDic)
    # print(ChicagoParks_fieldsExtracted.columns)
    
    # #testing data avoid big calculated amount
    # dataFp=r"D:\data\data_01_Chicago\QGisDat"
    # fnDic={"ChicagoParkBoundaries":os.path.join(dataFp,r"t_poly.shp"),
    #         "ChicagoParkFacilities":os.path.join(dataFp,r"t_pts.shp")}
    
    G=vectorSpatialAnalysis_basis(dataFp, fnDic) #discard
    G_A=networkAnalysis_A(ChicagoParks_fieldsExtracted)
    G_display(G_A)

    networkAnalysis_B(G_A)

    #——————————————————————————————————————————————————————————————————————————
    #文件："Crimes_-_2015_to_present_-_Map.shp"
    crimesCSV2001_20_presentFn=r"Crimes_-_2001_to_present_-_Map.csv"
    crimesCSV2001_20_presentOutFn=r"Crimes_-_2015_to_present_-_Map.shp"
    #CSV转.shp
    # crimes_pd, crimes_fields=CSV2SHP(dataFp,crimesCSV2001_20_presentFn,crimesCSV2001_20_presentOutFn)
    
    #读取CSV数据并统计分析
    # crimesPf,crimes_fields=CSVSpatialAnalysis_basis(dataFp,crimesCSV2001_20_presentFn)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    