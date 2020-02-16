# 37_Chicago_07_建筑高度分布结构
由.las雷达数据提取1m高精度的芝加哥全城建筑高度数据，在分析计算时需要注意如何处理大数据量栅格数据，避免内存溢出，以及单独文件过大等问题。在“34_Chicago_04_SVF计算以及内存管理部分”提到内存管理的方法，在此处对于地理信息数据增加几点方法：
* 如果单独的栅格文件过大，例如100G，无法一次性读到内存中，则需要分块读取，例如使用rasterio.windows的方法；
* 注意对栅格数据存储类型的确定，尽可能在满足要求的条件下，选用最小的数据存储格式，例如byte, Int8,UInt8等；
* 增加计算速度，可以尝试使用numba库提供的并行计算，以及GPU计算的方法；
* 确定解决问题所能允许的精度，以及变化计算方法，例如大数据量单独栅格的聚类可能需要百G内存，因此适当降低数据量或转换数据格式来执行。

此次实验涉及的代码较多，个别单独文件代码可以合并，代码功能如下：
1. 由.las点云数据提取DSM和分类数据-pdal_las_lidar.py。（此文件在“33_Chicago_03_雷达.las数据处理”部分曾阐述）
2. 由.las点云数据提取DTM-generateDTMBUidingHeight.py
3. 合并栅格数据-rasterMosaic_rasterio.py
4. 栅格插值，补全缺失数据-interpolate2D_3D.py
5. 切分建筑高度生产单独的建筑空间分布数据-rasterBuildingHeightZSplit.py
6. 针对大数据量（例如100G）单独栅格文件的重分类方法（raster.windows分块读取）-rasterBuildingHeightZSplit_reclassify.py
7. 栅格聚类与点数据聚类方法的调整-pointsClustering.py / rasterClustering.py

# 计算结果
> 主要部分内容


