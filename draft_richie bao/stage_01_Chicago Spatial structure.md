# 阶段1 芝加哥城市空间结构/stage 1 the city spatial structure of Chicago
> 无参考文献版 /no reference version
## A. 城市物质空间连续距离聚类下空间结构变化 /Spatial structure changes under continuous distances clustering of urban material space
### 1 背景 /background
在一定程度上，城市的物质空间变化反应了城市的蔓延趋势，包括城市的扩张和收缩。城市在扩张阶段会不断的侵占自然资源，影响自然生态平衡，尤其对生物群落分布、地表径流区域、气候环境变化有直接的影响。而在城市的收缩阶段则需要考虑更多如何有效自然恢复的问题。同时，城市物质空间的变化反应了城市居民的分布情况，其集聚的程度，分布的结构变化反应了人们分布的密度和活动的程度。因此对于城市尺度下物质空间结构的分析可以理解城市的分布，尤其自然与城市的交融关系，为保护自然，恢复自然和改善城市环境提供基础的分析。

To a certain extent, the physical spatial changes of the city reflect the urban sprawl, including the expansion and contraction of a city. During the expansion phase, cities will constantly occupy natural resources and affect the natural ecological balance, especially the distribution of biological communities, surface runoff areas, and climatic environmental variarion. In the contracting phase of the city, more questions need to be asked about how to recover effectively and naturally. At the same time, the change of urban physical space reflects the distribution of urban residents, the degree of agglomeration and the structure change of distribution reflect the density and activity of people. Therefore, the analysis of material spatical structure at the urban scale can understand the distribution of cities, especially the relationship between nature and cities, and provide a basic analysis for the protection, restoration and improvement of urban environment.
### 2 数据 /data
使用Landsat 8 系列数据，其空间分辨率为30m。考虑到城市周边农田不同季节耕作对于影像解译的影响，选择了三个季节的卫星影像，具体数据为(包含NDVI的分类条件)：

Landsat 8 series data was used with a spatial resolution of 30m. Considering the impact of farmland cultivation around the city in different seasons on the image interpretation, satellite images of three seasons were selected, with speicfic data as follows(including the classification conditions of NDVI):
* LC08_L1TP_023031_20191007_20191018_01 :water<0;green>=0.213;0=<buit<0.213
* LC08_L1TP_023031_20190804_20190820_01 :water<0;green>=0.213;0=<buit<0.213
* LC08_L1TP_023031_20180310_20180320_01 :water<0;green>=0.14;0=<buit<0.213

### 3 方法 /method
#### 3.1 基于DBSCAN连续距离聚类建成区，分析城市空间结构的变化 /analyze changes of urban spatial structure based on continuous distances clustering built-up areas using DBSCAN
城市物质空间的结构通常是基于其位置的地理分布，其集聚的程度是以距离为基本约束条件，因此基于DBSCAN（Density-Based Spatial Clustering of Applications with Noise.）算法，设置一个连续的聚类距离，分别计算每一距离下的聚类。因为所选取的影像空间分辨率为30m，距离列表的间隔应该是该值的倍数，其距离列表为[30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480]，共计16个值。

The structure of urban material space is usually based on the geographical distribution of its location, and the degree of its agglomeration is according to distance as the basic constraint condition. Therefore, a continuous clustering distance is set in term of DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm, and the clustering under each distance is calculated separately. Since the selected images spatial resolution is 30m, the spacing distance of the distance lsit should be a multiple of thie value, and the distance list is [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480], with a total of 16 values.

聚类的目标为城市建成区，由所获取的Landsat 8不同季节的遥感影像，根据NDVI（Normalized difference vegetation index）值的变化提取建成区，植被和水体三类。

The target of clustering is urban built-up areas, which is interpreted from the remote sensing images of Landsat 8 in different seasons , contains three types: built-up area, vegetation and water according to the change of NDVI(Normalized difference vegetation index).

#### 3.2 分析连续距离聚类下聚类总数，最大聚类总数，聚类频数和最大聚类变化值的变化趋势，找到聚类的关键层级 /analyze the trends of the total number of clusters, the maximum number of clusters, the frequency of clusters and the maximum change value of clusters under continuous distance clustering to find the critical levels of clusters
计算获取多个距离层级聚类，可以观察城市建成区的蔓延趋势。同时，为了进一步分析层级间的变化特点，找到具有意义的层级，需要建立聚类总数，最大聚类总数，聚类频数和最大聚类变化值在连续聚类距离下的变化趋势折线图，由拐点找到曲线变化的关键点，即找到具有意义的关键层级。

Multiple distance hierachical clustering is obtained to observe the spreading trend of urban built-up areas. At the same time, in order to further analyze the characteristics of hierachy changes, find meaninful levels, need to establish changes line charts of a number of clustering, the largest number of clustering, clustering requency and maximum value under continous clustering distances. And then, find the meaningful level by the inflection points on the curve.

其中最大聚类变化值的变化趋势是计算两两连续层级间最大聚类的变化范围，首先提取每一层级的最大聚类区域，设置两两层级中的上层建成区值为1，下层为2，做和处理，则可能出现值为0，1，2，3等四种情况。其中，0代表两层均没有值，1代表上一层有值，2代表下一层有值，3代表两层均有值，从而通过计算可以分析最大聚类变化值的变化情况，同时建立最大聚类变化数量值在聚类距离下的折线图，观察数据变化。

