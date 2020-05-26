# Chicago_14_时空数据_01_时间序列

>数据来源：Chicago Data Portal https://data.cityofchicago.org 可以自行搜索Covid-19

### 时空数据分析方法
城市空间分析中重要的一项分析就是时空数据的分析，目前已经有很多的研究来探索城市空间格局变化的预测模型，来预测城市发展的趋势，以及与时空有关的各类分析技术。在python领域，与时空数据分析的模块库不胜其数，本次数据分析主要目的是分析市域尺度下，城市空间与城市健康之间的关系，所使用的库主要为PySAL(esda,inequlity,segregtion,giddy)，tfresh和dash(plotly)等。基于PySAL时空数据的分析方法可以包括:

1. 时间序列分析/time series analysis
2. 时空分布动态/GIddy/GeospatIal Distribution DYnamics 
3. 全局/局部空间自相关分析/Methods for testing for global and local autocorrelation in areal unit data.esda/
4. 空间分布的不平等性/inequality/Methods for measuring spatial inequality.
5. 城市隔离模式/segregation/analyzing patterns of urban segregation
6. 基于web图表分析-dash


### A-时空数据-时间序列分析
单纯的时间序列分析则不涉及到空间的问题，更多内容涉及到数据处理，随时间的变化规律，（feature）特征提取，预测模型例如ARIMA(autoregression integrated moving average model)或者自定义回归模型。

计算罗列如下：
#### 1-Chicago：Covid-19 基本数据
日感染人数与日死亡人数

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_01.png" width="400" align="left">  
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_02.png" width="400" align="left">  

