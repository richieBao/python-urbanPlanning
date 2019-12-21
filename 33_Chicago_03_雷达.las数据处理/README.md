# 33_Chicago_03_雷达.las数据处理
在“19_ROS-Kinetic深度相机3DSLAM三维点云建筑空间”部分阐述过三维点云数据，以及使用无人机航拍，建立三维模型以及正射影像的过程。数字技术的发展以及数据的收集、管理和开源，使我们能够方便的获取城市尺度的雷达数据，在以及将在城市规划，尤其城市设计层面和城市微更新中发挥重要作用。Illinois伊利诺伊州发布有全州的雷达数据，下载Chicago城市部分的数据用于数据的处理分析。雷达数据通常分辨率高，此次为1m，数据量大的特点。Chicago城区范围部分数据量约大于1T，所提供数据每一tile单元基本为（2501，2501），最大约1G多，最小几百M。网络搜索可以获取一些免费查看、修改.las雷达数据的工具，以及在线查看工具。.las数据此次的版本为1.4,关于.las数据信息可以从网络搜索获取。ENVI同样提供了雷达数据读取、查看和计算的工具。但是基本所有工具为手工操作，不能或不易实现批量处理。制约后期数据分析的需求。因此有必要使用Python的pdal库实现对.las雷达数据的处理。

## .las数据查看
* 点云数据（所有分类）
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/33_01.jpg)

* 建筑部分
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_02.jpg)

* 植被部分
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_03.jpg)

* 地形部分
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_04.jpg)

* 三维模型
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_05.jpg)

## pdal库批量处理数据
* dsm计算
> dsm 数据表面模型，反应le地表之上所有地物的高度，在进一步的城市空间分析中，将用于SVF(sky view factor)下垫面天空视域因子等内容的分析。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_06.jpg)

* 应用.las计算分类数据
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_07.jpg)

> 原始单一数据量约在2000多，批量处理完之后，需要拼合数据为一张。如果数据量较大，可能需要较高的内存，>64GB，甚至更高，关于如何使用较小内存拼接大数据，在之后研究中进一步探索。
部分数据：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_08.jpg)
