# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:36:55 2019

@author: RichieBao-caDesign设计(cadesign.cn)
参考：官方网站-https://docs.python.org/2/library/collections.html
"""
from collections import Counter,deque,defaultdict,namedtuple,OrderedDict
import itertools
import re

#指定最后n行，返回文本
def tail(filename, n=10):
    'Return the last n lines of a file'
    return deque(open(filename), n)

#平滑数据
def moving_average(iterable, n=3):
    print('#########')
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1)) #itertools库参看9-循环语句/机器学习-聚类-城市色彩-B-印象
    d.appendleft(0)
    s = sum(d)
    
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / float(n)

#移除指定位置元素
def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)
    
#由于named tuple命名元组是一个常规的Python类，所以很容易使用子类添加或更改功能。下面是如何添加计算字段和固定宽度的打印格式:   
class Point_class(namedtuple('Point', 'x y')):
    __slots__ = () #可以用来限制class能添加的属性，此处有助于通过防止创建实例字典来降低内存需求
    @property #用装饰器函数把 get/set 方法“装饰”成属性调用
    def hypot(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __str__(self):
        return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)   
    

if __name__=="__main__": 
    '''A:Counter Objects
    
    '''
    #01:counter tool计数器工具支持方便快捷的计数
    cnt=Counter()
    for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
        cnt[word] += 1
    print(cnt) #Counter({'blue': 3, 'red': 2, 'green': 1})
    
    for num in [1,2,3,3,4,3,2,5,7,8,6,5,4,4,3,2,2,2,5,6,6,6,7,8,8,8]:
        cnt[num]+=1
    print(cnt) #Counter({2: 5, 3: 4, 8: 4, 6: 4, 'blue': 3, 4: 3, 5: 3, 'red': 2, 7: 2, 'green': 1, 1: 1})
    
    hamlet=r'C:\Users\Richi\sf_richiebao\sf_monograph\22_socialAttribute_01_continuousClusteringBasedonDistance\data\hamlet.txt'
    words = re.findall(r'\w+', open(hamlet).read().lower()) #r'\w+'匹配数字、字母和下划线的多个字符
    print(Counter(words).most_common(10)) #计算频数，并提取最多的10个
    
    #02：Counter的初始化
    c = Counter()                           # 空值    
    c = Counter({'red': 4, 'blue': 2})      # 从映射中创建
    c = Counter(cats=4, dogs=8)             # 从关键字参数中创建
    c = Counter('caDesign.cn')              # 从可迭代的对象中创建
    print(c)
    '''
    Counter({'c': 2,
         'a': 1,
         'D': 1,
         'e': 1,
         's': 1,
         'i': 1,
         'g': 1,
         'n': 2,
         '.': 1})
    '''
    #03:待计数的对象不在列表中时，返回值为0，而不会返回异常
    c=Counter(['caDesign','digital-x','X','X'])
    print(c['X'])
    print(c['design'])

    #04：使用del移除元素
    del c['X']
    print(c)
    
    #05:elements() 任意顺序返回元素，个数同计数数量，如果计数小于1，则被忽略
    c = Counter(a=4, b=2, c=0, d=-2)
    print(list(c.elements())) #['a', 'a', 'a', 'a', 'b', 'b']
    
    #06:most_common([n]) 返回一个频数列表，如果指定n则返回最大的n个对象，否则返回全部元素，顺序随机
    print(Counter("abstraction").most_common(2)) #[('a', 2), ('t', 2)]
    
    #07:subtract([iterable-or-mapping]) 元素频数相减
    c = Counter(a=4, b=2, c=0, d=-2)
    d = Counter(a=1, b=2, c=3, d=4)
    c.subtract(d)
    print(c) #Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
    print(c['d']) #-6
    print(list(c.elements())) #['a', 'a', 'a']
    
    #08:常用操作
    c.clear()  #清空重置
    print(c)
    c=Counter(delicacy=349,hotel=232,spot=35,beauty=56,media=43,shopping=456)
    print(sum(c.values())) #计算总数
    print(list(c)) #返回元素列表（unique)
    print(set(c)) #返回元素集合
    print(dict(c)) #返回元素elem-频数cnt字典
    print(c.items()) #回元素elem-频数cnt对列表。dict_items([('delicacy', 349), ('hotel', 232), ('spot', 35), ('beauty', 56), ('media', 43), ('shopping', 456)])
    print(Counter(c.items())) #从（elem,cnt）对列表建立Counter
    print(c.most_common()[:-3-1:-1]) #c.most_common()[:-n-1:-1] ,获取频数最小的n个对象
    c['zero']=0
    c['negative']=-6
    print(c)
    c+=Counter() #移除0和负值
    print(c)
    
    #09：运算
    c = Counter(a=3, b=1)
    d = Counter(a=1, b=2)
    print(c+d) #频数之和
    print(c-d) #频数之差，仅保持正数
    print(c&d) #交集返回最小：min(c[x], d[x])
    print(c|d) #并集返回最大
    
    
    '''B:deque objects
    为“double-ended queue”的缩写，双端队列，可以实现队伍头尾快速增加和取出对象等操作。
    其效率高于使用列表的方法。
    '''    
    #01：初始化
    d=deque('caDesign')
    for elem in d:
        print(elem.upper())
    
    #02:append(x)与appendleft(x)
    d.append('.cn') #队尾追加
    d.appendleft('www.') #对首追加
    print(d)
    
    #03：pop()与popleft()
    print(d.pop()) #移除与返回队尾元素
    print(d.popleft()) #移除与返回队首元素
    print(d)
    
    #04：list(deque) 转换为列表
    print(list(d))
    
    #05:提取元素
    print(d[0])
    print(d[-1])
    
    #06:reversed() 将deque的元素反向放置，然后返回None
    print(list(reversed(d)))
    
    #07:搜索队列
    print('i' in d)
    
    #08:extend(iterable)与extendleft(iterable)
    reversed(d)
    d.extend('.cn') #队尾逐个顺序追加
    d.extendleft(':sptth') #队首逐个逆序追加
    print(d)
        
    #09：rotate(n=1) 正数右移，负数左移
    d.rotate(1)
    print(d)
    d.rotate(-1)
    print(d)
    
    #10:count(x) 计数指定的元素
    print(d.count('c'))   
    
    #11:clear() 清空队列
    d.clear()
    print(d)
    
    #12:tail(filename, n=10)函数：指定最后n行，返回文本
    print(tail(hamlet,n=5))
    
    #13:moving_average(iterable, n=3)函数平滑数据，http://en.wikipedia.org/wiki/Moving_average
    lst=[40, 30, 50, 46, 39, 44]
    print(list(moving_average(lst)))
    
    #14:delete_nth(d, n)函数:
    d=deque('caDesign.cn')
    delete_nth(d,3)
    print(d)

    '''C:defaultdict objects
    defaultdict 是内建 dict 类的子类，它覆写了一个方法并添加了一个可写的实例变量。其余功能与字典相同。
    '''   
    #01:使用list作为default_factory，很容易将一系列键值对分组到列表字典中,效率高于d.setdefault(k, []).append(v)
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d = defaultdict(list)
    for k,v in s:
        d[k].append(v)
    print(d.items()) #dict_items([('yellow', [1, 3]), ('blue', [2, 4]), ('red', [1])])
    
    #02:将default_factory设置为int,对于计数使得defaultdict非常有用
    s='caDesign.cn'
    d=defaultdict(int)
    for k in s:
        d[k]+=1
    print(d.items())
    
    #03:将default_factory设置为set使得defaultdict对于构建集合字典非常有用
    s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
    d = defaultdict(set)
    for k,v in s:
        d[k].add(v)
    print(d.items())
    
    '''D: namedtuple()
    命名元组将意义分配给元组中的每个位置，并允许更易于阅读、自文档化的代码。它们可以在任何使用常规元组的地方使用，并且它们添加了按名称而不是位置索引访问字段的功能。
    
    '''
    #01:基本操作，定义，实例化与取值
    Point = namedtuple('Point', ['x', 'y']) #定义namedtuple结构
    p=Point(11,y=22) #用位置或关键字参数实例化
    print(p[0]+p[1])
    x,y=p #序列解包
    print(x,y)
    print(p.x+p.y) #使用字段取值
    print(p)
    
    print(getattr(p,'x')) #使用getattr()读取值
    
    d = {'x': 77, 'y': 22}
    print(Point(**d)) #将字典转换为named tuple
    
    #02：类方法
    t=[33,22]
    p=Point._make(t) #类方法，使用现有的序列或可迭代对象建立新实例。
    print(p)
    
    d=p._asdict() #返回一个新的OrderedDict，它将字段名映射到对应的值
    print(d)
    
    new_p=p._replace(x=99) #返回指定元组的新实例，用新值替换指定字段
    print(new_p)
    '''
    for partnum, record in inventory.items():
        inventory[partnum] = record._replace(price=newprices[partnum], timestamp=time.now())
    '''
    
    print(p._fields) #查看字段名
    Color = namedtuple('Color', 'red green blue')
    Pixel = namedtuple('Pixel', Point._fields +('z',)+ Color._fields)
    print(Pixel(11, 22, 33, 128, 255, 0)) #Pixel(x=11, y=22, red=128, green=255, blue=0)
    
    #03:定义Point_class类
    for p in Point_class(3,4),Point_class(14,5/7):
        print(p)
    
    #04:默认值可以通过使用_replace()自定义原型实例来实现
    Account = namedtuple('Account', 'owner balance transaction_count')
    default_account = Account('<owner name>', 0.0, 0)
    print(default_account)
    johns_account = default_account._replace(owner='John')
    print(johns_account)
    
    #05:枚举常量可以用named tuple命名元组实现，但使用简单的类声明更简单、有效
    Status = namedtuple('Status', 'open pending closed')._make(range(3))
    print(Status.open, Status.pending, Status.closed)
    class Status:
        open,pending,closed=range(5,8)
    print(Status.open, Status.pending, Status.closed)
    
    '''D:OrderedDict objects
    有序字典
    当条目被删除时，新的排序字典保持它们的排序。但是，当添加新键时，键被附加到末尾。
    '''
    #无序字典
    d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    #有序字典，按键排序
    od=OrderedDict(sorted(d.items(), key=lambda t: t[0])) #对于二维或多维数据，排序时可以传入key参数自定义函数，其中t代表列表里的每一个元素
    print(od)
    
    #有序字典，按值排序
    od=OrderedDict(sorted(d.items(), key=lambda t: t[1]))
    print(od)
    
    #有序字典，按键字符串长度排序
    od=OrderedDict(sorted(d.items(), key=lambda t: len(t[0])))
    print(od)
    
    
    