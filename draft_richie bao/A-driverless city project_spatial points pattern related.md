


# A-无人驾驶城市_空间点（landmarks）模式相关/A-driverless city project_spatial points(landmarks) pattern related
> @author: Richie Bao-Chicago.IIT(driverless city project)  data:IIT.driverless city project
### 规划组在无人驾驶城市项目中的工作内容
当前无人驾驶城市项目的核心内容是探索GPS和车载激光雷达无人驾驶导航问题。无人驾驶的最终目的是应用研究成果于现实世界，服务人们的日常生活，因此需要探索城市布局与无人驾驶之间的博弈关系。一是改善导航技术，减弱城市空间对导航的影响；二是，对导航有影响的区域（例如高容积率，高密度的城市中心），适当布局城市，使得空间格局适应无人驾驶导航需求。

规划组则更多考虑城市空间布局的影响，尝试发现空间布局与导航评估值之间的关系，从抽象的特征数据到现实世界的模拟来不断发现与优化空间规划与无人驾驶之间的矛盾。

## A-数据
分析内容基于无人驾驶城市工程组激光雷达导航模拟数据结果。可以进一步划分为，原始测量数据，基于原始数据调整规划布局后的数据，重新规划后的数据。
此次实验数据包含两组，一组为原始模拟数据；一组为新规划模拟数据。
![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_01.png)
<p align="center">
<em>图1 原始模拟数据  /Fig 1 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_02.png)
<p align="center">
<em>图2 新规划模拟数据  /Fig 2 </em>
</p>

## B-关于相关性
使用pandas(python库)的# pandas.DataFrame.corr方法计算相关系数，其中参数method有三种方法，如下：
-   pearson : （线性数据）标准相关系数/standard correlation coefficient    
-   kendall : 等级相关系数/Kendall Tau correlation coefficient    
-   spearman :等级相关系数/Spearman rank correlation

或者scipy库scipy.stats.pearsonr/scipy.stats.kendalltau/scipy.stats.spearmanr计算，返回值1为pearson相关系数，值2为p-value（显著性检验）
![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_03S.jpg)
<p align="center">
<em>图3 pearson相关系数  /Fig 3 </em>
</p>

![enter image description here](https://github.com/richieBao/python-urbanPlanning/blob/master/images/dcp_spp_04.png)
<p align="center">
<em>图4 PHMI相关的pearson相关系数  /Fig 4 </em>
</p>

>相关系数值描述： |r|>0.95 存在显著性相关；|r|>=0.8 高度相关；0.5=<|r|<0.8 中度相关； 0.3=<|r|<0.5 低度相关； |r|<0.3 关系极弱，认为不相关；|r|=0 不相关。

与landmarks空间点模式相关的变量（指数）选择：
> landmarks为激光雷达拾取的环境特征点；location为无人车位置坐标。	

	1. landmarks点数量	<LM_amount>
	2.  location x与y坐标 <loc_x,loc_y>
	3. landmarks与location之间的距离：平均距离，最小和最大距离 <distance_mean,distance_min,distance_max>
	4. 以location为圆心划分36个方向：包含landmarks，不含landmarks，包含与否的边界 <direction_is, direction_none, direction_edge>
	5. landmarks密度（intensity）：最小边界范围，凸包 <intensity_mbb,intensity_hull>
	6. landmarks最近邻：最大值，最小值，均值以及最近邻为2个点的均值 <ndd_max,ndd_min,ndd_mean>
	7. 反应点模式为随机、均匀或者聚集的G函数值，其大于期望值（expectation）趋于聚集，小于则趋于均匀，等于则趋于随机 <G>
	8.  与连续距离（0-18）下样方统计的相关量：反应点模式的chi2均值，含有landmarks的样方数量，以及landmarks数量/含有landmarks的样方数量 <qdt_chi2_, qdt_num_, qdt_n/Q_>
	9. 离散化方法（可用于进一步预测模型的建立）：基于分位数，基于跳变点，基于pow(10,-5)即评估值的界定值 <PHMI_percentile, jitter_mean>

## C-问题
### 0-相关系数值的大小
* pearson 相关性显著性检验 p-value
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
### 1-距离是否影响激光雷达导航评估值

### 2-landmarks分布方向的影响

### 3-观察样方大小与landmarks分布距离对导航评估值的影响

### 4-评估值的划分途径

## D-验证方式的提出

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTE0OTA1MTA3MiwtMTQyNjExMzc4OCwtMT
c2NzAxODI0MCwtMTQwNDQ4NTMzMiwtMTEzNzcyMTI5NSwxNTI4
NzI3NDIwLDUyNjEwNjE3MywtMjc1NDIyNDc0LDEzNDU5MTkwMj
csNTY3NzA1OTAsMzMwNTcxNDg1LC0xNzA5MjI0ODE4LDE3NzI1
NTc5MzAsLTkzOTM3OTE1NSw1NzEwOTU4MjksMTk4MzM5MTMyNS
wtMTQ1ODg3MTMxMCwxODg0MzkwMzY0LDMxMTI0MDU2MF19
-->