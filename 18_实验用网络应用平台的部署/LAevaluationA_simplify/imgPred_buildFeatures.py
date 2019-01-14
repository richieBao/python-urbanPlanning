import numpy as np
import pandas as pd
import sqlite3
import pickle
import cv2
from sklearn.cluster import KMeans

flatten_lam=lambda lst:[m for n_lst in lst for m in flatten_lam(n_lst)] if type(lst) is list else [lst] #展平列表的lambda函数

'''定义类，用于处理Star特征检测相关函数'''
class StarFeatureDetector(object):
    def __init__(self):
        self.detector = cv2.xfeatures2d.StarDetector_create()
    def detect(self,img):
        return self.detector.detect(img)  #对输入图像运行检测器

'''提取网页图像打分存储到服务器SQLite数据库中的数据'''
def getImgPath():
    connPred = sqlite3.connect('local_data.db')  # 连接数据库
    sql = "select * from imageseval"
    data = pd.read_sql(sql=sql, con=connPred)  #根据pandas读取SQLite数据库参数要求配置参数
    # print(data[:5])
    return data

'''根据图像打分评价标志'好'，'中'和'差'分离数据，提取对应的图像路径'''
def load_training_data(imgPD):
    training_data=[]
    # print(input_folder)
    goodPD=imgPD[imgPD['eval']=='好'] #先判断获取bool值mask后提取数据
    mediumPD = imgPD[imgPD['eval'] == '中']
    poorPD = imgPD[imgPD['eval'] == '差']
    training_data.append([{'object_class':'good','image_path':i} for i in goodPD['imagename'].tolist()]) #根据评价类标提取对应的图像路径名
    training_data.append([{'object_class': 'moderate', 'image_path': i} for i in mediumPD['imagename'].tolist()])
    training_data.append([{'object_class': 'poor', 'image_path': i} for i in poorPD['imagename'].tolist()])
    training_dataFlat=flatten_lam(training_data)
    # print(training_dataFlat[:5])
    return training_dataFlat

'''调整图像大小，因已经处理过图像大小，此处定义函数未使用。一般直接使用misc.imresize()方法调整图像大小更加简便'''
def resize_image(input_img, new_size):
    h, w = input_img.shape[:2]
    scaling_factor = new_size / float(h)
    if w < h:
        scaling_factor = new_size / float(w)
    new_shape = (int(w * scaling_factor), int(h * scaling_factor))
    return cv2.resize(input_img, new_shape) #使用cv2.resize()方法调整图像大小

'''提取SIFT特征'''
def compute_sift_features(img,keypoints):
    if img is None:
        raise TypeError('Invalid input image')
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #将图像转为灰度
    keypoints,descriptors=cv2.xfeatures2d.SIFT_create().compute(img_gray,keypoints) #SIFT特征提取器提取特征
    return keypoints,descriptors

'''定义类处理词袋模型和向量量化'''
class BagOfWords(object):
    def __init__(self,num_clusters=32):
        self.num_dims=128
        self.num_clusters=num_clusters #KMeans聚类参数：定义聚类数量，关于聚类可以参考之前实验“机器学习-聚类”部分
        self.num_retries=10 #KMeans聚类参数：Number of time the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia.

    '''KMeans聚类'''
    def cluster(self,datapoints):
        kmeans=KMeans(self.num_clusters,n_init=max(self.num_retries,1),max_iter=10,tol=1.0)
        res=kmeans.fit(datapoints)
        centroids=res.cluster_centers_
        print(centroids.shape)
        return kmeans,centroids #返回KMeans聚类模型，以及聚类中心点

    '''归一化数据。其它方法可以参考之前相关实验处理技术'''
    def normalize(self,input_data):
        sum_input=np.sum(input_data)
        if sum_input>0:
            return input_data/sum_input #单一数值/总体数值之和，最终数值范围[0,1]
        else:
            return input_data

    '''提取SIFT特征'''
    def construct_feature(self,img,kmeans,centroid):
        keypoints=StarFeatureDetector().detect(img) #应用处理Star特征检测相关函数，返回检测出的特征关键点
        keypoints,feature_vectors=compute_sift_features(img,keypoints) #应用SIFT提取特征描述信息
        labels=kmeans.predict(feature_vectors) #对特征执行聚类预测类标
        # print(labels)
        feature_vector=np.zeros(self.num_clusters)

        for i,item in enumerate(feature_vectors): #计算特征聚类出现的频数/直方图
            # print(i,labels[i])
            feature_vector[labels[i]]+=1
        # print(feature_vector)
        feature_vector_img=np.reshape(feature_vector,((1,feature_vector.shape[0])))
        return self.normalize(feature_vector_img)

