# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 13:06:59 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project
"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import scipy.io as sio
import math
from decimal import *
from shapely.geometry import Point,MultiPoint
import networkx as nx
import pandas as pd
from tqdm import tqdm

getcontext().prec = 28
np.set_printoptions(precision=28)

#01-input simulation data file path 数据位置。 MatLab的.fig文件输出类型不同，此次包含typeA 和B两种，代码包含对这两种类型的读取
#Type A:
LandmarkMap_fn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_LM.fig" #coordinates of the landmarks file path
PHMI_fn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_PHMI.fig" #PHMI file path

#Typt B:
#LandmarkMap_fn==r"F:\data_02_Chicago\data_driverless City\IIT_data\LandmarkMap.fig"   
#PHMI_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\PHMI.fig"

#02-read coordinates data of landmarks 读取landmarks坐标值
def readMatLabFig_LandmarkMap(LandmarkMap_fn):
    LandmarkMap=loadmat(LandmarkMap_fn, squeeze_me=True, struct_as_record=False)
    y=loadmat(LandmarkMap_fn)
    print(sorted(LandmarkMap.keys()))
        
    LandmarkMap_dic={} #提取.fig值
    for object_idx in range(LandmarkMap['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=LandmarkMap['hgS_070000'].children.children[object_idx].properties.XData #good
            Y=LandmarkMap['hgS_070000'].children.children[object_idx].properties.YData 
            LandmarkMap_dic[object_idx]=(X,Y)
        except:
            pass
    
    # print(LandmarkMap_dic)
    fig= plt.figure(figsize=(130,20))
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    i=0
    for key in LandmarkMap_dic.keys():
        plt.scatter(LandmarkMap_dic[key][1],LandmarkMap_dic[key][0], s=dotSizes[i],marker=markers[i], color=colors[i],linewidth=linewidths[i])
        i+=1
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    return LandmarkMap_dic

#03-read PHMI values for evaluation of AVs' on-board lidar navigation 读取PHMI值
#the PHMI value less than pow(10,-5) is scaled to show clearly------on; the PHMI value larger than pow(10,-5) is scaled to show clearly------on
#数据类型A
def readMatLabFig_PHMI_A(PHMI_fn,LandmarkMap_dic):
    PHMI=loadmat(PHMI_fn, squeeze_me=True, struct_as_record=False)
    x=loadmat(PHMI_fn)
    print(sorted(PHMI.keys()))
    
    PHMI_dic={} #提取MatLab的.fig值
    ax1=[c for c in PHMI['hgS_070000'].children if c.type == 'axes']
    if(len(ax1) > 0):
        ax1 = ax1[0]
    i=0
    for line in ax1.children:
        # print(line)
    # for object_idx in range(PHMI['hgS_070000'].children.children.shape[0]):
        # print(object_idx)
        try:
            X=line.properties.XData #good   
            Y=line.properties.YData 
            Z=line.properties.ZData
            PHMI_dic[i]=(X,Y,Z)
        except:
            pass
        i+=1
    
    # print(PHMI2_dic)
    fig= plt.figure(figsize=(130,20)) #figsize=(20,130)
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    
    ScalePhmi=math.pow(10,1)    
    plt.plot(PHMI_dic[0][1],PHMI_dic[0][0],marker=markers[0], color=colors[0],linewidth=linewidths[0])  
    ref=math.pow(10,-5)
    
    #for display clearly
    PHmiValue=PHMI_dic[1][2]
    replaceValue=np.extract(PHmiValue<ref,PHmiValue)*-math.pow(10,5)
    PHmiValue[PHmiValue<ref]=replaceValue
    plt.plot( PHMI_dic[0][1],PHmiValue*ScalePhmi,marker=markers[0], color=colors[1],linewidth=1)
    
    # plt.plot(PHMI_dic[1][2]*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    #plt.axvline(x=ref*ScalePhmi)
    plt.axhline(y=ref*ScalePhmi)
    
    plt.scatter(LandmarkMap_dic[1][1],LandmarkMap_dic[1][0],marker=markers[1], s=dotSizes[1],color=colors[2],linewidth=10)
    
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    
    return PHMI_dic
#数据类型B
def readMatLabFig_PHMI_B(PHMI_fn,LandmarkMap_dic):
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
    fig= plt.figure(figsize=(130,20)) #figsize=(20,130)
    colors=['#7f7f7f','#d62728','#1f77b4','','','']
    markers=['.','+','o','','','']
    dotSizes=[200,3000,3000,0,0,0]
    linewidths=[2,10,10,0,0,0]
    
    ScalePhmi=math.pow(10,1)
    
    plt.plot(PHMI_dic[0][1],PHMI_dic[0][0],marker=markers[0], color=colors[0],linewidth=linewidths[0])    
    
    ref=math.pow(10,-5)
    
    #for display clearly
    PHmiValue=PHMI_dic[1][2]
    replaceValue=np.extract(PHmiValue<ref,PHmiValue)*-math.pow(10,5)
    PHmiValue[PHmiValue<ref]=replaceValue
    plt.plot( PHMI_dic[0][1],PHmiValue*ScalePhmi,marker=markers[0], color=colors[1],linewidth=1)
    
    # plt.plot(PHMI_dic[1][2]*ScalePhmi, PHMI_dic[0][1],marker=markers[0], color=colors[1],linewidth=1)
    #plt.axvline(x=ref*ScalePhmi)
    plt.axhline(y=ref*ScalePhmi)
    
    plt.scatter(LandmarkMap_dic[1][1],LandmarkMap_dic[1][0],marker=markers[1], s=dotSizes[1],color=colors[2],linewidth=10)
    
    plt.tick_params(axis='both',labelsize=80)
    plt.show()
    
    return PHMI_dic

# JupyterLab Support installation web address: https://plotly.com/python/getting-started/?utm_source=mailchimp-jan-2015&utm_medium=email&utm_campaign=generalemail-jan2015&utm_term=bubble-chart
#值分布
def singleBoxplot(array):
    import plotly.express as px
    import pandas as pd
    df=pd.DataFrame(array,columns=["value"])
    fig = px.box(df, y="value",points="all")
    # fig.show() #show in Jupyter
    import plotly
    plotly.offline.plot (fig) #works in spyder

#04-split curve into continuous parts based on the jumping position 使用1维卷积的方法，在曲线跳变点切分曲线
from numpy import convolve as npConv
import seaborn as sns 
from scipy import stats
def uniqueish_color():
    return plt.cm.gist_ncar(np.random.random())
def lindexsplit(some_list, args):
    if args:
        args = (0,) + tuple(data+1 for data in args) + (len(some_list)+1,)
    my_list = []
    for start, end in zip(args, args[1:]):
        my_list.append(some_list[start:end])
    return my_list

#1维卷积切分曲线跳变点
def con_1_dim(data):
    kernel_conv=[-1,2,-1] #卷积核，类似2维提取图像的边缘
    result_conv=npConv(data,kernel_conv,'same')
    plt.figure(figsize=(130, 20))
    # print(result_conv)
    z=np.abs(stats.zscore(result_conv))
    z_=stats.zscore(result_conv)
    # print(z)
    #print(len(z))
    threshold=1
    breakPts=np.where(z > threshold)
    breakPts_=np.where(z_ < -threshold)

    con_breakPtsNeg=lindexsplit(result_conv.tolist(), breakPts_[0].tolist())
    phmi_breakPtsNeg=lindexsplit(data, breakPts_[0].tolist())
    phmi_breakIdx=lindexsplit(list(range(len(data))), breakPts_[0].tolist())
    x=lindexsplit(PHMI_dic[0][1].tolist(),breakPts_[0].tolist())

    plt.scatter(PHMI_dic[0][1], [abs(v) for v in result_conv],s=1) #[abs(v) for v in discretizeIdx]

    for idx in range(len(phmi_breakPtsNeg)-1):
        phmi_breakPtsNeg[idx+1].insert(0,phmi_breakPtsNeg[idx][-1])
    phmi_breakPtsNeg.insert(0,phmi_breakPtsNeg[0])
    
    for idx in range(len(phmi_breakIdx)-1):
        phmi_breakIdx[idx+1].insert(0,phmi_breakIdx[idx][-1])
    phmi_breakIdx.insert(0,phmi_breakIdx[0])    
    
    for idx in range(len(x)-1):
        x[idx+1].insert(0,x[idx][-1])
    x.insert(0,x[0])      
        
    #for val,idx in zip(phmi_breakPtsNeg, phmi_breakIdx):
    #根据跳变点切分的曲线赋予不同的颜色打印
    for val,idx in zip(phmi_breakPtsNeg, x):
        # print(val,idx)
        # break
        # x, y = zip(start, stop)
        plt.plot(idx, val, color=uniqueish_color())
        
    #plt.scatter(list(range(len(result_conv))), [abs(v) for v in result_conv],s=1) #[abs(v) for v in discretizeIdx]    
    
    plt.show()             
    return con_breakPtsNeg,phmi_breakPtsNeg,phmi_breakIdx,x

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.io import output_notebook, show
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6
output_notebook()

#合并landmarks，locations和曲线跳变点切分，打印
def jitterCurve():
    output_file("PHmi_01.html")
    source=ColumnDataSource(data=dict(
        x=LandmarkMap_dic[1][0].tolist(),
        y=LandmarkMap_dic[1][1].tolist(),
        desc=[str(i) for i in list(range(LandmarkMap_dic[1][0].shape[0]))],
    ))
    TOOLTIPS=[
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("desc", "@desc"),
    ]

    p=figure(plot_width=1800, plot_height=320, tooltips=TOOLTIPS,title="partition")
    p.circle('y','x',  size=5, source=source)
    p.line(PHMI_dic[0][1],PHMI_dic[0][0],line_color="coral", line_dash="dotdash", line_width=2)

    colors=('aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen')
    ScalePhmi=math.pow(10,1)
    i=0
    for val,idx in zip(phmi_breakPtsNeg, plot_x):
        p.line(idx,np.array(val)*ScalePhmi,line_color=colors[i])
        i+=1

    show(p)

#05-network show between PHMI and landmarks 网络分析
#extract landmarks corresponding to the AVs' position along a route
def scanCircleBuffer(locations,landmarks,dradius):
    landmarks_pts=[Point(coordi[0],coordi[1]) for coordi in np.stack((landmarks[0], landmarks[1]), axis=-1)]
    # print(len(landmarks_pts))
    # print(landmarks_pts)
    locations_pts=[Point(coordi[0],coordi[1]) for coordi in np.stack((locations[0], locations[1]), axis=-1)]
    # print(len(locations_pts))
    scanCircleBuffer=[pt.buffer(radius) for pt in locations_pts] #apply Shapely library
    # print(scanCircleBuffer)
    targetPts={} #landmarks characteristics
    targetPts_idx={} #build the indexes of landmarks position to the location of AV
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

#flatten function
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]     
#creat network between landmarks position and location of AV,using Networkx library
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
        G.position[i]=(pts[1],pts[0])        
        # G.targetPtsNum[LM]=(len(targetPts[key]))
        i+=1
    
    G.add_edges_from(edges)
    
    plt.figure(figsize=(130,20))
    nx.draw(G,G.position,linewidths=1,edge_color='gray')
    plt.show()
    return G
#网络交互图表
def interactiveG(G):
    from bokeh.models.graphs import NodesAndLinkedEdges,from_networkx
    from bokeh.models import Circle, HoverTool, MultiLine,Plot,Range1d,StaticLayoutProvider
    from bokeh.plotting import figure, output_file, show, ColumnDataSource
    from bokeh.io import output_notebook, show
    output_notebook()
    # We could use figure here but don't want all the axes and titles  
    #plot=Plot(plot_width=1600, plot_height=300, tooltips=TOOLTIPS,title="PHmi+landmarks+route+power(10,-5)",x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
    
    output_file("PHMI_network")
    source=ColumnDataSource(data=dict(
        x=locations[0].tolist(),
        #x=[idx for idx in range(len(PHMIList))],
        #y=locations[1].tolist(),
        y=PHMIList,
        #desc=[str(i) for i in PHMIList],
        #PHMI_value=PHMI_dic[0][0].tolist(),    
    ))
    TOOLTIPS=[
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        #("desc", "@desc"),
        #("PHMI", "$PHMI_value"),
    ]
    
    
    plot=figure(x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1),plot_width=2200, plot_height=500,tooltips=TOOLTIPS,title="PHMI_network")
    
    #G_position={key:(G.position[key][1],G.position[key][0]) for key in G.position.keys()}
    graph = from_networkx(G,nx.spring_layout,scale=1, center=(0,0))  
    #plot.renderers.append(graph) 
    
    fixed_layout_provider = StaticLayoutProvider(graph_layout=G.position)
    graph.layout_provider = fixed_layout_provider
    plot.renderers.append(graph)
    
    # Blue circles for nodes, and light grey lines for edges  
    graph.node_renderer.glyph = Circle(size=5, fill_color='#2b83ba')  
    graph.edge_renderer.glyph = MultiLine(line_color="#cccccc", line_alpha=0.8, line_width=2)  
      
    # green hover for both nodes and edges  
    graph.node_renderer.hover_glyph = Circle(size=25, fill_color='#abdda4')  
    graph.edge_renderer.hover_glyph = MultiLine(line_color='#abdda4', line_width=4)  
      
    # When we hover over nodes, highlight adjecent edges too  
    graph.inspection_policy = NodesAndLinkedEdges()  
      
    plot.add_tools(HoverTool(tooltips=None))  
     
    colors=('aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen')
    ScalePhmi=math.pow(10,1)
    i=0
    for val,idx in zip(phmi_breakPtsNeg, plot_x):
        plot.line(idx,np.array(val)*ScalePhmi,line_color=colors[i])
        i+=1    
        
    show(plot)
    
