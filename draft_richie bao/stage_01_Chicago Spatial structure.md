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
首先利用Landsat 8遥感影像解译所需要的土地用地类型，如图1，影像的分辨率为30m。如果30×30m单元栅格中某一解译要素占主导数量，则标识为该元素类型，所以可以从解译影像中观察到分散的建设用地，因为绿化覆盖率较高，而大量居住建筑高度又通常低于树木高度，则该部分区域解译为植被区域。因此，基于该影像解译数据的计算是在考虑到了植被覆盖因素在内，建设用地的分布情况。
</br></br>
First, Landsat 8 remote sensing image is used to interpret the types of land used, as shown in figure 1. The resolution of image is 30m. If a certain interpretation element dominates the number of 30×30m grid cells, it is identified as the element type. Therefore, because the green coverage rate is high, and the height of a large number of residential buildings is usually lower than the height of trees, scatterd construction land is interpreted as a vegeation area. In consequence, the calculation based on the interpretation data of the image takes into account the distribution of construction land with vegetation cover.

![ ](https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_6.jpg)
<p align="center">
<em>图2 建成区连续距离聚类结果 /Fig2 continuous distance clustering results based on built-up area</em>
</p>
图2中30m层级的聚类结果中，最大的聚类区域已经基本提取了芝加哥城的主要区域，并纳入了部分临近的区域，主要包括Elk Grove Village, Northlack, Melrose Park, Cicero, Berwyn, Summit, Bedford Park, Evergreen Park, Whiting等。同时沿城市主要道路延申，主要包括Tri-State Tollway(Toll road), Jane Addams Memorial Tollway(Toll road), Chicago-Kansas City Expy(Toll road)等。随着聚类距离的增加，城市建成区的范围延芝加哥城边界向往逐步扩展（除东部湖区外），约至Fox river和Fox lake止，在Fox river西部有部分延续。至聚类距离480m时，最远有道路Tri-State Tollway向北延伸至Waukegan，  延Jane Addams Memorial Tollway(Toll road)向西北延申至Belvidere和Rockford，延Fox river和Des Plaines river至西南Ottawa。
</br></br>
Among the 30m clustering results in figure 2, the largest clustering area has basically extracted the main area of Chicago city and included some adjacent areas, including Elk Grove Village, Northlack, Melrose Park, Cicero, Berwyn, Summit, Bedford Park, Evergreen Park, Whiting etc. Meanwhile, it extends along the main roads of the city, mainly including Tri-State Tollway(Toll road), Jane Addams Memorial Tollway(Toll road), Chicago-Kansas City Expy(Toll road), etc. With the increase of clustering distance, the scope of urban built-up area extends to the boundary of the city of Chicago and gradually expands (except the eastern lake district), ending at Fox river and Fox lake, and extending partly to the west of Fox river. When the clustering distance was 480 m, road Tri-State Tollway extends as far north as Waukegan, road Jane Addams Memorial Tollway(Toll road) extends as far northwest as Belvidere and Rockford, rivers Fox river and Des Plaines river extends as far southwest as Ottawa.

![ ](https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_8.jpg)
<p align="center">
<em>图3 最大聚类区域两两层级的变化 /Fig3 the maximum clustering region changes in two levels</em>
</p>
图3则进一步说明了最大聚类区域即芝加哥主城区向外扩张延申的过程。
</br></br>
Fig.3  further illustrate the process of the expansion and extension of the maximum clustering area, namely the main city of Chicago.

##### 4.4.2 关键层级的提取及其覆盖范围 /extraction of critical levels and their coverage
<p>
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_1.jpg" width="400">  
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_01.jpg" width="400">  
</p>
<p>
<em>图4 聚类总数变化曲线及其拐点 /Fig4 the change line graph of the total number of clusters and its inflection point</em>
</p>
<p>
<em>图5 180m聚类距离最大聚类区域及水文要素 /Fig5 the maximum clustering area at the 180m distance and hydrological factors</em>
</p>
聚类总数随着聚类距离的增加而降低（图4），在180m拐点之前降低的速度较之之后快。该拐点说明了城市建成区在扩张过程中，在该距离之下达到相对稳定的一个状态。自然因素在该过程中起到主要的作用，从图5中可以观察到，建成区基本位于海拔约200m及其以下的区域，而早期的大部分建筑就建在芝加哥河口附近的低矮沙丘上。延Fox river南北方向发展起来的区域，在一定程度上在东西向与芝加哥城相互吸引而建立联系，同时Des Plaines river在两岸延西向拓展。
</br></br>
The total number of clusters decreased with the increase of the clustering distance(Fig 5), and the rate of the decline before the inflection point of 180m was faster than after. The infleciton point indicates that the urban built-up area reaches a relatively stable state under this distance during the expansion process. Natural factors play a major role in this process. As can been seen from Fig.6, the built-up area is basically located at an altitude of about 200m and below, while most of the early building began on low dunes around the Chicago River's mouth. The area developed along the north and south direction of the Fox river to some extent establishes a connection with the city of Chicago by attracting each other in the east and west direction, and the Des Planines river expands westward on both sides.
<p>
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_4.jpg" width="400">  
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/31_7.jpg" width="400"> </p>
<p>
<em>图6 最大聚类区域所包含数量变化值 /Fig6 the quantitative variation value contained in the maximum clustering region</em>
</p>
<p>
<em>图7 最大聚类区域的连续扩张 /Fig7 continous expansion of the maximum clustering region</em>
</p>
180m是建成区相对稳定的层级，图6，7进一步印证了该结论。在180m到210m层级间的拓展达到谷底，说名180m层级在进一步拓展中，增加的拓展区域相对较小，而谷底之后集聚数量增加，是因为较远建成区域由道路连接加入到已集聚的区域。
</br></br>
180m is a relatively stable level of built-up area, which is further confirmed by Fig 6 and 7. The expansion between 180m and 210 reached the valley bottom. It is said that in the further expansion of 180m, the increased expasion area is relatively small. And the number of agglomeration increased after the valley bottom, because the far built-up area was connected by road to join the already concentrated area.

