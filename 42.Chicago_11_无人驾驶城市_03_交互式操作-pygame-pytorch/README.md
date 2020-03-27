# Chicago_12_无人驾驶城市_03_交互式操作-pygame-pytorch
交互式操作在观察数据变化，寻找预期的结果过程中具有重要的作用，可以直观的进行调试，有目的性的寻找结果。在38_Chicago_08_数据图表描述中，有些库可以实现互动性的操作，例如即使的显示图表中要素的值，或者通过数值条来改变参数，但是这些操作相对比较简单，可以处理简单的交互问题，但是如果处理较为复杂的交互操作，则需要寻找新的库，此次实验使用pygame库来实现相关分析。

因为需要寻找模式Pattern，即调整栅格landmarks点的位置，观察phmi值的变化。使用“41.Chicago_11_无人驾驶城市_02_pytorch深度学习模型-beta”，训练好的模型。这个过程，需要交互式操作，能够直接观察位置变化，和对应的预测值变化，从而能够直观的分析landamarks的位置模式。使用pygame库实现。

## 演示
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/42_00.gif)

## 两个变化比较图
> 第1组
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/42_01.png" width="300" align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/42_02.png" width="300" align="right">

> 第2组
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/42_03.png" width="300" align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/42_04.png" width="300" align="right">
