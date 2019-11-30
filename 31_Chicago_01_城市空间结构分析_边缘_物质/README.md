# 31.Chicago_01_城市空间结构分析_边缘_物理
此次实验大组选择Chicago作为城市空间结构分析的对象，涉及的分析内容将较为系统丰富，部分代码的功能直接采用之前的研究成果，并不断增加新的研究内容。Chicago的城市结构与国内城市具有显著性差别，在具体分析时将会标识处其差异性，尤其分析结果的比对会进一步确定之间的异同。此次实验预计涉及的内容较多，根据研究分析进度实时发布每一阶段的成果，尤其代码分享，为有意进入应用Python语言分析城市结构的规划设计师所参考。

第1阶段的代码结构如下：
## Chicago_SDAM_basis.py

### 基础类：class baseClass:
  1. 配置工作环境：def filePath(self,dirpath,fileType):
  2. 以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义：def filePath(self,dirpath,fileType):
  3. 读取landsat *_MTL.txt文件，提取需要的信息：def MTL_info(self):
  4. 栅格数据读取程序，.tif,单波段。读取需要的波段数据并存储。未裁切影像方法：def singleBand(self, rasterFp):
  5. 影像数据裁切：def rasterClip(self,rasterFp,clipRange):
  6. 保存栅格数据，1个波段：def rasterRW(self, rasterValue,resultsPath,rasterSavingFn,para):
  7. 栅格数据显示查看程序：def rasterShow(self, rasterFp):
  8. 计算数据(数组)显示：def arrayShow(self,data): 
  9. 显示图像：def imgShow(self,imges,titleName,xyticksRange=False): 
  10. 加载numpy 数组数据。可省略该函数，直接调用np.load()方法：def npArrayLoad(self,dataLoadFn):
  11. 读取多个numpy数组数据，并追加在一个数组中：def npyRead(self,filePath):
  12. 读取Numpy数组数据，因为每一数组shape不同，因此最终追加在一个列表中：def npyReadMulti(self,filePath):
  
### 计算：class calculate:
  1. 调整分类数据，合并夏季和秋季农田区域：def classificationAdjust(self,cl_a,cl_b):
  2. 实现栅格聚类的方法：def rasterCluster(self,rasterArray,val,eps,modelLoad=""):
  3. 折线图，及计算knee/inflection points拐点：def lineGraph(self,x,y):
  4. 箱型图统计：def boxplot(self,data,labels):

### 组合：class combo():
  1. 设置聚类距离，批量计算聚类，并保存raster文件，及array数组：def clusterBundleCal(self,epsList):
  2. 批量图表统计：def graphAnalysis(self):
  3. 最大聚类提取并存储为raster：def maxClusterRaster(self,clusterArray,clusterFrequency):
  4. 最大聚类变化区写入raster：def clusterMaxVariaton(self,clusterArray,clusterFrequency):
  
# 影像解译分类

数据使用Landsat 8系列，包含的数据如下：
. LC08_L1TP_023031_20191007_20191018_01 秋季，NDVI分类条件：water<0;green>=0.213;0=<buit<0.213
. LC08_L1TP_023031_20190804_20190820_01 夏季，NDVI分类条件：water<0;green>=0.213;0=<buit<0.213
. LC08_L1TP_023031_20180310_20180320_01 冬季，NDVI分类条件：water<0;green>=0.14;0=<buit<0.213
因为受到农田季节性变化，因此将夏季和秋季所提取的绿地合并。
最终结果为：
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_5.jpg" width="400" align="right">

# 聚类建设用地

使用DBSCAN距离聚类，其方法与前文生活圈分析种POI聚类方法同。但是POI是点数据，此次实验亦意在完成基于栅格raster数据的聚类实现。因为Ladsat 8影像数据的高空分辨率为30m（可由pan提升至15m），因此聚类距离的步幅大小设置为30m，聚类16个层级，聚类结果如下：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_6.jpg)
