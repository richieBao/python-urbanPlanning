# 26-30_城市热环境_01-05_基于LST（Land surface temperature）
在探索地表温度在学科领域的应用时，发现大部分的研究在分析地表温度和土地利用途径（地表覆盖）时，
偏向于分析剖面温度或者计算多个缓冲区的平均温度变化来探索之间的关系，但是未落到具体的区域中去，对指导规划的落地性较弱。因此开展了该方向的部分探索，并写下不少代码，不仅方便数据处理，而且探索了一些新的方法。其中包括基于地表温度差值数量变化界定全区植被降温效应的空间分布，基于卷积温度梯度变化界定冷区和热区的空间分布结构和基于机器学习回归算法建立用于绿地规划评估的地表温度预测模型等方法。

代码在Github上分享，希冀能够带动在该方向的探索者以更进一步的研究。

涉及代码的内容详细列于下：
## LST.py

### 基础类 class AUXILIARY:
  1. 配置工作环境/def __init__(self,dataPath='',resultsPath=''):
  2. 读取landsat *_MTL.txt文件，提取需要的信息 def MTL_info(self):
  3. 栅格数据读取程序，.tif,单波段。读取需要的波段数据并存储。未裁切影像方法 def singleBand(self, rasterFp):
  4. 影像数据裁切 def rasterClip(self,rasterFp):
  5. 栅格数据显示查看程序 def rasterShow(self, rasterFp):
  6. 计算数据(数组)显示 def arrayShow(self,data):
  7. 保存栅格数据，1个波段def rasterRW(self, LSTValue,resultsPath,LSTSavingFn,para):
  8. 解译精度评价。采样的数据是使用GIS平台人工判断提取，样例文件在Github中获取。  def InterpretaionACCuracyEstimaton(self,InterAccuEstiFp):
  9. 直方图与拟合曲线 def histogramFig(self,x):
 10. 箱型图  def boxplot_outlier(self,data):
    
###  定义LST计算类 class LST():
  1. 初始化相关值 def __init__(self,b10,b11,b4,b5,parameterValues):
  2. 计算TOA(top of atmosphere) 
        1. def TOARadiance(self,Qcal,ML,AL):
        2. def TOABrightnessTemperature(self,TOARadianceVal,K1,K2):
        3. def TOAAverage(self):
  3. 计算NDVI  def NDVI(self,RED,NIR):
  4. 计算 Land Surface Emissivity (LSE):  def LSE(self,NDVI):
  5. 计算LST def LST(self,BT,W,E):
  6. 计算B10，B11的LST的均值  def LSTAverage(self):
  
### 分析数据，并建立机器学习/深度学习模型类。地物/用地分类与LST的关系等 class DLModel_preprocessing():
  1. 基于NDVI 解译水体/绿地/裸地 def interpret_NDVI(self,NDVI):
  2. 将栅格数据分为多个单元块 def trainBlock(self,array,row,col):
  
### 建立用于LST进一步分析的函数方法 class LSTAnalysis():
 1. 应用spectral_clustering（）聚类 def LSTClustering(self):
 2. 基于卷积温度梯度变化界定冷区和热区的空间分布结构  def LSTConvolue(self):
 3. 显示图像 def imgShow(self,imges,titleName,xyticksRange=False):
 4. 三维显示数据，并显示剖面线，可以分析数据三维空间的变化  def ThrShow(self,data):
  
## Fit_estimators.py
1. 基于机器学习回归算法建立用于绿地规划评估的地表温度预测模型
2. 计算F1_score,以及召回率recall_score, 准确率precision_score def ACCuracy_mean(data):
3. 折线图 def lineGraph(array,estimators): 
4. 箱型图和小提琴图 def violinPlot(all_data,estimators):


# (26)01_LST反演地表温度

4、5年前在使用Landsat系列遥感影像反演地表温度时，还清晰记得在GIS平台下处理的繁琐流程，如果要批量处理几十年的数据将会是一个怎样的状态，而且又如何进一步方便的进行数据分析呢！因此，还是python写了处理的程序，这样为之后研究地表温度时空序列数据时，节省海量的处理时间。反演地表温度参考了Estimation of Land Surface Temperature using LANDSAT 8 和USGS提供的计算TOA的公式。具体的逻辑在程序中分享，可以自行调整计算的方式，使其适合于所分析数据的需求。

LANDSAT_PRODUCT_ID = "LC08_L1TP_127036_20180810_20180815_01_T1数据LST计算结果

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_01.jpg" width="400" align="right">

# (27)02_基于地表温度差值数量变化界定全区植被降温效应的空间分布

