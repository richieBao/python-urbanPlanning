# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 23:27:04 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(19680801)  #固定随机状态，确保每次运行后输出结果相同
'''
points=np.random.random((2,20,3)) #秩(rank)为3的的多维数组，即3轴(axes)，0轴第1个维度长度为2，1轴第2个维度长度为20，2轴第3个维度长度为3。
#print(points)
#points[1,:,2]+=1  #0轴索引值为1项，1轴全部，2轴索引值为2项的值均加1.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors=('b','r','g','c','m','y','k','w')
markers=('o','^','+','*','v','x','_','.')
for i in range(points.shape[0]):  #循环0轴
    #print(points.reshape(-1,3),points)
    #print(points[i,:,0],points[i,:,1],points[i,:,2])
    #print(points[i])
    ax.scatter(points[i,:,0],points[i,:,1],points[i,:,2], c=points[i], marker=markers[i])
ax.set_xlabel('X coordi')
ax.set_ylabel('Y coordi')
ax.set_zlabel('Z coordi')
fig.set_figheight(12)
fig.set_figwidth(12)

plt.show()
'''
'''
关于numpy.random.seed()问题：
1.如果使用相同的seed( )值，则每次生成的随即数都相同； 
2.如果不设置这个值，则系统根据时间来自己选择这个值，此时每次生成的随机数因时间差异而不同；
3.设置的seed()值仅一次有效。
'''

num=0
print('随机种子仅一次有效,因此随机结果因时间差异而不同\t')
while(num<5):
    print(np.random.random())
    num+=1
print('为了获取相同的随机数结果，每次均需要调用seed种子\t')
while(num<10):
    np.random.seed(19680801) 
    print(np.random.random())
    num+=1
    

