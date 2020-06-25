# 47.Chicago_17_时空数据_04_不平等性与隔离 spatial-temporal data_04_inequality and segregation
参考/reference：PySAL Notebooks Book http://pysal.org/notebooks/explore/segregation/intro.html

本次关于城市健康的空间分析包括两部分内容，一是空间分布的不平等（不均衡）性及城市隔离模式。本次使用的数据除了Covid-19分布数据，还包括主要疾病
分布数据。基于Gini基尼系数主要用于经济中收入不均等分析，将其应用于Covid-19在Chicago城不同区域感染案例分布的分析，其中0表示完全均衡，而1表示
完全不均衡，通过Gini分析可以获知，随着时间的推移，不同区域的不均衡性逐渐拉大，此时，因为疫情并未结束，感染人数仍在增加，因此后续变化未给出。

The spatial analysis of public health includes two parts. One is the inequality (imbalance) of spatial distribution and the pattern of urban segregation. In addition to the Covid-19 distribution data, the data used in this study also includes the spreading of significant diseases. Based on the Gini coefficient, which is mainly used to analyze income inequality in the economy, the Gini coefficient was applied to analyze the distribution of Covid-19 infection cases in different areas of Chicago, where 0 means perfect equilibrium and 1 means wholly unbalanced. Through the Gini analysis, it can be learned that, over time, the imbalance of different regions is gradually increasing. At this point, because the epidemic is not over, the number of infected people is still growing, so the subsequent change is not given. 

城市空间隔离模式通常用于种族隔离分析，关于隔离指数的研究非常丰富，相关指数亦有很多，Gini指数实际上也是隔离指数。PySAL在已有隔离指数分析基础上
亦给出了基于Shapley分解不均衡变化值为两个分量，其一为空间分量，通常挂钩于w空间权重；其二为属性分量，即所分析的数据，本次为感染案例的两个时间点数据。
为确定分析的可靠性，推断统计显著性。同时，以Chicago疾病分布数据为例，探索多组空间隔离指标，以及除了空间区域权重，加入反映人人之间接触容易程度
的路网因素。

The urban spatial segregation model is usually for the analysis of ethnic segregation. There are a lot of studies on the segregation index, and there are many related indexes.  Based on the existing isolation index analysis, PySAL also gives the Shapley decomposition disequilibrium variation value as two components. One is the spatial element, which is usually linked to the spatial weight of W. The second is the attribute component, that is, the data of two-time points of the infection case. Meanwhile, to determine the reliability of the analysis and statistical significance., taking Chicago disease distribution data as an example, multiple sets of spatial isolation indicators were explored. And road network factors reflecting the ease of contact between people were added in addition to spatial area weights.

## 空间分布的不平等性/inequality/Methods for measuring spatial inequality.
> Gini度量不均衡指标 /Gini measures imbalances
* 基础数据 /basic data
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_02_01.jpg)

* 基尼系数/Gini Gini系数在学术界有广泛争议，需谨慎使用
```python
gini_19-g: 0.6038053983886671
ginis: [0.2945679012345679, 0.2945679012345679, 0.2916666666666667, 0.38165193488387406, 0.40337166127679963, 0.4139282614025671, 0.4790247985472705, 0.5366671234197612, 0.5866767499867325, 0.6038053983886671, 0.5939761284190763]
p_sim: 0.02
p_values: [0.07, 0.1, 0.1, 0.14, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
wgs: [0.2841975308641975, 0.2841975308641975, 0.2815372829417773, 0.3687719124981482, 0.39274663632371143, 0.40483006315064046, 0.46804420610600384, 0.5241444760788254, 0.57299129650268, 0.5894393257422903, 0.579897493309077]
bgs: [0.7158024691358025, 0.7158024691358025, 0.7184627170582227, 0.6312280875018518, 0.6072533636762886, 0.5951699368493595, 0.5319557938939962, 0.4758555239211746, 0.42700870349732, 0.4105606742577097, 0.42010250669092297]
```
> 0表示完全均衡，1表示完全不均衡

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_05.png)

## 城市隔离模式/segregation/analyzing patterns of urban segregation
### 01-隔离模型/指数/PySAL segregation module for aspatial indexes 
```python
dissimilarity: 0.2514104848644326
Gini: 0.3431758903870853
Entropy: 0.0638402221878651
Atkinson: 0.0979389074656376
Concentration Profile: 0.1348143466256669
Isolation: 0.30999981199698434
Exposure: 0.6900001880030157
Correlation Ratio: 0.06916324447557028
Modified Dissimilarity: 0.2197276595293781
Modified Gini : 0.3022909570381693
Density-Corrected Dissimilarity: 0.24539833442240042
Minimum-Maximum Index (MM): 0.4018033857078772
```
### 02-分解/decomposition 基于Shapley分解

1. Composition Approach (default) 
```python
G19_gini: 0.3845662699919272
G15_gini: 0.38466250563878474
G_19-G_15: -9.623564685751207e-05
```
分解为两个分量：空间分量，属性分量/The Spatial component and the attribute component
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_06.png)
```python
Shapley's Spatial Component of the decomposition: 0.019061416254844782
Shapley's Attribute Component of the decomposition: -0.019157651901702294
```
可视化分量累积量/visualize the cumulative distribution functions of the compositions/shares
|Spatial Component|>|Attribute Component|
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_07.png)
'maps' : visualize the spatial distributions for original data and counterfactuals generated and Shapley's components (only available for GeoDataFrames)