#06-single landmarks pattern 无人车位置点与对应landmarks栅格图
#convert location and corresponding landmarks to raster data format using numpy.histogram2d
def colorMesh_phmi(landmarks,locations,targetPts_idx,Phmi):
    patternValuesDic={}
    for key in targetPts_idx.keys():
        patternValuesDic[key]=[0.5]*len(targetPts_idx[key])
        patternValuesDic[key].append(0.9)
    
    patternDic={}
    for key in patternValuesDic.keys():
        patternDic[key]={"x":landmarks[0][targetPts_idx[key]],
                         "y":landmarks[1][targetPts_idx[key]],
                         "z":patternValuesDic[key]
                         }
        patternDic[key]["x"]=np.append(patternDic[key]["x"],locations[0][key])
        patternDic[key]["y"]=np.append(patternDic[key]["y"],locations[1][key])
        
    histogram2dDic={}
    binNumber=(32,32) #32,25,68,70
    for key in patternDic.keys():
        zi, yi, xi = np.histogram2d(patternDic[key]["y"], patternDic[key]["x"], bins=binNumber, weights=patternDic[key]["z"], normed=False)
        counts, _, _ = np.histogram2d(patternDic[key]["y"], patternDic[key]["x"],bins=binNumber)
        # print(counts)
        histogram2dDic[key]={"xi":xi,"yi":yi,"zi":zi,"count":counts,"ziCount":zi / counts,"ziMasked":np.ma.masked_invalid(zi)}
    
    
    for key in histogram2dDic.keys():
        xi=histogram2dDic[key]["xi"]
        yi=histogram2dDic[key]["yi"]
        zi=histogram2dDic[key]["ziMasked"]
        
        x=patternDic[key]["x"]
        y=patternDic[key]["y"]
        z=patternDic[key]["z"]
        # print(x,y,z)
        #plot it
        '''
        fig, ax = plt.subplots(figsize=(25,20))
        ax.pcolormesh(xi, yi, zi, edgecolors='black')
        scat = ax.scatter(x, y, c=z, s=30)
        fig.colorbar(scat)
        ax.margins(0.05)
        
        plt.title("PHmi_%d:%f"%(key,Phmi[key]))
        plt.show()        
        
        if key==20:
            break
        '''
    return histogram2dDic,patternDic

