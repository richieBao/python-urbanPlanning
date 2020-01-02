# 阶段1 芝加哥城市空间结构/stage 1 the city spatial structure of Chicago
> 无参考文献版 /no reference version  初稿 /draft  by richie bao
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
</br></br>
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

The phisical space of a city is an urban entity built by human beings, carrying human life and production activities, and reflecting the way of urban life to a certain extent . When from the macroscope to the proper area can further reflect the way of people life with the social attribute of infrastructure, for example, parking, place_of_worship，restaurant，school，fuel，cafe，fast_food，waste_basket，bank，bicycle_parking，pharmacy，toilets，toilets，police，clinic,etc, can be further concrete exploration of urban living space distribution structure, found the operation mode of people's lives in a city.
### 2 数据 /data
数据使用OSM(open street map)提供的开源数据。OSM地图数据已经被广泛应用于制作地图以及相关研究，用户包括Facebook、Craigslist、Seznam、OsmAnd、Geocaching等，芝加哥部分的OSM数据nodes（点数据）内容满足本次研究的要求。

The data uses open source data provided by OSM(open street map). OSM map has been widely used in mapping and related research including Facebook、Craigslist、Seznam、OsmAnd、Geocaching, etc. OSM data content in Chicago met the requirement of this study.
<p align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_03.jpg" width="400">  
</p>
<p>
<em>图1 OSM点数据范围 /Fig1 OSM points data range</em>
</p>
图1所提取的该部分数据包括81519个点，含所有类型的标签，“other_tags”字段非空标识为66263个点，其中"key"字段包含的类型有198个，未标识部分为公路设施内容，包含内容如下列表：
</br></br>
The extracted data shown in Fig 1 contains 81519points, including all types of tags, "other_tags" field have 66263 points, among witch the "key" field contains 198 types, and the undentified part is the content of highway facilities, contains the following list:

>  公路设施标签 /highway facility label

```python
['motorway_junction' None 'traffic_signals' 'crossing' 'turning_circle' 'stop' 'turning_loop' 'passing_place' 'mini_roundabout' 'give_way' 'bus_stop' 'stop;crossing' 'priority' 'construction' 'elevator' 'steps' 'speed_camera' 'street_lamp' 'rest_area' 'footway']
```

> "key"字段标签（1级标签） /“key” field label (primary label)

```python
['"curve_geometry"' '"noref"' '"operator"' '"amenity"' '"addr:housenumber"' '"traffic_signals"' '"railway"' '"network"' '"population"' '"ref:left"' '"bicycle"' '"crossing"' '"noexit"' '"subway"' '"public_transport"' '"light_rail"' '"gnis:id"' '"census:population"' '"gnis:Class"' '"alt_name"' '"access"' '"traffic_calming"' '"stop"' '"foot"' '"crossing:barrier"' '"power"' '"bus"' '"restriction:hgv"' '"addr:city"' '"gnis:feature_id"' '"direction"' '"button_operated"' '"cycleway"' '"old_name"' '"layer"' '"train"' '"junction"' '"entrance"' '"lit"' '"fee"' '"designation"' '"traffic_sign"' '"odbl"' '"owner"' '"lanes"' '"tourism"' '"FIXME:ref"' '"sport"' '"leisure"' '"shop"' '"waterway"' '"seamark:type"' '"level"' '"aeroway"' '"brand"' '"sprays"' '"fishing"' '"url"' '"bench"' '"kerb"' '"enforcement"' '"ref:right"' '"gnis:county_id"' '"gnis:created"' '"addr:postcode"' '"religion"' '"end_date"' '"building"' '"abandoned"' '"natural"' '"landuse"' '"communication:radio"' '"tower:type"' '"historic"' '"artist_name"' '"disused"' '"harbour"' '"addr:state"' '"phone"' '"access:conditional"' '"height"' '"Comment"' '"type"' '"water"' '"atm"' '"addr:street"' '"wifi"' '"internet_access"' '"milepost"' '"construction"' '"closed"' '"electrified"' '"bottle"' '"restriction:conditional"' '"attraction"' '"dataset"' '"tower"' '"emergency"' '"addr:housename"' '"platforms"' '"office"' '"craft"' '"disused:railway"' '"opening_hours"' '"artwork_type"' '"surveillance"' '"name:ru"' '"door"' '"addr:country"' '"covered"' '"male"' '"chicago:building_id"' '"solar"' '"advertising"' '"bollard"' '"toilets:wheelchair"' '"website"' '"information"' '"vacant"' '"addr:street:name"' '"shower"' '"TODO"' '"contact:phone"' '"contact:fax"' '"description"' '"service"' '"elevator"' '"food"' '"wikidata"' '"crossing_ref"' '"fax"' '"wikipedia"' '"size"' '"addr:floor"' '"ele:msl"' '"sloped_curb"' '"shelter"' '"local_ref"' '"club"' '"email"' '"motor_vehicle"' '"artist"' '"diet:vegan"' '"country"' '"name:en"' '"indoor"' '"camera:mount"' '"disused:amenity"' '"beauty"' '"destination"' '"maxspeed"' '"healthcare"' '"NHS"' '"razed:amenity"' '"tower:construction"' '"lamp_type"' '"manhole"' '"material"' '"abandoned:highway"' '"playground"' '"healthcare:speciality"' '"traffic_signals:direction"' '"dock"' '"cuisine"' '"stars"' '"denotation"' '"generator:method"' '"elevation"' '"building:material"' '"cutting"' '"leaf_cycle"' '"label"' '"board_type"' '"cemetery"' '"restriction"' '"xmas:day_date"' '"was:xmas:feature"' '"payment:cash"' '"dance:teaching"' '"abandoned:railway"' '"leaf_type"' '"inscription"' '"color"' '"bin"' '"side"' '"bridge:support"' '"clothes"' '"airmark"' '"artwork"' '"ford"' '"contact:website"' '"bonnet:colour"' '"max_age"' '"colour"' '"disused:country"' '"flag:colour"' '"communication:mobile_phone"' '"automatic_door"']
```

