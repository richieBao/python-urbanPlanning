# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 09:36:36 2020

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import pdal,os,re,gdal,pickle
from tqdm import tqdm


'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
def filePath(dirpath,fileType):
    fileInfo={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       #print(i,'\n')
       #print(dirpath,'\n',dirNames,'\n',fileNames,'\n')
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           #if not tempList :
               #print(i,"NULL")
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               fileInfo.setdefault(dirpath,tempList)
    return fileInfo  


#读取.las文件，提取DTM数据
def readAndWriteLas(lasFn,outputFn):   
    #pdal建立DTM数据， 分类2即为ground分类
    json_dtm = """
        {
            "pipeline": [
                "%s",
                {
                    "type":"filters.range",
                    "limits":"Classification[2:2]"
                },            
                {
                    "filename":"%s",
                    "gdaldriver":"GTiff",
                    "resolution": 1,
                    "output_type":"mean",
                    "type":"writers.gdal"
                }
                
            ]
        }"""%(lasFn,outputFn[0])    
    
'''实验   
    json_hag_bpf="""
        {
           "pipeline":[
                "%s",
                {
                    "type":"filters.hag"
                },
                {
                    "type":"writers.bpf",
                    "filename":"%s",
                    "output_dims":"X,Y,Z,HeightAboveGround"
                }
            ]
        }"""%(lasFn,outputFn[0])  
        
    json_hagInplace="""
        {
           "pipeline":[
                "%s",
                {
                    "type":"filters.hag"
                },
                {
                    "type":"filters.ferry",
                    "dimensions":"HeightAboveGround=Z"
                },
                "autzen-height-as-Z.laz"
            ]
        }"""%lasFn

    json_HeightAboveGround="""
        {
            "pipeline": [
                "%s",
            
                {
                    "filename":"%s",
                    "type":"writers.gdal",
                    "dimension":"Z",
                    "data_type":"uint16_t",
                    "output_type":"mean",  
                    "resolution": 1
                }
                
            ]
        }"""%(lasFn,outputFn[0]) 
'''   
    
    jsonMulti=[json_dtm] #仅计算DTM数据
    for json in jsonMulti:
        pipeline = pdal.Pipeline(json)
        pipeline.loglevel = 8 #really noisy
        if pipeline.validate(): # check if our JSON and options were good
            print("^"*50)
            print(pipeline.validate())
            try:
                count = pipeline.execute()
            except:
                print("\nAn exception occurred，the file name:%s"%lasFn)
                return lasFn
#            arrays = pipeline.arrays
#            metadata = pipeline.metadata
#            log = pipeline.log
#        print(metadata)
        else:
            print("pipline unvalidate!!!")        

        
'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]

#批量处理
def combo_dtm(dirpath,outputFp):
    fileType=["las"]  
    lasFnDic=filePath(dirpath,fileType)
    lasFnList=flatten_lst([[os.path.join(k,lasFnDic[k][i]) for i in range(len(lasFnDic[k]))] for k in lasFnDic.keys()])
    # lasFnList=lasFnList[:3]
    pattern=re.compile(r'[_](.*?)[.]', re.S)
    crackedFns=[]
    for i in tqdm(lasFnList): 
        fnNum=re.findall(pattern, i.split("\\")[-1])[0] #提取文件名字符串中的数字

        #注意文件名路径中"\"和"/"，不同库支持的类型可能有所不同，需自行调整
        outputFn=[
              # os.path.join(outputFp,"classification_%s.tif"%fnNum).replace("\\","/"),
              # os.path.join(outputFp,"building_%s.tif"%fnNum).replace("\\","/"),
                os.path.join(outputFp,"Tdtm_%s.tif"%fnNum).replace("\\","/")
               # os.path.join(outputFp,"Tdtm_%s.bpf"%fnNum).replace("\\","/")
              ]  
        print(i)
        crackedFn=readAndWriteLas(i.replace("\\","/"),outputFn)
        crackedFns.append(crackedFn)
    return crackedFns

if __name__=="__main__":    
    dirpath=r"D:\data\data_01_Chicago\lidar\lidar_bundle\14_hinsdale"
    outputFp=r"D:\data\data_01_Chicago\lidar\lidar_bundle\14_hinsdaleD_dtm"
    crackedFnsList=crackedFnsList=combo_dtm(dirpath,outputFp)