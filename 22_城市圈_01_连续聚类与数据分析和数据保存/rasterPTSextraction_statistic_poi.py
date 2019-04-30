# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 12:27:47 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import base
from sklearn import cluster,covariance, manifold
from scipy.stats import chi2_contingency
from matplotlib.collections import LineCollection

import gdal, ogr, os,osr
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import Subplot
from tqdm import tqdm
import time
from sklearn import cluster
import math
from collections import Counter #用于一些特殊数据统计，以及实现了些方便实用的数据结构
from sklearn import preprocessing
from pylab import mpl
import conversionofCoordi as cc

mpl.rcParams['font.sans-serif']=['STXihei']

gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES");  #解决目录中文乱码
gdal.SetConfigOption("SHAPE_ENCODING", "CP936");  #解决属性表中文乱码


'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
def filePath(dirpath,fileType):
    fileInfo={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       #print(i,'\n')
       #print(dirpath,'\n',dirNames,'\n',fileNames,'\n')
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           #if not tempList :
               #print(i,"NULL")
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               fileInfo.setdefault(dirpath,tempList)
    return fileInfo 

'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]

'''提取分析所需数据，并转换为skleran的bunch存储方式，统一格式，方便读取。注意poi行业分类类标的设置'''
def jsonDataFilter(fileInfo):   #传入数据，面向不同的数据存储方式，需要调整函数内读取的代码
    rootPath=list(fileInfo.keys())  #待读取数据文件的根目录
#    print(rootPath)
    dataName=flatten_lst(list(fileInfo.values()))  #待读取数据文件的文件名列表
#    print(dataName)
    coodiDic=[]
    for fName in dataName:  #逐一读取json数据格式文件，并将需要数据存储于列表中，本次实验数据为poi的经纬度信息和一级行业分类名，注意使用了百度坐标系，未转换为WGS84.    
        f=open(os.path.join(rootPath[0],fName))
        jsonDecodes=json.load(f)
        coodiDic.append([(coordi['location']['lat'],coordi['location']['lng'],fName[:-5]) for coordi in jsonDecodes])
        coodiDic=flatten_lst(coodiDic) #读取的数据多层嵌套，需展平处理。       
#    print(coodiDic)
    data=np.array([(v[0],v[1]) for v in coodiDic])  #经纬度信息
    targetNames=np.array([v[2] for v in coodiDic])  #一级分类
#    print(data)
#    print(targetNames)
    class_label=LabelEncoder()  #以整数形式编码一级分类名
    targetLabel=class_label.fit_transform(targetNames)
    class_mapping=[(idx,label) for idx,label in enumerate(class_label.classes_)]  #建立一级分类名和整数编码的映射列表
#    print(class_mapping)
    dataBunch=base.Bunch(DESCR=r'spatial points datasets of poi',data=data,feature_names=["XCoordinate","yCoordinate"],target=targetLabel,target_names=class_mapping)  #建立sklearn的数据存储格式bunch
    return dataBunch,class_mapping  #返回bunch格式的数据和分类名映射列表

'''独立性检验(列联表)与poi空间分布结构'''
def contingencyTableChi2andPOISpaceStructure(dataBunch,pred,class_mapping,dbLabel,savefigFn):
    '''独立性检验'''
    mergingData=np.hstack((pred.reshape(-1,1),dataBunch.target.reshape(-1,1)))  #水平组合聚类预测值和行业分类类标
    targetStack=[]
    for i in range(len(np.array(class_mapping)[...,0])): #按行业类标重新组织数据，每行对应行业类标所有的聚类预测值
        targetStack.append(mergingData[mergingData[...,-1]==int(np.array(class_mapping)[...,0][i])]) 
    clusterFrequency={}
    for p in targetStack:  #按行业类标计算每类所有点所属聚类簇的数量(频数)
        clusterFrequency[(p[...,-1][0])]=[(j,np.sum(p[...,0]==int(j))+1) for j in dbLabel if j!=-1] #独立性检验值不能为零，因此将所有值+1
#    print(clusterFrequency)  
    CTableTarget=list(clusterFrequency.keys())
    CTableIdx=np.array(list(clusterFrequency.values()))
    CTable=CTableIdx[...,1]  #建立用于独立性分析的列联表，横向为行业类所属聚类簇频数，纵向为行业类标
    totalIndependence=chi2_contingency(CTable)  #列联表的独立性检验   
    g, p, dof, expctd=totalIndependence #提取卡方值g，p值，自由度dof和与元数据数组同维度的对应理论值。此次实验计算p=0.00120633349692，小于0.05，因此行业分类与聚类簇相关。
    print(g, p, dof)  

    '''poi的空间分布结构。参考官方案例Visualizing the stock market structure：http://scikit-learn.org/stable/auto_examples/applications/plot_stock_market.html#sphx-glr-auto-examples-applications-plot-stock-market-py'''
    #A-协方差逆矩阵(精度矩阵)。The matrix inverse of the covariance matrix, often called the precision matrix, is proportional to the partial correlation matrix. It gives the partial independence relationship. In other words, if two features are independent conditionally on the others, the corresponding coefficient in the precision matrix will be zero。来自官网说明摘录
    edge_model=covariance.GraphLassoCV()   #稀疏逆协方差估计器GraphLassoCV()，翻译有待数学专业确认。官网解释：http://scikit-learn.org/stable/modules/covariance.html#sparse-inverse-covariance    
    X=CTable.copy().T    
    print(X,X.shape)
    X=X/X.std(axis=0)  #标准化。可以自行实验小规模数组，查看变化，分析结果，获取结论。
    print(X)
    edge_model.fit(X)
    print("******************************************************************")
    print(edge_model.covariance_.shape)
    
    #B-affinity_propagation(AP)聚类算法是基于数据点间"信息传递"的一种聚类算法，不用预先给出cluster簇数。聚类协方差矩阵
    _, labels=cluster.affinity_propagation(edge_model.covariance_)
    n_labels=labels.max()
    print(labels)
    
    #C-Manifold中的降维方法可以能够处理数据中的非线性结构信息。具体可以查看官网http://scikit-learn.org/stable/modules/manifold.html#locally-linear-embedding。降维的目的是降到2维，作为xy坐标值，在二维图表中绘制为点。
    node_position_model=manifold.LocallyLinearEmbedding(n_components=2, eigen_solver='dense', n_neighbors=6)
    embedding=node_position_model.fit_transform(X.T).T
    print(embedding.shape)
    
    '''图表可视化poi空间分布结构'''
    plt.figure(1, facecolor='w', figsize=(10, 8))
    plt.clf()
    ax=plt.axes([0., 0., 1., 1.]) #可以参考官方示例程序 http://matplotlib.org/examples/pylab_examples/axis_equal_demo.html
    plt.axis('off')    
    
    # Display a graph of the partial correlations/偏相关分析:在多要素所构成的系统中，当研究某一个要素对另一个要素的影响或相关程度时，把其他要素的影响视作常数（保持不变），即暂时不考虑其他要素影响，单独研究两个要素之间的相互关系的密切程度，所得数值结果为偏相关系数。在多元相关分析中，简单相关系数可能不能够真实的反映出变量X和Y之间的相关性，因为变量之间的关系很复杂，它们可能受到不止一个变量的影响。这个时候偏相关系数是一个更好的选择。
    partial_correlations=edge_model.precision_.copy()
    print(partial_correlations.shape)
#    print(partial_correlations)
    d=1/np.sqrt(np.diag(partial_correlations)) #umpy.diag()返回一个矩阵的对角线元素，计算该元素平方根的倒数。
    partial_correlations*=d
    partial_correlations*=d[:, np.newaxis]
    non_zero=(np.abs(np.triu(partial_correlations, k=1)) > 0.02) #np.triu()返回矩阵的上三角矩阵。
    
    # Plot the nodes using the coordinates of our embedding    
    plt.scatter(embedding[0], embedding[1], s=300*d**2, c=labels,cmap=plt.cm.Spectral) #簇类标用于定义节点的颜色，降维后数据作为点坐标
    
    # Plot the edges
    start_idx, end_idx=np.where(non_zero)  #numpy.where(condition[, x, y])这里x,y是可选参数，condition是条件，这三个输入参数都是array_like的形式；而且三者的维度相同。当conditon的某个位置的为true时，输出x的对应位置的元素，否则选择y对应位置的元素；如果只有参数condition，则函数返回为true的元素的坐标位置信息；
    segments=[[embedding[:, start], embedding[:, stop]] for start, stop in zip(start_idx, end_idx)]
    values=np.abs(partial_correlations[non_zero])
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(len(segments))
    print(len(values))
    cm=plt.cm.get_cmap('OrRd') #具体的`matplotlib.colors.Colormap'实例可以查看matplotlib官网 http://matplotlib.org/users/colormaps.html，替换不同色系
    lc=LineCollection(segments,zorder=0,cmap=cm,norm=plt.Normalize(0, .7 * values.max()))  
    lc.set_array(values) 
    lc.set_linewidths(15 * values) #定义边缘的强度。
    ax.add_collection(lc)
    
    # Add a label to each node. The challenge here is that we want to position the labels to avoid overlap with other labels，添加行业分类标签，并避免标签重叠。
    names=[i[-1] for i in class_mapping]
    for index, (name, label, (x, y)) in enumerate(zip(names, labels, embedding.T)):    
        dx = x - embedding[0]
        dx[index] = 1
        dy = y - embedding[1]
        dy[index] = 1
        this_dx = dx[np.argmin(np.abs(dy))]
        this_dy = dy[np.argmin(np.abs(dx))]
        if this_dx > 0:
            horizontalalignment = 'left'
            x = x + .002
        else:
            horizontalalignment = 'right'
            x = x - .002
        if this_dy > 0:
            verticalalignment = 'bottom'
            y = y + .002
        else:
            verticalalignment = 'top'
            y = y - .002
        plt.text(x, y, name, size=10,horizontalalignment=horizontalalignment,verticalalignment=verticalalignment,bbox=dict(facecolor='w',edgecolor=plt.cm.Spectral(label/float(n_labels)),alpha=.6))    
    plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),embedding[0].max() + .10 * embedding[0].ptp(),) #numpy.ptp()极差函数返回沿轴的值的范围(最大值-最小值)。
    plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),embedding[1].max() + .03 * embedding[1].ptp())    
    plt.savefig(os.path.join(savingFig,savefigFn))  #保存打印的图表
    plt.show()   
    return CTable,np.array(partial_correlations)