因为每一个点数据均代表了人们潜在的日常行为活动，因此所使用的OSM的Nodes节点数据包括所有一级分类Key标签及公路设施部分。
 
Since each point data represents the potential daily behavior activities of people, the Nodes node data of OSM used includes all primary classification "Key" labels and highway facilities.
### 3 方法 /method
#### 3.1 基于节点的位置信息研究城市生活行为的空间距离层级变化特征 /Based on the location information of nodes, study the spatial distance hierachy variation characteristics
基于OSM的Nodes的位置信息发现城市生活空间的行为结果，将会包含两层含义，一层是数据本身所具有的属性意义，所包含的数据越准确，越全面，则分析的结果趋于真实；另一层是数据建立的行为，因为OSM数据的收集包含志愿者参与数据贡献的行为，某些区域可能广为关注，而部分区域则少人问津，因此会存在同类数据分布的不平衡，但同时也反应了人们更为关注的城市区域。

Based on the location information of Nodes from OSM, the behaviour results in urban living space will contain two meanings. The first one is the atribute meaning of the data itself. The more accurate and comprehensive the data is, the more real the analysis results will be. The other one is the behavior of data establishment. Since the collection of OSM data was influenced by the behavior of volunteers participating in the data contribution, some areas may be widely concerned, while some areas are less visited, so there will  be an unbalanced distribution of similar data, but it also reflects the urban areas that people pay more attention to.

城市生活行为是受到距离的影响，在不同的距离区间下，人们的生活行为往往会存在差异。因此发展了关于城市生活圈的研究，例如按照居民日常生活中各类活动发生的时间、空间以及功能特征，可以将居民的日常生活圈划分为五个等级层次，包括社会生活圈、基本生活圈、通勤生活圈、扩展生活圈以及都市区之间的协调生活圈*(柴彦威,张雪,孙道胜.基于时空间行为的城市生活圈规划研究——以北京市为例[J].城市规划学刊,2015(03):61-69.)*。在探索这些具有属性特征Nodes，基于 DBSCAN（Density-Based Spatial Clustering of Applications with Noise）聚类分析时，设置不同的空间距离，此次设置的距离列表为从20m到520m，每10m设置一个值，共计50个距离值。

