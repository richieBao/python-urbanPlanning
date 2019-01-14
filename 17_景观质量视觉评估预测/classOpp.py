# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 20:58:55 2018

@author: richieBao-caDesign设计(cadesign.cn)
"""

class Bird: #定义一般鸟类的属性与方法，语句class Bird:中Bird为类的名称
    fly='Whirring' #定义一般鸟类飞的属性
    def __init__(self): #调用__init__构造函数，初始化对象的各属性，类的各属性（成员变量）均可以在构造函数中定义；每一个类方法的第一个参数（self)，包括 __init__，总是指向类的当前实例的一个引用。按照习惯这个参数被命名为 self，强烈建立除了self 不要把它命名为别的名称，这是一个既定的习惯
        self.hungry=True #初始化变量hungry的属性为True,在类实例化后执行
    def eat(self): #通过定义函数构建类的方法，即鸟类都具有吃的方法，self被指向该方法被调用的对象即实例
        if self.hungry: #判断类的属性（变量）hungry是否为True，即鸟是否需要进食，初始值在初始方法中已经定义为True,即鸟未进食需要吃东西
            print('Aaaah...') #如果hungry为True则执行该语句
            self.hungry=False #执行完打印语句后，将hungry的属性更改为False，即鸟已经吃过了食物
        else: #当类属性hungry为False时执行语句
            print('No,Thanks!')
        
class Apodidae(Bird): #定义鸟类的子类雨燕目的属性与方法，因为雨燕目是鸟类的子类，所以除了自身的属性与方法外，也包括一般鸟类的属性与方法，因此在class foo(superclass):定义类方法时，在圆括号内输入子类的超类即鸟类Bird，使子类雨燕目具有一般鸟类的属性和方法
    def __init__(self): #初始化类雨燕目对象的各属性
        super(Apodidae,self).__init__() #使用super()函数，可以避免子类初始化构造方法重写超类的初始化构造方法，使引用的实例不具有超类的初始化方法，即self.hungry=True，吃的方法
        self.sound='Squawk!' #初始化变量sound的属性为字符串'Squawk!'
    def sing(self): #定义类雨燕目的sing()方法，即雨燕目类的鸟都会唱歌
        print(self.sound)