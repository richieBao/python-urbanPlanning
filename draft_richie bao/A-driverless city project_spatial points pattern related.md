


# A-无人驾驶城市_空间点（landmarks）模式相关/A-driverless city project_spatial points(landmarks) pattern related
> @author: Richie Bao-Chicago.IIT(driverless city project)  data:IIT.driverless city project
### 规划组在无人驾驶城市项目中的工作内容 /The work content of the planning group in the driverless city project
当前无人驾驶城市项目的核心内容是探索GPS和车载激光雷达无人驾驶导航问题。无人驾驶的最终目的是应用研究成果于现实世界，服务人们的日常生活，因此需要探索城市布局与无人驾驶之间的博弈关系。一是改善导航技术，减弱城市空间对导航的影响；二是，对导航有影响的区域（例如高容积率，高密度的城市中心），适当布局城市，使得空间格局适应无人驾驶导航需求。

The critical content of the current driverless city project is to explore the problem of GPS and vehicle-mounted lidar driverless navigation. The ultimate goal of driverless city project is to apply the research results to the real world and serve people's daily life. Therefore, it is necessary to explore the game relationship between urban layout and driverless vehicles. One is to improve navigation technology and reduce the impact of urban space on navigation. Second, in areas that affect shipping (such as high plot ratio and high-density urban centers), cities should be appropriately laid out to make the spatial pattern adapt to AVs' navigation needs.

规划组则更多考虑城市空间布局的影响，尝试发现空间布局与导航评估值之间的关系，从抽象的特征数据到现实世界的模拟来不断发现与优化空间规划与无人驾驶之间的矛盾。

The planning group considers the impact of urban spatial layout and tries to find the relationship between spatial arrangement and navigation value.   From abstract feature data to real-world simulation, the planning group continuously finds and optimizes the contradiction between spatial planning and AVs.

## A-数据 /data
分析内容基于无人驾驶城市工程组激光雷达导航模拟数据结果。可以进一步划分为，原始测量数据，基于原始数据调整规划布局后的数据，重新规划后的数据。
此次实验数据包含两组，一组为原始模拟数据；一组为新规划模拟数据。

The analysis content is based on the results of the lidar navigation simulation data of the engineering group. It can be further into the original measurement data, the data after adjusting the layout based on the original data, and the data after re-planning. The experimental data includes two groups; one group is the original simulated data; Another is a set of simulated data for the new program.
![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_01.png)
<p align="center">
<em>图1 原始模拟数据  /Fig 1 raw simulation data </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_02.png)
<p align="center">
<em>图2 新规划模拟数据  /Fig 2 new program simulation data</em>
</p>

## B-关于相关性/about correlation
使用pandas(python库)的# pandas.DataFrame.corr方法计算相关系数，其中参数method有三种方法，如下：

The correlation coefficient is calculated using pandas.DataFrame.corr, in which the parameter method has three ways, as follows:

-   pearson : （线性数据）标准相关系数/standard correlation coefficient    
-   kendall : 等级相关系数/Kendall Tau correlation coefficient    
-   spearman :等级相关系数/Spearman rank correlation

或者scipy库scipy.stats.pearsonr/scipy.stats.kendalltau/scipy.stats.spearmanr计算，返回值1为pearson相关系数，值2为p-value（显著性检验）

Or use scipy library scipy.stats.pearsonr/scipy.stats.kendalltau/scipy.stats.spearmanr calculation, the return value 1 is the Pearson correlation, the value 2 p-value(significant test).
![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_03S.jpg)
<p align="center">
<em>图3 pearson相关系数  /Fig 3  pearson correlation</em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_04.png)
<p align="center">
<em>图4 PHMI相关的pearson相关系数  /Fig 4 Pearson correlation coefficient related to PHMI</em>
</p>

>相关系数值描述： |r|>0.95 存在显著性相关；|r|>=0.8 高度相关；0.5=<|r|<0.8 中度相关； 0.3=<|r|<0.5 低度相关； |r|<0.3 关系极弱，认为不相关；|r|=0 不相关。

>Correlation value description: |r|>0.95 there was a significant correlation; |r|>=0.8 highly correlation; 0.5=<|r|<0.8  moderately correlation; 0.3=<|r|<0.5  low correlation; |r|<0.3 the relationship is so weak that it is considered irrelevant; |r|=0 is irrelevant.

与landmarks空间点模式相关的变量（指数）选择：

Selection of variables(metrics) related to the landmarks space point pattern:

> landmarks为激光雷达拾取的环境特征点；location为无人车位置坐标。	

>Landmarks are environmental feature points picked up by lidar; Location is the position coordinate of the AV.

	1. landmarks点数量	<LM_amount>
	2.  location x与y坐标 <loc_x,loc_y>
	3. landmarks与location之间的距离：平均距离，最小和最大距离 <distance_mean,distance_min,distance_max>
	4. 以location为圆心划分36个方向：包含landmarks，不含landmarks，包含与否的边界 <direction_is, direction_none, direction_edge>
	5. landmarks密度（intensity）：最小边界范围，凸包 <intensity_mbb,intensity_hull>
	6. landmarks最近邻：最大值，最小值，均值以及最近邻为2个点的均值 <ndd_max,ndd_min,ndd_mean>
	7. 反应点模式为随机、均匀或者聚集的G函数值，其大于期望值（expectation）趋于聚集，小于则趋于均匀，等于则趋于随机 <G>
	8.  与连续距离（0-18）下样方统计的相关量：反应点模式的chi2均值，含有landmarks的样方数量，以及landmarks数量/含有landmarks的样方数量 <qdt_chi2_, qdt_num_, qdt_n/Q_>
	9. 离散化方法（可用于进一步预测模型的建立）：基于分位数，基于跳变点，基于pow(10,-5)即评估值的界定值 <PHMI_percentile, jitter_mean>

	1.  The number of landmarks
	2.  Location x and y
	3.  The distance between landmarks and location: average distance, minimum, and maximum distance
	4.  Divide 36 directions with a location as the center of the circle: landmarks included, landmarks excluded, and the boundary of inclusion or exclusion
	5.  Landmarks intensity: minimum boundary range, convex hull
	6.  Landmarks nearest neighbor: the maximum, minimum, mean and the mean of nearest neighbor with 2 points
	7.  The mode of spatial points is random, uniform, or aggregated value of G function, which is higher than the expectation and tends to aggregate; if it is less than, it tends to be uniform; if it is equal to, it tends to be random.
	8.  Correlation quantity of quadrat statistics under continuous distance(0-18): the chi2 mean value representing the point pattern, the number of quadrats containing landmarks, and the number of landmarks / the number of quadrats containing landmarks
	9.  Discretization method(which can be used for further establishment of prediction model): based on a quantile, based on jump point, and based on pow(10,-5), which is the defined value of the evaluation value
 

