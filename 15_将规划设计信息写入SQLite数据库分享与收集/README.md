随着网络技术的发展，及其应用的大幅度普及，更多的线下工具逐步由网络提供，直接在网页上操作，实时存储数据。各项实验的开展，也因此需要在线下和线上同时展开，满足不同的需要。 实际上，结合python的数据分析(机器/深度学习)，使用Flask轻量级Web应用框架(自由性)，结合SQLite/MySQL数据库，并应用echats/hicharts等图表库，可以实现规划设计行业相关探索，也必定是该行业目前及未来发展的一个 主要分支。 

## 技术内容
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/953.png)

## 将图像信息写入SQLite数据库
### SQLite数据库
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/949.png)
### 数据模型/表结构
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/950.png)
### 原始存储图像信息的.csv文件
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/951.png)
```python
'''
Created on Wed Feb  7 02:35:31 2018

@author: RichieBall-caDesign设计(cadesign.cn)
'''
import pandas as pd
import sqlite3
from scipy import misc
import matplotlib.image as mpimg
import os
from config import DevConfig

fileName_1=r'static/images/imagesA/2017.12.15-GF-S-WTSolutions-GPS.csv'  #记录所拍摄图像的信息文件，不同的手机app，获取信息的存储方式不同，例如前文在基于GPS调研与数据读取部分
fileName_2=r'static/images/imagesA/2017.12.15-lmk-S-WTSolutions-GPS.csv'
imresizeFN=r'static/images/imresize/' #用于存储调整图像大小后的图像路径

'''读取存储图像信息文件为dataframe格式'''
def csvReading(fileName):
    csvData=pd.read_csv(fileName)  #读取存储有图像信息的csv文件，并存储到dataframe中
    return csvData

'''调整图像大小并存储，及返回需要的图像信息'''
def getPixData(imgInfo):  #调整图像大小，便于网页显示
    imgPath=imgInfo['imagename']
    pathTemp=[]
    for img in imgPath:
        try:
            lum_img = mpimg.imread(os.path.join('static/images/imagesA',img))  # 读取图像为数组，值为RGB格式0-255
        except:pass
        lum_imgSmall = misc.imresize(lum_img, 0.3)  # 传入图像的数组，调整图片大小。scipy.misc.imresize(*args, **kwds)：This function is only available if Python Imaging Library (PIL) is installed.使用pip install Pillow安装
        misc.imsave(os.path.join(imresizeFN,img),lum_imgSmall) #存储调整大小的图像，用于下一步的图像识别，以及减小网页显示的压力
        pathTemp.append(imresizeFN+img[:-4]+'.jpg')
    #print(pathTemp)
    imgInfo['imagename']=pathTemp
    return imgInfo

if __name__ == "__main__":
    fn_1 = csvReading(fileName_1)
    fn_2 = csvReading(fileName_2)
    imageFN = pd.concat([fn_1, fn_2]) #手机app拍摄图像时，信息存储在了两个文件中，需要分别读取后并合并
    imageFN.columns = ['imagename', 'time', 'long', 'lat'] #为方便编程，修改framedata的列索引为英文
    imgInfo=getPixData(imageFN)
    # print(imgInfo)
    conn=sqlite3.connect(DevConfig().DATABASE) #连接数据库
    imgInfo.to_sql('imagesinfodf',conn)  #将dataframe数据存储到SQlite数据库中，表结构根据framedata索引自动建立

```
## 阶段A-目录结构
![](https://github.com/richieBao/python-urbanPlanning/blob/master/images/952.png)
