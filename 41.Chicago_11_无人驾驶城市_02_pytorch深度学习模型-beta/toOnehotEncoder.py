# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:45:27 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
"""
import numpy as np
import torch,pickle
import pandas as pd

def featureBoolDic(featureDicFn,phmi_labelFn,ptsVectorsFn):
    with open(featureDicFn, 'rb') as handle:
        b = pickle.load(handle)    
    
    '''展平列表函数'''
    flatten_lst=lambda lst: [m for n_lst in lst for m in flatten_lst(n_lst)] if type(lst) is list else [lst]
    
    labelsKey={}
    for key in b.keys():
        labelsKey[key]=flatten_lst(b[key]["label"])
    
    with open(phmi_labelFn, 'rb') as handle:
        phmi_label=pickle.load(handle)    
        
    labelsKeyDf=pd.DataFrame(data=phmi_label)    
    # labelsKeyDummies=pd.get_dummies(labelsKeyDf)
    
    # print(labelsKey)
    
    with open(ptsVectorsFn, 'rb') as handle:
        ptsVectors=pickle.load(handle)

    
    featureDic={}
    for key in labelsKey.keys():
        boolArray=np.isin(phmi_label,labelsKey[key])
        fearureMinusValue=np.full(boolArray.shape,0)
        # print(fearureMinusValue)
        fearureMinusValue[boolArray]=labelsKey[key]
        
        fearureDisArray=np.full(boolArray.shape,-1)
        fearureDisArray[boolArray]=ptsVectors[key]["distance"]
        
        # print(fearureMinusValue)
        featureDic[key]={"featureBool":boolArray,
                          "featureValue":fearureMinusValue,
                          "featureDistance":fearureDisArray
                          }
        
        # if key==0:
        #     break
    
    
    return featureDic,[b[key]["Phmi"] for key in b.keys()]


def data_iter(batch_size, features, labels):
    import random
    num_examples = len(features)
    indices = list(range(num_examples))
    random.shuffle(indices)  # 样本的读取顺序是随机的
    for i in range(0, num_examples, batch_size):
        j = torch.LongTensor(indices[i: min(i + batch_size, num_examples)]) # 最后一次可能不足一个batch
        yield  features.index_select(0, j), labels.index_select(0, j)

if __name__ == "__main__":
    pass
    featureDicFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmiFeature.pkl"
    phmi_labelFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmi_label.pkl"
    ptsVectorsFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\ptsVectors.pkl"
    featureDic,targetVal=featureBoolDic(featureDicFn,phmi_labelFn,ptsVectorsFn)
    
    
    
    featureBoolArray=np.array([featureDic[key]["featureBool"].astype(int) for key in featureDic.keys()])
    featureValueArray=np.array([featureDic[key]["featureValue"].astype(int) for key in featureDic.keys()])
    
    features=torch.tensor(featureValueArray)
    labels=torch.tensor(targetVal)
            
    
    
    
    # batch_size=100
    # data_iter(batch_size, features, labels)
    # for X, y in data_iter(batch_size, features, labels):
    #     print(X.shape, y.shape)
    #     break
    
    

   
