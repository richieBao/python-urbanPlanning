# Chicago_11_无人驾驶城市_02_pytorch深度学习模型-beta
针对无人车激光雷达部分，当前的主要目的是找到评估值变化的空间模式及影响原因。因为工程团队当前的代码在MatLab中完成，并且为测试阶段，代码较为凌乱。因此景观/规划部分
先尝试自行建立基于pytorch的深度学习模型，学习工程团队的模型，用于空间模式的探索，待工程部分代码完善，可以替换模型。
### 目的：
* 探索影响无人车激光雷达导航的空间模式
* 建立可以适应评估值要求的空间模式
  1. 预测调整适应
  2. 自动生成空间模式
### 方法
#### 训练数据集的建立
* 特征值
  1. location 无人车位置值
  2. landmarks  激光扫描区域特征点
* 空间特征表示方法-栅格化
  1. 应用numpy.histogram2d转换位置点及对应扫描区特征点为图片栅格数据（紧凑形式，位置点未在中心）
  ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/41_02.jpg)
  2. 将位置点作为栅格中心，图片栅格格式(位置点在栅格中心)
  ![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/41_01.jpg)
* 输出类别
  1. 原始连续值
  2. 用Percentile百分位数分类连续数值用作输出类别
  3. 均分方式分类连续数值用作输出类别
  4. math.pow(10,-5)为评估标准值，设置为大于和小于等于两个值
### 结果
* 二值，非位置中心点，MLP网络
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/41_04.jpg)
* 二值，位置中心点，MLP网络
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/41_03.jpg)

比较的深度学习网络：
> 深度卷积网络 AlexNet Model
> 网络中的网络 NiN Model
> 多层感知机 MLP