#show raster 
from IPython import display
from matplotlib import pyplot as plt
def use_svg_display():
    """Use svg format to display plot in jupyter"""
    display.set_matplotlib_formats('svg')    
def colorMeshShow(histogram2dDic_part,patternDic_part,Phmi_part,condi):
    use_svg_display()
    xiArray=np.array([histogram2dDic_part[key]["xi"].tolist() for key in histogram2dDic_part.keys()])
    yiArray=np.array([histogram2dDic_part[key]["yi"].tolist() for key in histogram2dDic_part.keys()])
    ziArray=np.array([histogram2dDic_part[key]["ziMasked"].tolist() for key in histogram2dDic_part.keys()])
    
    xArray=np.array([patternDic_part[key]["x"].tolist() for key in patternDic_part.keys()])
    yArray=np.array([patternDic_part[key]["y"].tolist() for key in patternDic_part.keys()])
    zArray=np.array([patternDic_part[key]["z"] for key in patternDic_part.keys()])
    
    # print(xiArray)
    
    width=int(round(math.sqrt(len(xArray)),2))  
    # print("+"*50)
    # print(width)
    fig, axs = plt.subplots(width, width, figsize=(10, 10),constrained_layout=True)
    for ax, xi, yi, zi, x, y,z,titleV,key in zip(axs.flat, xiArray,yiArray,ziArray,xArray, yArray,zArray,Phmi_part,condi):

        ax.pcolormesh(xi, yi, zi, edgecolors='black')
        scat = ax.scatter(x, y, c="r", s=15) #c=z
        fig.colorbar(scat)
        ax.margins(0.05)
        
        ax.set_title("PHmi_%d:%f"%(key,titleV))
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

    plt.show() 

