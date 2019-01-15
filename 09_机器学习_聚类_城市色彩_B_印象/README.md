应用聚类的方法提取图像的主题色，以图表散点形式显示，获取直观印象。此次实验选择了两条调研路线，一为杭州虎跑部分，二为北京碧云寺。使用 km=cluster.KMeans(n_clusters=params['n_clusters'])算法计算。聚类部分的计算代码移植“Comparing different clustering algorithms on toy datasets”，尽量保留了移植的痕迹，方便比较和查看差异变化。设置[57] 'n_clusters': 7聚类数量为7，获取每幅图像的7个主题色，可以修改聚类数量调整色彩主题色提取的多少。KMeans聚类算法可以很好分离色彩数据提取主题色。提取所有图像的主题色之后汇总于一个数组中，以 varied=datasets.make_blobs(n_samples=n_samples,cluster_std=[1.0, 2.5, 0.5],random_state=random_state)散点形式打印主题色，使其直观反映城市色彩印象。

虎跑主题色偏灰偏暗（建筑的色调），掺杂植被的绿色和天空的蓝色，朴实素雅。碧云寺因为建筑本身多为红色，穿插植被和天空后，整体感觉斑斓绚烂。碧云寺计算有124张图像，聚类前使用自定义函数 def getPixData(img):压缩图像，减少计算量。用一般8G内存，Intel(R) Core(TM) i7-4500U CPU @ 1.80GHz 2.40GHz的配置，约需3~4个小时的计算时间。因为要显示图像和聚类提取后的主题色图表的计算仍需部分时间。因此在程序调试时，可以先减少图像样本量，并增加图像压缩程度，待程序调试运行正常后，在进行最后的计算。通过城市主题色的提取和印象感官的呈现来研究城市色彩，可以针对于不同的城市空间，不同的时间调研，分析色彩的变化。

## 杭州虎跑色彩印象
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/922.png)

## 北京碧云寺色彩印象
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/923.png)

## 杭州虎跑调研图像、聚类结果和主题色提取
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/920.png)

## 北京碧云寺调研图像、聚类结果和主题色提取
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/921.png)
