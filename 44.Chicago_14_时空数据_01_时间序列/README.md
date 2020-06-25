# Chicago_14_时空数据_01_时间序列 /spatial-temporal data_01_time-series 

> 数据来源/Data source: Chicago Data Portal https://data.cityofchicago.org 可以自行搜索Covid-19 /You can search for yourself

> 参考/reference:1.Open Machine Learning Course. Topic 9. Part 1. Time series analysis in Python https://medium.com/open-machine-learning-course/open-machine-learning-course-topic-9-time-series-analysis-in-python-a270cb05e0b3

> 2. 时间序列分析完整过程 /the whole process of time series analysis  https://blog.csdn.net/jh1137921986/article/details/90257764

> 3. 时间序列与时间序列分析 /time-series and time series analysis https://www.cnblogs.com/tianqizhi/p/9277376.html

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
#### Chicago：Covid-19 基本数据
* 01-日感染人数与日死亡人数

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_01.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_02.png)

* 02-数据预处理 （见文件 <em>44.Chicago_14_时空数据_01_时间序列.html</em>）
#日期索引/#缺失数据填充/#数据采样

* 03-平滑/滑动窗口
> A-平均平滑数据

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_03.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_04.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_05.png)

> B-指数平滑

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_09.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_10.png)

> C-加权平均/weighted average
> D-异常检测/置信区间

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_06.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_07.png)

* 04-时间序列交叉验证/Time series cross validation
* 05-特征提取
> A-时间序列滞后值
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_11.png)
> B-窗口相关统计量
> C-日期和时间特征
> D-ts|fresh features

* 06-时间序列的（非）线性模型
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_12.png)

#### ARIMA（autoregression integrated moving average model） 差分自回归移动平均模型
* 07-平稳性检验-差分法
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_20.png)

* 08-相关函数评估方法
> A-相关函数

偏自相关函数PACF(partial autocorrelation function)
自相关函数ACF（autocorrelation function）
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_14.png)

> B-散点图
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_15.png)

> C-模型评估标准

AIC-akaike information criterion，赤池信息准则
BIC-bayesian information criterion, 贝叶斯准则
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_17.png)

> D-综合
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_16.png)

* 09-模型残差检验
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_18.png)

* 10-模型预测
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/44_21.png)
