# 46.Chicago_16_时空数据_03_全局-局部空间自相关分析
参考：PySAL Notebooks Book http://pysal.org/notebooks/explore/esda/intro.html

在特定时间点上，空间数据的分布结构是分析城市空间属性内在关系的重要内容。最为常用的方法是全局/局部空间自相关（spatial autocorrelation），以及各子区域内，间，缘之间的吻合度/相似度等内容(silhouette statistics)。本次数据分析使用PySAL库。

分析结果内容罗列如下：
### 01-分位数/spatial lag_quantile-Attribute Similarity
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_01.png)
### 02-全局空间自相关 Global Spatial Autocorrelation
2位/Binary Case / 2位连接数/Join counts / 连续情况/Continuous Case
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_02.jpg)
### 03-局部自相关：热点，冷点和异常值/Local Autocorrelation: Hot Spots, Cold Spots, and Spatial Outliers
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_03.jpg)
### 04-聚类（分析区域）内及间观测值特征相似性/Silhouette statistics
* 感染数分布/社区分类
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_04.jpg)
* 分组吻合度（well-fit）/The Silhouette Score /benchmark
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_05.png)
> 使用sklearn.cluster.KMeans聚类后，用于Silhouette Score分析，比较社区分类
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_06.jpg)
* 最近邻吻合分布/Nearest Label
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_07.jpg)
* 地理/网络结构/Geographical Structure
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_08.png)
* 组间|内相似度/Path Silhouettes
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/46_09.png)