## C-问题 /question
### 0-相关系数值的大小 /The magnitude of the correlation coefficient
* pearson 相关性显著性检验 p-value /Pearson correlation significance test for p-value
```python
{'LM_amount': (0.12098482115871922, 6.382570797569555e-16),
 'loc_x': (0.17850258172741662, 4.720879152755005e-33),
 'loc_y': (-0.2178350753911575, 9.395833194024788e-49),
 'distance_mean': (0.10827296084597499, 4.926678335662525e-13),
 'distance_min': (-0.007745403087658743, 0.6062043140384599),
 'distance_max': (0.05882887545740473, 8.902054331810178e-05),
 'direction_is': (0.09709517565291108, 9.329880951182354e-11),
 'direction_none': (-0.09709517565291108, 9.329880951182354e-11),
 'direction_edge': (0.0735726402184724, 9.427092877763175e-07),
 'intensity_mbb': (-0.11348881207141291, 3.5178264091237454e-14),
 'intensity_hull': (-0.11037398850799626, 1.7267975757524983e-13),
 'nnd_max': (0.07837285524525486, 1.7500237255601293e-07),
 'nnd_min': (-0.16830906813381713, 1.604995848262056e-29),
 'nnd_mean': (-0.1362772945351204, 8.057506209705536e-20),
 'nnd2_mean': (0.042616437824948505, 0.004545348744835969),
 'G': (0.12168635025366975, 4.3285658092840924e-16),
 'chi2_10': (-0.10884639884038408, 3.7080340839692314e-13),
 'chi2_10_pval': (0.09848013315408069, 5.022386195664488e-11),
 'qdt_chi2_10dis': (-0.03398008579609409, 0.023686254276302075),
 'qdt_chi2_11dis': (0.05755802734366226, 0.00012611531767907697),
 'qdt_chi2_12dis': (0.17441676552262925, 1.305086790413563e-31),
 'qdt_chi2_13dis': (0.12022332563104801, 9.704178521007763e-16),
 'qdt_chi2_14dis': (0.1092107597328163, 3.0931008823772916e-13),
 'qdt_chi2_15dis': (0.13880733974344114, 1.6442879844521928e-20),
 'qdt_chi2_16dis': (0.10671147277077356, 1.06008140842146e-12),
 'qdt_chi2_17dis': (0.14084248188065462, 4.481240863949557e-21),
 'qdt_chi2_18dis': (0.12093675389549237, 6.554137514444971e-16),
 'qdt_chi2_19dis': (0.1009229954697013, 1.649733960527631e-11),
 'qdt_chi2_2dis': (0.12278374462503157, 2.3472802766407615e-16),
 'qdt_chi2_3dis': (-0.12036992455606758, 8.95401025252445e-16),
 'qdt_chi2_4dis': (0.12231963547306085, 3.0427049056541484e-16),
 'qdt_chi2_5dis': (0.16153804231646002, 2.7012814720197085e-27),
 'qdt_chi2_6dis': (0.010122511713723893, 0.5004919797731758),
 'qdt_chi2_7dis': (-0.1249090657625917, 7.063587690575604e-17),
 'qdt_chi2_8dis': (-0.006522668876065249, 0.6642031089483985),
 'qdt_chi2_9dis': (-0.04434923769301939, 0.0031460635331646706),
 'qdt_num_10dis': (0.12846927881710613, 9.020196984589894e-18),
 'qdt_num_11dis': (0.09042780933611005, 1.6321560165675333e-09),
 'qdt_num_12dis': (0.04299250258028851, 0.004200910284944702),
 'qdt_num_13dis': (0.07789372706010769, 2.0797215867139878e-07),
 'qdt_num_14dis': (0.08848680307520956, 3.61806103242767e-09),
 'qdt_num_15dis': (0.08422124889584881, 1.9624344127175603e-08),
 'qdt_num_16dis': (0.09577444980402383, 1.6707211849707632e-10),
 'qdt_num_17dis': (0.09299800356330726, 5.543894881091101e-10),
 'qdt_num_18dis': (0.09884615504807787, 4.257992108569129e-11),
 'qdt_num_19dis': (0.10526070450844854, 2.139202847313207e-12),
 'qdt_num_2dis': (nan, nan),
 'qdt_num_3dis': (0.15379300646203864, 7.274738215885313e-25),
 'qdt_num_4dis': (0.06979163942312835, 3.3094146273026727e-06),
 'qdt_num_5dis': (0.016615324261063543, 0.2687694791316126),
 'qdt_num_6dis': (0.09643271686952981, 1.2508752647631514e-10),
 'qdt_num_7dis': (0.16313483647090032, 8.225338840207966e-28),
 'qdt_num_8dis': (0.10205729582405537, 9.749105287047005e-12),
 'qdt_num_9dis': (0.12578018184022804, 4.2920246109503394e-17),
 'qdt_n/Q_10dis': (0.01981954220605587, 0.18709922509413546),
 'qdt_n/Q_11dis': (0.11160211173300359, 9.270059451429245e-14),
 'qdt_n/Q_12dis': (0.1787167104948144, 3.9582503602681626e-33),
 'qdt_n/Q_13dis': (0.14377673592467594, 6.647319427154761e-22),
 'qdt_n/Q_14dis': (0.12956096221867566, 4.7432431998372244e-18),
 'qdt_n/Q_15dis': (0.14841890765865706, 2.991098245006072e-23),
 'qdt_n/Q_16dis': (0.13411656849591866, 3.0582167421951987e-19),
 'qdt_n/Q_17dis': (0.14840386683676418, 3.0217963808669206e-23),
 'qdt_n/Q_18dis': (0.14214670828313222, 1.9283427964825516e-21),
 'qdt_n/Q_19dis': (0.12951314826870464, 4.879228752593167e-18),
 'qdt_n/Q_2dis': (0.12098482115871922, 6.382570797569555e-16),
 'qdt_n/Q_3dis': (-0.0058065507871446105, 0.699159517047621),
 'qdt_n/Q_4dis': (0.1104284936385315, 1.680019717852777e-13),
 'qdt_n/Q_5dis': (0.13811303349171716, 2.5507997792562158e-20),
 'qdt_n/Q_6dis': (0.025989374538291227, 0.08362996424243235),
 'qdt_n/Q_7dis': (-0.05295509998572752, 0.0004204964188767892),
 'qdt_n/Q_8dis': (0.010257012920512738, 0.49481652101961304),
 'qdt_n/Q_9dis': (0.0002287915288687048, 0.9878509986703182),
 'PHMI_percentile': (0.882532006101935, 0.0),
 'jitter_mean': (0.9600013225494279, 0.0),
 'PHMI': (0.999999999999999, 0.0)}
```
 pearson相关系数显著性检验中，distance_min，（qdt_chi2_6dis，qdt_chi2_8dis），qdt_num_5dis，（qdt_n/Q_10dis，qdt_n/Q_3dis，qdt_n/Q_6dis，qdt_n/Q_8dis，qdt_n/Q_9dis）p-value大于0.05，不能拒绝原假设，因此放弃对应的相关性分析，其中包括连续距离（0-18）下样方统计的相关量qdt_n/Q_。

