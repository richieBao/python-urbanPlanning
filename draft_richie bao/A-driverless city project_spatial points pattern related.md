


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


### 1-距离是否影响激光雷达导航评估值

### 2-landmarks分布方向的影响

### 3-观察样方大小与landmarks分布距离对导航评估值的影响

### 4-评估值的划分途径

## D-验证方式的提出

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE3NjcwMTgyNDAsLTE0MDQ0ODUzMzIsLT
ExMzc3MjEyOTUsMTUyODcyNzQyMCw1MjYxMDYxNzMsLTI3NTQy
MjQ3NCwxMzQ1OTE5MDI3LDU2NzcwNTkwLDMzMDU3MTQ4NSwtMT
cwOTIyNDgxOCwxNzcyNTU3OTMwLC05MzkzNzkxNTUsNTcxMDk1
ODI5LDE5ODMzOTEzMjUsLTE0NTg4NzEzMTAsMTg4NDM5MDM2NC
wzMTEyNDA1NjBdfQ==
-->