'''图像特征提取'''
class FeatureBuilder(object):
    '''计算图像特征，返回关键点及特征向量'''
    def extract_features(self,img):
        keypoints=StarFeatureDetector().detect(img)
        # print(len(keypoints),keypoints[:5])
        keypoints,feature_vectors=compute_sift_features(img,keypoints)
        # print(len(keypoints),keypoints[:5])
        # print(len(feature_vectors),[len(i) for i in feature_vectors[:5]],feature_vectors[0])
        return feature_vectors

    '''提取指定采样图像数量的图像特征，此时图像评价指标有3类'good','moderate'和'poor'。'''
    def get_codewords(self,input_map,scaling_size,max_samples=200): #max_samples为采样数量，例如键为'good','moderate','poor'的分别各自取12个图像，当程序调试正确后，调大该值
        keypoints_all=[]
        count=0
        cur_class=''
        for item in input_map:
            if count>=max_samples:
                if cur_class != item['object_class']:
                    count=0
                else:
                    continue
            count+=1

            if count==max_samples:
                print("Build centroid for",item['object_class'])

            cur_class=item['object_class']
            img=cv2.imread(item['image_path'])

            num_dims=128
            feature_vectors=self.extract_features(img)
            keypoints_all.extend(feature_vectors) #提取每一图像特征，并追加在列表中
        # print(len(keypoints_all),keypoints_all[0])
        kmeans,centroids=BagOfWords().cluster(keypoints_all)  #聚类特征
        # print(kmeans,centroids.shape,centroids)
        return kmeans,centroids


def get_feature_map(input_map,kmeans,centroids,scaling_size):
    feature_map=[]
    for item in input_map:
        temp_dict={}
        temp_dict['object_class']=item['object_class']
        print("Extracting feature for",item['image_path'])
        img=cv2.imread(item['image_path'])
        # img=resize_image(img,scaling_size)

        temp_dict['feature_vector']=BagOfWords().construct_feature(img,kmeans,centroids)
        if temp_dict['feature_vector'] is not None:
            feature_map.append(temp_dict)
    print(feature_map[0]['feature_vector'].shape,feature_map[0])
    return feature_map

if __name__ == "__main__":
    resizeImgData=getImgPath()
    training_data=load_training_data(resizeImgData)
    scaling_size=100
    kmeans,centroids=FeatureBuilder().get_codewords(training_data,scaling_size)

    with open('featK.pkl','wb') as f1: # 使用with结构避免手动的文件关闭操作
       pickle.dump((kmeans,centroids),f1) #存储kmeans模型，以及聚类中心点

    feature_map=get_feature_map(training_data,kmeans,centroids,scaling_size)
    with open('feature_map.pkl','wb') as f2:
        pickle.dump(feature_map,f2) #存储特征


'''
关于opencv-python，不要用pip install opencv-python自动安装，需要自行从https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
下载对应版本，本pycharm对应的opencv为opencv_python-3.4.0+contrib-cp36-cp36m-win32.whl，下载后放置于\venv\Lib\site-packages目录下
，在使用pip install venv\Lib\site-packages\opencv_python-3.4.0+contrib-cp36-cp36m-win32.whl本地安装，即可解决ImportError:DLL load failed:找不到指定模块等问题。
注：需下载+contrib版本，其中包含要使用的一些模块，例如cv2.xfeatures2d.StarDetector_create()。
linux python2.7 需安装opencv_contrib_python-3.4.0.12-cp27-cp27mu-manylinux1_x86_64.whl

如果从x86_64 + ubuntu14.04 + python3.6中import cv2(opencv3.3), 遇到以下错误：
[plain] view plain copy
ImportError: libSM.so.6: cannot open shared object file: No such file or directory  
ImportError: libXrender.so.1: cannot open shared object file: No such file or directory  
ImportError: libXext.so.6: cannot open shared object file: No such file or directory  
安装对应的软件包解决：
[plain] view plain copy
apt-get install libsm6  
apt-get install libxrender1  
apt-get install libxext-dev 

关于python3与2中的pickle
You should write the pickled data with a lower protocol number in Python 3. Python 3 introduced a new protocol with the number 3 (and uses it as default), so switch back to a value of 2 which can be read by Python 2.
Check the protocolparameter in pickle.dump. Your resulting code will look like this.
pickle.dump(your_object, your_file, protocol=2)
There is no protocolparameter in pickle.load because pickle can determine the protocol from the file.

机器学习部分code ref:<Python Machine Learning Cookbook>
'''