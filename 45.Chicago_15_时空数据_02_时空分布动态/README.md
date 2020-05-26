# 45.Chicago_15_时空数据_02_时空分布动态
数据来源：Chicago Data Portal https://data.cityofchicago.org 可以自行搜索Covid-19，以及所用到的相关数据

参考：1-PySAL Notebooks Book: .http://pysal.org/notebooks/explore/esda/intro.html 
2-GIDDY/GeospatIal Distribution DYnamics https://giddy.readthedocs.io/en/latest/index.html

城市时空数据分析的目的，通常是探查城市区域间某一随时间变化因素之间存在的关系，例如全局相关性变化，LISA变化，从一分位数区域转变到另一分位数区域的概率、
时间，以及方向，亦包括各区域变化因素的稳定性确定等内容。本次分析所使用的python库为giddy，用于探索城市时空分布动态-Covid-19时空变化。

> 分析结果罗列如下：

### 00-基础数据处理
* csv数据（Covid-19 by zip code）

  转换为时间序列dataframe

  使用多重索引 multi index

* 读取zip .shp文件
* 人口数据分位数/父区域划分（zip）
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_01.jpg)

### 01-时空数据绝对-相对动态变化/absolute dynamics and relative dynamics
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_02.jpg)

### 02-离散马尔可夫链/Discrete Markov Chains
转移矩阵|转移概率|稳态分布 |平均通过时间 
```python
DMC-transitions:
 [[111.  14.   2.   2.   4.]
 [ 17.  74.  16.   6.   2.]
 [  1.  20.  78.  20.   4.]
 [  0.   5.  21.  60.  24.]
 [  0.   3.   5.  26.  85.]]
DMC-p:
 [[0.83458647 0.10526316 0.01503759 0.01503759 0.03007519]
 [0.14782609 0.64347826 0.13913043 0.05217391 0.0173913 ]
 [0.00813008 0.16260163 0.63414634 0.16260163 0.03252033]
 [0.         0.04545455 0.19090909 0.54545455 0.21818182]
 [0.         0.02521008 0.04201681 0.21848739 0.71428571]]
DMC-steady state
 [0.18106311 0.19097839 0.21140026 0.20515134 0.21140689]
DMC-fmpt [[ 5.52293606 11.32091921 16.01694736 16.98271948 21.43511836]
 [22.44417827  5.23619451 11.2558902  14.00636983 20.08856333]
 [32.08691759 10.91501993  4.73036312  9.88597376 17.22359321]
 [36.04830893 14.59026638  8.66164073  4.87445017 11.44276548]
 [37.76538691 16.26241251 11.1167744   6.18967583  4.73021478]]
```
 
 ### 03-区域背景（分位数）与莫兰指数/Regional context and Morans Is
 各周感染案例分位数（5）
 ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_03.png)
 值为正且显著，各感染区域并不相互独立
 ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_04.png)
 
### 04-空间马尔可夫/spatial markov
(空间)马尔可夫转移概率矩阵
空间滞后，参数之一为邻里区域距离范围均值（y）;看对角线值，可以说明邻里区感染率高，则该区感染率高，反之亦然
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_05.jpg)

### 05-LISA）马尔可夫/LISA(Local Indicators of Spatial Association) markov 局域空间自相关分析
HH(=1), LH(=2), LL(=3), HL(=4)
```python
LISA transitions:]
 [[150.  14.   9.  12.]
 [ 19. 103.  20.   1.]
 [  6.  19. 186.   8.]
 [ 10.   7.  12.  34.]]
estimated transition probability matrix:
 [[0.81081081 0.07567568 0.04864865 0.06486486]
 [0.13286713 0.72027972 0.13986014 0.00699301]
 [0.02739726 0.08675799 0.84931507 0.03652968]
 [0.15873016 0.11111111 0.19047619 0.53968254]]
steady state distribution of the chain:
 [0.28609488 0.2331318  0.40479362 0.07597969]
the first mean passage time for the LISAs:
 [[ 3.49534387 12.05055375 12.04738556 23.75265661]
 [12.12993911  4.28941907  9.51308179 28.5555686 ]
 [16.5132091  11.51665581  2.47039467 27.39611343]
 [11.93338217 11.0932899   8.6229458  13.16141123]]
chi-2:
 (248.5444534389835, 0.0, 9)
 ```
 
 ### 06-全秩马尔可夫|地理秩马尔可夫/full rank markov and Geographic Rank Markov
 全秩马尔可夫
 ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_06.jpg)
 Geographic Rank Markov
  ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_07.jpg)
 
