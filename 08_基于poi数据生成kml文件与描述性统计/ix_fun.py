# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 22:57:49 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import numpy as np

def ix_cal(ufct,*vectors):
    vs=np.ix_(*vectors)
    r=ufct.identity
    #print(r)
    for v in vs:
        r=ufct(r,v)
    return r


if __name__=="__main__":
    a=np.array([12,13,14,15])
    b=np.array([2,5,1])
    c=np.array([21,22,23,25,28])
    result=ix_cal(np.add,a,b,c)
    print(result)


    