In the Pearson correlation coefficient test, distance_min，（qdt_chi2_6dis，qdt_chi2_8dis），qdt_num_5dis，（qdt_n/Q_10dis，qdt_n/Q_3dis，qdt_n/Q_6dis，qdt_n/Q_8dis，qdt_n/Q_9dis）can not reject null hypothesis, so the corresponding analysis is abandoned, which includes the correlation quantity qdt_n/Q_ of the quadrilateral statistics under the continuous distance(0-18).
 
* corr_kendall_jitterMean
```python
{'LM_amount': KendalltauResult(correlation=0.09868247928894343, pvalue=3.318901980646537e-20),
 'loc_x': KendalltauResult(correlation=0.18587229156553534, pvalue=5.852005934852762e-76),
 'loc_y': KendalltauResult(correlation=-0.1811599713444254, pvalue=2.9947435483670355e-72),
 'distance_mean': KendalltauResult(correlation=0.10663443009641238, pvalue=3.598774174886995e-26),
 'distance_min': KendalltauResult(correlation=0.017501025618766815, pvalue=0.08242408318141854),
 'distance_max': KendalltauResult(correlation=0.04034586725107563, pvalue=6.230702321140347e-05),
 'direction_is': KendalltauResult(correlation=0.08504182378874513, pvalue=3.064036636625572e-15),
 'direction_none': KendalltauResult(correlation=-0.08504182378874513, pvalue=3.064036636625572e-15),
 'direction_edge': KendalltauResult(correlation=0.03337902482977431, pvalue=0.005940876021607218),
 'intensity_mbb': KendalltauResult(correlation=-0.10491250077564505, pvalue=2.5470165729009158e-25),
 'intensity_hull': KendalltauResult(correlation=-0.10982671977946788, pvalue=1.366597652311725e-27),
 'nnd_max': KendalltauResult(correlation=0.10766554584412595, pvalue=7.071103705421172e-26),
 'nnd_min': KendalltauResult(correlation=-0.1330647845573663, pvalue=1.2540228804227788e-37),
 'nnd_mean': KendalltauResult(correlation=-0.049620624995553496, pvalue=8.762750757266004e-07),
 'nnd2_mean': KendalltauResult(correlation=0.07623834087363987, pvalue=4.228622147333801e-14),
 'G': KendalltauResult(correlation=0.12432147020532276, pvalue=1.1921412069572789e-30),
 'chi2_10': KendalltauResult(correlation=-0.09187933092516117, pvalue=7.047487895698813e-19),
 'chi2_10_pval': KendalltauResult(correlation=0.08240106290397214, pvalue=3.215444079309133e-16),
 'qdt_chi2_10dis': KendalltauResult(correlation=-0.016456319468745442, pvalue=0.10650316470526575),
 'qdt_chi2_11dis': KendalltauResult(correlation=0.046269635926137954, pvalue=6.260926071528166e-06),
 'qdt_chi2_12dis': KendalltauResult(correlation=0.18177710975168265, pvalue=1.2133497349177524e-69),
 'qdt_chi2_13dis': KendalltauResult(correlation=0.15356435230908425, pvalue=5.3748993599251385e-49),
 'qdt_chi2_14dis': KendalltauResult(correlation=0.1617630212543716, pvalue=1.864618921739115e-55),
 'qdt_chi2_15dis': KendalltauResult(correlation=0.1391173294654868, pvalue=5.471825156188185e-41),
 'qdt_chi2_16dis': KendalltauResult(correlation=0.1012599603078974, pvalue=2.010891764032187e-22),
 'qdt_chi2_17dis': KendalltauResult(correlation=0.13429753054245808, pvalue=1.5245920997652237e-37),
 'qdt_chi2_18dis': KendalltauResult(correlation=0.08472720958081646, pvalue=3.376007532412867e-16),
 'qdt_chi2_19dis': KendalltauResult(correlation=0.06755668126491308, pvalue=8.260836447115661e-11),
 'qdt_chi2_2dis': KendalltauResult(correlation=0.1704247526437565, pvalue=2.9162480608530156e-60),
 'qdt_chi2_3dis': KendalltauResult(correlation=-0.10329133065099631, pvalue=1.1229883883596247e-23),
 'qdt_chi2_4dis': KendalltauResult(correlation=0.09942502685363583, pvalue=6.733827050475811e-22),
 'qdt_chi2_5dis': KendalltauResult(correlation=0.16184994011882853, pvalue=5.417867341537424e-57),
 'qdt_chi2_6dis': KendalltauResult(correlation=0.022856172375246245, pvalue=0.026450236890911357),
 'qdt_chi2_7dis': KendalltauResult(correlation=-0.09356969854338783, pvalue=3.852252856252567e-20),
 'qdt_chi2_8dis': KendalltauResult(correlation=-0.04530257198304244, pvalue=8.790545860197431e-06),
 'qdt_chi2_9dis': KendalltauResult(correlation=-0.03219050331811142, pvalue=0.00163502254528459),
 'qdt_num_10dis': KendalltauResult(correlation=0.10545511362014753, pvalue=5.83144795321116e-23),
 'qdt_num_11dis': KendalltauResult(correlation=0.08352609590812776, pvalue=7.268494584965335e-15),
 'qdt_num_12dis': KendalltauResult(correlation=0.029527899416711936, pvalue=0.0059950219722086934),
 'qdt_num_13dis': KendalltauResult(correlation=0.06570125215285438, pvalue=1.0233435649099037e-09),
 'qdt_num_14dis': KendalltauResult(correlation=0.07602565302709258, pvalue=1.5343329054350684e-12),
 'qdt_num_15dis': KendalltauResult(correlation=0.07194762507964002, pvalue=2.157535128965317e-11),
 'qdt_num_16dis': KendalltauResult(correlation=0.08599612780520371, pvalue=1.019938683847995e-15),
 'qdt_num_17dis': KendalltauResult(correlation=0.07892099576836793, pvalue=2.068849442391113e-13),
 'qdt_num_18dis': KendalltauResult(correlation=0.08783513572247198, pvalue=2.601301328026302e-16),
 'qdt_num_19dis': KendalltauResult(correlation=0.08860837596161139, pvalue=1.3726402819152883e-16),
 'qdt_num_2dis': KendalltauResult(correlation=nan, pvalue=nan),
 'qdt_num_3dis': KendalltauResult(correlation=0.13203757112938963, pvalue=3.578654604328611e-29),
 'qdt_num_4dis': KendalltauResult(correlation=0.061838705686883086, pvalue=7.730891941721151e-08),
 'qdt_num_5dis': KendalltauResult(correlation=0.0021310513556453536, pvalue=0.8465326207328754),
 'qdt_num_6dis': KendalltauResult(correlation=0.07148083167319869, pvalue=2.8789454066233553e-11),
 'qdt_num_7dis': KendalltauResult(correlation=0.1520245079333533, pvalue=9.030098183504689e-46),
 'qdt_num_8dis': KendalltauResult(correlation=0.09689743703142684, pvalue=7.503936358957514e-20),
 'qdt_num_9dis': KendalltauResult(correlation=0.10040473249859222, pvalue=4.358541542791735e-21),
 'qdt_n/Q_10dis': KendalltauResult(correlation=0.015846746214016723, pvalue=0.13279775031802224),
 'qdt_n/Q_11dis': KendalltauResult(correlation=0.07649952856699095, pvalue=2.048299642084916e-13),
 'qdt_n/Q_12dis': KendalltauResult(correlation=0.12951535041534826, pvalue=2.1561652763842747e-35),
 'qdt_n/Q_13dis': KendalltauResult(correlation=0.07811455445773774, pvalue=1.159553048987222e-13),
 'qdt_n/Q_14dis': KendalltauResult(correlation=0.07524294903179317, pvalue=9.611711775070177e-13),
 'qdt_n/Q_15dis': KendalltauResult(correlation=0.10567624385986685, pvalue=1.493324345063105e-23),
 'qdt_n/Q_16dis': KendalltauResult(correlation=0.08056386218494016, pvalue=2.4147667184091273e-14),
 'qdt_n/Q_17dis': KendalltauResult(correlation=0.10875692564715271, pvalue=9.45511815785388e-25),
 'qdt_n/Q_18dis': KendalltauResult(correlation=0.09277020235407253, pvalue=2.10142850512827e-18),
 'qdt_n/Q_19dis': KendalltauResult(correlation=0.08695429551267415, pvalue=2.641029742128601e-16),
 'qdt_n/Q_2dis': KendalltauResult(correlation=0.09868247928894343, pvalue=3.318901980646537e-20),
 'qdt_n/Q_3dis': KendalltauResult(correlation=-0.008118676791906499, pvalue=0.4400953189249811),
 'qdt_n/Q_4dis': KendalltauResult(correlation=0.09796799516603319, pvalue=1.490821075012661e-20),
 'qdt_n/Q_5dis': KendalltauResult(correlation=0.12995822518181024, pvalue=2.6997787953385667e-36),
 'qdt_n/Q_6dis': KendalltauResult(correlation=0.02663638318208966, pvalue=0.010347407430248211),
 'qdt_n/Q_7dis': KendalltauResult(correlation=-0.05134394768715538, pvalue=6.135647884826619e-07),
 'qdt_n/Q_8dis': KendalltauResult(correlation=-0.019151957015804147, pvalue=0.06551624276137824),
 'qdt_n/Q_9dis': KendalltauResult(correlation=0.0029382361805451143, pvalue=0.7814853284360774),
 'PHMI_percentile': KendalltauResult(correlation=0.7807271070109543, pvalue=0.0),
 'jitter_mean': KendalltauResult(correlation=0.9999999999999999, pvalue=0.0),
 'PHMI': KendalltauResult(correlation=0.7738124836302662, pvalue=0.0)}
```
* corr_kendall_phmiPercentile
```python
{'LM_amount': KendalltauResult(correlation=0.08961546276798454, pvalue=2.223047713516011e-15),
 'loc_x': KendalltauResult(correlation=0.1876276969165557, pvalue=9.803649669663785e-70),
 'loc_y': KendalltauResult(correlation=-0.18641850360590406, pvalue=7.302761802157774e-69),
 'distance_mean': KendalltauResult(correlation=0.10095425066773046, pvalue=2.1212347260433728e-21),
 'distance_min': KendalltauResult(correlation=0.0048559946198022605, pvalue=0.6477386543010681),
 'distance_max': KendalltauResult(correlation=0.05187769767832519, pvalue=1.054260175019762e-06),
 'direction_is': KendalltauResult(correlation=0.08094245073176216, pvalue=1.0912271345221358e-12),
 'direction_none': KendalltauResult(correlation=-0.08094245073176216, pvalue=1.0912271345221358e-12),
 'direction_edge': KendalltauResult(correlation=0.05105446729636025, pvalue=6.622757030430316e-05),
 'intensity_mbb': KendalltauResult(correlation=-0.12496438468773123, pvalue=7.744049700875297e-32),
 'intensity_hull': KendalltauResult(correlation=-0.11707354743052766, pvalue=3.788487054735656e-28),
 'nnd_max': KendalltauResult(correlation=0.11154311342417249, pvalue=5.031023580458995e-25),
 'nnd_min': KendalltauResult(correlation=-0.14599017231622016, pvalue=1.4214571356887376e-40),
 'nnd_mean': KendalltauResult(correlation=-0.027841862799819643, pvalue=0.008894629915481485),
 'nnd2_mean': KendalltauResult(correlation=0.09760673146326482, pvalue=4.7629134074104553e-20),
 'G': KendalltauResult(correlation=0.12999595248808604, pvalue=3.7415612024370314e-30),
 'chi2_10': KendalltauResult(correlation=-0.11937988988004337, pvalue=8.096393407786574e-28),
 'chi2_10_pval': KendalltauResult(correlation=0.1060422496363851, pvalue=2.2258889843361202e-23),
 'qdt_chi2_10dis': KendalltauResult(correlation=-0.04374444048118387, pvalue=4.740523271978433e-05),
 'qdt_chi2_11dis': KendalltauResult(correlation=0.038540932155002594, pvalue=0.0003602598487254125),
 'qdt_chi2_12dis': KendalltauResult(correlation=0.18899057646902404, pvalue=1.0066544615986812e-67),
 'qdt_chi2_13dis': KendalltauResult(correlation=0.16128591737817127, pvalue=1.3391173016119451e-48),
 'qdt_chi2_14dis': KendalltauResult(correlation=0.1795108477679639, pvalue=3.395523066865452e-61),
 'qdt_chi2_15dis': KendalltauResult(correlation=0.14252406390139033, pvalue=9.039838553276616e-39),
 'qdt_chi2_16dis': KendalltauResult(correlation=0.11271914551101037, pvalue=8.579072140138712e-25),
 'qdt_chi2_17dis': KendalltauResult(correlation=0.13541164304221515, pvalue=1.8541670745709252e-34),
 'qdt_chi2_18dis': KendalltauResult(correlation=0.09022658830135098, pvalue=1.7527875301316066e-16),
 'qdt_chi2_19dis': KendalltauResult(correlation=0.06871669299568499, pvalue=3.739694683719628e-10),
 'qdt_chi2_2dis': KendalltauResult(correlation=0.18168277183165535, pvalue=1.5906922852940667e-61),
 'qdt_chi2_3dis': KendalltauResult(correlation=-0.12883220200070897, pvalue=1.8796442405085248e-32),
 'qdt_chi2_4dis': KendalltauResult(correlation=0.11862590996562515, pvalue=1.4402334536172776e-27),
 'qdt_chi2_5dis': KendalltauResult(correlation=0.16769553345005014, pvalue=4.60206017932778e-55),
 'qdt_chi2_6dis': KendalltauResult(correlation=0.007176170776773096, pvalue=0.5087940783441287),
 'qdt_chi2_7dis': KendalltauResult(correlation=-0.08453338337522931, pvalue=3.4463888527478023e-15),
 'qdt_chi2_8dis': KendalltauResult(correlation=-0.060962484853064276, pvalue=1.4182853127371603e-08),
 'qdt_chi2_9dis': KendalltauResult(correlation=-0.05550579145369161, pvalue=2.6179619199753596e-07),
 'qdt_num_10dis': KendalltauResult(correlation=0.10927997930704673, pvalue=3.20919962014549e-22),
 'qdt_num_11dis': KendalltauResult(correlation=0.07925356257491366, pvalue=2.5819472932465053e-12),
 'qdt_num_12dis': KendalltauResult(correlation=0.02596550406938023, pvalue=0.021955415499862668),
 'qdt_num_13dis': KendalltauResult(correlation=0.06112669325549831, pvalue=7.209224248563611e-08),
 'qdt_num_14dis': KendalltauResult(correlation=0.06711044875789476, pvalue=3.253603703458507e-09),
 'qdt_num_15dis': KendalltauResult(correlation=0.06620925261871313, pvalue=5.17883454828841e-09),
 'qdt_num_16dis': KendalltauResult(correlation=0.07820562728528012, pvalue=4.552377470127661e-12),
 'qdt_num_17dis': KendalltauResult(correlation=0.07245768980044065, pvalue=1.6269714264584118e-10),
 'qdt_num_18dis': KendalltauResult(correlation=0.07952653495322036, pvalue=2.0507256035132146e-12),
 'qdt_num_19dis': KendalltauResult(correlation=0.0813286658112664, pvalue=6.28186143492422e-13),
 'qdt_num_2dis': KendalltauResult(correlation=nan, pvalue=nan),
 'qdt_num_3dis': KendalltauResult(correlation=0.15514165846542866, pvalue=8.487300223920043e-36),
 'qdt_num_4dis': KendalltauResult(correlation=0.06926706941834453, pvalue=1.1534918915387463e-08),
 'qdt_num_5dis': KendalltauResult(correlation=0.0045028658957819885, pvalue=0.6982110032839934),
 'qdt_num_6dis': KendalltauResult(correlation=0.079820654674057, pvalue=1.8762986708407602e-12),
 'qdt_num_7dis': KendalltauResult(correlation=0.14464336009551293, pvalue=1.43202394595863e-37),
 'qdt_num_8dis': KendalltauResult(correlation=0.10516993944519157, pvalue=6.281214468489417e-21),
 'qdt_num_9dis': KendalltauResult(correlation=0.10773187540913474, pvalue=9.094175931824968e-22),
 'qdt_n/Q_10dis': KendalltauResult(correlation=-0.013589573131979641, pvalue=0.22164120398341147),
 'qdt_n/Q_11dis': KendalltauResult(correlation=0.06375164190787723, pvalue=6.477211445396178e-09),
 'qdt_n/Q_12dis': KendalltauResult(correlation=0.13123527321467277, pvalue=8.49899400041638e-33),
 'qdt_n/Q_13dis': KendalltauResult(correlation=0.07947719408840288, pvalue=8.124499417046193e-13),
 'qdt_n/Q_14dis': KendalltauResult(correlation=0.07669430217857677, pvalue=5.3398658255254135e-12),
 'qdt_n/Q_15dis': KendalltauResult(correlation=0.09563992027806814, pvalue=9.28658060455712e-18),
 'qdt_n/Q_16dis': KendalltauResult(correlation=0.07961891067613498, pvalue=8.94204411775824e-13),
 'qdt_n/Q_17dis': KendalltauResult(correlation=0.09542183467510656, pvalue=1.2892174054725692e-17),
 'qdt_n/Q_18dis': KendalltauResult(correlation=0.09196053313497345, pvalue=1.9480689792257866e-16),
 'qdt_n/Q_19dis': KendalltauResult(correlation=0.0791909175613904, pvalue=1.5418501668246077e-12),
 'qdt_n/Q_2dis': KendalltauResult(correlation=0.08961546276798454, pvalue=2.223047713516011e-15),
 'qdt_n/Q_3dis': KendalltauResult(correlation=-0.027668697474119493, pvalue=0.012609763624936043),
 'qdt_n/Q_4dis': KendalltauResult(correlation=0.08356657336430603, pvalue=5.6397536882338285e-14),
 'qdt_n/Q_5dis': KendalltauResult(correlation=0.12138935244230212, pvalue=7.882768496012775e-29),
 'qdt_n/Q_6dis': KendalltauResult(correlation=0.010476672011104837, pvalue=0.33899306464773993),
 'qdt_n/Q_7dis': KendalltauResult(correlation=-0.04925688095983496, pvalue=5.73348123568502e-06),
 'qdt_n/Q_8dis': KendalltauResult(correlation=-0.03582773322813216, pvalue=0.0010885648912275564),
 'qdt_n/Q_9dis': KendalltauResult(correlation=-0.019265429328328997, pvalue=0.08463728424443277),
 'PHMI_percentile': KendalltauResult(correlation=1.0, pvalue=0.0),
 'jitter_mean': KendalltauResult(correlation=0.7807271070109543, pvalue=0.0),
 'PHMI': KendalltauResult(correlation=0.9530007857079026, pvalue=0.0)}
```
计算结果中相关系数比较低，一是所选择的自变量与PHMI的相关性极弱，可以继续尝试反映空间模式的新指数；二是所选择数据
不能涵盖所有情况或数据量偏低，可以丰富数据模拟类型，以及增加数据量。