### 07-数值流动性/mobility of values
```python
Shorrock1’s mobility measure: 0.40061912189412874
Shorroks2’s mobility measure: 0.8947596046400575
Sommers and Conlisk’s mobility measure: 0.1512614999713907
Bartholomew1’s mobility measure: 0.45222897037897725
Bartholomew2’s mobility measure: 0.11041662306388621
```

### 08-动态LISA方向分析/directional analysis of dynamic LISAs
 ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_08.jpg)
 
### 09-肯德尔等级相关系数/kendalls tao
* 经典/Classic Kendall’s tau
```python
tau.concordant: 1113.0
tau.discordant: 894.0
tau.tau: 0.10585418308712077
tau.tau_p: 0.20891363352187065
```

* 空间/Spatial Kendall’s tau
```python
tau_w.concordant: 1113.0
tau_w.concordant_spatial: 50
tau_w.discordant: 894.0
tau_w.discordant_spatial: 24
tau_w.tau_spatial: 0.3337725078760129
tau_w.tau_spatial_psim: 0.001
```

* 区域间，区域内，Kendall'stau 分解/Inter- and Intra-regional decomposition of Kendall’s tau
```python
tau_w.tau_reg: [[ 0.7         0.6        -0.6         1.          1.          1.
   0.52       -0.4        -0.2         0.6         0.6         1.
   0.8        -0.6         0.2         0.         -0.2         0.2
   0.          0.4         0.6         0.2        -0.6         0.2
  -0.2         0.          0.6         0.75      ]
 [ 0.6         1.          0.          1.         -1.          1.
   0.3        -0.83333333 -0.5         0.          1.          0.75
   1.          0.         -0.5         0.14285714 -0.5         0.
  -0.75        1.         -0.125       0.         -1.         -0.5
  -1.         -0.33333333  0.         -0.25      ]
  
  tau_w.tau_reg_pvalues: [[0.088 0.129 0.147 0.001 0.095 0.092 0.06  0.068 0.302 0.285 0.274 0.011
  0.143 0.169 0.543 0.336 0.275 0.562 0.344 0.293 0.039 0.529 0.174 0.53
  0.417 0.43  0.139 0.006]
 [0.129 0.506 0.628 0.027 0.2   0.308 0.359 0.028 0.22  0.618 0.3   0.16
  0.305 0.633 0.279 0.504 0.22  0.6   0.017 0.107 0.34  0.642 0.219 0.275
  0.224 0.285 0.578 0.272]
  
  tau_w.tau_reg * (tau_w.tau_reg_pvalues<0.05): [[ 0.          0.         -0.          1.          0.          0.
   0.         -0.         -0.          0.          0.          1.
   0.         -0.          0.          0.         -0.          0.
   0.          0.          0.6         0.         -0.          0.
  -0.          0.          0.          0.75      ]
 [ 0.          0.          0.          1.         -0.          0.
   0.         -0.83333333 -0.          0.          0.          0.
   0.          0.         -0.          0.         -0.          0.
  -0.75        0.         -0.          0.         -0.         -0.
  -0.         -0.          0.         -0.        ]
 [-0.          0.                 nan  0.         -0.          0.
  -1.          0.         -0.         -0.         -0.         -0.
   0.         -0.         -0.          0.         -0.         -0.
  -1.         -0.          0.         -0.         -0.          0.
  -0.         -0.         -0.         -0.        ]
  ```
  
* 本地/Local Kendall’s tau
```python
Local Kendall’s tau:   STATE_NAME  $\tau_r$
0      60647  0.030769
1      60639 -0.569231
2      60622  0.046154
3      60651 -0.569231
4      60641 -0.430769
```

* 基于本地LIMA流动性指标/Local indicator of mobility association-LIMA
  Neighbor set LIMA
 ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_09.jpg)
 
  Neighborhood set LIMA
  ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/45_10.jpg)