#### 4.2 建成区连接度及其关键层级边缘 /connectivity of built-up areas and their critical level edges
##### 4.2.1 建成区连接度及其各个层级最大聚类的变化 /the connectivity  of built-up areas and the variation of maximum clustering at each level
采用距离聚类的方法可以将满足指定距离要求的位置集聚，每一聚类组团自身在空间上是连续的。为了探究空间上连续的程度，计算每一单元与周边单元在连续卷积核距离下的连接程度，计算结果如图8。

The distance clustering method can be used to gather the positions that meet the requirements of the specific distance, and each cluster itself is spatically continous. In order to explore the degree of spatial continuity, the connection degree between each cell and the surrounding cells under the distance of continuous convolution kernel is calculated, and the calculated result is shown in Fig 8.
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_3.jpg)
<p align="center">
<em>图8 连续卷积核距离下的连接度 /Fig 8 connection degree at continuous convolution kernel distance</em>
</p>
当卷积核距离较小时，例如3×3的卷积核，在30m高空分辨率下所达到的范围为90×90m方格，计算每一单元的连接度基本相同，随着卷积核距离的增加，每一单元与周边单元连接范围的扩大，每一单元的连接度值逐渐开始分化，具有更强连接程度的单元开始显现。为了能够清晰的观察连接的程度分布，计算每一层级连接度的结果，如图9。

When convolution kernel distance is small, such as 3×3 convolution kernel, under 30m high attitude resolution is 90×90m square, the connections of each cell are basically the same, with the increase of convolution kernel distance, each cell connected to the peripheral cells scope expands, the connection degree of each unit is gradually began to differentiate, the cells with stronger connection degree begin to emerge. In order to clearly observe the connection degree distribution, cluster the results of connection degrees at each level, as shown in Fig 9.
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_4.jpg)
<p align="center">
<em>图9 连接度聚类（前20组） /Fig 9 connectivity clustering(first 20 groups)</em>
</p>

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_02.jpg)
<p align="center">
<em>图10 3×3m连接度聚类分布（前20组） /Fig 103×3m connectivity clustering distribution (first 20 groups)</em>
</p>
计算建成区的连接度，最小距离卷积核计算结果呈现出最大关联的区域，也是绿地率相对较小的区域。从图10结果分析，从芝加哥市中心向外延申为连续的建成区域，以W Garfield Blvd和CSXT运输铁路为界，主要集中于其北部和西部，是面积最大的连续建成区。同时机场O'Hare International Airport、Gary/Chicago International Airport，港口Indiana Harbor，仓储等地的绿地率较小，具有较大面积的不透水区域。
</br></br>
The connection degree of the built-up area is calculated, and the result of the calculation of the minimum distance convolution kernel presents the region with the greatest correlation, which is also the region with relatively small green land rate. According to the result analysis in Fig 10, the continuous built-up area from downtown of Chicago mainly concentrated in the north and west of the area bounded by W Garfield Blvd and CSXT transportation railway. At the same time, airport O'Hare International Airport, Gary/Chicago International Airport, port ndiana Harbor, storage and other places have small green rate, with relatively large areas of impervious areas.

##### 4.2.2  连接度空间变化趋势及其空间范围变化 /the variation trend of connectivity space and its spacial range variation
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/32_5.jpg)
> 待解决 /to be solved.
### 5 讨论 /discusion
#### 5.1 

#### 5.2 绿地与建成区互为钳制的关系



___
## B.  城市生活空间连续距离聚类下空间结构变化 /the spatial structure of urban living space changes under continous distance clustering
### 1 背景 /background
城市的物质空间是人类建造的城市实体，承载着人类的生活、生产活动，并在一定程度上反应了城市生活的方式。当从宏观的建成区区域落实到能进一步反应人们生活方式，具有社会属性的基础设施时，例如停车场、礼拜、餐馆、学校、  加油站、咖啡馆、快餐馆、垃圾桶、银行，自行车停车位、药房、厕所、医院、警局、诊所等，则可以进一步具体探索城市生活空间的分布结构，发现城市中人们生活的运行方式。

The phisical space of a city is an urban entity built by human beings, carrying human life and production activities, and reflecting the way of urban life to a certain extent . 






<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEwMTEzODQ1NDUsLTI3Nzc4MzgyOCwtMT
c0MDE3MzY1OSwxMDIxMDcyMTYxLC0zODY3ODYzODksLTExMDA5
Njg1OTgsMTAzNTU4NTg5OCwxNDg5Nzk1MjU2LC0xMDg5MDY4MT
EsLTE5Mjc2MDY3ODQsMTI4MDE1MzY2MywtMTY3MzQ2MzQxMiw5
NzYwNDA2ODksLTEzNDYzMTg0MTgsLTU1MDA4MDg4LDgzMTI1OT
MyNywxNzUxMjIzNDgsNDM0ODUzMzY2LC01Njg0NDk5ODEsLTEx
MDM1NjgyMjddfQ==
-->