The correlation coefficient in the calculation results is relatively low. First, the correlation between the selected independent variable and PHMI is extremely weak, so we can continue to try the new index representing the spatial model. Second, the selected data can not cover all situations, or the data volume is low, which can enrich the data simulation types and increase the data volume.

虽然相关系数比较低，但是通过对某一类型自变量相关系数的比较分析，可以得出有价值的一些结论，或者得出时间序列下空间点模式的特征，用于指导提升导航评估值的规划方式。

Although the correlation coefficient is relatively low, some valuable conclusions can be drawn through the comparison and analysis of the correlation coefficient of a particular type of independent variable. Or the characteristics of the spatial point pattern under the time series can be obtained, which can be used to guide the planning method to improve the navigation evaluation value.


### 1-距离是否影响激光雷达导航评估值/Whether distance affects the evaluation of lidar navigation
PHMI与距离的相关系数distance_mean(0.10827296084597499, 4.926678335662525e-13)，distance_min (-0.007745403087658743, 0.6062043140384599)和distance_max(0.05882887545740473, 8.902054331810178e-05)中放弃distance_min最小距离（不显著）。均值和最大值相关性极弱。

The distance_min minimum distance (not significant) is abandoned in the correlation coefficient between PHMI and distance. The correlation, including the mean and the maximum, is extremely weak.