#07相关性分析
#classification PHMI with percentile
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

#图表汇总，根据需要取消注释
def graphMerge(num_meanDis_DF):
    plt.clf()
    import plotly.express as px
    from plotly.offline import plot
    
    #01-draw scatter paring
    # coore_columns=["number","mean distance","PHMI"]
    # fig = px.scatter_matrix(num_meanDis_DF[coore_columns],width=1800, height=800)
    # # fig.show() #show in jupyter
    # plot(fig)
     
    #02-draw correlation using plt.matshow-A
    # Corrcoef=np.corrcoef(np.array(num_meanDis_DF[coore_columns]).transpose()) #sns_columns=["number","mean distance","PHMI"]
    # print(Corrcoef)
    # plt.matshow(num_meanDis_DF[coore_columns].corr())
    # plt.xticks(range(len(coore_columns)), coore_columns)
    # plt.yticks(range(len(coore_columns)), coore_columns)
    # plt.colorbar()
    # plt.show()    
    
    #03-draw correlation -B
    # Compute the correlation matrix
    # plt.clf()
    # corr_columns_b=["number","mean distance","PHMI"]
    # corr = num_meanDis_DF[corr_columns_b].corr()    
    corr = num_meanDis_DF.corr()  
    # # Generate a mask for the upper triangle
    # mask = np.triu(np.ones_like(corr, dtype=np.bool))    
    # # Set up the matplotlib figure
    # f, ax = plt.subplots(figsize=(11, 9))    
    # # Generate a custom diverging colormap
    # cmap = sns.diverging_palette(220, 10, as_cmap=True)    
    # # Draw the heatmap with the mask and correct aspect ratio
    # sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    #04
    # Draw a heatmap with the numeric values in each cell
    plt.clf()
    sns.set()
    f, ax = plt.subplots(figsize=(15, 13))
    sns.heatmap(corr, annot=True, fmt=".2f", linewidths=.5, ax=ax)
        
    #04-draw curves
    # plt.clf()
    # sns_columns=["number","mean distance","PHMI"]
    # sns.set(rc={'figure.figsize':(25,3)})
    # sns.lineplot(data=num_meanDis_DF[sns_columns], palette="tab10", linewidth=2.5)
   
