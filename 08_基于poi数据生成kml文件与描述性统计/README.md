## POI数据转换为.kml文件，在Google Earth中加载
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/917.png)

前述实验中阐述过百度地图POI数据采集，基于上述代码，调整为一次性采集所有业态类型数据，并存储为.csv和.json格式文件，方便数据分析调用。为方便网址请求参数的设置及打开网址，使用urllib库完成此部分的操作。同样调入conversionofCoordi坐标转换文件，实现百度坐标系到WGS84（World Geodetic System 1984）全球定位系统坐标系统的转换。在百度地图拾取坐标系统网址中，确定leftBottom=[108.756024,34.146366]左下角坐标和[88] rightTop=[109.033852,34.449955]右上角坐标，根据指定的范围采集数据。

## 描述性统计图表-程序代码计算结果
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/919.png)

## 百度地图POI散点图
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/918.png)
