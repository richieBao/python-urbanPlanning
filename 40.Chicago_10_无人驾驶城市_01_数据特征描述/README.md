# 40.Chicago_10_无人驾驶城市_01_数据特征描述市场化
无人驾驶如火如荼的进行了多年，目前已经取得了丰硕的成果，虽然保守预测2030s-2040s年左右能够达到无人驾驶的市场化，但是位于6个阶段的哪个阶段，需要时间来验证。
* SAE Level 0 No Automation
* SAE Level 1 Driver assistance
* SAE Level 2 Partial automation
* SAE Level 3 Conditional automation
* SAE Level 4 High automation
* SAE Level 5 Full automation
无人驾驶项目的细分方向很多，各大研究部门通常负责其中的一部分，最后整合所有的研究成果推进无人驾驶项目。此次由Illinois Institute of Technology(IIT)主持的无人驾驶城市项目成员分工架构为：工程学院-GPS无人驾驶导航部分（Boris S. Pervan/Kana），车载激光雷达无人驾驶导航部分（Matthew Spenko /Yihe）；景观及规划学院-无人驾驶城市环境（Ron Henderson/Alexis Arias/Richie Bao）。

> 当前仅分享可以分享的部分，所有研究成果归IIT无人驾驶项目团队所有，特此声明。

因为仅涉及GPS和车载激光雷达导航，因此在无人驾驶城市环境部分目前只涉及这两部分与城市环境之间的关系研究，随着研究的深入，将系统化的探索无人驾驶城市影响。通常城市环境部分需要对接工程团队，针对GPS和车载雷达激光部分的研究分别使用了不同的研究方法，GPS部分针对当前Chicago城市中心高层建筑对信号接收数量、强度做评估，激光雷达部分配合使用ROS（+Gazebo）模拟及对应算法计算评估。根据所获取的数据进行数据特征描述。

### 无人车位置与扫描区域特征点
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/40_01.png)

### 激光雷达扫描评估值
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/40_02.png)

### 网络结构的建立
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/40_03.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/40_05.png)

### 特征描述方法-A
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/40_06.png)
