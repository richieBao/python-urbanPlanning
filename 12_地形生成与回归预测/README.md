# 百度poi数据采集"酒店 ":"hotel"数据
## 1 '''读取文本数据'''
```python
'''读取文本数据'''
def txtReading(fn):
    f=open(fn,'r')
    dataList=[]
    pat=re.compile('{(.*?)}')
    while True:
        line=f.readline().strip()    
        if len(line)!=0:
            line=pat.findall(line)[0].split(',')
            line=[float(i) for i in lineCoordi]
            dataList.append(line)
        if not line:break
    f.close()
    dataArray=np.array(dataList) #数据输出为数组形式
    return dataArray
```
## 2 '''提取分析所需数据，并转换为skleran的bunch存储方式，统一格式，方便读取。'''
```python
'''提取分析所需数据，并转换为skleran的bunch存储方式，统一格式，方便读取。'''
def json2bunch(fName):   #传入数据，面向不同的数据存储方式，需要调整函数内读取的代码
    infoDic=[]
    f=open(fName)
    jsonDecodes=json.load(f)
    j=0
    for info in jsonDecodes:
        condiKeys=info['detail_info'].keys()
        if 'price' in condiKeys and'overall_rating' in condiKeys and 'service_rating' in condiKeys and 'facility_rating' in condiKeys and 'hygiene_rating' in condiKeys and 'image_num' in condiKeys and 'comment_num' in condiKeys and 'favorite_num' in condiKeys: #提取的键都有数据时，才提取，否则忽略掉此数据
            if 50<float(info['detail_info']['price'])<1000: #设置价格区间，提取数据
                j+=1
                infoDic.append([info['location']['lat'],info['location']['lng'],info['detail_info']['price'],info['detail_info']['overall_rating'],info['detail_info']['service_rating'],info['detail_info']['facility_rating'],info['detail_info']['hygiene_rating'],info['detail_info']['image_num'],info['detail_info']['comment_num'],info['detail_info']['favorite_num'],info['detail_info']['checkin_num'],info['name']])
            else:pass
        else:pass
    print('.....................................',j)

    data=np.array([(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10]) for v in infoDic],dtype='float')  #解释变量(特征)数据部分
    targetInfo=np.array([v[11] for v in infoDic])  #目标变量(类标)部分
    dataBunch=base.Bunch(DESCR=r'info of poi',data=data,feature_names=['lat','lng','price','overall_rating','service_rating','facility_rating','hygiene_rating','image_num','comment_num','favorite_num','checkin_num'],target=targetInfo,target_names=['price','name'])  #建立sklearn的数据存储格式bunch
    return dataBunch #返回bunch格式的数据
```

## 3 描述性统计
```python
'''描述性统计，分析解释变量之间及与目标变量之间的关系'''
def basicStat(dataBunch):
    sns.set(style='whitegrid',context='notebook')
    cols=['lat','lng','price','overall_rating','service_rating','facility_rating','hygiene_rating','image_num','comment_num','favorite_num','checkin_num']  #用于标识frame数据框的列索引
    frame=pd.DataFrame(dataBunch.data[:],columns=cols)  #转换为pandas库的frame数据框格式，方便数据观察和提取
#    print(frame)
    sns.pairplot(frame[cols],size=2.5)  #两两数据的散点图，用于观察数据间的关系
    plt.show()    
   
    cm=np.corrcoef(frame[cols].values.T)  #计算两两间的相关系数
    sns.set(font_scale=1.3)
    hm=sns.heatmap(cm,cbar=True,annot=True,square=True,fmt='.2f',annot_kws={'size':13},yticklabels=cols,xticklabels=cols) #热力图显示相关系数，方便直观查看
    plt.show
```

## 4 统计结果
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/935.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/936.png)

# 地形生成<基于随机森林回归模型|结合参数化(grasshopper)>
## grasshopper程序
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/937.png)
## 生成结果
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/938.png)
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/939.png)
