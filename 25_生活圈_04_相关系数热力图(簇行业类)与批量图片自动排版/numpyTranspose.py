# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:05:12 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
"""
import numpy as np

if __name__=="__main__":
    x=np.arange(4).reshape((2,2))
    print(x,'\nshape=',x.shape)
    xTrans=x.transpose()
    print(xTrans,'\nshape=',xTrans.shape)
    '''
    解释：二维默认条件下索引转置，即原来索引为（x,y）,则transpose()后变为(y,x)对应位置的值。
    例如原来元素1的索引为（0，1），变化后位置变为（1，0）即次索引的值为1，以此类推。
    '''
    
    y=np.arange(12).reshape((2,2,3))
    print(y,'\nshape=',y.shape)
    yTrans=y.transpose((2,0,1))
    print(yTrans,'\nshape=',yTrans.shape)
    '''
    即索引位置为（x,y,z）的值移动到位置（z,x,y）所在的位置。例如值4的原索引为(0,1,1)，变化后移动到(1,0,1)的位置。
    同时，原来的shape为（2，2，3），转换后，shape变换为(3,2,2)
    '''
    
    