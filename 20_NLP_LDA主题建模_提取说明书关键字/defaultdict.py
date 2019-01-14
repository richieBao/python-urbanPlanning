# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 17:36:34 2018

@author:richieBao-caDesign设计(cadesign.cn)
"""
from collections import defaultdict

##Example 1
#string="caDesign:-robot-x.top/cadesign.cn/digit-x.org"
#dic=defaultdict(int)
#for key in string:
#    dic[key]+=1
#print(dic)

#Example 2-1
#data=[('veg',120),('bare',304),('water',246),('veg',300),('water',230),('farm',356)]
#dic=defaultdict(list)
#for key,value in data:
#    dic[key].append(value)
#print(dic)
#
#Example 2-2
data=[('veg',120),('bare',304),('water',246),('veg',300),('water',230),('farm',356)]
dic=defaultdict(set)
for key,value in data:
    dic[key].add(value)
print(dic)