#rpy2调用R编程，参考：https://rpy2.github.io/doc/v2.9.x/html/introduction.html
import rpy2
print(rpy2.__version__)    
from rpy2.rinterface import R_VERSION_BUILD
print(R_VERSION_BUILD)
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
#import spatial points pattern analysis
sp=importr("spatstat") #spatstat是spatial point patterns空间点格局模式分析的R扩展库，参考：《Spatial Point Patterns Methodology and Applications with R》；https://cran.r-project.org/web/packages/spatstat/index.html
# import R's "base" package
base = importr('base')
# import R's "utils" package
utils = importr('utils')     
    
import pointpats.quadrat_statistics as qs #应用PySAL的Quadrat_statistics
print(dir(qs)) #查看包括的方法
from shapely import *
from shapely.geometry import *
import libpysal as ps
import numpy as np
from pointpats import PointPattern #亦可以使用R的spatstat空间点格局模式库

#rpy2调用R语言编程，安装R扩张库
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
packnames = ('pandas2ri','r')
utils = rpackages.importr('utils')
utils.install_packages(StrVector(packnames))

from rpy2.robjects import r, pandas2ri #C:\Users\richi\conda\envs\pyG\lib\site-packages\rpy2\robjects\pandas2ri.py:17: FutureWarning: pandas.core.index is deprecated and will be removed in a future version.  The public classes are available in the top-level namespace.  from pandas.core.index import Index as PandasIndex
from pandas.core.index import Index as PandasIndex