在landmarks分布方向分析中，去除landmarks与location间的距离影响，其与PHMI的相关系数基本保持不变，可以初步说明距离与PHMI值相关性不明显。

In the analysis of landmarks distribution direction, the distance between landmarks and location is removed, and its correlation coefficient with PHMI remains unchanged. It can be preliminarily shown that the correlation between distance and PHMI value is not apparent.

通过上述两个方向的分析，初步确定基于本次实验数据下，距离对于激光雷达评估值的影响不明显，即在规划布局中可以不用考虑特征点与无人车间的距离关系。



### 2-landmarks分布方向的影响
![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_0506.jpg)
<p align="center">
<em>图5 无人车位置点方向划分  /Fig 5 </em>
<em>图6 36个方向与PHMI的pearson相关系数  /Fig6 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_07.jpg)
<p align="center">
<em>图7 含距离值（左）/有无landmarks（中）/空间点变化（右）与PHMI的相关系数  /Fig 7 </em>
</p>

激光雷达在每个位置点旋转扫描，提取的特征点位于各个方向上，因此尝试在每个位置点划分36个方向区域（数量大小在进一步分析中可以为连续数量切分，例如4份，8份...72份），分析landmarks位置对PHMI值的影响。同时应用三种数据类型：
* 一是含距离值，数据示例：
```python
distance_eachDirection_df.head()
Out[81]: 
        0          1            2          3       4          5          6  \
0  9999.0  11.490950  9999.000000   2.751266  9999.0  17.413646  23.491434   
1  9999.0  11.486002     2.741686  14.473857  9999.0  17.396861  23.472224   
2  9999.0  11.456180     2.704563  14.431471  9999.0  17.350079  23.423365   
3  9999.0  11.430686     2.671471  14.392030  9999.0  17.305323  23.375761   
4  9999.0  11.370793     2.596659  14.302477  9999.0  17.204885  23.269791   

        7     8          9         10        11      12      13      14  \
0  9999.0  9999  15.588632  10.335842  6.213166  9999.0  9999.0  9999.0   
1  9999.0  9999  15.565101  10.312495  6.190678  9999.0  9999.0  9999.0   
2  9999.0  9999  15.520838  10.270573  6.153960  9999.0  9999.0  9999.0   
3  9999.0  9999  15.474667  10.226346  6.114320  9999.0  9999.0  9999.0   
4  9999.0  9999  15.375237  10.131754  6.030940  9999.0  9999.0  9999.0   

       15      16      17      18      19      20         21         22  \
0  9999.0  9999.0  9999.0  9999.0  9999.0  9999.0  22.502490  15.843701   
1  9999.0  9999.0  9999.0  9999.0  9999.0  9999.0  22.512685  15.859148   
2  9999.0  9999.0  9999.0  9999.0  9999.0  9999.0  22.551097  15.904529   
3  9999.0  9999.0  9999.0  9999.0  9999.0  9999.0  22.586144  15.947603   
4  9999.0  9999.0  9999.0  9999.0  9999.0  9999.0  22.666945  16.044875   

          23        24      25      26         27         28        29  \
0  19.046001  4.849670  9999.0  9999.0  22.554779  12.448359  8.247009   
1  19.064365  4.869159  9999.0  9999.0  22.578324  12.471727  8.269631   
2  19.112615  4.918216  9999.0  9999.0  22.623241  12.513906  8.307191   
3  19.159350  4.966165  9999.0  9999.0  22.669966  12.558443  8.347829   
4  19.263753  5.072861  9999.0  9999.0  22.770910  12.654137  8.434492   

       30         31        32      33      34        35      PHMI     loc_x  \
0  9999.0  14.997691  9.272780  9999.0  9999.0  8.784750  1.000000  0.000000   
1  9999.0  15.016364  9.288382  9999.0  9999.0  8.789476  1.000000 -0.002472   
2  9999.0  15.039432  9.302728  9999.0  9999.0  8.778212  0.004501  0.013612   
3  9999.0  15.066838  9.321943  9999.0  9999.0  8.772126  0.033961  0.024895   
4  9999.0  15.123139  9.360188  9999.0  9999.0  8.754592  0.075248  0.054708   

   PHMI_percentile  jitter_mean  
0                8     1.000000  
1                8     1.000000  
2                4     0.059328  
3                5     0.059328  
4                6     0.059328  
```
每一方向以最近点距离占位，如果没有landmark则配置值为9999.

