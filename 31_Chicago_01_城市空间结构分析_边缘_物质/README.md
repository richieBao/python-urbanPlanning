# 31.Chicago_01_城市空间结构分析_边缘_物理
此次实验大组选择Chicago作为城市空间结构分析的对象，涉及的分析内容将较为系统丰富，部分代码的功能直接采用之前的研究成果，并不断增加新的研究内容。Chicago的城市结构与国内城市具有显著性差别，在具体分析时将会标识处其差异性，尤其分析结果的比对会进一步确定之间的异同。此次实验预计涉及的内容较多，根据研究分析进度实时发布每一阶段的成果，尤其代码分享，为有意进入应用Python语言分析城市结构的规划设计师所参考。

第1阶段的代码结构如下：
## Chicago_SDAM_basis.py

### 基础类：class baseClass:
  1. 配置工作环境：def filePath(self,dirpath,fileType):
  2. 以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义：def filePath(self,dirpath,fileType):
  3. 读取landsat *_MTL.txt文件，提取需要的信息：def MTL_info(self):
  4. 栅格数据读取程序，.tif,单波段。读取需要的波段数据并存储。未裁切影像方法：def singleBand(self, rasterFp):
  5. 影像数据裁切：def rasterClip(self,rasterFp,clipRange):
  6. 保存栅格数据，1个波段：def rasterRW(self, rasterValue,resultsPath,rasterSavingFn,para):
  7. 栅格数据显示查看程序：def rasterShow(self, rasterFp):
  8. 计算数据(数组)显示：def arrayShow(self,data): 
  9. 显示图像：def imgShow(self,imges,titleName,xyticksRange=False): 
  10. 加载numpy 数组数据。可省略该函数，直接调用np.load()方法：def npArrayLoad(self,dataLoadFn):
  11. 读取多个numpy数组数据，并追加在一个数组中：def npyRead(self,filePath):
  12. 读取Numpy数组数据，因为每一数组shape不同，因此最终追加在一个列表中：def npyReadMulti(self,filePath):
  
