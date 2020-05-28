# 47.Chicago_17_时空数据_04_不平等性与隔离
参考：PySAL Notebooks Book http://pysal.org/notebooks/explore/segregation/intro.html

本次关于城市健康的空间分析包括两部分内容，一是空间分布的不平等（不均衡）性及城市隔离模式。本次使用的数据除了Covid-19分布数据，还包括主要疾病
分布数据。基于Gini基尼系数主要用于经济中收入不均等分析，将其应用于Covid-19在Chicago城不同区域感染案例分布的分析，其中0表示完全均衡，而1表示
完全不均衡，通过Gini分析可以获知，随着时间的推移，不同区域的不均衡性逐渐拉大，此时，因为疫情并未结束，感染人数仍在增加，因此后续变化未给出。

城市空间隔离模式通常用于种族隔离分析，关于隔离指数的研究非常丰富，相关指数亦有很多，Gini指数实际上也是隔离指数。PySAL在已有隔离指数分析基础上
亦给出了基于Shapley分解不均衡变化值为两个分量，其一为空间分量，通常挂钩于w空间权重；其二为属性分量，即所分析的数据，本次为感染案例的两个时间点数据。
为确定分析的可靠性，推断统计显著性。同时，以Chicago疾病分布数据为例，探索多组空间隔离指标，以及除了空间区域权重，加入反映人人之间接触容易程度
的路网因素。

## 空间分布的不平等性/inequality/Methods for measuring spatial inequality.
> Gini度量不均衡指标

* 基础数据
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_02_01.jpg)
