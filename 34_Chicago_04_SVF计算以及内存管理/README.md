# 34_Chicago_04_SVF计算以及内存管理
城市三维空间数据分析中，SVF（sky view factor）天空视域因子是一个关键的计算量。依旧为了进一步进行数据批量处理以及数据分析，尤其数据的深度挖掘，需要摆脱软件平台的束缚，采用python编写程序。在程序编写过程中遇到待解决的关键问题：
* CVF的算法实现，尤其按照视线提取栅格值的方法。
* 城市区域的CVF计算，数据量大，如果使用python自身的for循环，计算时长远超预期，不能完成任务。
* np.arange(6000000000,dtype=np.float64)数组，预计占用45.7GB，如果内存小于该值，将溢出。6000000000数据量，相当于77459.6m × 77459.6m的城市区域。如果在这个过程中，存在其它计算，则将大幅度增加所用内存，因此如何管理内存与释放内存在大数据处理过程中显得尤为重要。

> 为处理上述问题，需要对应采取相应的策略。
## CVF算法的核心
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/34_01.jpg" width="300" align="left">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/34_02.jpg" width="300" align="right">