#合并数据于dataFrame中，根据研究目的增减
def dataMerge(targetPts_idx,locations_pts):
    percentilePhmi=labelsPercentile_upgrade(Phmi)    
    
    LA_numbers=list(zip([key for key in targetPts_idx.keys()],[len(vals) for vals in targetPts_idx.values()]))
    ScalePhmi=math.pow(10,1) #scale PHMI values
    distance_single={} #存储所有位置，对应的所有landmarks距离
    distance_mean=[] #存储距离均值
    minDisList=[] #存储最小距离
    maxDisList=[] #存储最大距离
    containsResults={} #存储无人车位置点划分视角，存储每一视角存在的landmark布尔值
    containsResults_num={} #存储无人车位置点划分视角，存储每一视角存在的landmark数量
    containsResults_num_is=[] #存储视角存在landmark的数量
    containsResults_num_none=[] #存储视角不存在landmark的数量
    evenDistribution=[] #存储视角有无landmark变化，使用1维卷积的方法
    intensityPts=[] #存储landmarks二维空间点格局的intsity值，外接矩形
    intensityPts_convexHull=[] #存储landmarks二维空间点格局的intsity值，凸包
    chi2_5=[] #
    chi2_10=[]
    chi2_15=[]
    chi2_8=[]
    VMR=[]
    F_km=[]
    G_km=[]
    i=0
    def Average(lst): 
        return sum(lst) / len(lst) 
    for key in tqdm(targetPts_idx.keys()):
        distance_temp=[locations_pts[key].distance(pt) for pt in targetPts[key]]
        # print(distance_temp)
        minDisList.append(min(distance_temp))
        maxDisList.append(max(distance_temp))
        distance_single[key]=distance_temp
        distance_mean.append(Average(distance_temp))
        
        
        p=locations_pts[key]
        # print("_"*50)
        # print(p)
        lidarScanDis=25
        bufferCircle = p.buffer(lidarScanDis).boundary
        circleLen=bufferCircle.length
        
        num=36 #36
        divisionRange=np.arange(0.,circleLen,(circleLen-0)/num)
        # point = bufferCircle.interpolate(0)
        interpolationPts=[bufferCircle.interpolate(i) for i in divisionRange]
        # points = MultiPoint(interpolationPts)
        interpolationPtsPairs=list(zip(interpolationPts, interpolationPts[1:] + interpolationPts[:1]))         
        segments=[Polygon([p,i[0],i[1]]) for i in interpolationPtsPairs]
        # multiSegs=MultiPolygon(segments)
        
        # print(targetPts[key])
        containsResults[key]=[([seg.contains(pt) for pt in targetPts[key]]) for seg in segments]
        containsResults_num[key]=[val.count(True) for val in containsResults[key]]
        containsResults_num_is.append(sum(i>0 for i in containsResults_num[key]))
        containsResults_num_none.append(sum(i==0 for i in containsResults_num[key]))
        
        # print(containsResults[key])
        kernel_conv_even=[-1,2,-1]
        result_conv_even=npConv([int(i) for i in containsResults[key][0]],kernel_conv_even,'same')
        # print(result_conv_even)
        evenDistribution.append(sum([abs(v) for v in result_conv_even]))
        
        p1 = PointPattern([coordinate.coords[:][0] for coordinate in targetPts[key]])
        #Intensity based on minimum bounding box:
        intensityPts.append(p1.lambda_mbb)
        #Intensity based on convex hull:
        intensityPts_convexHull.append(p1.lambda_hull)
        
        #应用PySAL的Quadrat_statistics样方统计,亦可以替换用R的spatstat库实现，获取更多功能。参考：https://pointpats.readthedocs.io/en/latest/  https://pysal.org/notebooks/explore/pointpats/Quadrat_statistics.html
        #样方分析（Quadrat Analysis ，QA ）法是样方内点数均值变差的分析方法，是由Greig-Smith 于1964年提出的。其具体做法是用一组样方覆盖在研究区域上并作叠置分析，统计落在每一个样方上的样本数，通过统计不同的具有m 个点数的样方的个数及其频率，并与完全随机过程（Poisson 分布）对比来判断点模式的空间分布特征。其结果一般用方差均值比（V ariance-Mean Ratio ，VMR ）判断。
        #合理地确定样方的大小较为重要，一般地样方大小的确定采用符合“拇指规则（rule of thumb ）”，即样方大小应当是平均每个点所占面积的两倍. ref:《黄土丘陵沟壑区农村居民点分布模式空间统计分析——以甘谷县为例》
        q_r_10 = qs.QStatistic(p1,shape= "rectangle",nx = 10, ny = 10)
        chi2_10.append(q_r_10.chi2) #观察点模式的卡方检验统计量 chi-squared test statistic for the observed point pattern
        #By comparing the observed point counts against the expected counts and calculate a χ2 test statistic,e can decide whether to reject the null based on the position of the χ2 test statistic in the sampling distribution. ref:https://nbviewer.jupyter.org/github/pysal/pointpats/blob/master/notebooks/Quadrat_statistics.ipynb#Quadrat-Statistic
        #Complete Spatial Randomness (CSR)       
        q_r_5 = qs.QStatistic(p1,shape= "rectangle",nx = 5, ny = 5)
        chi2_5.append(q_r_5.chi2)
        
        q_r_15 = qs.QStatistic(p1,shape= "rectangle",nx =15, ny = 15)
        chi2_15.append(q_r_15.chi2)
        
        q_r_8 = qs.QStatistic(p1,shape= "rectangle",nx =8, ny = 8)
        chi2_8.append(q_r_8.chi2)
        
        # print(targetPts[key][0].coords[:])
        # print(targetPts[key])
        #建立Landmarks的坐标点dataframe用于R下的计算
        pts_df=pd.DataFrame(zip([pt.coords[:][0][0] for pt in targetPts[key]],[pt.coords[:][0][1] for pt in targetPts[key]]),columns=["x","y"])
        # print("+"*50)
        # print(pts_df)
        # print(min(pts_df.x),max(pts_df.x))
        # print(min(pts_df.y),max(pts_df.y))
        r_vals=r_cal_b(pts_df) #使用R的spatstat计算空间点格局模式，本次计算Variance/Mean Ratio (VMR)方差均值比, ref:https://rspatial.org/raster/analysis/8-pointpat.html
        r2p=pandas2ri.ri2py(r_vals) #将R数据格式（list）转换为python数据格式
        F_km.append(r2p[1][0])
        G_km.append(r2p[2][0])
        VMR.append(r2p[0][0])
        
        
        # VMR.append(vmr_single[0])

        # if i==0:break
        # i+=1
    #建立dataFrame,汇集数据   
    num_meanDis_DF=pd.DataFrame(zip([num[1] for num in LA_numbers],distance_mean,Phmi*ScalePhmi,PHMI_dic[0][0],PHMI_dic[0][1],percentilePhmi),columns=["number","mean distance","PHMI","X","y","percentilePhmi"])
    num_meanDis_DF["minDistance"]=minDisList
    num_meanDis_DF["maxDistance"]=maxDisList
    num_meanDis_DF["direction_is"]=containsResults_num_is
    num_meanDis_DF["direction_none"]=containsResults_num_none
    num_meanDis_DF["evenDistribution"]=evenDistribution
    num_meanDis_DF["intensityPts"]=intensityPts
    num_meanDis_DF["intensityPts_hull"]=intensityPts_convexHull
    num_meanDis_DF["chi2_10"]=chi2_10
    num_meanDis_DF["chi2_5"]=chi2_5
    num_meanDis_DF["chi2_15"]=chi2_15
    num_meanDis_DF["chi2_8"]=chi2_8
    num_meanDis_DF["VMR"]=VMR
    num_meanDis_DF["F_km"]=F_km
    num_meanDis_DF["G_km"]=G_km
    
    
    return num_meanDis_DF  

