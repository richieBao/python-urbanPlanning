# Chicago_19_时空数据_05_dash 基于WEB 图表分析 /spaital-temporal data_05_dash based on web chart analysis
数据分析过程中有需要协作及分享的过程，例如，需要数据的收集，并依据后台模型分析计算获取结果；提供分析服务的平台，交互式操作配置参数，获取对应的计算结果；或者仅是呈现数据分析过程及结果；以及多人协作等内容。在第“16_Flask构建实验用网络应用平台”部分，解析应用flask构建网络应用平台，可以呈现、收集、分析数据。对于需要大量图表的数据分析，则可以借助python库dash(plotly)实现，地图底图则使用mapbox提供的地理信息数据。dash提供有大量交互用户界面组件，可以组织数据的交互形式，同时对于规划，因为可以应用地理信息数据，有助于规划专业的数据分析。因此，在图表分析领域，应用plotly进行丰富的图表分析，以及基于plotly的网页交互图表分析的dash，有助于数据分析的交互呈现。
In the process of data analysis, there are collaborative and sharing methods, such as data collection, analysis, and calculation of results based on the background model; the platform provides analysis service, interactively operates configuration parameters, and obtains corresponding calculation results; or present the data analysis process and outcomes; and multi-person collaboration and so on. Dash provides a large number of interactive user interface components that can organize the interactive form of data. For planning, because geographic information data can be applied, it helps to plan professional analysis. Therefore, in the area of chart analysis, the application of Plotly for rich chart analysis, and dash for interaction chart analysis base on the web page, contribute to the interactive presentation of data analysis.


此次实验基于dash提供的案例，将互动网页图表的dash应用于时空数据分析，尝试表现形式，包括地理信息数据的可视化呈现，尤其.shp的point数据和polygon数据的处理；基本折线图表的呈现，以及交互式操作等。当然，在数据分析过程中一开始就基于dash进行图表分析，并不是很理智，专业内容的分析需要将更多的精力放在研究内容上，而不是图表表现上，因为dash更倾向于后期数据图表的交互分享，因此当分析内容结束后，再将代码直接加入dash部分就可以，增加数据分析表现和功用的力度。

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/49_01.jpg)
> satellite地理信息数据为底图
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/49_02.jpg)
