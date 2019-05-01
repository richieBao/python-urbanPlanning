# 生活圈_02_通过计算曲线拐点找到特征层级
matplotlib提供了大量图表用于数据的可视化表达，以及数据分析，通过图式寻找到数据的变化关系。有时也需要在图表之上计算并找出关键的信息，例如计算曲线的曲率，找到曲率变化最快的位置，也许这些特殊位置反映了数据变化的特征，进一步说明了实际研究对象的某些特征，对于定量的研究具有重要意义。

在使用Python计算曲率变化最快的位置，即拐点时，可以直接安装kneed库，直接调用作者已经编写好的方法。例如在分析聚类过程中，聚类数量与聚类距离的关系时，对应的聚类距离为120m：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/clusterSum.png)

而在计算POI独立点总数随聚类距离的变化时，拐点对应的距离为160m。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/singlePtsKneePt.png)

这些位置在一定程度上说明了在连续聚类变化中，能够反映城市业态分布特点的关键点，可以通过进一步分析聚类的分析结果来研究城市生活圈的变化特征。

利用拐点寻找折线图的的变化特征来寻找反映实际业态空间变化的特征，可以通用于相关的不同目的的分析。matplotlib所提供的大量案例文件，不只是数据的一种可视化，而是透过这些数据的图形化表达找到隐含在数据背后所反映的实际意义。例如，箱型图（小提琴图）亦是寻找数据变化的重要分析图形，能够查看数据分布的变化特征。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/boxPLotClustering_1.png)

在这个箱型图中，除了寻找到数据随聚类距离变化的主要分布特征外，还可以找到聚类频数最大，即簇最大的位置。这个位置反映了基于业态城市最大生活圈的范围，这个以量化的方式寻找到具体空间的边缘，对于进一步的城市相关研究是具有落实作用的。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/coreBoundaryOrderB_s.jpg)

从定性走向定量需要以数据作为基础，以图表分析作为手段，从中洞察到未曾发现或者需要定量的信息。当然，掌握python数据分析方法的工具却是实现这些的前提。
