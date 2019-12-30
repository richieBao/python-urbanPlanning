# 阶段1 芝加哥城市空间结构/stage 1 the city spatial structure of Chicago
> 无参考文献版 /no reference version
## 1. 城市物质空间连续距离聚类下空间结构变化 /Spatial structure changes under continuous distances clustering of urban material space
### 1.1 背景 /background
在一定程度上，城市的物质空间变化反应了城市的蔓延趋势，包括城市的扩张和收缩。城市在扩张阶段会不断的侵占自然资源，影响自然生态平衡，尤其对生物群落分布、地表径流区域、气候环境变化有直接的影响。而在城市的收缩阶段则需要考虑更多如何有效自然恢复的问题。同时，城市物质空间的变化反应了城市居民的分布情况，其集聚的程度，分布的结构变化反应了人们分布的密度和活动的程度。因此对于城市尺度下物质空间结构的分析可以理解城市的分布，尤其自然与城市的交融关系，为保护自然，恢复自然和改善城市环境提供基础的分析。

To a certain extent, the physical spatial changes of the city reflect the urban sprawl, including the expansion and contraction of a city. During the expansion phase, cities will constantly occupy natural resources and affect the natural ecological balance, especially the distribution of biological communities, surface runoff areas, and climatic environmental variarion. In the contracting phase of the city, more questions need to be asked about how to recover effectively and naturally. At the same time, the change of urban physical space reflects the distribution of urban residents, the degree of agglomeration and the structure change of distribution reflect the density and activity of people. Therefore, the analysis of material spatical structure at the urban scale can understand the distribution of cities, especially the relationship between nature and cities, and provide a basic analysis for the protection, restoration and improvement of urban environment.
### 1.2 数据 /data
使用Landsat 8 系列数据，其空间分辨率为30m。考虑到城市周边农田不同季节耕作对于影像解译的影响，选择了三个季节的卫星影像，具体数据为(包含NDVI的分类条件)：

Landsat 8 series data was used with a spatial resolution of 30m. Considering the impact of farmland cultivation around the city in different seasons on the image interpretation, satellite images of three seasons were selected, with speicfic data as follows(including the classification conditions of NDVI):
* LC08_L1TP_023031_20191007_20191018_01 :water<0;green>=0.213;0=<buit<0.213
* LC08_L1TP_023031_20190804_20190820_01 :water<0;green>=0.213;0=<buit<0.213
* LC08_L1TP_023031_20180310_20180320_01 :water<0;green>=0.14;0=<buit<0.213

### 1.3 方法 /method
#### 1.3.1 基于DBSCAN连续距离聚类建成区，分析城市空间结构的变化 /analyze changes of urban spatial structure based on continuous distances clustering built-up areas using DBSCAN
城市物质空间的结构通常是基于其位置的地理分布，其集聚的程度是以距离为基本约束条件，因此基于DBSCAN（Density-Based Spatial Clustering of Applications with Noise.）算法，设置一个连续的聚类距离，分别计算每一距离下的聚类。因为所选取的影像空间分辨率为30m，距离列表的间隔应该是该值的倍数，其距离列表为[30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480]，共计16个值。

The structure of urban material space is usually based on the geographical distribution of its location, and the degree of its agglomeration is according to distance as the basic constraint condition. Therefore, a continuous clustering distance is set in term of DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm, and the clustering under each distance is calculated separately. Since the 


聚类的目标为城市建成区，由所获取的Landsat 8不同季节的遥感影像，根据NDVI（Normalized difference vegetation index）值的变化提取建成区，植被和水体三类。


#### 1.3.2 分析连续距离聚类下聚类总数，最大聚类总数，聚类频数和最大聚类变化值的变化趋势，找到聚类的关键层级 /analyze the trends of the total number of clusters, the maximum number of clusters, the frequency of clusters and the maximum change value of clusters under continuous distance clustering to find the critical levels of clusters


#### 1.3.3 应用卷积的方法计算连接度，分析建成区连接的变化程度 /calculate the connection degree by convolution method to analyze the change degree of connection in built-up area


#### 1.3.4 连续距离聚类连接度及分析连接度聚类频数找到关键变化层级 /continuous distance clustering and analysis of connectivity clustering  frequency to find the critical levels of change









<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2NTE3MTA4MCwxMjM3MDI0NDMxLDgxOT
I4NTUwMiwtMTc3OTg2NTQ0LC0yMDg4NjMyMTc5LC02NDUwMTE1
MDEsMjAxNTg1OTU2MSw5Mzc0NDc4NjMsLTEwMzUyNDI4NjIsLT
E2NzQ0MzQzNDIsNzY5NzcxMzEwLC0yMDg5MDU3MDE4LC0xNjEw
OTk2NTIzLC0xNzMwMjY1MTI3XX0=
-->