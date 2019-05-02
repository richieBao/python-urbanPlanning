# 生活圈_04_相关系数热力图(簇行业类)与批量图片自动排版
相关系数计算是数据分析的重要内容，常规的分析结果是数字表格的表达方式，如果数据量比较多时，查看数据的变化就有些不容易，因此可以将相关系数的关系表达为热力图的形式，从而能够方便的通过色彩的变化来查看数值的变化情况，也有助于自身的分析和他人的查看。matplotlib提供有热力图(heatmap)的方法，但是此次使用使用了一个类似其图表表达的库seaborn，使用seaborn.heatmap( )实现。关于具体使用哪个库，可以根据自身数据分析的目的，以及操作方便与否进行选择。例如其中一个相关系数的热力图：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/partialCorrle_14.png)
最近的几项实验都会计算大量的图表结果，一般每个结果有50张图，对于这么多的图表，希望发表或分享时合并为一个，用通常的photoshop等工具操作的确是比较麻烦的事。因此，可以自行编写代码，自动将所有的图片自动排版，从而节约时间，避免手工劳作，例如拼合的一个结果：
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/results——s.jpg)