'''将聚类的POI数据，写入.shp文件，用于GIS调用。'''
def point2Shp(poiBunch,valueArray,fn,pt_lyrName_w,ref_lyr=False):
    ds=ogr.Open(fn,1)
#    '''参考层，用于空间坐标投影，字段属性等参照'''
#    ref_lyr=ds.GetLayer(ref_lyr)
#    ref_sr=ref_lyr.GetSpatialRef()
#    print(ref_sr)
#    ref_schema=ref_lyr.schema #查看属性表字段名和类型
#    for field in ref_schema:
#        print(field.name,field.GetTypeName())     
        
    '''建立新的datasource数据源'''
    sf_driver=ogr.GetDriverByName('ESRI Shapefile')
    sfDS=os.path.join(fn,r'sf')
#    if os.path.exists(sfDS):
#        sf_driver.DeleteDataSource(sfDS)
    pt_ds=sf_driver.CreateDataSource(sfDS)
    if pt_ds is None:
        sys.exit('Could not open{0}'.format(sfDS))
        
    '''建立新layer层'''    
    if pt_ds.GetLayer(pt_lyrName_w):
        pt_ds.DeleteLayer(pt_lyrName_w)    
       
    spatialRef = osr.SpatialReference()
    spatialRef.SetWellKnownGeogCS("WGS84") #需要注意直接定义大地坐标未"WGS84"，而未使用参考层提取的坐标投影系统
    
    pt_lyr=pt_ds.CreateLayer(pt_lyrName_w,spatialRef,ogr.wkbPoint)    
