import pickle
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing

'''用极端随机森林训练图像分类器'''
class ERFTrainer(object):
    def __init__(self, X, label_words):
        self.le=preprocessing.LabelEncoder()
        self.clf=ExtraTreesClassifier(n_estimators=100,max_depth=16,random_state=0) #http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html
        y=self.encode_labels(label_words)
        self.clf.fit(np.asarray(X),y)
        with open('clf.pkl', 'wb') as f:  #存储训练好的图像分类器模型
            pickle.dump(self.clf, f)

    '''对标签编码，及训练分类器'''
    def encode_labels(self,label_words):
        self.le.fit(label_words)
        return np.array(self.le.transform(label_words),dtype=np.float64)

    '''对未知数据的预测分类'''
    def classify(self,X):
        label_nums=self.clf.predict(np.asarray(X))
        label_words=self.le.inverse_transform([int(x) for x in label_nums])
        return label_words

if __name__ == "__main__":
    with open(r'feature_map.pkl','rb') as f:  #读取存入的特征
        feature_map=pickle.load(f)
    # print(feature_map[0])
    label_words=[x['object_class'] for x in feature_map]
    # print(label_words)
    dim_size=feature_map[0]['feature_vector'].shape[1]
    # print(dim_size)
    X=[np.reshape(x['feature_vector'],(dim_size,)) for x in feature_map]
    # print(X[:2])
    erf=ERFTrainer(X,label_words)
    with open('erf.pkl','wb') as f: #存储类(含训练号的图像分类器模型)。在上传到服务器后，使用pickle方法存入类，会出现错误，因此未使用，而是直接存入图像分类器模型
        pickle.dump(erf,f)


'''
https://stackoverflow.com/questions/21033038/scikits-learn-randomforrest-trained-on-64bit-python-wont-open-on-32bit-python
32bit和64bit python训练Scikits-Learn RandomForrest trained on 64bit python wont open on 32bit python，会提示'ValueError: Buffer dtype mismatch, expected 'SIZE_t' but got 'long long''
目前暂无解决方法，如果本地上传到服务器，则直接在服务器中运行模型，获取训练模型的文件。
'''