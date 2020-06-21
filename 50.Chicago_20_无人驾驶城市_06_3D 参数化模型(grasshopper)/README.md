# Chicago_20_无人驾驶城市_06_3D 参数化模型(grasshopper)
> 在参数化平台grasshopper下可视化数据，用于后续辅助规划部分。

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/50_01.gif)

无人驾驶项目中的一种探索是基于当前车载激光雷达导航技术，在高容积率的城市中心，GPS信号受到影响的环境下，如何借助城市本身的要素来辅助无人车导航，这时就需要将城市环境与导航评估值结合起来，一方面可以探究影响导航评估值的城市因素；另一方面是，辅助规划优化导航结果。当然这里需要注意的是，当技术不断的发展，再复杂的环境也不会对导航造成影响时，实际上使用规划来辅助导航的意义会随之减弱。

基于当前技术条件，将无人驾驶工程组分析结果用于规划专业，进一步分析及实行空间规划，基于3D模型的参数化技术（grasshopper<GH>）来融合数据是比较好的选择。当前融合数据需要解除几个障碍，一是将工程组基于ROS以及MatLab的模拟数据导入到GH平台，这个过程包括数据转换为GH可以导入的数据格式和GH导入该数据的代码；二是在参数化GH平台下可视化结果，及进一步分析和规划。
  
## 1. 转换模拟数据
数据转换时，将MatLab的.fig数据转换为.csv数据存储，为了方便GH数据的调入，分别转换为landmarks坐标，location坐标和PHMI导航评估值三个文件。该部分代码存储在`driverlessCityProject_2grasshopper.py`和`driverlessCityProject_spatialPointsPattern_association_basic.py`文件中。使用时将两个文件放置于同一文件夹下，打开第1个文件，替换MatLab的.fig对应文件，以及配置保存路径计算转换和保存三个文件。

## 2. 编写GH的导入部分组件
GH支持python语言，而为了避免使用GH自己组件繁琐的连接过程，直接使用GhPython编写代码可以方便简化流程。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/50_02.jpg)
