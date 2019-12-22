# 34_Chicago_04_SVF计算以及内存管理
城市三维空间数据分析中，SVF（sky view factor）天空视域因子是一个关键的计算量。依旧为了进一步进行数据批量处理以及数据分析，尤其数据的深度挖掘，需要摆脱软件平台的束缚，采用python编写程序。在程序编写过程中遇到待解决的关键问题：
* CVF的算法实现，尤其按照视线提取栅格值的方法。
* 城市区域的CVF计算，数据量大，如果使用python自身的for循环，计算时长远超预期，不能完成任务。
* np.arange(6000000000,dtype=np.float64)数组，预计占用45.7GB，如果内存小于该值，将溢出。6000000000数据量，相当于77459.6m × 77459.6m的城市区域。如果在这个过程中，存在其它计算，则将大幅度增加所用内存，因此如何管理内存与释放内存在大数据处理过程中显得尤为重要。

> 为处理上述问题，需要对应采取相应的策略。
## CVF算法的核心
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/34_01.jpg" width="300" align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/34_02.jpg" width="300" align="right">
此草图非彼草图。很多时候需要图解帮助思考，并将其逐步的转换为代码，达到计算的目的。
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/34_03.png" width="300" align="right">
<img src="https://github.com/richieBao/python-urbanPlanning/blob/master/images/34_04.png" width="300" align="right">

## 增加计算速度与缓解内存压力
* 使用内存管理/减压工具。h5py库/psutil库/memory_profiler库/del 方法等。
> 强烈推荐使用：h5py。大数组尽量避免使用np.save工具，该工具保存的数据占据的磁盘空间较大
* 避免使用for等循环，而是使用numpy直接数组间计算，可以大幅度增加计算速度，但会占用较大内存，需使用内存管理/减压工具处理
* 数据分批处理，并保存与硬盘中，所有处理完后，读取所有文件进行后续处理。需平衡分批与一次性数组计算量，每次数组大计算速度快，但占用内存多，如果增加批次，则会降低单次数组量，但会增加计算时间。
* 如果不必要，不需保存中间过渡的大数组，应用后，迅速del释放内存，仅保留和存储必要的计算结果或中间结果。大数组尽量使用h5py保存于硬盘中
* 大数据处理过程中，尽量避免使用matplotlib查看数据，只有必要分析时，可以单独处理
* 因为为了减缓内存，数据及过程数据存储于大的硬盘中。根据自身数据大小，可以准备高容量的外置硬盘使用