#    pt_lyr=pt_ds.CreateLayer(pt_lyrName_w,ref_sr,ogr.wkbPoint)  

    '''配置字段，名称以及类型和相关参数'''
#    pt_lyr.CreateFields(ref_schema)
    LatFd=ogr.FieldDefn("origiLat",ogr.OFTReal)
    LatFd.SetWidth(20)
    LatFd.SetPrecision(3)
    pt_lyr.CreateField(LatFd)
    LatFd.SetName("origiLong")
    pt_lyr.CreateField(LatFd)
    
#    pt_lyr.CreateFields(ref_schema)
    preFd=ogr.FieldDefn("poi",ogr.OFTInteger)
    pt_lyr.CreateField(preFd)
    preFd.SetName("cluster")
    pt_lyr.CreateField(preFd)
    
#    stationName=ogr.FieldDefn("stationN",ogr.OFTString)
#    pt_lyr.CreateField(stationName)    
    
#    preFd.SetName("ObservTime")
#    pt_lyr.CreateField(preFd)  
#   
     
    '''建立feature空特征和设置geometry几何类型'''
    print(pt_lyr.GetLayerDefn())
    pt_feat=ogr.Feature(pt_lyr.GetLayerDefn())    
   
#    idx=0
    for i in tqdm(range(valueArray.shape[0])):  #循环feature         
