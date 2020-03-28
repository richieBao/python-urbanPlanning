# 阶段2 芝加哥城市空间结构/stage 2 the city spatial structure of Chicago
> 无参考文献版 /no reference version  初稿 /draft  by richie bao
## A. 无人驾驶城市-1 /Driverless City Project -1
> @author: Richie Bao-Chicago.IIT(driverless city project)  data:IIT.driverless city project
### 1 背景 /background 
无人驾驶研究已经取得了丰富的研究成果，保守预测2030s-2040s年左右能够达到无人驾驶的市场化。此次研究是由Illinois Institute of Technology(IIT)主持的无人驾驶城市项目，目前主要涉及GPS和车载激光雷达导航两部分。对于景观/规划学科与无人驾驶工程学科的跨学科结合，景观/规划部分主要分析城市要素与导航之间的关系，一方面将分析反馈给工程组，用于模拟模型的调整，提高导航精度；再者是指导规划，找出和避免影响导航的潜在规划因素，及达到适于未来无人驾驶可能的城市模式指引。

Abundant research achievements have been made in autonomous vehicle (AVs). It is conservatively predicted that the market of AVs will be achieved in 2030s to 2040s. The study, a driverless city project led by the Illinois Institute of Technology (IIT), currently involves two parts: GPS and on-board lidar navigation. For the interdisciplinary combination of landscape /planning discipline and UVs engineering discipline, the landscape /planning section mainly analyzes the relationship between urban elements and navigation. The third is to guide the planning, to identify and avoid the potential planning factors affecting the navigation, and to achieve the city model suitable for future driverless possible guidance.

### 2 数据 /data
以工程组的测量和模拟数据为地标空间模式分析的分析数据，工程组的数据处理流程为：延城市道路实测数据（激光雷达扫描的三维点云数据、相机二维图像、惯性测量单元(Inertial measurement unit,IMU)测量三轴姿态角及加速度）。--->三维点云数据处理，及格式转换。--->针对地标的数据特征提取（二维空间位置）。--->基于MatLab模拟计算Phmi值。--->图表打印分析。

For the data of landmark spatial pattern analysis by the measurement of engineering group, the data processing is: data measured along city road (3d lidar scanning points cloud data, 2d images shoot by camera, (Inertial measurement unit, IMU) measuring three-axis attitude angle and acceleration) --> 3d point cloud data processing, and format conversion -->data feature extraction for landmarks (2d spatial position) --> Phmi value simulated based on MatLab. --> chart printing analysis.

通过工程组计算，获取特征提取后的地标位置，以及对应的无人车位置，和用于车载激光雷达导航评估的Phmi值。

Through the calculation of the engineering group, the landmark position after feature extraction, the corresponding AV’s position, and the Phmi value for on-board lidar navigation evaluation are obtained.

### 3 方法 /method
#### 3.1 模式数据特征描述 /Pattern feature description
在测量和模拟部分已经完成地标与Phmi之间的对应关系，为更加清晰的观察随时间推移测量和模拟的数值对应的空间位置变化关系，给出新的图表表达方法，主要包括两类，其一是静态的显示地标与Phmi的空间位置；其二是构建无人车测量位置与地标对应关系的网络结构，交互显示对应空间关系。

In the measurement and simulation part, the correspondence between the landmarks and Phmi has been completed. In order to observe more clearly the spatial position change relation corresponding to the measured and simulated values over time, a new chart expression method is presented. The second is to construct the network structure of the corresponding relationship between the measured position of the AV and the landmarks, and to interactively display the corresponding spatial relationship.

图表表述主要使用python的matplotlib和bokeh库；网络结果的建立使用networkx库，互动网络结构结合bokeh库。网络结构建立过程确定无人车各个位置对应激光雷达扫描距离为25m，提取所有无人车位置对应该范围内的地标建立网络结构。

The chart presentation mainly uses python’s matplotlib and bokeh libraries. The establishment of network uses the network library, and the interactive network structure combines with the bokeh library. During the construction of the network structure, the corresponding lidar scanning distance of each AV’s position was determined to be 25m, and the network structure was built by extracting all the landmarks within the range of the AV’s position pairs.

#### 3.2  基于模式预测phmi学习模型 /Prediction of the Phmi learning model based on spatial pattern
探索空间模式与Phmi评估值之间关系最好的方式是直接使用工程组的模拟模型，出于几个原因单独建立预测模型。其一模拟模型当前建立于MatLab环境下，需要建立与python的接口调用模型；其二是为了寻找地标与无人车采样位置点的空间模式，需要找到表达空间模式的途径，从而能够指导无人驾驶城市规划，同时将信息反馈到工程组改进模拟模型，提高车载激光雷达扫描导航的精度；其三用于建立交互式操作探索模式特征的平台。

The best way to explore the relationship between spatial patterns and Phmi evalution values is to use the engineering group’s simulation model directly, but there are several reasons to build the prediction model. First, the simulation model is currently established in the MatLab environment, so the interface call model with python needs to be coded. Secondly, in order to find the spatial pattern of landmarks and the AV’s data sampling locations, it is necessary to find a way to express the spatial pattern, so as to guide the planning of the driverless city. At the same time, the analysis information will be feedback to the engineering team to improve the simulation model, so as to develop the accuracy of on-board lidar scanning navigation. Third, it is used to establish a platform for interactive operation to explore the characteristics of the landmarks spatial pattern.

* 建立特征值数据结构 /Establish the feature data structure

