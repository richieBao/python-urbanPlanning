# Chicago_22_无人驾驶城市_08_点云分割_点特征

对城市空间的表达有很多种途径，不同的途径往往由当时的技术水平所决定， 当然，不同的途径也有各自更适合的应用领域，这个并不由技术所确定。 点云数据的类型可以根据其扫描的位置分为：由卫星扫描获取，俯瞰（天空）视角的点云数据；和由车载或者手持扫描获取地面视角的点云数据。

因为无人驾驶技术的发展，对环境的识别也是包含多种技术途径，例如对于拍摄传统图像（.jpg,.png,.bmp等）的识别（图像分割），以及雷达扫描点云数据（三维点云分割）。 虽然点云数据，尤其无人驾驶中所获取的点云数据为行驶路线下扫描获取，为具有一定连续固定视角的三维点云，并不是完整全部表面的反映，天空视角的点云数据同样会缺失，但是这个数据亦可以帮助我们从点云数据这一视角来探究城市环境因素。

目前三维点云数据的处理库日益完善，大部分数据处理无需自行从新编写代码。 点云数据的分割方法也丰富多彩， 不同的方法对原始数据处理的方式也基本会不同，主要有几种方式，一是将三维数据投影到二维平面，或直接投影为矩形图像，或转换为极坐标的方式；再者就是寻找三维点云本身的关系，例如使用体素（voxel），或者近似平面法线方向，以及应用PyTorch Geometric(PyG)建立图结构，使用图神经网络等。在下述的代码中迁移与调整已有研究成果（代码或算法），来比较不同方式下点云数据的处理。

* 原始车载激光雷达扫描的三维点云数据（IIT,Chicago）

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/52_02.gif" width="1000">

* 点云数据的DBSCAN聚类

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/52_01.gif" width="1000">

* 投影

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/52_05.gif" width="1000">

* 极坐标投影

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/52_04.gif" width="1000">


