# 阶段2 芝加哥城市空间结构/stage 2 the city spatial structure of Chicago
> 无参考文献版 /no reference version  初稿 /draft  by richie bao
## A. 无人驾驶城市-1
> @author: Richie Bao-Chicago.IIT(driverless city project)  data:IIT.driverless city project
### 1 背景 /background 



### 2 数据 /data



### 3 方法 /method
#### 3.1 模式数据特征描述
在测量和模拟部分已经完成地标与Phmi之间的对应关系，为更加清晰的观察随时间推移测量和模拟的数值对应的空间位置变化关系，给出新的图表表达方法，主要包括两类，其一是静态的显示地标与Phmi的空间位置；其二是构建无人车测量位置与地标对应关系的网络结构，交互显示对应空间关系。

图表表述主要使用python的matplotlib和bokeh库；网络结果的建立使用networkx库，互动网络结构结合bokeh库。网络结构建立过程确定无人车各个位置对应激光雷达扫描距离为25m，提取所有无人车位置对应该范围内的地标建立网络结构。

#### 3.2  基于模式预测phmi学习模型



#### 3.3 交互式操作探索模式特征

### 4 结果 /results
##### 4.1 模式数据特征描述
*  静态空间位置描述
为了能够观察无人车位置、地标与Phmi激光雷达扫描导航评估值之间的关系，建立图表1，灰色线为无人车行驶路径，蓝色十字为地标，红色折现为Phmi值。Phmi值小于pow(10,-5)不满足基于激光雷达扫描导航要求，因为值的变化比较小不易于观察不满足要求的变化位置，因此通过缩放该部分的值来突出显示。

此次测量区域Phmi值大部分位于0.05之下，在此之上多处跳变到较高值，并持续不同变化的行驶区域后跳变回低值。不满足导航需求的位置点多数为单点跳变，少部分持续较小的行驶距离。


![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/40_02.png)
<p align="center">
<em>图1 无人车位置、地标与Phmi /Fig 1 </em>
</p>

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/report_02_a.gif)
<p align="center">
<em>图2 Phmi数值分布 /Fig2 </em>
</p>

* 交互网络结构
因为无人车位置点采样密集，如图3所示的静态图表格式很难观察各个车行采样位置点与对应25m扫描区域地标的关系，因此借助bokeh库实现交互观察变化关系图4。无人车连续扫描采样，地标的空间位置相对无人车连续移动变化，交互方式可以很好的观察空间对位关系，但是连续动态密集的采样过程，仍旧很难通过肉眼观察地标空间模式的变化与Phmi的关系。

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/report_03.png)
<p align="center">
<em>图3 无人车采样位置点与对应地标网络  /Fig 3 </em>
</p>

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/report_03_c.gif)
<p align="center">
<em>图4 交互网络结构 /Fig4 </em>
</p>

##### 4.2 基于模式预测phmi学习模型
探索空间模式与Phmi评估值之间关系最好的方式是直接使用工程组的模拟模型，出于几个原因单独建立预测模型。其一模拟模型当前建立于MatLab环境下，需要建立与python的接口调用模型；其二是为了寻找地标与无人车采样位置点的空间模式，需要找到表达空间模式的途径，从而能够指导无人驾驶城市规划，同时将信息反馈到工程组改进模拟模型，提高车载激光雷达扫描导航的精度；其三用于建立交互式操作探索模式特征的平台。

* 建立特征值数据结构




* 输出类别的方式


##### 4.3 交互式操作探索模式特征



### 5 讨论 /discussion




## B 已完成论文
### 1 芝加哥物质空间连续距离聚类下的空间结构变化
> 摘 要： 对城市物质空间结构变化的量化描述可以为城市的可持续发展提供有效的参照。以芝加哥城为研究对象，将其视为具有层级结构的物质空间，提出连续距离聚类描述城市空间结构特征的方法，同时视空间结构存在连续变化的关联强度，提出连续距离卷积核卷积计算连接度的方法，界定城市建成区连接度强度，确定具有意义的关键层级，获得180m聚类距离城市建成区边缘的界定；15×15卷积核城市建成区连接强度界定；39m建筑高度城市建筑高度分布区间的界定；130m聚类距离建筑高度水平向分布的特征界定。连续距离聚类的动态量化描述城市物质空间结构的方法，可以界定具体的空间范围，落实规划内容并提供有效参照。

> 

> 关键词：城市规划；物质空间；聚类；动态层级；芝加哥；

> Keywords：Urban planning；Physical space；Clustering；Dynamic hierarchy；Chicago


### 2 芝加哥城公园属性描述与空间分布结构/Property Description and Spatial Distribution Structure of Chicago City Parks
> 摘要：城市公园绿地是城市重要组成部分，在城市生态、居民健康和生活质量上有积极影响，基于数据统计分析描述城市公园属性与空间网络结构，进一步完善城市公园绿地规划配置方法。提出公园自身属性描述、公园多属性邻里环境描述和城市公园网络结构分析三个层次描述与分析城市公园，并基于芝加哥城公园数据分析为例。计算结果在多层次上系统的量化描述公园属性并提取城市公园自身、之间及邻里环境间的空间分布结构和特点，表明基于三个层次量化描述城市公园属性结构的可行性，为城市公园绿地开放空间的规划配置提供参照

> Abstract: City park and green space are  important parts of a city, have a positive impact on urban ecology, residents’ health and quality of life, based on statistical analysis of data to describe the city park attributes and spatial network structure, further improve the city park green space planning and allocation method. This paper presents three levels of description and analysis of urban park, namely, park attribute description, park multi-attribute neighborhood environment description and urban park network structure analysis, meanwhile, takes Chicago city park data analysis as an example. The results show that it is feasible to quantitatively describe the urban park property structure based on three levels and provide reference for the planning and configuration of urban park green space.

> 关键词：风景园林；城市公园；芝加哥；多源数据；空间关联性

> Keywords: Landscape Architecture; City parks; Chicago; Multi-source data; Spatial relevance



<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkzMTQyNTM5MiwxNzc4NjQ2MjE2LC0xMj
IxOTEwNDAzLC0xMTg4NjMxODQ2LDE1ODcwOTkxMDcsNzg5NjU5
Mjg1LDE1NDcyMjkwMzUsMTQ4MzkzMTc4MSwtMTA1NjEzNDA1LC
05MTkxMTI3MTMsLTE3ODIwMjM0ODIsMTg5MjcwNDgyNSw0Nzg5
MjA4NzAsLTQyMTQwOTE1NCwxNTMxMDA3Njk4LDE3Njc4OTIwMD
gsLTEwMzY4MDU1MDEsNjQzMjc4ODQzLC0xOTEyMzI4NTQ2LDk4
ODA4NDIyNl19
-->