当今对于城市规划而言，可以获取越来越多的数据，但是这些数据往往存在问题，要么存在错误值，要么不符合研究的目的而需要提取或调整数据结构，因此前期要对数据进行处理。此次实验是对数据中包含的异常值清理，看下面给出的直方图，这个直方图显示了数据清理前和数据清理后两组数据的数值分布情况，这部分数据是数组array([2.1, 2.6, 2.4, 2.5, 2.3, 2.1, 2.3, 2.6, 8.2, 8.3])。这个数组的范围从2.1到8.3，但是8.2和8.3这两个数值相对主要数据偏离较远，即为异常值。如何通过相关算法移除这些异常值？本次实验的算法采用“How to Detect and Handle Outliers"”论文中所提到的计算公式。根据该公式编写程序，计算后的值为[1.57383333, 0.6745, 0.22483333, 0.22483333, 0.6745, 1.57383333, 0.6745, 0.6745 25.85583333, 26.3055]，能够明显的观察到8.2,和8.3对应的25.85和26.3偏离核心区域。 此时设置阈值为3.5，大于预值3.5后的值，标识为true，结果为[False, False, False, False, False ,False, False, False, True, True]，这就是进行异常值处理的一种方法。

## 调研图片信息数据异常值清理前后数据分布直方图
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/910.png)

## 调研.kml路径数据异常值清理前后数据分布直方图
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/911.png)

## 调研数据清理后图表显示
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/912.png)
