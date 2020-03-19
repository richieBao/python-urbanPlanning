# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 23:02:18 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
reference:https://github.com/d2l-ai/d2l-zh  《动手学深度学习》(PyTorch版)
"""
import time,os,glob
import torch
from torch import nn, optim
import torch.nn.functional as F
import torchvision
import phmiData2rasterBunch as phmiBunch 
import sys
import numpy as np
from torchsummary import summary
sys.path.append("..") 
#import d2lzh_pytorch as d2l
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(torch.__version__)
print(torchvision.__version__)
print(device)

'''深度卷积网络 AlexNet Model'''
class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 64,11, 4), # in_channels, out_channels, kernel_size, stride, padding
            nn.ReLU(),
            nn.MaxPool2d(3, 2), # kernel_size, stride
            # 减小卷积窗口，使用填充为2来使得输入与输出的高和宽一致，且增大输出通道数
            nn.Conv2d(64, 192, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(3, 2),
            # 连续3个卷积层，且使用更小的卷积窗口。除了最后的卷积层外，进一步增大了输出通道数。
            # 前两个卷积层后不使用池化层来减小输入的高和宽
            nn.Conv2d(192, 384, 3, 1, 1),
            nn.ReLU(),
            nn.Conv2d(384, 256, 3, 1, 1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(3, 2)
        )
         # 这里全连接层的输出个数比LeNet中的大数倍。使用丢弃层来缓解过拟合
        self.fc = nn.Sequential(
            nn.Linear(256*2*2, 4096),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Dropout(0.5),
            # 输出层。输出类别根据训练数据输出类别确定
            nn.Linear(4096, 2),
        )

    def forward(self, img):
        feature = self.conv(img)
        output = self.fc(feature.view(img.shape[0], -1))
        return output 


'''网络中的网络 NiN Model'''
#定义展平层，子类，继承torch.nn.Module
class FlattenLayer(torch.nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()
    def forward(self, x): # x shape: (batch, *, *, ...)
        return x.view(x.shape[0], -1)

def nin_block(in_channels, out_channels, kernel_size, stride, padding):
    blk = nn.Sequential(nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
                        nn.ReLU(),
                        nn.Conv2d(out_channels, out_channels, kernel_size=1),
                        nn.ReLU(),
                        nn.Conv2d(out_channels, out_channels, kernel_size=1),
                        nn.ReLU())
    return blk


import torch.nn.functional as F
class GlobalAvgPool2d(nn.Module):
    # 全局平均池化层可通过将池化窗口形状设置成输入的高和宽实现
    def __init__(self):
        super(GlobalAvgPool2d, self).__init__()
    def forward(self, x):
        return F.avg_pool2d(x, kernel_size=x.size()[2:])

net_NiN = nn.Sequential(
    nin_block(1, 96, kernel_size=11, stride=4, padding=0),
    nn.MaxPool2d(kernel_size=3, stride=2),
    nin_block(96, 256, kernel_size=5, stride=1, padding=2),
    nn.MaxPool2d(kernel_size=3, stride=2),
    nin_block(256, 384, kernel_size=3, stride=1, padding=1),
    nn.MaxPool2d(kernel_size=3, stride=2), 
    nn.Dropout(0.5),
    # 标签类别数
    nin_block(384, 5, kernel_size=3, stride=1, padding=1),
    GlobalAvgPool2d(), 
    # 将四维的输出转成二维的输出，其形状为(批量大小, 标签类别数)
    FlattenLayer())


'''Net Cifar10'''
import torch.nn as nn
import torch.nn.functional as F
class Net_cifar10(nn.Module):
    def __init__(self):
        super(Net_cifar10, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 5)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

'''多层感知机 MLP'''
num_inputs, num_outputs, num_hiddens = 1024,2, 256
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
            else: # 自定义的模型, 3.13节之后不会用到, 不考虑GPU
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

    for epoch in range(re_epochs,num_epochs):
        train_iter=phmiBunch.data_iter(batch_size, features[:trainVStest], labels[:trainVStest])
        test_iter=phmiBunch.data_iter(batch_size, features[trainVStest:], labels[trainVStest:])

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
        if epoch %100==0:
        # if epoch %20==0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': net.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss':loss,
            }, os.path.join(PATH,'phmiAlexNet-epoch{}.pth'.format(epoch+1)))            
            # torch.save(save_checkpoint,os.path.join(PATH,'phmiAlexNet-epoch{}.pth'.format(epoch+1)))

'''计算结果，图像显示'''
from IPython import display
from matplotlib import pyplot as plt
def use_svg_display():
    """Use svg format to display plot in jupyter"""
    display.set_matplotlib_formats('svg')

def show_images(images, labels):
    use_svg_display()
    # 这里的_表示我们忽略（不使用）的变量
    _, figs = plt.subplots(1, len(images), figsize=(12, 12))
    for f, img, lbl in zip(figs, images, labels):
        f.imshow(img.view((32, 32)).numpy())
        f.set_title(lbl)
        f.axes.get_xaxis().set_visible(False)
        f.axes.get_yaxis().set_visible(False)
    # plt.show()
    
if __name__ == "__main__":    
    '''尝试用不同的模型训练'''
    # net=net_NiN.cuda()
    # print(net)
    # summary(net,(1,70,70))        
        
    net=MLP.cuda()
    summary(net,(1,32,32)) 
    
    # net=AlexNet().cuda()
    # summary(net,(1,100,100)) 
    
    # net=net_NiN .cuda()
    # summary(net,(1,68,68))
       
    # net = AlexNet().cuda()
    # net = NiN().cuda()
    # print(net)
    # model=net
    # summary(model,(1,30,30))
    
    # #如出现“out of memory”的报错信息，可减小batch_size或resize
        
    # batch_size=100
    #LandmarkMap
    LandmarkMap_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\LandmarkMap.fig"
    #PHmi
    PHMI_fn=r"F:\data_02_Chicago\data_driverless City\IIT_data\PHMI.fig"
    LandmarkMap_dic=phmiBunch.readMatLabFig_LandmarkMap(LandmarkMap_fn)    
    PHMI_dic=phmiBunch.readMatLabFig_PHMI(PHMI_fn,LandmarkMap_dic)
    
    locations=PHMI_dic[0]
    landmarks=LandmarkMap_dic[1]
    radius=20
    targetPts,locations_pts,targetPts_idx=phmiBunch.scanCircleBuffer(locations,landmarks,radius)
    Phmi=PHMI_dic[1][2]
    data=phmiBunch.colorMesh_phmi(landmarks,locations,targetPts_idx,Phmi)
    # features=torch.tensor(np.asarray([data[val]["zi"] for val in data.keys()]))
    featuresArray=np.asarray([data[0][val]['zi'] for val in data[0].keys()])
    fShape=featuresArray.shape
    features=torch.tensor(featuresArray.reshape(fShape[0],1,fShape[1],fShape[2]),dtype=torch.float)
    
    # labels=torch.tensor(phmiBunch.labelsPercentile(Phmi),dtype=torch.long)
    labels=torch.tensor(phmiBunch.labels2Values(Phmi),dtype=torch.long)
        
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
   
    #批量大小，用于读取小批量数据样本
    batch_size = 20 #20
    trainVStest=350 #1500
    # # iterTemp=phmiBunch.data_iter(batch_size, features[trainVStest:], labels[trainVStest:])
    # iterTemp=phmiBunch.data_iter(batch_size, features[:trainVStest], labels[:trainVStest])
    # # iterTemp=phmiBunch.data_iter(batch_size, features, labels)
    # i=0
    # for X,y in iterTemp:
    #     print(X.shape,y.shape) 
    #     print(i)
    #     i+=1

    
    PATH=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\phmiAlexNetChechpoints"
    lr, num_epochs = 0.001, 200 #学习率和迭代周期数
    optimizer = torch.optim.Adam(net.parameters(), lr=lr) #优化器选择，Adam算法
    train_epochs(net,batch_size, optimizer, device, num_epochs) #训练模型
    # train_ch5(net, train_iter, test_iter, batch_size, optimizer, device, num_epochs)
    PATHState=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\PhmiAlexNet_state.pt"
    torch.save(net.state_dict(), PATHState)
    PATHModel=r"C:\Users\richi\omen-richiebao\omen-code\Chicago_code\modelsSave\PhmiAlexNet_model.pt"
    torch.save(net, PATHModel)
    
    model = torch.load(PATHModel)   
    model.state_dict()
    
    # netStatesLoad=AlexNet()
    # netStatesLoad.load_state_dict(torch.load(PATHState))
    
    # optimizer.state_dict()
    
    #显示部分结果图像
    test_iter=phmiBunch.data_iter(batch_size, features[trainVStest:], labels[trainVStest:])
    # for X,y in test_iter:
    #     print(X,y)
    #     print(X.shape,y.shape)
    #     break
    
    X,y= next(test_iter)

    X=X.to(device)    
    # print(y)
    
    pred_labels = net(X).argmax(dim=1).cpu().detach().numpy()
    print(pred_labels )
    titles = ["True "+str(true) + '\n' + "pred"+str(pred) for true, pred in zip(y.numpy(), pred_labels)]    
    show_images(X[0:9].cpu(), titles[0:9])

    # torch.cuda.empty_cache() 