在数据分析过程中，当前有很多的方法，依据Landscape and Urban Planning 中的论文内容，粗略估计主要使用的有箱型图，这个的确用的很多，在分析空间数据时，通常会涉及到很多情景，例如如果分析2010-2019年间的地表覆盖数据、温度变化数据、人口分布数据...给个箱型图（小提琴图）能够很好的观察到每年的数据分布情况，这是只看二维平面，甚至三维都无法观察到的；对于上述案例，也可以使用折线图，但是如果是一景Landsat8的遥感数据，它的数据量约是7081×7931（包含NoData），即使提取1/4，如果都在折线图上体现，也不宜观察数据的变化，此时需要对数据做些聚类等方法的处理，降低数据量，来观察数据变化的趋势；同时，基本统计中的直方图是必须的，在此次实验中观察温度差值的变化分布情况使用的是直方图，并拟合曲线分析变化，此时用箱型图就看不到变化的趋势；在拟合了曲线或者折线图拟合的曲线中，甚至回归模型的曲线，想获抓住数据变化的关键点，寻找拐点是跑不掉的方法，利用这些拐点在再二维空间数据中重分类数据，将会获得一些分析结果；散点图很重要，尤其观察两组或多组数据之间的相关关系，通常结合回归模型来分析；当然在相关关系分析时，热力图体现了其重要的价值，是反映相关关系的热力图，由方格网组成，可以色彩的变化，可以一眼看透多数据间之间的相关性大小；当然还有一种热力图，例如百度热力图，是二维空间数据大小的显示，在进一步分析中还是要深入到分析的层面，要挖掘到数据潜在的价值，具体的方法因问题而不同；多个数据的变化除了用折线图，也可以用雷达图（同polar chart?），还是能够很好表达多组数据同时在不同分析因素下变化的关系；三维曲面剖线图，可以观察三维空间数据的变化，但是还不是很容易抓住到数据的关键位置，需要做进一步的分析处理。基于图表的数据分析方法还有很多，在《城市空间数据分析方法——PYTHON语言实现》的50个实验全部完成后（目前到30，含分解），做个系统的阐述，应该会有所价值。

此次实验通过箱型图及拟合的曲线观察了温度差的分布情况，提取了数据的拐点位置值：

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_02.jpg" width="300" align="right">

依据这些拐点位置值来探索二维空间数据分布，确实可以发现一些温度变化的空间特征，如图：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_03s.jpg)

# (28)03_基于卷积温度梯度变化界定冷区和热区的空间分布结构

（局部）空间自相关/local indicators of spatial autocorrelation LISA， 是为了探析基于空间点属性值，空间上相互存在的相关性。如果某一位置变量值高，则其附近位置该值的变量也高，为正空间自相关，否则，为负空间自相关。在分析数据的冷区和热区（热点）时，即空间自相关有些现成的方法，例如基于ArcGIS的的Hot Spot Analysis（基于Getis-Ord Gi*统计）,具体计算公式可从ArcGis帮助中获取，及Optimized Hot Spot Anaylysis工具；如图对LST的计算结果：

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_10.jpg" width="400" align="right">

同时，GeoDa提供了基于Moran's I莫兰指数的全局和局部空间自相关。例如如下计算结果：  

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_11.jpg" width="400" align="right">

python库PySAL同样也提供了（全局/局部）莫兰指数计算。在后续实验中将采取该种方法。当然在空间关系的分析中还有一类，就是卷积。通常卷积应用于图像的处理过程，例如图像的锐化、边缘检测、浮雕、均值/高斯模糊等等。因为其能够提取空间数据之间的特征，目前是深度学习中重要的内容。那么就卷积来找出数据的空间发呢不特征，在之前的实验中已经详细阐述，此次则寻找每一栅格数据与周边栅格数据之间的差值变化，并基于变化值为零的位置来分出冷区和热区，即热区是栅格变量高于周边栅格变量值，冷区相反，来分析LST的空间变化情况。如下图：

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_04.png" width="400" align="right">

基于上述分析结果是能够找到独立的冷区，当然亦可以找到独立的热区，如图：  

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_05S.jpg" width="400" align="right">

附：因为机器学习scikit-learn提供了很多聚类的方法，来发现空间数据间的关系，因此试图探索一些算法，能够为分析带来什么样的一个结果，如spectral_clustering（）聚类方法，当然在此处未加以深入解析，可自行探索其计算结果的价值，如图。

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/26_06.png" width="400" align="right">

# (29)04_地表覆盖与精度评价

# (30)05_基于机器学习回归算法建立用于绿地规划评估的地表温度预测模型