* 二是有无landmarks，数据示例：
``` python
distance_eachDirection_isOrNone.head()
Out[83]: 
   0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  \
0  1  0  1  0  1  0  0  1  1  0   0   0   1   1   1   1   1   1   1   1   1   
1  1  0  0  0  1  0  0  1  1  0   0   0   1   1   1   1   1   1   1   1   1   
2  1  0  0  0  1  0  0  1  1  0   0   0   1   1   1   1   1   1   1   1   1   
3  1  0  0  0  1  0  0  1  1  0   0   0   1   1   1   1   1   1   1   1   1   
4  1  0  0  0  1  0  0  1  1  0   0   0   1   1   1   1   1   1   1   1   1   

   21  22  23  24  25  26  27  28  29  30  31  32  33  34  35      PHMI  \
0   0   0   0   0   1   1   0   0   0   1   0   0   1   1   0  1.000000   
1   0   0   0   0   1   1   0   0   0   1   0   0   1   1   0  1.000000   
2   0   0   0   0   1   1   0   0   0   1   0   0   1   1   0  0.004501   
3   0   0   0   0   1   1   0   0   0   1   0   0   1   1   0  0.033961   
4   0   0   0   0   1   1   0   0   0   1   0   0   1   1   0  0.075248   

      loc_x  
0  0.000000  
1 -0.002472  
2  0.013612  
3  0.024895  
4  0.054708  
```
如果存在landmark则配置值为0，如果不含landmarkze 配置值为1.

