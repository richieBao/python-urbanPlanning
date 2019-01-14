# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 18:59:44 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import os
import matplotlib.pyplot as plt
import re
import numpy as np

dirpath=r"D:\digit-x\southernInternship"

'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
fileType=["jpg","png"] 
kmlType=["kml"]
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
        
#fileInfo=filePath(dirpath,fileType)
#kmlInfo=filePath(dirpath,kmlType)
#kmlInfo.pop((list(kmlInfo.keys())[0]))
#print(fileInfo)
#print(kmlInfo)

'''提取文件名包含的信息，本次实验中文件名格式为'20170719093319_30.242473-120.09893-49.2_.jpg'，可以提取出日期、经度、维度、高程和文件类型。以字典形式存储，便于后期数据处理'''
def coordiExtraction(fileInfo):
    coordiInfo={} #定义以文件夹为键，以tempDic子字典为值的字典
    for key in fileInfo.keys():
        tempDic={} #d定义子字典，以文件名为键，提取的各类信息列表为值
        for val in fileInfo[key]:
            valList=re.split('[_-]',val)        
            if '' in valList:
                valList.remove('')
                valList[3]=-float(valList[3])
            valList[0]=int(valList[0])    
            valList[1]=float(valList[1])
            valList[2]=float(valList[2])
            valList[3]=float(valList[3])              
            #print(valList)
            tempDic.setdefault(val,valList)
        coordiInfo.setdefault(key,tempDic)
    return coordiInfo
#coordiInfo=coordiExtraction(fileInfo)
#coordiSubKey=list(coordiInfo.keys())[0] #本次实验提取一个文件夹为进一步的实验对象
##print(coordiInfo)
#coordiSub=coordiInfo[coordiSubKey]
#print(coordiSubKey,'\n',coordiSub)

'''提取.kml文件中的坐标信息'''
def kmlCoordi(kmlInfo):    
    kmlCoordiInfo={}
    pat=re.compile('<coordinates>(.*?)</coordinates>') 
    '''正则表达式函数，将字符串转换为模式对象.号匹配除换行符之外的任何字符串，但只匹配一个字母，增加*？字符代表匹配前面表达式的0个
    或多个副本，并匹配尽可能少的副本'''
    count=0
    for key in kmlInfo.keys():
        tempDic={}
        for val in kmlInfo[key]:
            f=open(os.path.join(key,val),'r',encoding='UTF-8') #.kml文件中含有中文
            content=f.read().replace('\n',' ') #移除换行，从而可以根据模式对象提取标识符间的内容，同时忽略换行
            coordiInfo=pat.findall(content)
            coordiInfoStr=''
            for i in coordiInfo: #将提取的多个字符连为一个，便于统一处理
                coordiInfoStr+=i        
            coordiInfoStrip=coordiInfoStr.strip(' ')
            #print(coordiInfoStrip)
            coordiInfoList=coordiInfoStrip.split('\t\t')  #根据制表符切分字符串为列表，不同的文件可能切分符不同，根据实际调整
            #print(coordiInfoList)
            coordi=[]
            for i in coordiInfoList:
                coordiSplit=i.split(',')
                temp=[]
                for j in coordiSplit:                    
                    try:  #提取的坐标值字符，可能不正确，不能转换为浮点数，因此通过异常处理
                        temp.append(float(j))
                    except ValueError:
                        #print("ValureError")
                        count+=1
                if len(temp)==3:  #可能提取的坐标值除了经纬度和高程，会出现多余或者少于3的情况，判断后将其忽略
                    coordi.append(temp)
            f.close()
            tempDic.setdefault(val,coordi)        
        kmlCoordiInfo.setdefault(key,tempDic)  
    print("ValureError=",count)
    return kmlCoordiInfo
#kmlCoordiInfo=kmlCoordi(kmlInfo)
#kmlSub=kmlCoordiInfo[coordiSubKey]
#print(kmlSub)
#print(len(list(kmlSub.keys())))

'''读取经纬度坐标，根据.kml文件打印成路径,同时定位图片位置并显示高程变化 '''
def researchPath(coordiSub,kmlSub):
    coordiValues=list(coordiSub.values())        
    coordiValuesArray=np.array(coordiValues) #将存储了值(子列表)的列表转化为numpy的数组
    kmlSubValues=list(kmlSub.values())[0]
    kmlSubArray=np.array(kmlSubValues)
    print(coordiValuesArray.shape)
    print(kmlSubArray.shape)
    print('\n','数组的维数/秩=',coordiValuesArray.ndim,'\n','数组的维度/轴=',coordiValuesArray.shape,'\n','数组元素的总个数=',coordiValuesArray.size,'\n','数组中每个元素的字节大小=',coordiValuesArray.itemsize,'\n','数据类型=',coordiValuesArray.dtype)
    fig,ax=plt.subplots()
    ax.plot(kmlSubArray[:,0],kmlSubArray[:,1],'r-',lw=0.5,markersize=5)
    #print(kmlSubArray[:,0][0:30].tolist())
    #ax.plot(coordiValuesArray[:,2],coordiValuesArray[:,1],'r+-',lw=0.5,markersize=5)
    cm=plt.cm.get_cmap('hot') #具体的`matplotlib.colors.Colormap'实例可以查看matplotlib官网 http://matplotlib.org/users/colormaps.html，替换不同色系
    sc=ax.scatter(coordiValuesArray[:,2],coordiValuesArray[:,1],c=coordiValuesArray[:,3],s=50,alpha=0.8,cmap=cm)  #按高程显示散点颜色
    fig.colorbar(sc)
    ax.set_xlabel('lng')
    ax.set_ylabel('lat')
    #print(coordiValues[0][1],coordiValues[0][2])
    ax.annotate('origin',xy=(coordiValues[0][2],coordiValues[0][1]),xycoords='data',xytext=(coordiValues[0][2]+0.015, coordiValues[0][1]-0.006),fontsize=14,arrowprops=dict(facecolor='black',shrink=0.05))
    fig.text(0.50,0.92,'research path',fontsize=20,color='gray',horizontalalignment='center',va='top',alpha=0.5)    
    fig.set_figheight(15)
    fig.set_figwidth(15)
    plt.show()
#researchPath(coordiSub,kmlSub)
    
if __name__=="__main__":
    fileInfo=filePath(dirpath,fileType)
    kmlInfo=filePath(dirpath,kmlType)
    kmlInfo.pop((list(kmlInfo.keys())[0]))
    
    coordiInfo=coordiExtraction(fileInfo)
    coordiSubKey=list(coordiInfo.keys())[0] #本次实验提取一个文件夹为进一步的实验对象
    print(coordiInfo)
    coordiSub=coordiInfo[coordiSubKey]
    
    kmlCoordiInfo=kmlCoordi(kmlInfo)
    kmlSub=kmlCoordiInfo[coordiSubKey]
    print(kmlSub)
    print(len(list(kmlSub.keys())))
    
    
    researchPath(coordiSub,kmlSub)
    