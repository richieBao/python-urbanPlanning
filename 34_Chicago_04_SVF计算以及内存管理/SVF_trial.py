# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:26:30 2019

@author: Richie Bao-caDesign设计(cadesign.cn).Chicago
"""
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import math
from tqdm import tqdm


#数组延直线截面提取单元值
def lineProfile(zValue,originalPoint,endPoint,equalDistance):    
    z=zValue    
    x0, y0 =originalPoint
    x1, y1 =endPoint
    num = equalDistance+1
    x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
    
    # Extract the values along the line, using cubic interpolation
    zi = scipy.ndimage.map_coordinates(z, np.vstack((x,y)),cval=0,mode="nearest",order=0)
    
    x_around=np.around(x).astype(np.int)
    y_around=np.around(y).astype(np.int)
    #zi = z[x_around, y_around]
    
    '''
    #-- Plot...
    #plt.figure(figsize=(20,20))
    fig, axes = plt.subplots(nrows=2,figsize=(20, 20))
    axes[0].imshow(z)
    #axes[0].plot([x0, x1], [y0, y1], 'ro-')
    axes[0].plot(x,y, 'ro-')
    
    axes[0].axis('image')
    
    
    for i in range(6):
        for j in range(6):
            axes[0].text(j, i, z[i, j],ha="center", va="center", color="w",size=20)
    for i in range(len(x)):
            axes[0].text(x[i],y[i],round(zi[i],2),fontsize=20,color="r")
    
    #axes[1].plot(zi)
    
    plt.show()
    '''

    # #-- Plot...
    # #plt.figure(figsize=(20,20))
    # fig, axes = plt.subplots(nrows=1,figsize=(20, 20))
    # axes.imshow(z)
    # #axes[0].plot([x0, x1], [y0, y1], 'ro-')
    # axes.plot(y,x, 'ro-')
    
    # axes.axis('image')
    
    
    # for i in range(6):
    #     for j in range(6):
    #         axes.text(j, i, z[i, j],ha="center", va="center", color="w",size=20)
    # for i in range(len(x)):
    # #        axes.text(y[i],x[i],"%s:[%s,%s]"%(round(zi[i],2),round(x[i],2),round(y[i],2)),fontsize=20,color="r")
    #         axes.text(y[i],x[i],"%s:[%s,%s]"%(round(zi[i],2),x_around[i],y_around[i]),fontsize=20,color="r")
    
    # plt.show()
    
    return zi,(x,y)

'''
from skimage import viewer
from skimage import data, img_as_float
coins = img_as_float(data.coins())
new_viewer = viewer.ImageViewer(coins) 
from skimage.viewer.plugins import lineprofile
new_viewer += lineprofile.LineProfile() 


new_viewer.show() 
'''

'''
import numpy as np
from scipy import ndimage as ndi
from skimage.viewer.plugins import lineprofile
#x = np.array([[1, 1, 1, 2, 2, 2]])
#img = np.vstack([np.zeros_like(x), x, x, x, np.zeros_like(x)])
img=np.arange(36.).reshape((6, 6))
'''

def equalCircleDivide(originalCoordi,radious,lineProfileAmount):
    angle_s=360/lineProfileAmount
#    print(angle_s)
    angle_List=[i*angle_s for i in range(lineProfileAmount)]
    print("\nanglie_list",angle_List)
    coordiList=[]
    for angle in tqdm(angle_List):
        opposite=math.sin(math.radians(angle))*radious
        adjacent=math.cos(math.radians(angle))*radious
        coordiList.append((adjacent+originalCoordi[0],opposite+originalCoordi[1]))
#    print("_"*60)
#    print(coordiList)
    
    
    fig, ax = plt.subplots(figsize=(20, 20))
    x=[i[0] for i in coordiList]
    y=[i[1] for i in coordiList]
    # Using set_dashes() to modify dashing of an existing line
    line1, = ax.plot(x, y, label='Using set_dashes()')
    line1.set_dashes([2, 2, 10, 2])  # 2pt line, 2pt break, 10pt line, 2pt break    
    ax.legend()
    
    for i in range(len(x)):
        ax.text(x[i],y[i],"[%s,%s]"%(round(x[i],2),round(y[i],2)),fontsize=20,color="r")
    ax.text(originalCoordi[0],originalCoordi[1],originalCoordi,fontsize=20)
    ax.plot(originalCoordi[0],originalCoordi[1],"ro")
    plt.show()

    return coordiList

def combo_profile(zValue,originalPoint,coordiList,equalDistance):
    ziList=[]
    subCoordiList=[]
    for i in tqdm(coordiList):
        zi,subCoordi=lineProfile(zValue,originalPoint,i,equalDistance)
        ziList.append(zi)
        subCoordiList.append(subCoordi)
        

    #-- Plot...
    #plt.figure(figsize=(20,20))
    fig, axes = plt.subplots(nrows=1,figsize=zValue.shape*np.array([2]))
    axes.imshow(zValue)
    #axes[0].plot([x0, x1], [y0, y1], 'ro-')
#    print(ziList)
    for n in range(len(subCoordiList)):
#        print("#"*50)
#        print(coordi)
        x,y=subCoordiList[n]
        axes.plot(y,x, 'ro-')        
        axes.axis('image')
        
#        print(ziList[n])
        for i in range(zValue.shape[0]):
            for j in range(zValue.shape[1]):
                axes.text(j, i, zValue[i, j],ha="center", va="center", color="w",size=15)
        for i in range(len(x)):
        #        axes.text(y[i],x[i],"%s:[%s,%s]"%(round(zi[i],2),round(x[i],2),round(y[i],2)),fontsize=20,color="r")
                axes.text(y[i],x[i],"%s:(%s,%s)"%(round(ziList[n][i],2),round(x[i]),round(y[i])),fontsize=15,color="r")
        
    plt.show()

        
    return ziList

#计算障碍角度和高度
def SVF(radious,equalDistance,ziList):
    segment=radious/equalDistance
    distanceList=[i*segment for i in range(equalDistance+1)]
    print(distanceList)
    distanceList=distanceList[1:]
    
    sinValueList=[]
    for i in tqdm(ziList):
        sinMaximum=0
        for j in range(len(distanceList)):
            # print("^"*50)
            # print(i,i[0],i[j+1],distanceList[j])
            sinTemp=(i[j+1]-i[0])/math.sqrt(math.pow(distanceList[j],2)+math.pow(i[j+1]-i[0],2))
#            print(sinTemp)
            if sinTemp>sinMaximum:
                sinMaximum=sinTemp
            else:pass
        sinValueList.append(sinMaximum)
    
#    print(sinValueList)
    SVFValue=1-sum(sinValueList)/len(ziList)
    print("\nSVF resluts:%s"%SVFValue)
        
    return SVFValue
    


if __name__=="__main__":  
    pass
    #数组延直线截面提取单元值
#    zValue=np.arange(35.).reshape(5,7)
    zValue=np.round(np.random.rand(10,10)*0.5,2)
    originalPoint=[4,4]
#    endPoint=[5,0]
    equalDistance=5
#    lineProfile(zValue,originalPoint,endPoint,equalDistance)

    #延指定半径圆周等分坐标值
    radious=3
    lineProfileAmount=16
    coordiList=equalCircleDivide(originalPoint,radious,lineProfileAmount)

    #批量截面数据提取
    
    ziList=combo_profile(zValue,originalPoint,coordiList,equalDistance)

    #计算障碍角度和高度
    SVFValue=SVF(radious,equalDistance,ziList)
    
    
    
    
    
    
    