* 三是有无landmarks，数据示例：
```python
direction_change.head()
Out[85]: 
   0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  \
0  3  0  2  0  3  0  0  3  3  0   0   0   3   3   3   3   3   3   3   3   3   
1  3  0  0  0  3  0  0  3  3  0   0   0   3   3   3   3   3   3   3   3   3   
2  3  0  0  0  3  0  0  3  3  0   0   0   3   3   3   3   3   3   3   3   3   
3  3  0  0  0  3  0  0  3  3  0   0   0   3   3   3   3   3   3   3   3   3   
4  3  0  0  0  3  0  0  3  3  0   0   0   3   3   3   3   3   3   3   3   3   

   21  22  23  24  25  26  27  28  29  30  31  32  33  34  35      PHMI  \
0   0   0   0   0   3   3   0   0   0   3   0   0   3   3   0  1.000000   
1   0   0   0   0   3   3   0   0   0   3   0   0   3   3   0  1.000000   
2   0   0   0   0   3   3   0   0   0   3   0   0   3   3   0  0.004501   
3   0   0   0   0   3   3   0   0   0   3   0   0   3   3   0  0.033961   
4   0   0   0   0   3   3   0   0   0   3   0   0   3   3   0  0.075248   

      loc_x  
0  0.000000  
1 -0.002472  
2  0.013612  
3  0.024895  
4  0.054708  
```
在从一个位置点变化到另一个位置点有4中变化情况，有->有（11），有->无（10），无->无（00）和无到有（01），分别配置值为"00":0,"01":1,"10":2,"11":3}。