#应用R语言及其库spatstat分析空间点格局模式，具体内容将在之后对应空间点格局模式研究中详细说明
#ref:《Spatial Point Patterns Methodology and Applications with R》；https://cran.r-project.org/web/packages/spatstat/index.html
def r_cal_b(df):
    robjects.r('''
        # create a function `f`
        f <- function(df, verbose=FALSE) {
            if (verbose) {
                cat("I am calling f().\n")
            }          
            xMin<-min(df$x)
            xMax<-max(df$x)
            yMin<-min(df$y)
            yMax<-max(df$y)
            
            xy_PPP <- with(df, ppp(x, y, c(xMin,xMin+50), c(yMin,yMin+50)))            
            #xy_PPP <- with(df, ppp(x, y, c(xMin,xMax), c(yMin,yMax)))
            #xy_PPP <- with(df, ppp(x, y, c(-25,25), c(-25,25)))
            #plot(xy_PPP)
            
            xy=df
            summary(xy)
            xy <- unique(xy)
            xy<-data.matrix(xy)
            # mean center
            mc <- apply(xy, 2, mean)   
            # standard distance
            sd <- sqrt(sum((xy[,1] - mc[1])^2 + (xy[,2] - mc[2])^2) / nrow(xy))
            #study area
            buffer_area=50*50
            #Density
            dens <- nrow(xy) / buffer_area
            library(spatstat)
            win<-owin(c(-25,25), c(-25,25))

            #弃之，python下无法安装rspatial，R环境下可以
            #library(devtools)
            #if (!require("rspatial")) devtools::install_github('rspatial/rspatial')
            #remotes::install_github("rspatial/rspatial")
            #devtools::install_github("rspatial/rspatial")
            #devtools::install_github("rstudio/sparkapi")
            
            #library(rspatial)
            #r <- raster(win)
            #样方统计
            quadrat_C<-quadratcount(xy_PPP,nx=5,ny=5)
            #plot(quadrat_C)
            # number of quadrats
            quadrats <- sum(quadrat_C)
            f<-table(quadrat_C)
            f<-data.frame(f)
            # number of cases
            cases <- sum(as.integer(f$quadrat_C) * f$Freq)
            mu <- cases / quadrats
            
            ff <- data.frame(as.integer(f$quadrat_C),f$Freq)
            colnames(ff) <- c('K', 'X')
            ff$Kmu <- ff$K - mu
            ff$Kmu2 <- ff$Kmu^2
            ff$XKmu2 <- ff$Kmu2 * ff$X
            #The observed variance s2 is
            s2 <- sum(ff$XKmu2) / (sum(ff$X)-1)
            #the VMR is
            VMR <- s2 / mu
            
            #Estimators of the empty-space function F(r)
            Fs<-Fest(xy_PPP)
            #plot(Fs)
            F_km<-mean(Fs$km)
            
            #nearest-neighbour function G(r)
            Gs<-Gest(xy_PPP)
            G_km<--mean(Gs$km)
            
            newlist<-list(VMR,F_km,G_km)
            return(newlist)
        
            #return(VMR)
        }
        ''')
    r_f = robjects.r['f']
    pandas2ri.activate()
    r_DF=pandas2ri.py2ri(df[["x","y"]]) #将python下的dataFrame转换为R下的data.frame,传入R语言，即robjects.r（）定义的函数

    res = r_f(r_DF)#返回R语言计算的结果
    # print("+"*50)
    # print(res)
    return res

