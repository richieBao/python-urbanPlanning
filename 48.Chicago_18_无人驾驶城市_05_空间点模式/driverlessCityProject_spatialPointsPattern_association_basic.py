# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:56:09 2020

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
import copy
from statistics import mean 
from numpy import convolve as npConv
import seaborn as sns 
from scipy import stats

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.io import output_notebook, show
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral6
output_notebook()

from IPython import display

getcontext().prec = 28
np.set_printoptions(precision=28)

'''A:basic
1.read data and show
2.box plot shows the distribution of values
3.split curve to several parts based on jump points
4.network between the locations of car and the corresponding landmarks
5.raster pattern to show points pattern at each epoch
'''
#flatten function
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst] 
#01-read coordinates data of landmarks 读取landmarks坐标值
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

#02-read PHMI values for evaluation of AVs' on-board lidar navigation 读取PHMI值
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

#03-split curve into continuous parts based on the jumping position 使用1维卷积的方法，在曲线跳变点切分曲线
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
def con_1_dim(data,loc_x):
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
    x=lindexsplit(loc_x.tolist(),breakPts_[0].tolist())

    plt.scatter(loc_x, [abs(v) for v in result_conv],s=1) #[abs(v) for v in discretizeIdx]

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

#合并landmarks，locations和曲线跳变点切分，打印
def jitterCurve(phmi_breakPtsNeg,landmarks_coordi,PHMI_coordi,plot_x): #LandmarkMap_dic,PHMI_dic
    output_file("PHmi_01.html")
    source=ColumnDataSource(data=dict(
        x=landmarks_coordi[0].tolist(),
        y=landmarks_coordi[1].tolist(),
        desc=[str(i) for i in list(range(landmarks_coordi[0].shape[0]))],
    ))
    TOOLTIPS=[
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("desc", "@desc"),
    ]

    p=figure(plot_width=1800, plot_height=320, tooltips=TOOLTIPS,title="partition")
    p.circle('y','x',  size=5, source=source)
    p.line(PHMI_coordi[1],PHMI_coordi[0],line_color="coral", line_dash="dotdash", line_width=2)

    colors=('aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen')
    colors=colors*5
    ScalePhmi=math.pow(10,1)
    i=0
    for val,idx in zip(phmi_breakPtsNeg, plot_x):
        p.line(idx,np.array(val)*ScalePhmi,line_color=colors[i])
        i+=1

    show(p)

#04-network show between PHMI and landmarks 网络分析
#extract landmarks corresponding to the AVs' position along a route
def scanCircleBuffer(locations,landmarks,radius):
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
    
#05-single landmarks pattern 无人车位置点与对应landmarks栅格图
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


if __name__ == "__main__":
    #merge data together
    dataPath=[
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_LM.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\06\04-10-2020_312LM_PHMI.fig" },
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_LM.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\05\04-10-2020_PHMI.fig"},
        {"landmark":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\LM.fig",
          "phmi":r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\phmi_Data_Analysis\data\02\PHMI.fig"},
        # {"landmark":,
        #  "phmi":  },
        ]   
    i=0
    for dat in dataPath:
        landmarks_fn=dat["landmark"]
        phmi_fn=dat["phmi"]
        #01   
        LandmarkMap_dic=readMatLabFig_LandmarkMap(landmarks_fn)
        try:
            PHMI_dic=readMatLabFig_PHMI_A(phmi_fn,LandmarkMap_dic)
            print("applied type -A")
        except:
            PHMI_dic=readMatLabFig_PHMI_B(phmi_fn,LandmarkMap_dic)
            print("applied type -B")    
        #-01    
        Phmi=PHMI_dic[1][2]         
        #-03
        PHMIList=PHMI_dic[1][2].tolist()
        con_breakPtsNeg,phmi_breakPtsNeg,phmi_breakIdx,plot_x=con_1_dim(PHMIList,PHMI_dic[0][1])
        
        landmarks_coordi=LandmarkMap_dic[1]
        PHMI_coordi=PHMI_dic[0]
        
        jitterCurve(phmi_breakPtsNeg,landmarks_coordi,PHMI_coordi,plot_x)
        #04
        locations=PHMI_dic[0] #the coordinates of AV
        landmarks=LandmarkMap_dic[1] #无distribution feature of landmarks
        radius=25 # scanning area of on_board lidar
        targetPts,locations_pts,targetPts_idx=scanCircleBuffer(locations,landmarks,radius)
        
        G=location_landmarks_network(targetPts_idx,locations,landmarks)
        #05
        histogram2dDic,patternDic=colorMesh_phmi(landmarks,locations,targetPts_idx,Phmi)
        #Sets the number of locations to display
        condi={i for i in range(20)}
        histogram2dDic_part={key: histogram2dDic[key] for key in histogram2dDic.keys() & condi} 
        patternDic_part={key:patternDic[key] for key in patternDic.keys() & condi} 
        Phmi_part=[Phmi[i] for i in condi]
        colorMeshShow(histogram2dDic_part,patternDic_part,Phmi_part,condi)
        
        if i==0:break
        i+=1            
                
    
    