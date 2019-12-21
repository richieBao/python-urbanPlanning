# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 22:25:18 2019

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

#读取.las文件，并分布存储为分类数据、建筑高度数据、DTM数据
def readAndWriteLas(lasFn,outputFn):   
    #pdal建立分类数据
    json_a = """
        {
            "pipeline": [
                "%s",
            
                {
                    "filename":"%s",
                    "type":"writers.gdal",
                    "dimension":"Classification",
                    "data_type":"uint16_t",
                    "output_type":"mean",  
                    "resolution": 1
                }
                
            ]
        }"""%(lasFn,outputFn[0])     
    #"output_type":"all",        

    #pdal建立建筑类数据。有些数据无建筑分类，因此在执行execute时，报错中断    
    json_b = """
        {
            "pipeline": [
                "%s",
                {
                "type":"filters.range",
                "limits":"Z[0:],Classification[6:6]"
                },
            
                {
                    "filename":"%s",
                    "type":"writers.gdal",
                    "gdaldriver":"GTiff",
                    "output_type":"mean",
                    "resolution": 1                    
                }
                
            ]
        }"""%(lasFn,outputFn[1])

    #pdal建立dtm数据
    json_c = """
        {
            "pipeline": [
                "%s",
          
                {
                    "filename":"%s",
                    "gdaldriver":"GTiff",
                    "type":"writers.gdal",
                    "output_type":"mean",
                    "resolution": 1                    
                }
                
            ]
        }"""%(lasFn, outputFn[2])
            
#    jsonMulti=[json_a,json_b,json_c]
    jsonMulti=[json_a,json_c] #仅计算分类数据和dtm数据
    for json in jsonMulti:
        pipeline = pdal.Pipeline(json)
        pipeline.loglevel = 8 #really noisy
        if pipeline.validate(): # check if our JSON and options were good
#            print("^"*50)
#            print(pipeline.validate())
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
            
#    pipeline = pdal.Pipeline(json_a)
#    pipeline.loglevel = 8 #really noisy
#    pipeline.validate() # check if our JSON and options were good
#    count = pipeline.execute()
#    arrays = pipeline.arrays
#    metadata = pipeline.metadata
#    log = pipeline.log
#    print(metadata)            

'''展平列表函数'''
flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]

#批量处理las文件
def combo_las(dirpath,outputFp):
    fileType=["las"]     
    lasFnDic=filePath(dirpath,fileType)
#    print(lasFnList)
    lasFnList=flatten_lst([[os.path.join(k,lasFnDic[k][i]) for i in range(len(lasFnDic[k]))] for k in lasFnDic.keys()])
#    print(lasFnList)
#    print(lasFnList)
#    print(ok)     
    
    pattern=re.compile(r'[_](.*?)[.]', re.S)    

    crackedFns=[]
    for i in tqdm(lasFnList):  
#        print("_"*50)
#        print(i)
#        print(re.findall(pattern, i))
        fnNum=re.findall(pattern, i.split("\\")[-1])[0] #提取文件名字符串中的数字
#        print("\n",fnNum)
#        print("#"*50)
        #注意文件名路径中"\"和"/"，不同库支持的类型可能有所不同，需自行调整
        outputFn=[os.path.join(outputFp,"classification_%s.tif"%fnNum).replace("\\","/"),
              os.path.join(outputFp,"building_%s.tif"%fnNum).replace("\\","/"),
              os.path.join(outputFp,"dtm_%s.tif"%fnNum).replace("\\","/")]  
#        print(outputFn)
#        print("#"*50)
#        print("dealing with .las file:",i.replace("\\","/"))
        
        crackedFn=readAndWriteLas(i.replace("\\","/"),outputFn)
        crackedFns.append(crackedFn)
    # with open("D:\data\lidar\lidar_bundle\03_Chicago_loop_done\crackedFns.txt", "wb") as fp: 
    #     pickle.dump(crackedFn, fp)
    return crackedFns
      

if __name__=="__main__":     
#    lasFn="D:/data/lidar/pdal_exercise/LAS_17508825.las"
#    fp=r"D:/data/lidar/pdal_exercise"
#    outputFn=[r"D:/data/lidar/pdal_exercise/classification.tif",
#              r"D:/data/lidar/pdal_exercise/building.tif",
#              r"D:/data/lidar/pdal_exercise/dtm.tif"]
#    readAndWriteLas(lasFn,outputFn)
    
    #批量处理
    dirpath=r"D:\data\lidar\lidar_bundle\06_river forest"
    outputFp=r"D:\data\lidar\lidar_bundle\06_river forest_done"
    crackedFnsList=combo_las(dirpath,outputFp)
    
    