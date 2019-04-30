# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:38:42 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import numpy as np

if __name__=="__main__": 
    arr=np.arange(20).reshape((4,5))
    print(arr)

    #arr.ravel()与arr.flatten()默认行序有限
    print(arr.ravel())
    print(arr.flatten())
    
    #列序优先传入参数'F'
    print(arr.ravel('F'))
    print(arr.flatten('F'))
    
    print(arr.reshape(-1)) #用.reshape(-1)的方法将数组将为1维
    print(arr.T.reshape(-1)) #用.T.reshape(-1)的方法实现列序降维
    
    '''    
    arr
    array([[ 0,  1,  2,  3,  4],
       [ 5,  6,  7,  8,  9],
       [10, 11, 12, 13, 14],
       [15, 16, 17, 18, 19]])
    '''
    arr.flatten()[1]=999 #.flatten()返回copy，对copy所作的修改不影响原始数组
    print(arr)
    arr.ravel()[1]=777 #.ravel()返回view，影响原始数组
    print(arr)