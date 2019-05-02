# 生活圈_03_信息熵与均衡度
信息熵与均衡度计算并不是一个新鲜的概念，在2000年左右，城市相关研究中应用信息熵和均衡度来分析城市土地利用结构和形态演变。随着2015年左右大数据的兴起，部分研究者也基于POI数据分析城市的行业类分布的信息熵情况。其计算的方式包括，获取不同年份的POI数据，计算指定区域的信息熵或均衡度分析均质性；或将城市切分成很多方形单元，计算每一单元的信息熵，从而能够纵观城市的信息熵变化的情况。

过去对于信息熵的计算多是应用于GIS平台，在2015年左右曾发布有基于ArcGIS下ArcPy的信息熵计算代码。但是，如果将计算于python中完成，在数据处理上则更加的自由，例如此次实验下基于簇计算均衡度的问题。首先簇的数量多达几万计，再者各个簇的范围是大小不一的，另外计算量较大，因此基于python来处理是首选。

部分计算结果如下：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/EntropyMS.jpg)

另外，仍然使用箱型图来观察不同距离聚类下信息熵分布的一个情况。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/entropyBoxPlot.png)