Urban living behavior is influenced by distance, and people's living behavior is often different at different distances. Therefore developed teh research on city life circle, for example, according to all kinds of activity time, space, and function characteristics of resident's daily life, it can be divided into five hierarchy, refering to social life circle, basic life circle, commuter life circle, extend life circle and the coordination circle between metropolitan areas.*((yan-wei chai,zhang xue,  dao-sheng sun.A Study on Life Circle Planning Based on Space Time Behabior Analysis: A Case Study of Beijing [J]. Journal of urban planning, 2015 (03) : 61-69. )* When exploring these Nodes with attribute characteristics and base on DBSCAN（Density-Based Spatial Clustering of Applications with Noise）clustering analysis, differnet spatial distances were set. The distance list was set from 20m to 520m with an inteval of 10m, a total of 50 distance values.

同时为了观察各个层级聚类结果中最大组团的变化，分别增加字段“idx"和“layer”，其中每一层级的"idx"字段值均为1，对求和所有层级，则值越大的区域在各层级中出现的次数越多，可以观察最大组团扩张的趋势；而每一层级的“layer”字段为层级标识，融合时按照顺序保留字段值，重叠的区域仅保留上层字段值，计算结果反应了节点在各个层级下出现的次序。

Meanwhile, in order to observe the change of the largest group in the clustering resluts of each level, the field "idx" and "layer" were added, where the field value of "idx" in each level was 1, if the sum was applied to all levels, the larger the value, the more times the area appeared in each level, and the trend of the largest group expansion could be observed. The "layer" field of each layer is the identificaiton of the hierarchy, and the value of the field is kept in order during the fusion, while only the value of upper layer field is kept in the overlapping area. The calculated results reflects the order in which the nodes appear at each level. 

#### 3.2 寻找城市生活空间的关键距离层级 /find the critical distance hierarhcy of urban living spaces
城市生活行为受到距离的影响，根据每一层级的聚类结果，通过建立聚类最大总数、独立点频数与聚类距离的关系曲线，计算拐点，以及通过建立聚类频数与聚类距离的箱型图，确定城市生活空间的关键距离层级。

City life behavior is affected by the distance, in line with the clustering results of each level, through the establishment of line graph between the maximum number of clusters, independent point frequency and clustering distance, and by establishing the box graph between clustering frequency and clustering distance, determine the critical level of urban life space.

### 4 结果 /results
#### 4.1 基于节点的位置信息研究城市生活行为的空间距离层级变化特征 /Based on the location information of nodes, study the spatial distance hierachy variation characteristics
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/35_01.jpg)
<p align="middle">
<em>图2 OSM的Nodes点50个层级聚类结果 /Fig2 OSM Nodes 50 hierarchical clustering results</em>
</p>
随着聚类距离的不断增加，点数据不断的集聚（图2），形成大大小小的组团，每一组团代表着组团内的成员之间具有较强的空间依赖关系。最初形成的具有一定规模的组团主要分布于downtown、Evaston、O'Hare International Airport、Oak Park等区域，进而在downtown周边不断出现新的组团，并不断融入到downtown，downtown具有明显的吸附作用。
</br></br>
With the continuous increase of clustering distance, point data is continuously gathered(Fig 2), forming clusters with large and small sizes. Each cluster represents a strong spatial dependency among the members of the cluster. The group with a certain size formed at the beginning were mainly ditributed in downtown、Evaston、O'Hare International Airport、Oak Park , etc, and new groups were constantly emerging around downtown ,and then integrating into downtown, which had an obvious adsorption effect. 

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_07.jpg)
<p align="middle">
<em>图3 各层级最大组团变化与芝加哥社区 /Fig3 Maximum group change at each level with Chicago community areas</em>
</p>
将每个层级最大的聚类组团的变化（图3）与芝加哥不同的社区叠合，描述随着聚类距离的增加，最大组团的形成与扩张途径。在20m～70m距离下，Loop 和Near North Side形成多个较大的组团，并不断融合，同时Evaston在该距离下亦具有明显优势；在70m～100m距离下，开始向Near West Side方向延申，但基本位于其东半部；100m～140m距离下，延湖岸向北延申至Lincoin Park、Lake View、Up Town区域，向南延申至Near South Side，在此距离下北部多数沿岸区域与起始downtown区域联系紧密，而南部较弱；在140m～180m距离下，延申方向指向西北方向，西向和西南方向，分别至Logan Suqare、Avondale、Humboldt Park、East Garfield Park、North Lawndale和South Lawndale，向北则包含Edge Water、Rogers Park与Evaston相连；自180m开始向西和南延申，并逐渐的延外层边缘向外拓展，至250m时，已经基本涵盖所有区域，除O'Hare机场区域、South Deering 高尔夫球场等区域外。
</br></br>
The changes of the largest cluster groups at each level (Fig 3) were superimposed with the different Chicago community areas to describe the formation and expansion of the largest cluster grjoups as the clustering distance increased. At the distance of 20 ～70m,  Loop and Near North Side form a number of larger groups and continue to merge. At the same time, Evaston also has obvious advantages at this distance. At the distance of 70m～100m, it begins to expand to Near West Side, but basically lies in its eastern half. At the distance of 100m～140m, along the Lake Michigan extends northward to Lincoin Park、Lake View、Up Town, and southward to Near South Side. At this distance , most coastal areas in the north are closely related to the initial downtown area, while the south is weak. At the distance of 140m～180m, the extension points to the northwest, west and southwest, to Logan Suqare、Avondale、Humboldt Park、East Garfield Park、North Lawndale and South Lawndale, and to the north, Edge Water、Rogers Park and Evaston are connected. Since 180m, it has extended to the west and south and gradually extended to the outer edge. By 250m, it has basically covered all areas, except the area of O'Hare airport and South Deering golf course.
<p>
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_09.jpg" width="400">  
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_08.jpg" width="400"> </p>
<p>
<em>图4 主城区扩张的延申方向(待替换)/Fig 4 the extended direcrion of the expasion of the main urban area(to be replaced)</em>
</p>
<p>
<em>图5 占绝对优势的层级/Fig5 the dominant hierarchy</em>
</p>
计算每一社区中最先出现的最大组团所在层级（图4），反应了聚类距离增加过程中，主要组团不断拓展的方向，其Chicago Sanitary and Ship Canal成为南北区域划分的关键线性空间。图5则计算每一社区中占绝对数量优势组团所在的层级，反映了该区域在整个芝加哥城中倾向的距离层级。例如O'Hare区域，为第40层级，即410m的距离，因为机场的功能性需求，处于城区的外围，通常需要跨越较大的距离才能够到达；而标识为15层级的中心城区，距离为160m，是可达性较高的区域。
</br></br>
The hierarchy of the largest group that first appeared in each community areas was calculated(Fig 5), which reflected the direction of the main groups expanding in the process of increasing the clustering distance. And Chicago Sanitary and Ship Canal became the key linear space for the division  of the north and south regions. Fig 6 calculates the hierarchy of the groups with the absolute majority amount in earch community area, reflecting the distance hierarchy that this area tends to have in the entire city of Chicago. For example, O'Hare area is the 40th level, that is the distance of 410m. Because of the functional requirements of the airport , it is located at the periphery of the urban area,  which usually needs to be reached over a large distance. The downtown area marked as level 15, with a distance of 160m, is the area with high accessibility.

