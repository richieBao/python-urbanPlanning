# Chicago_23_无人驾驶城市_09_点云分割_model

* PyTorch Geometric(PyG)图结构+PointNet++结果

<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/skitti_pytorchGeo_test_s.gif" width="1000">

该部分核心的深度学习模型为已有研究相关作者的代码迁移，仅在数据集处理上重新调整和编写了代码。初步测试的模型包括两个，一个是基于[PyTorch Geometric(PyG)](https://pytorch-geometric.readthedocs.io/en/latest/)的图结构及PointNet++模型；二是[polarNet](https://github.com/edwardzhou130/PolarSeg)模型；模型训练的数据集为[SemanticKITTI](http://semantic-kitti.org/)，