#        print(key)
        '''设置几何体'''
        #pt_ref=feat.geometry().Clone()
        converCoordiGCJ=cc.bd09togcj02(dataBunch.data[i][1],dataBunch.data[i][0])
        converCoordiGPS84=cc.gcj02towgs84(converCoordiGCJ[0],converCoordiGCJ[1])
#        print(wdCoordiDicSingle[key][1],wdCoordiDicSingle[key][0])
#        print(converCoordiGPS84[0], converCoordiGPS84[1])
        wkt="POINT(%f %f)" %  (converCoordiGPS84[0], converCoordiGPS84[1])
#        wkt="POINT(%f %f)" %  (dataBunch.data[i][0], dataBunch.data[i][1])
        newPt=ogr.CreateGeometryFromWkt(wkt) #使用wkt的方法建立点
        pt_feat.SetGeometry(newPt)
        '''设置字段值'''
#        for i_field in range(feat.GetFieldCount()):
#            pt_feat.SetField(i_field,feat.GetField(i_field))
        pt_feat.SetField("origiLat",dataBunch.data[i][0])
        pt_feat.SetField("origiLong",dataBunch.data[i][1])
        
        
#        print(wdDicComplete[key]['20140901190000'])
        pt_feat.SetField("poi",int(dataBunch.target[i])) #
        pt_feat.SetField("cluster",int(valueArray[i]))
#        print(idx,int(valueArray[idx]),pt_ref.GetX())
#        idx+=1
        
        '''根据设置的几何体和字段值，建立feature。循环建立多个feature特征'''
        pt_lyr.CreateFeature(pt_feat)    
    del ds       

