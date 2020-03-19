# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 10:14:25 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
reference:https://github.com/d2l-ai/d2l-zh  《动手学深度学习》(PyTorch版)
"""
import toOnehotEncoder as ohe
import phmiData2rasterBunch as phmiBunch 

import torch
import time,os,glob
from torch import nn, optim
import torch.nn.functional as F
import torchvision
import sys
import numpy as np
from torchsummary import summary
sys.path.append("..") 
#import d2lzh_pytorch as d2l
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(torch.__version__)
print(torchvision.__version__)
print(device)

#定义展平层，子类，继承torch.nn.Module
class FlattenLayer(torch.nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()
    def forward(self, x): # x shape: (batch, *, *, ...)
        return x.view(x.shape[0], -1)

'''MLP，torch.nn.Module 多层感知机'''
num_inputs, num_outputs, num_hiddens = 2601, 2, 256
MLP = nn.Sequential(
        FlattenLayer(),
        nn.Linear(num_inputs, num_hiddens),
        nn.ReLU(),
        nn.Linear(num_hiddens, num_outputs), 
        )   

#计算准确率，支持GPU
def evaluate_accuracy(data_iter, net, device=None):
    if device is None and isinstance(net, torch.nn.Module):
        # 如果没指定device就使用net的device
        device = list(net.parameters())[0].device 
    acc_sum, n = 0.0, 0
    with torch.no_grad():
        for X, y in data_iter:
            # print(X.shape)
            if isinstance(net, torch.nn.Module):
                net.eval() # 评估模式, 这会关闭dropout
                acc_sum += (net(X.to(device)).argmax(dim=1) == y.to(device)).float().sum().cpu().item()
                net.train() # 改回训练模式
            else: # 自定义的模型
                if('is_training' in net.__code__.co_varnames): # 如果有is_training这个参数
                    # 将is_training设置成False
                    acc_sum += (net(X, is_training=False).argmax(dim=1) == y).float().sum().item() 
                else:
                    acc_sum += (net(X).argmax(dim=1) == y).float().sum().item() 
            # print("+"*50)
            # print(y.shape)
            n += y.shape[0]
            # print(n)
    # print("+"*50)
    # print(n)
    # print(acc_sum)
    returnValue=acc_sum / n
    return returnValue

#训练模型，含模型保存及断点重启，避免因为特殊原因中断计算后重新计算，而是从断点开始继续计算
def train_epochs(net, batch_size, optimizer, device, num_epochs):
    net = net.to(device)
    
    print("training on ", device)
    loss = torch.nn.CrossEntropyLoss()
    re_epochs=0
    #断点重启
    if os.path.exists(PATH):
        list_of_files = glob.glob(PATH+"/*")
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            checkpoint = torch.load(latest_file)
            net.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            epoch = checkpoint['epoch']
            loss = checkpoint['loss']        
            re_epochs=epoch    

    #迭代训练。超参数：num_epochs迭代周期数，lr学习率
    for epoch in range(re_epochs,num_epochs):
        #迭代读取训练数据
        train_iter=ohe.data_iter(batch_size, features[:trainVStest], labels[:trainVStest])
        test_iter=ohe.data_iter(batch_size, features[trainVStest:], labels[trainVStest:])
        
        # print("epoch----------------",epoch)
        train_l_sum, train_acc_sum, n, batch_count, start = 0.0, 0.0, 0, 0, time.time()
        for X, y in train_iter:
            # print("_"*50)
            # print(epoch)
            # print(X.shape,y.shape)
            X = X.to(device)
            y = y.to(device)
            y_hat = net(X)
            # print("+"*50)
            # print(y_hat)
            l = loss(y_hat, y)
            optimizer.zero_grad()
            l.backward()
            optimizer.step()
            train_l_sum += l.cpu().item()
            train_acc_sum += (y_hat.argmax(dim=1) == y).sum().cpu().item()
            n += y.shape[0]
            batch_count += 1

        test_acc = evaluate_accuracy(test_iter, net)
        print('epoch %d, loss %.4f, train acc %.3f, test acc %.3f, time %.1f sec'
              % (epoch + 1, train_l_sum / batch_count, train_acc_sum / n, test_acc, time.time() - start))
        #保持模型
        if epoch %100==0:
        # if epoch %20==0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': net.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss':loss,
            }, os.path.join(PATH,'phmiAlexNet-epoch{}.pth'.format(epoch+1)))    
            # torch.save(save_checkpoint,os.path.join(PATH,'phmiAlexNet-epoch{}.pth'.format(epoch+1)))
            
'''图像显示-迁移-未调整'''
from IPython import display
from matplotlib import pyplot as plt
def use_svg_display():
    """Use svg format to display plot in jupyter"""
    display.set_matplotlib_formats('svg')
def get_fashion_mnist_labels(labels):
    text_labels = ['t-shirt', 'trouser', 'pullover', 'dress', 'coat',
                   'sandal', 'shirt', 'sneaker', 'bag', 'ankle boot']
    return [text_labels[int(i)] for i in labels]

#图像批量显示
def show_preImages(images, labels):
    use_svg_display()
    # 这里的_表示我们忽略（不使用）的变量
    import math
    width=int(round(math.sqrt(len(images)),2))
    fig, axs = plt.subplots(width, width, figsize=(10, 10),constrained_layout=True)
    for ax, img, lbl in zip(axs.flat, images, labels):
        centerIdx=kk=[math.floor(round(i/2)) for i in img.shape]
        # img[centerIdx[0],centerIdx[1]]=0.5

        scat = ax.scatter(centerIdx[0],centerIdx[1], c="r", s=30)
        # print(img,img.shape)
        ax.imshow(img.view((51, 51)).numpy())
        ax.set_title(lbl)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
    plt.show()


if __name__ == "__main__":
    featureDicFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmiFeature.pkl"
    phmi_labelFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\phmi_label.pkl"
    ptsVectorsFn=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\data\ptsVectors.pkl"
    featureBool,targetVal=ohe.featureBoolDic(featureDicFn,phmi_labelFn,ptsVectorsFn)
    # featureBoolArray=np.array([featureBool[key]["featureBool"].astype(int) for key in featureBool.keys()])
    featureValueArray=np.array([featureBool[key]["featureDistance"].astype(int) for key in featureBool.keys()])

    features=torch.tensor(featureValueArray,dtype=torch.float) #特征值
    
    '''不同方式的分类连续数值用作输出类别'''
    # labels=torch.tensor(phmiBunch.labelsPercentile(targetVal),dtype=torch.long)
    # labels=torch.tensor(phmiBunch.labelsPercentile_extent(targetVal),dtype=torch.long)
    # labels=torch.tensor(phmiBunch.labelsPercentile_upgrade(targetVal),dtype=torch.long)
    labels=torch.tensor(phmiBunch.labels2Values(np.array(targetVal)),dtype=torch.long) #输出类别
    
    
    (unique, counts) = np.unique(labels, return_counts=True)
    print((unique, counts))
    
    
    #因为样本输出分类数量悬殊，为了避免影响，随机调整类别数量比例至均衡，因此样本量会大量减少，需要获取更多样本。remove some values 1, reduce the impact of it.
    labelBool=labels.numpy()==0
    randomBool=np.random.choice([True, False], size=len(labels), p=[0.1, 0.9])
    labelMask=np.logical_or(labelBool,randomBool,dtype=bool)
    
    features=features[labelMask]
    labels=labels[labelMask]
    
    (unique, counts) = np.unique(labels, return_counts=True)
    print((unique, counts))
    print("amount:",len(labels))
    
    
    print(np.unique(labels),"amount:",len(np.unique(labels)))
    
    (unique, counts) = np.unique(labels, return_counts=True)
    print((unique, counts))
    
    #实例化网络，可以尝试不同网络，比较计算过程变化及结果精度
    net=MLP.cuda()
    print(net)
    summary(net,(1,51,51))  #测试网络参数是否正确

    #批量大小，用于读取小批量数据样本
    batch_size = 20 #20  100
    trainVStest=350 #1500   1800 #根据小批量样本量，调整训练数据集和测试数据集的划分点
    
    
    PATH=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\phmiAlexNetChechpoints" #训练模型保存位置
    lr, num_epochs = 0.001,200 #学习率和迭代周期数
    optimizer = torch.optim.Adam(net.parameters(), lr=lr) #优化器选择，Adam算法
    train_epochs(net,batch_size, optimizer, device, num_epochs) #训练模型
    # train_ch5(net, train_iter, test_iter, batch_size, optimizer, device, num_epochs)
    PATHState=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\PhmiAlexNet_state.pt"
    torch.save(net.state_dict(), PATHState)
    PATHModel=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\PhmiAlexNet_model.pt"
    torch.save(net, PATHModel)
    
    model = torch.load(PATHModel)   
    model.state_dict()
    
    
    #显示部分结果图像
    test_iter=ohe.data_iter(batch_size, features[trainVStest:], labels[trainVStest:])
    X,y= next(test_iter)

    X=X.to(device)    
    pred_labels = model(X).argmax(dim=1).cpu().detach().numpy()
    # print(pred_labels )
    titles = ["True "+str(true) + '\n' + "pred"+str(pred) for true, pred in zip(y.numpy(), pred_labels)]    
    show_preImages(X[10:30].cpu(), titles[10:30])    
    