# 32_Chicago_02_城市空间结构分析_连接度_建成区
聚类的方法可以根据指定的距离或者其它数据类型将相近的数据分别标识为不同组，同组的数据具有相同或相近的特征，例如距离上接近。然而如何计算数据间连接的程度，或者每点与周围点连接的程度，可以使用卷积的方式计算。不同大小的卷积核，例如(3,3),(5,5)...(n,n)，其中n设置为奇数，中心值设置为0，其它值均为1，例如一个（3，3）的卷积核，形式为[[1,1,1],[1,0,1],[1,1,1]]，计算每一位置与周边临近的8个位置的连接关系，而(5,5)则计算每一位置与周边临近的24个位置的连接关系，依次类推。计算连接度的结果会获得每一个位置连接程度的数值标识，可以同样使用聚类的方法，将具有近似连接程度的位置集聚，从而可以观察城市空间结构，此次计算的连接度为建成区（无绿地或者绿地稀少区域）在聚类距离为180m下（上一单元实验结果，聚类单元转折点位置）的连接度，并进而再次聚类连接度观察建成区分布情况。

## connectivity.py
代码结构中新增加的函数，主要包括：
> '''基于卷积计算连接度'''    def connectivity(self,array2D,distance=3):
> '''按数量多少排序的前n个值，''' def N_maxClusterRaster(self,clusterArray,clusterFrequency,n,kernalDistance):

# 计算结果
## 连接度
共计24组，```[i for i in range(50) if i%2!=0 and i>=3]```,即卷积核距离为：[3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_3.jpg)

## 连接度的聚类
对连接度的聚类取聚类距离为1，即30m（此次分析数据遥感影像的高空分辨率为30m）。
* 聚类前最大20组结果
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_4.jpg)
* 聚类最大，24组变化值
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_5.jpg)

## 统计图表
* 连接度最大聚类折线图以及拐点
* 连接度聚类频数boxplot
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_1.jpg" width="300" align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_2.jpg" width="300" align="right">