The change trend of the maximum clustering various value is to calculate the change range of the maximum clustering values between consecutive layers. First, extract the maximum clustering area of each layer. Second, set the value of the upper built-up area in the two layers to 1, and the value of the lower one to 2, and then, sum the two layers. The result value may appear  four cases: 0,1,2,3. Where, 0 represents no value for both layers, 1 represents value for the upper layer, 2 represents value for the lower layer, and 3 represents value for both layers. In this way, the change of the maximum clustering values can be analyzed through calculation. Plus, establish the line chart of the maximum clustering change values to observe the data change trend.

#### 3.3 应用卷积的方法计算连接度，分析建成区连接的变化程度 /calculate the connection degree by convolution method to analyze the change degree of connection in built-up area
聚类的方法可以根据指定的距离或者其它数据类型将相近的数据分别标识为不同组，同组的数据具有相同或相近的特征，例如距离上接近。同时，为了进一步观察建成区的联系程度，可以计算建成区每一位置点与周边位置点连接的程度，使用卷积的方式计算。

The clustering method can identify similar data as different groups according to the specified distance or other data types, and the data in the same group have the same or similar characteristics, such as proximity in distance. Meanwhile, in order to further observe the connection degree of the built-up area, we can calculate the connection degree of each position point of the built-up area with the surrounding postion points using convolution to calculate.

在卷积计算中，不同大小的卷积核，例如(3,3),(5,5)...(n,n)，其中n设置为奇数，中心值设置为0，其它值均为1，例如一个（3，3）的卷积核，形式为[[1,1,1],[1,0,1],[1,1,1]]，计算每一位置与周边临近的8个位置的连接关系，而(5,5)则计算每一位置与周边临近的24个位置的连接关系，依次类推。共设置24组卷积核，即卷积核距离为[3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49]，其实际距离需要乘以栅格分辨率的值，即30m。

In convolution calculations, there are diffent sizes convolution kernels, such as (3,3),(5,5)...(n,n), where n is set as odd, the center value is set as 0, and all other values are 1. For example, a convolution kernel of (3,3) is set as [[1,1,1],[1,0,1],[1,1,1]], calculate the conneciton relation between each position and 8 adjacent positions. And, (5,5) calculate the conneciton relation between earch postion and 24 adjacent positions, and so on. A total of 24 sets of convolution kernels are set, the kernel distance list is [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49], the actual distance needs to be multipled by the value of the raster resolution, namely 30m.

#### 3.4 连续距离聚类连接度及分析连接度聚类频数找到关键变化层级 /continuous distance clustering and analysis of connectivity clustering  frequency to find the critical levels of change
计算连接度的结果会获得每一个位置连接程度的数值标识，进一步使用DBSCAN聚类的方法，将具有近似连接程度的位置集聚，从而可以观察城市连接程度的空间结构，观察建成区分布情况。同样应用折现图找出具有意义变化的关键层级。

The result of calculating connectivity degree will obtain the numerical mark of each location, DBSCAN clustering method will be further used to cluster locations with approximate connectivity degree, so that the spatial structure of urban connectivity degree and the distribution of built-up areas can be observed. Also, use the line graph to find the key levels of meaningful change.

### 4 结果 /results
#### 4.1 连续距离聚类建成区及其关键层级覆盖范围 /continuous distance clustering built-up area and their critical level coverage area
##### 4.1.1  连续距离聚类建成区 /continuous distance clustering built-up area 
<p align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_5.jpg" width="400"> 
</p>
<p align="right">
<em>图1 遥感影像解译 /Fig1 remote sensing imagery interpretation</em>
</p>
首先利用Landsat 8遥感影像



##### 4.4.2 关键层级的提取及其覆盖范围 /extraction of critical levels and their coverage




#### 4.2 建成区连接度及其关键层级边缘 /connectivity of built-up areas and their critical level edges
##### 4.2.1 建成区连接度及其各个层级最大聚类的变化 /the connectivity  of built-up areas and the variation of maximum clustering at each level


##### 4.2.2  连接度的关键层级确定及其空间范围变化 /critical level determinaiton of connectivity and its spacial range variation













<!--stackedit_data:
eyJoaXN0b3J5IjpbLTY5MDk2ODgwMCwtNjgxMzk0NjI4LDE5OD
Y0NDIxNTYsLTgxMzU0NTA0NSwtMTMxNzA1MTY0OSwxODE0NjI4
Njc5LC04NTM0MjM2MzUsMTk4NTk1MjQyMCwxMDczOTgzMDAsLT
UzMTI1NDMyMiwtMTE5NTUyNzIyOCwtNTA0NDIyNzEyLDEyMzcw
MjQ0MzEsODE5Mjg1NTAyLC0xNzc5ODY1NDQsLTIwODg2MzIxNz
ksLTY0NTAxMTUwMSwyMDE1ODU5NTYxLDkzNzQ0Nzg2MywtMTAz
NTI0Mjg2Ml19
-->