#类似robjects.r（）的方法，调用R语言
def r_cal(df):
    string = """
    ptsPPP <- function(df) {
        X <- with(df, ppp(x, y, c(-25,25), c(-25,25)))
        plot(X)
        return(X)
    }
    """
    sp = SignatureTranslatedAnonymousPackage(string, "powerpack")   
    pandas2ri.activate()
    r_num_meanDis_DF=pandas2ri.py2ri(df[["x","y"]])
    ptsPPP=sp.ptsPPP(r_num_meanDis_DF)
    # print("+"*50)
    # print(ptsPPP)
    # return ptsPPP


if __name__ == "__main__":
    #01   
    LandmarkMap_dic=readMatLabFig_LandmarkMap(LandmarkMap_fn)
    try:
        PHMI_dic=readMatLabFig_PHMI_A(PHMI_fn,LandmarkMap_dic)
        print("applied type -A")
    except ExceptionType1:
        PHMI_dic=readMatLabFig_PHMI_B(PHMI_fn,LandmarkMap_dic)
        print("applied type -B")
    except ExceptionType2:
        print("datatype error!!!")
        
    #03
    Phmi=PHMI_dic[1][2]
    singleBoxplot(Phmi) 
    
    #04
    PHMIList=PHMI_dic[1][2].tolist()
    con_breakPtsNeg,phmi_breakPtsNeg,phmi_breakIdx,plot_x=con_1_dim(PHMIList)
    jitterCurve()
    
    #05
    locations=PHMI_dic[0] #the coordinates of AV
    landmarks=LandmarkMap_dic[1] #无distribution feature of landmarks
    radius=25 # scanning area of on_board lidar
    targetPts,locations_pts,targetPts_idx=scanCircleBuffer(locations,landmarks,radius)
    
    G=location_landmarks_network(targetPts_idx,locations,landmarks)
    
    #06
    #Sets the number of locations to display
    condi={i for i in range(20)}
    histogram2dDic_part={key: histogram2dDic[key] for key in histogram2dDic.keys() & condi} 
    patternDic_part={key:patternDic[key] for key in patternDic.keys() & condi} 
    Phmi_part=[Phmi[i] for i in condi]
    colorMeshShow(histogram2dDic_part,patternDic_part,Phmi_part,condi)
    
    #07
    num_meanDis_DF=dataMerge(targetPts_idx,locations_pts)
    graphMerge(num_meanDis_DF)