'''DBSCAN基于密度空间的聚类，聚类所有poi特征点'''
def affinityPropagationForPoints(dataArray,epsValue):
    print("--------------------Clustering")
    data=dataArray
    t1=time.time()     
    db=cluster.DBSCAN(eps=epsValue,min_samples=3,metric='euclidean') #meter=degree*(2 * math.pi * 6378137.0)/ 360  degree=50/(2 * math.pi * 6378137.0) * 360，在调参时，eps为邻域的距离阈值，而分析的数据为经纬度数据，为了便于调参，可依据上述公式可以在米和度之间互相转换，此时设置eps=0.0008，约为90m，如果poi的空间点之间距离在90m内则为一簇；min_samples为样本点要成为核心对象所需要的邻域样本数阈值。参数需要自行根据所分析的数据不断调试，直至达到较好聚类的结果。
    y_db=db.fit_predict(data)  #获取聚类预测类标
    t2=time.time()    
    tDiff_af=t2-t1 #用于计算聚类所需时间
    print(tDiff_af)
    
    pred=y_db  
    print(pred,len(np.unique(pred)))  #打印查看预测类标和计算聚类簇数
    
#    t3=time.time()
#    plt.close('all')
#    plt.figure(1,figsize=(20,20))
#    plt.clf()
#    cm=plt.cm.get_cmap('nipy_spectral')  #获取内置色带
#    plt.scatter(data[...,0],data[...,1],s=10,alpha=0.8,c=pred,cmap=cm) #c参数设置为预测值，传入色带，根据c值显示颜色
#    plt.show()
#    t4=time.time()
#    tDiff_plt=t4-t3  #计算图表显示时间
#    print(tDiff_plt)
    print("-------------------cluster Finishing")
    return pred,np.unique(pred)  #返回DBSCAN聚类预测值。和簇类标

'''绘制箱型图和小提琴图'''
def violinPlot(all_data,eps):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18*2, 8*2))
    # plot violin plot
    axes[0].violinplot(all_data,showmeans=False,showmedians=True)
    axes[0].set_title('Violin plot',fontsize=30)
    
    # plot box plot
    axes[1].boxplot(all_data,flierprops={'marker':'o','markerfacecolor':'red','color':'black'})
    axes[1].set_title('Box plot',fontsize=30)
   
    # adding horizontal grid lines
    for ax in axes:
        ax.yaxis.grid(True)
        ax.set_xticks([y + 1 for y in range(len(all_data))])
        ax.set_xlabel('聚类距离',fontsize=30)
        ax.set_ylabel('聚类频数(标准化)',fontsize=30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=20)
        
    # add x-tick labels
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data)) if y%2==0],xticklabels=[eps[i] for i in range(len(eps)) if i%2==0])
    fig.autofmt_xdate()
#    plt.tick_params(labelsize=20)
#    plt.rcParams('font.sans-serif')=['STXihei'] #在开始已经设置mpl.rcParams['font.sans-serif']=['STXihei']，因此此处可忽略
    plt.savefig(os.path.join(savingFig,"violinPlot"))
    plt.show()

'''绘制折线图'''
def lineGraph(all_data,eps):
    fig = plt.figure(1, (18*2, 9*2))
    ax = Subplot(fig, 111)  
    fig.add_subplot(ax)

    ax.plot(eps,all_data, 'ro-',label='POI聚类总数')
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)
    ax.set_xlabel('聚类距离',fontsize=30)
    ax.set_ylabel('聚类总数',fontsize=30)
    ax.tick_params(labelsize=20)
    
    plt.legend()
    plt.savefig(os.path.join(savingFig,"lineGraph"))
    plt.show()

'''批量计算'''
def loopCalculate(xyzArray,eps,fn):
    robustScaleList=[]
    totalNumber=[]
    CTableDic={}
    partialCorrelationsList=[]
    counter=0
    
    #逐一计算所有距离的聚类
    for i in eps:        
        pred,predLable=affinityPropagationForPoints(xyzArray,i) #聚类计算，返回预测值及簇类标

        pt_lyrName_w=r'%s_POI'%i #字符串格式化输出文件名
        point2Shp(dataBunch,pred,fn,pt_lyrName_w) 
        print("%s has been written to disk"%i)

        counterData=Counter(pred)   #聚类簇类标频数统计
