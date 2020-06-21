# Chicago_20_无人驾驶城市_06_3D 参数化模型(grasshopper) /Parametric model based on Grasshopper
> 在参数化平台grasshopper下可视化数据，用于后续辅助规划部分。

> Visual data under Grasshopper (GH), a parameterized platform, is used for subsequent auxiliary planning.

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/50_01.gif)

无人驾驶项目中的一种探索是基于当前车载激光雷达导航技术，在高容积率的城市中心，GPS信号受到影响的环境下，如何借助城市本身的要素来辅助无人车导航，这时就需要将城市环境与导航评估值结合起来，一方面可以探究影响导航评估值的城市因素；另一方面是，辅助规划优化导航结果。当然这里需要注意的是，当技术不断的发展，再复杂的环境也不会对导航造成影响时，实际上使用规划来辅助导航的意义会随之减弱。

One exploration in the driverless city project is based on the current vehicle-mounted navigation technology, in the downtown with high floor ratio and under the environment where GPS signals are affected, how to assist driverless vehicle navigation with the help of urban elements? At this time, it is necessary to combine the urban environment with the navigation evaluation value. On the one hand, we can explore the urban factors that influence navigation evaluation values. On the other hand, assist the planning in optimizing the navigation results. Of course, it is essential to note that planning to support navigation becomes less useful as technology continues to evolve so that the most sophisticated environment does not affect navigation.

基于当前技术条件，将无人驾驶工程组分析结果用于规划专业，进一步分析及实行空间规划，基于3D模型的参数化技术（grasshopper<GH>）来融合数据是比较好的选择。当前融合数据需要解除几个障碍，一是将工程组基于ROS以及MatLab的模拟数据导入到GH平台，这个过程包括数据转换为GH可以导入的数据格式和GH导入该数据的代码；二是在参数化GH平台下可视化结果，及进一步分析和规划。
  
Based on the current technical conditions, the result of driverless navigation engineering group analysis is applied to the planning profession for further study and implementation of spatial planning; a better choice is the parametric technology based on the 3D model to fuse data. At present, several obstacles need to be removed for data fusion. First, the simulation data of the engineering group based on ROS and MatLab should be imported into the GH platform. Second,  the visualization results under the parameterized GH platform and further analysis and planning.
  
## 1. 转换模拟数据 /transform simulation data
数据转换时，将MatLab的.fig数据转换为.csv数据存储，为了方便GH数据的调入，分别转换为landmarks坐标，location坐标和PHMI导航评估值三个文件。该部分代码存储在`driverlessCityProject_2grasshopper.py`和`driverlessCityProject_spatialPointsPattern_association_basic.py`文件中。使用时将两个文件放置于同一文件夹下，打开第1个文件，替换MatLab的.fig对应文件，以及配置保存路径计算转换和保存三个文件。

During data conversion, MatLab .fig data is converted to.csv data storage.  Three files were saved to facilitate the input of  GH data, including landmarks coordinates, location coordinates, and PHMI navigation evaluation values. When in use, place the `driverlessCityProject_2grasshopper.py` and`driverlessCityProject_spatialPointsPattern_association_basic.py` files in the same folder, open the first file, replace the corresponding data of .fig of MatLab, and configure the saving path to calculate, transform and save the three files.

## 2. 编写GH的导入部分组件 /Write the import component of GH
GH支持python语言，而为了避免使用GH自己组件繁琐的连接过程，直接使用GhPython编写代码可以方便简化流程。

GH supports the Python language, and to avoid the tedious writing process of using GH's components, writing code directly in GhPython makes the process easier.
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/50_02.jpg)

## 3. GH参数化技术下，实现数据的动态可视化
该部分的第1阶段，只实现了已有数据的可视化。为了能够获取真实世界的地理位置，调入实际地图（使用OSM数据），根据实际实验城市区段，在[OSM](https://www.openstreetmap.org/#map=11/43.0092/-88.0621)开源数据网站下载对应区域地图，在GH下应用Elk组件调入地图数据（相对坐标）。并根据已有实际地图来对位模拟数据的空间位置。 同时显示landmarks、location的点位置，并对位location的位置显示PHMI值及其曲线，标识不符合导航要求的PHMI值的位置点，及每一位置下雷达扫描范围下对应的landmarks。 

同时，无人车行驶的过程是可以模拟的，在模拟车行驶的过程中， 动态标识出每一位置的landmarks数量和对应的PHMI值，当PHMI值不满足要求时，显示的值会以颜色的变化标识。
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/50_03.jpg)
