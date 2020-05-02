# 43.Chicago_13_无人驾驶城市_04_数据特征描述_B
> 数据来源：Driverless city project-Illinois Institute of Technology(IIT)
对于数据特征的描述，此次增加了两部分内容，其一是按照曲线的跳变点切分曲线，从而可以分组对应的多种数据，做进一步分析。所使用的方法借助1维卷积；其二是
引入空间点格局，借助rpy2库调用R语言，及其spatstat库，实现样方分析，最近距离分等内容，判断空间点模式是趋于均匀分布，还是趋于集中分布。计算有Variance-Mean Ratio(VMR)方差均值比，以及F(r)和G(r)等，推荐参考：Adrian Baddeley,Ege Rubak,Rolf Turner.Spatial point patterns methodology and application with R[M].CRC Press. 2016. 空间点格局部分是城市空间数据分析方法的一项重要内容，在后续的研究中将由实际研究案例详细阐述，本次无人驾驶部分仅是分析landmarks分布特点是否与雷达导航评估值之间存在相关性。
