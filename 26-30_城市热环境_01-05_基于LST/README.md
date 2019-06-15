# 26-30_城市热环境_01-05_基于LST
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




![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/partialCorrle_14.png)


![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/results——s.jpg)
