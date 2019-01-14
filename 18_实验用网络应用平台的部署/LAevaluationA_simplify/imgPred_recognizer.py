import cv2
import os
import pickle
from imgPred_training import ERFTrainer
import imgPred_buildFeatures as bf
import random
import numpy as np
from sklearn import preprocessing

'''创建图像识别/分类器'''
class ImageTagExtractor(object):

    def __init__(self, model_file, featK):
        with open(model_file,'rb') as f1:  #读取存储的图像分类器模型
            self.clf=pickle.load(f1)

        with open(featK,'rb') as f2:  #读取存储的聚类模型和聚类中心点
            self.kmeans,self.centroids=pickle.load(f2)

        '''对标签编码'''
        with open(r'feature_map.pkl', 'rb') as f:
            self.feature_map = pickle.load(f)
        self.label_words = [x['object_class'] for x in self.feature_map]
        self.le = preprocessing.LabelEncoder()
        self.le.fit(self.label_words)

    def predict(self,img,scaling_size):
        img=bf.resize_image(img,scaling_size)
        feature_vector=bf.BagOfWords().construct_feature(img,self.kmeans,self.centroids)  #提取图像特征
        label_nums = self.clf.predict(np.asarray(feature_vector)) #进行图像识别/分类
        image_tag = self.le.inverse_transform([int(x) for x in label_nums])[0] #获取图像分类标签
        print(label_nums,image_tag)
        return image_tag

'''以文件夹名为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
def filePath(dirpath,fileType):
    fileInfo={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               fileInfo.setdefault(dirpath,tempList)
    return fileInfo

'''配置参数。随机抽取用于识别/分类的图像，验证模型预测结果'''
class predConfig(object):
    def __init__(self):
        self.model_file=r'clf.pkl'
        self.featK=r'featK.pkl'
        self.imgPred = r'static/images/imgpred'
        self.fileType = ["jpg", "JPG"]
        self.selectNum=3
        self.scaling_size = 200

    def pred(self):
        fileInfo=filePath(self.imgPred, self.fileType)
        imgFNList = [key+r'/'+fn for key in fileInfo.keys() for fn in fileInfo[key]]
        rndImg=random.sample(imgFNList ,random.randint(self.selectNum,len(imgFNList )))
        predInfo={fn:ImageTagExtractor(self.model_file,self.featK).predict(cv2.imread(fn),self.scaling_size) for fn in rndImg}

        return predInfo

if __name__=='__main__':
    predInfo=predConfig().pred()
    print(predInfo)