#        print(counterData)
        counterValue=np.array(list(counterData.values()))
        cvFloat=counterValue.astype(float)
        robustScale=preprocessing.robust_scale(cvFloat.reshape(-1,1))  #如果数据中含有异常值，那么使用均值和方差缩放数据的效果并不好，因此用preprocessing.robust_scale()缩放带有outlier的数据 
        cvF=robustScale.ravel() #展平，注意numpy的ravel() 和 flatten()函数的区别
        robustScaleList.append(cvF)        
        totalNumber.append(len(predLable)) #预测类标的数量
        
        CTable,partial_correlations=contingencyTableChi2andPOISpaceStructure(dataBunch,pred,class_mapping,predLable,pt_lyrName_w) #返回列联表与偏相关分析
        CTableDic[counter]=CTable
        counter+=1
        partialCorrelationsList.append(partial_correlations)
        
    return robustScaleList,totalNumber,CTableDic,partialCorrelationsList #返回所有计算距离：1.缩放后的聚类簇类标频数统计 2.预测类标的数量 3.列联表 4.偏相关分析

'''使用numpy保存与读取数据'''
def savingData(fp,fn,data):
    np.save(os.path.join(fp,fn),data) #保存一个数组到一个二进制的文件中,保存格式是.npy
    
def savingDataZ(fp,fn,data):
    np.savez(os.path.join(fp,fn),dic=data)   #保存多个数组到同一个文件中,保存格式是.npz,可以同时保持字典

#读取numpy保存的数据    
def readingData(fp,fn):
    readedData=np.load(os.path.join(fp,fn+".npy"))
    return readedData
def readingDataz(fp,fn):
    readedData=np.load(os.path.join(fp,fn+".npz"))
    return readedData


if __name__=="__main__":  
    #reading POI .json
    dirpath=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\data\xianPOI_36' #爬取的百度POI数据
    fileType=["json"] #读取指定的文件格式
    fileInfo=filePath(dirpath,fileType) #文件夹名为键，值为包含该文件夹下所有文件名的列表
#    print(fileInfo)
    dataBunch,class_mapping=jsonDataFilter(fileInfo) #提取分析所需数据，并转换为skleran的bunch存储方式
    xyzArray=dataBunch.data 
    xyzArray=xyzArray*(2 * math.pi * 6378137.0)/ 360 #如果读取的是度，将其转换为距离单位
#    print(xyzArray)

    # clustering   
    fn=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\results'  #工作路径，存储生成的.shp地理信息文件
    savingFig=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\figure' #存储数据分析的图表-POI空间分布结构，.jpg格式
    eps=list(range(20,520,10)) #设置多个聚类距离，因为已经将经纬度转换为了米制距离单位，因此不用如下行代码处理
#    eps=np.array(list(range(20,520,200)))/(2 * math.pi * 6378137.0) * 360
    robustScaleList,totalNumber,CTableDic,partialCorrelationsList=loopCalculate(xyzArray,eps,fn) #循环计算，
    
    #绘制图表，观察数据变化
    violinPlot(robustScaleList,eps) #绘制箱型图/小提琴图
    lineGraph(totalNumber,eps) #绘制折线图/曲线图

    #saving data
    savingFp=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\results_data' #将数据保存到硬盘中，便于日后使用，减少重复计算时间
    
    savingFn=r'POI_violin'
    tempData=robustScaleList
    savingData(savingFp,savingFn,tempData)    
    X=readingData(savingFp,savingFn)
   
    savingData(savingFp,"POI__LineGraph",totalNumber)  
    Y=readingData(savingFp,"POI__LineGraph")
    savingData(savingFp,"POI__eps",eps)  
    Z=readingData(savingFp,"POI__eps")
    
    savingDataZ(savingFp,"POI__CTable",CTableDic)  
    A=readingDataz(savingFp,"POI__CTable")["dic"]
    savingData(savingFp,"POI__partialCorrelations",partialCorrelationsList)  