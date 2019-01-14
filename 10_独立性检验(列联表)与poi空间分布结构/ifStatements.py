# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:12:15 2017

@author: richieBao-caDesign设计(cadesign.cn)
"""
poiNameClassify={
        "美食 ":"delicacy",
        "酒店 ":"hotel",
        "购物 ":"shopping",
        "生活服务":"lifeService",
        "丽人 ":"beauty",
        "旅游景点":"spot",
        "休闲娱乐":"entertainment",
        "运动健身":"sports",
        "教育培训":"education",
        "文化传媒":"media",
        "医疗 ":"medicalTreatment",
        "汽车服务":"carService",
        "交通设施":"trafficFacilities",
        "金融":"finance",
        "房地产":"realEstate",
        "公司企业":"corporation",
        "政府机构":"government"
        }
count=0
for idx,(name,nameID) in enumerate(poiNameClassify.items()):
    if name.strip()=='美食':
        print(idx,nameID)
    elif name.strip()=='金融':
        print(idx,nameID)
    elif name.strip()=='运动健身':
        print(idx,nameID)
    elif not name.strip()=='文化传媒':
        count+=1    
    else:
        pass
print("count=%s"%count)    
if "购物" in [v.strip() for v in poiNameClassify.keys()]:
    print("True")
else:
    print("False")

