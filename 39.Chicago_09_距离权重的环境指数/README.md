# 39.Chicago_09_距离权重的环境指数
在“36.Chicago_06_网络结构分析_networkx”部分，建立网络节点之间的空间权重时，使用过pysal计算空间距离权重，pysal给出了多种不同类型计算空间权重的方法，
并给出多种空间统计模型来分析区域间的空间关系，但是当前Pysal库分析的内容多为vector对象，如果已知多个vector对象，而要分析对象与栅格值之间的空间关系时，
当前则需要自行code。本次实验需要分析614个Chicago城公园外环境对公园自身的影响，包括SVF天空视域因子和人口分布，距离公园polygon边界近的raser cell单元，
应该具有较高的权重值，因此需要计算614个polygon对象在一定范围下所有Raster cell单元的空间距离权重值。对于人口分布，因为其统计数据为46337个polygon对象，
较之1m-3m高空分辨率的raster数据，数据量较小，因此可以直接计算614个公园每个公园边界到所有人口分布polygon之间的距离。

## polygon缓冲区下提取raster值结果
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/39_03.jpg)

SVF权重环境
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/39_02.jpg)

## 人口权重环境压力
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/39_01.jpg)