因为本次实验所使用的数据类型相对比较单一，不能涵盖各种空间分布形式，因此相关系数分析结果更多反映的是当前数据实验下landmarks在各个方向上landmarks变化的影响。如果比较各个方向上与PHMI的相关程度，需要建立典型的landmarks空间分布，进而比较得出相关结论。

同时，三种数据类型所获得的相关系数基本相同，因此可初步判断，在该实验数据下，landmarks与location的距离对PHMI基本没有影响；再者，前后1步的landmarks空间分布在各个方向上的变化对相关系数也基本没有影响，初步判断基于1步的landmarks空间分布对PHMI没有影响。

### 3-观察样方大小与landmarks分布距离
![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_08.jpg)
<p align="center">
<em>图8 样方示例  /Fig 8 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_09.jpg)
<p align="center">
<em>图9 一位置点G值示例  /Fig 9 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_10.png)
<p align="center">
<em>图10 连续距离样方G值均值变化  /Fig 10 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_11.png)
<p align="center">
<em>图11 连续距离样方G值均值绝对值变化  /Fig 11 </em>
</p>

空间点模式样方分析目的是探索空间点分布的特征，包括均匀，随机和聚集的评判。计算反映空间点分布特征的G值，即反映了每一位置下的landmarks分布特征，计算G值均值与PHMI 的相关系数，在一定程度上反映了landmarks空间点特征的变化对PHMI的影响。从分析结果来看（PHMI_nQ因为p-value基本大于0.05，因此放弃，仅参照PHMI_qdtN和PHMI_chi2），当分类数量为10m，即样方大小约为6×6m时，相关系数区域稳定，一定程度上可以推断6m样方下landmarkd的位置变化可能会影响PHMI值的变化。

同时，计算6m样方下的G值，计算结果*chi2_10_pvale /the amount:50/4432*， 即4432个位置点，仅有50个p-value<0.05，因此接受原假设，本次实验所分析的数据空间点分布基本为随机分布。


### 4-评估值的离散化

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_13.png)
<p align="center">
<em>图12 跳变点切分  /Fig 12 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_12.png)
<p align="center">
<em>图13 PHMI及其离散值  /Fig 13 </em>
</p>


离散化的方式中选择了两种，一种是分位数，*percentileNumber=[0,1,10,20, 30, 40,50,60, 70, 80, 90,100]*划分了10份；另一种是使用跳变点切分，在同一范围内取均值。比较PHMI连续值及其离散值的相对系数变化曲线，可以观察到三者基本吻合，跳变点切分则更趋于吻合，初步判断在特定的分析中可以使用离散值。

## D-待分析的基础数据的调整
为进一步明确空间点分布特点与PHMI之间的相关关系，可以有针对性的规划空间点分布用于分析。
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTU1NDQ3Njc5MywxODg5ODQ2MTY3LC0xMT
U3OTIxMDgsLTE1NTE0MDgyOTksLTEwMzY1ODM4OTMsLTIxOTYy
MTYxNCw3NDkxNDkxNDAsLTEzODEwMTQ2NCwxMzA1MzUyMTAwLC
0zNjYyNjgzNywyNTU2MTY0NjMsLTUzMzA0MzMxNywtNzk3MzEw
NTk5LC0yMDM5OTAwODYsLTQ5NDQ5MTQ1MSwxNDk3MzEzNjAwLC
03NzQyNDQ2NzQsLTE0MjU2MTg4OTMsLTEzNDQwODMwMTUsMzUx
OTIyNTgzXX0=
-->