#### 4.2 寻找城市生活空间的关键距离层级 /find the critical distance hierarhcy of urban living spaces
<p>
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/35_05.jpg" width="280">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/35_06.jpg" width="280">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/35_07.jpg" width="280">
</p>
<p>
<em>图6 独立点频数变化曲线与拐点/Fig 6 independent point frequency line graph and infleciton point</em>
</p>
<p>
<em>图7 聚类最大总数变化曲线与拐点/Fig 7 the maximum total amount and inflection point</em>
</p>
<p>
<em>图8 聚类频数分布与最大聚类组团数量变化/Fig 8 the clustering frequency distribution and the maximu cluster number change</em>
</p>
<p>
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_10.jpg" width="400">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_11.jpg" width="400">
</p>
<p>
<em>图9 140m/Fig 9 independent point frequency line graph and infleciton point</em>
</p>
<p>
<em>图10 聚类最大总数变化曲线与拐点/Fig 10 the maximum total amount and inflection point</em>
</p>
<p>
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_12.jpg" width="400">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/replenish_13.jpg" width="400">
</p>
<p>
<em>图11 独立点频数变化曲线与拐点/Fig 11 independent point frequency line graph and infleciton point</em>
</p>
<p>
<em>图12 聚类最大总数变化曲线与拐点/Fig 12 the maximum total amount and inflection point</em>
</p>

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTUwMTQxMDM3OSwyMDIyNzgzNzU4LC05OT
A3MjQ0OTQsLTI4MTI0MjE5NywxMDY4MzQwMTQ1LC0yMDQ5ODc2
NzcxLC0yMzgzMDI4NTQsLTIxMTA4Nzc0NzMsLTUzMzcxMzcyNi
wxODg1NDE0MDk4LC04MTI0NDc3NjEsMjgxODU1MzY0LDE1OTkx
NDM5MjIsLTE2Nzk5NTE3OSwtNzk3MjM5Njk0LC0xNDA5OTM1MT
k1LDQ2MDI3OTMyOCwtNTU4ODQ3MTE4LDE3MzM5NzY3MzcsLTE4
MzE0NTA4MzVdfQ==
-->