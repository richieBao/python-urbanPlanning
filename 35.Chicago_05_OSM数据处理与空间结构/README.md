# 35.Chicago_05_OSM数据处理与空间结构
在中国可以从百度服务器中下载到POI（points of interets）兴趣点数据，在之前的探索中详细的阐述了该数据下载，处理以及分析的一些方法。对于Chicago类似的数据分析中，则采用OSM(open street map)提供的数据。对于OSM数据的处理，可以采用osmium及其python库Pyosmium，实现数据的读取和基本处理操作。

此次分析中，在数据处理上除了使用OSM数据之外，也增加了新的数据处理方法，例如直接从.shp格式文件中读取points点数据信息为dataframe格式数据，进一步阐释和应用pandas库处理数据的方式；合并多层级最大频数区域的函数，分析变化趋势等。此次对于Chicago的分析可以与22-25生活圈对于西安的分析做比较，发现中西城市发展的一些不同。

# 计算结果
## 聚类过程
> OSM points聚类 50层级 list(range(20,520,10))
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/35_01.jpg)
> 最大聚类变化
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/35_02.jpg)
