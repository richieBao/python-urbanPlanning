## 实验目的
不管是退耕还林还是被破坏的环境要以修复，一般都会还原原生植被群落，也因此思量究竟受到影像的区域在恢复过程中与其周围环境的联系建立，既然通过回归预测能够根据所提供的解释变量预测对应的值，那么是否可以根据待修复地周围未受影响的环境为解释变量，通过使用环境较好区域
的数据建立回归模型后预测呢？此次实验探索就是这样的一个目的。

## 技术路线
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/940.png)

### 1 预测数据处理
草绿线：修复地外围环境范围
桔色线：修复地范围
影像：Landsat8 OLI 基本处理后
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/941.png)

### 2 训练数据处理
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/942.png)

### 3 训练模型与保存
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/943.png)

### 4 加载模型与预测
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/944.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/945.png)