2. Share Approach
The share approach takes into consideration the share of each group in each city
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_08_09.jpg)

3. Dual Composition Approach 
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_10_11.jpg)

4. Inspecting a different index: Relative Concentration
```python
RCO_19.statistic - RCO_15.statistic -0.5248753285836719
RCO_DS_composition.c_s: -0.5613371055626936
RCO_DS_composition.c_a: 0.03646177697902156
```

### 03-推断统计显著性实现/inferencewrappers use cases
1. 单值测试/SingleValueTest：
* 以差异性为例/Dissimilarity case
```python
dissimilarity: 0.2853070962596731
infer_D_eve.est_sim.mean: 0.052974912348536435
infer_D_eve.p_value: 0.0
```
null_approach = "evenness" 拒绝原假设，即区域间存在差异性  | null_approach = "systematic"
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_12._13jpg.jpg)

2. 二值测试/TwoValueTest /比较推断/Comparative Inference
* 仍以差异性为例/Comparative Dissimilarity | 以Gini为例/Comparative Gini | 以空间差异性为例/Comparative Spatial Dissimilarity
```python
D_19-D_15: -7.507823217456355e-05
compare_D_fit.p_value: 0.986
```
接受原假设，即15周和19周两个时期的感染率区域差异性分布变化不明显


* 相对集中隔离指数/Relative Concentration (RCO) segregation index
### 04-隔离局部方法/Local Measures of segregation
1. 基础数据处理
```python
                    'Community Area':'社区', 
                    'Community Area Name':'社区名',
                    'Birth Rate':'出生率',
                    'General Fertility Rate':'一般生育率',
                    'Low Birth Weight':'低出生体重',
                    'Prenatal Care Beginning in First Trimester':'产前3个月护理', 
                    'Preterm Births':'早产',
                    'Teen Birth Rate':'青少年生育率',
                    'Assault (Homicide)':'攻击（杀人）',
                    'Breast cancer in females':'女性乳腺癌',
                    'Cancer (All Sites)':'癌症', 
                    'Colorectal Cancer':'结肠直肠癌',
                    'Diabetes-related':'糖尿病相关',
                    'Firearm-related':'枪支相关',
                    'Infant Mortality Rate':'婴儿死亡率', 
                    'Lung Cancer':'肺癌',
                    'Prostate Cancer in Males':'男性前列腺癌',
                    'Stroke (Cerebrovascular Disease)':'中风(脑血管疾病)',
                    'Childhood Blood Lead Level Screening':'儿童血铅水平检查',
                    'Childhood Lead Poisoning':'儿童铅中毒',
                    'Gonorrhea in Females':'女性淋病', 
                    'Gonorrhea in Males':'男性淋病', 
                    'Tuberculosis':'肺结核',
                    'Below Poverty Level':'贫困水平以下', 
                    'Crowded Housing':'拥挤的住房', 
                    'Dependency':'依赖',
                    'No High School Diploma':'没有高中文凭', 
                    'Per Capita Income':'人均收入',
                    'Unemployment':'失业',
```

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_14_15_16.jpg)
> 分析要素组成比例
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_17_18.jpg)
2. 测量指数
空间分布相对集中程度
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_18.jpg)
区位多样性/Local Diversity | 区位熵/Local Entropy | Local Simpson Interaction | 区位辛普森集中度/Local Simpson Concentration  | 区位集中度/Local Centralization
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_20_21_22_23_24.jpg)
### 05-多组空间隔离指标/Multigroup aspatial indexes of segregation
```python
MultiDissim 0.385428235157427
Multigroup Gini Index: 0.495131873642657
Multigroup Normalized Exposure Index: 0.2190304202432846
Multigroup Information Theory Index: 0.16298313632840697
Multigroup Relative Diversity Index: 0.18906928526838498
Multigroup Squared Coefficient of Variation Index: 0.08438918370781343
Multigroup Diversity Index: 0.7195336679224532
Simpson's Concentration Index (lambda): 0.6012630764331958
Simpson's Interaction Index (I) 0.39873692356680424
Multigroup Divergence Index 0.1172718538918839
```
### 06-城市空间因素影响
1. 权重空间结构/weights matrices structure
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_25.png)
2. 权重影响
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_26.png)
```python
aspatial: 0.16298313632840697
rook neighborhood: 0.07958101545505616
queen neighborhood: 0.08128474935636046
kernel distance neighborhood_A: 0.14482963125123702
kernel distance neighborhood_B: 0.13043727028007907

euclidian_profile {0: 0.058180633435165705, 2000.0: 0.15484216004384405, 3000.0: 0.13043727028007907, 4000.0: 0.10541368127271342, 5000.0: 0.088480858647156}.
```
3. 城市路网影响
> 人人之间，接触的容易程度

get_osm_network
> 计算较花时间，计算距离越大，计算时间逾常

![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_27.png)
### 07-城市空间因素.路网/context-a walkabel street network
避免了单位区域面积大小的影响，尤其单个区域数值高，而面积大的部分，使分析区域合理
距离：5000m
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_28.png)
距离权重密度/distance-weighted densities
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/47_29.png)
