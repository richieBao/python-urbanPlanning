# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:36:49 2019

@author: RichieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import os

if __name__=="__main__": 
    data_a=np.arange(20).reshape((2,10))
    '''A:保存数据为.npy
    help(np.save)
    save(file, arr, allow_pickle=True, fix_imports=True)
    '''
    fp=r'C:\Users\Richi\sf_richiebao\sf_code\results'
    fn_a=r'data_a' #保存时不用指定文件类型
    np.save(os.path.join(fp,fn_a),data_a)
    
    #读取.npy数据
    data_a_r=np.load(os.path.join(fp,fn_a)+".npy") #读取时需要指定文件类型
    print(data_a_r)
    
    '''B:保存数据为.npz
    help(np.savez)
    savez(file, *args, **kwds)    
    **args:待存储的数组，可以存储多个，如果没有给数组指定keywords,则默认为'arr_0', 'arr_1', etc.
    **kwds:即keywords，为不同数组指定关键字/字段
    用给定kwds的方法，可以方便保存机器学习中的训练集、验证集、测试集
    '''
    data_b=np.cos(data_a)
    print(data_b)
    fn_ab=r'data_ab'
    np.savez(os.path.join(fp,fn_ab),dataA=data_a,dataB=data_b)
    #读取.npz数据
    data_ab=np.load(os.path.join(fp,fn_ab)+".npz")
    print("data_a:\n",data_ab["dataA"],"\n","data_b:\n",data_ab["dataB"])
    
    '''C:保存数据为.txt
    help(np.savetxt)
    savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ', encoding=None)
    X:待存储的1D或2D数组
    fmt:控制数据存储的格式
    delimiter:数据列之间的分隔符
    newline:数据行之间的分隔符
    header:文件头部写入的字符串
    footer:文件底部写入的字符串
    comments:文件头部或者尾部字符串的开头字符,默认是'#'
    encoding:使用默认参数
    '''
    x=np.ones((3,4))
    '''
    x
    array([[1., 1., 1., 1.],
       [1., 1., 1., 1.],
       [1., 1., 1., 1.]])
    '''
    np.savetxt(os.path.join(fp,"dataTxt.txt"),x,fmt='%.2e',delimiter=",",header="start",footer="end") #%e用科学计数法格式化浮点数
    y=np.loadtxt(os.path.join(fp,"dataTxt.txt"),delimiter=",")
    print(y)