无人车与扫描获取的地标存在空间位置关系，该位置关系的变化影响到激光雷达导航的精度，因此采用二维栅格（array数组/矩阵）的形式表述空间位置关系，不同栅格单元值代表不同要素，包括无人车位置、地标和占位栅格。

The spatial position relation exists between the AV and the landmarks, and the change of the spatial position relation affects the accuracy of the lidar navigation. Therefore, the spatial position relation is expressed in the form of two-dimensional array or matrix. The values of different cells represent different elements, including the position of the AV’s, the landmarks and the occupied grid.

* 输出类别的方式 /The way of the output category  

调试学习模型过程同时，探索不同特征值数据结构和输出类别方式优化模型，及细分问题。输出类别可以分为Phmi的原始连续值；用Percentile百分位数分类连续数值用作输出类别；均分方式分类连续数值用作输出类别；math.pow(10,-5)为评估标准值，设置为大于和小于等于两个值；基于跳变区间变化确定输出分类。

In the process of debugging the learning machine, different feature data structures and output categories are explored to optimize the model and subdivide the problem. The output category can be divided into the original continuous value of Phmi, using percentile to classify continuous values as output categories, splitting continuous values by means of equipartition, setting to greater than and less than the math.pow(10,-5) to two values, splitting bases on the change of jump interval.

模型选择上比较了深度卷积网络 AlexNet Model、网络中的网络 NiN Model和多层感知机 MLP等机器学习模型。

The deep convolutional network AlexNet Model, network NiN Model and MLP are compared in the model selection.

#### 3.3 交互式操作探索模式特征 /Exploring pattern characteristics using interactive operations 
寻找地标空间模式是能够通过调整地标的位置，或增减地标，根据变化的Phmi预测值来确定调整方案的合理性。为了能够交互式操作，使用python的pygame库建立平台，基于pytorch训练的机器模型预测Phmi值。

To find the landmarks pattern, we can determine the rationality of the plan by adjusting the position of the landmarks, adding or removing the landmark according to the change of the Phmi predicted value. In order to be able to operate interactively, the platform was built using python’s pygame library, and the Phmi value was predicted bases on the machine learning model trained by pytorch.

### 4 结果 /results
#### 4.1 模式数据特征描述 /Pattern feature description
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

#### 4.2 基于模式预测phmi学习模型
* 建立特征值数据结构
设置栅格单元大小为1m，计算地标位于栅格的位置，红色圆点为地标实际位置，绿色栅格单元包含各个地标，为地标位置的空间标识。黄色栅格单元为栅格中心位置，即无人车采样位置。如图5给出了16个随机采样位置的栅格，并标识了对应的Phmi值。

同时，除了栅格所表述的空间位置关系，在模型调试过程中，将代表地标的栅格单元赋值为各个地标到无人车位置的距离值，增加相关因素，收敛模型。

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/41_01.jpg)
<p align="center">
<em>图5 特征值栅格 /Fig5 </em>
</p>
以小于和大于math.pow(10,-5)Phmi评估值为界划分分类输出，并赋值为0和1，0为小于评估值，即不满足激光雷达导航要求；1为大于评估值，满足导航要求。图6为基于MLP网络模型测试数据集下的预测结果。

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/41_03.jpg)
<p align="center">
<em>图6 MLP网络预测模型结果 /Fig6 </em>
</p>

#### 4.3 交互式操作探索模式特征
图7中红色中间位置为无人车位置，多个绿色块为Landmarks位置，并标识了数字为其到无人处的距离。右上角PHmi_reclassify显示更新预测值。基于pytorch训练的深度学习模型预测变化地标空间模式的Phmi预测值。

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/42_00.gif)
<p align="center">
<em>图7 交互式操作 /Fig7 </em>
</p>


### 5 讨论 /discussion
#### 5.1 时间序列空间数据与独立位置数据分析
无人驾驶车载激光雷达导航是延车行路径的一个时间性连续过程，前后测量结果相互影响；同时地标空间模式随车行变化是一个连续移动的变化模式；再者，针对独立位置的地标变化是会影响到前后位置的导航评估，因此如果满足了独立位置的导航要求，即Phmi值大于math.pow(10,-5)，可能带来前后位置评估的变化，尤其降低Phmi值至不满足要求。

本次实验主要针对独立位置的数据分析，探索无人驾驶激光雷达导航下地标空间模式与采样位置关系的方法，通过模式数据特征描述初步观察地标空间位置与评估值直接的关系；通过建立学习模型尝试对任何地标空间模式预测评估值的变化；并通过交互式操作探索模式特征。在独立位置数据分析基础上，进一步分析无人驾驶时间序列空间数据。
___



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
eyJoaXN0b3J5IjpbLTE0NTQzNzIwNDYsMTA4NDc4OTIzNSwxOD
k4NDg5Nzk3LDU2MzU0NjY4MiwxNDUyNTIwMDgzLC01ODc0NTY2
NjcsLTc0ODU1OTA5Niw5MTQ3NjY1NzksLTMyNjg0OTYyNiwxNz
AxNzI2MTA2LC04MzYzMjM5ODksMjA3NDQ3NzUzOSwtMTMwNDI0
NTk2OSwxNjQ2NzgwNTc0LDEyNDA5MTU1MDIsMTg1NTEwNTcyNS
w5NDMxMTQ5NTcsLTEyMDYzNTAxOTAsMTI2OTQyMTkwMywtOTIy
MDA4ODEyXX0=
-->