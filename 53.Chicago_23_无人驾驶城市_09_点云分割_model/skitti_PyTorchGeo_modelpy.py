# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:07:27 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
ref: PyTorch Geometric Example
"""
import os.path as osp
import numpy as np

import torch
import torch.nn.functional as F
from torch.nn import Sequential as Seq, Linear as Lin, ReLU, BatchNorm1d as BN
from torch_geometric.datasets import ModelNet
import torch_geometric.transforms as T
from torch_geometric.data import DataLoader
from torch_geometric.nn import PointConv, fps, radius, global_max_pool

from torch_geometric.nn import knn_interpolate
from torch_geometric.utils import intersection_and_union as i_and_u
from torch.utils import data

class SAModule(torch.nn.Module):
    def __init__(self, ratio, r, nn):
        super(SAModule, self).__init__()
        self.ratio = ratio
        self.r = r
        self.conv = PointConv(nn)

    def forward(self, x, pos, batch):
        idx = fps(pos, batch, ratio=self.ratio)
        row, col = radius(pos, pos[idx], self.r, batch, batch[idx],
                          max_num_neighbors=64)
        edge_index = torch.stack([col, row], dim=0)
        # print(pos[idx])
        x = self.conv(x, (pos, pos[idx]), edge_index)
        pos, batch = pos[idx], batch[idx]
        return x, pos, batch


class GlobalSAModule(torch.nn.Module):
    def __init__(self, nn):
        super(GlobalSAModule, self).__init__()
        self.nn = nn

    def forward(self, x, pos, batch):
        x = self.nn(torch.cat([x, pos], dim=1))
        x = global_max_pool(x, batch)
        pos = pos.new_zeros((x.size(0), 3))
        batch = torch.arange(x.size(0), device=batch.device)
        return x, pos, batch


def MLP(channels, batch_norm=True):
    return Seq(*[
        Seq(Lin(channels[i - 1], channels[i]), ReLU(), BN(channels[i]))
        for i in range(1, len(channels))
    ])


class FPModule(torch.nn.Module):
    def __init__(self, k, nn):
        super(FPModule, self).__init__()
        self.k = k
        self.nn = nn

    def forward(self, x, pos, batch, x_skip, pos_skip, batch_skip):
        x = knn_interpolate(x, pos, pos_skip, batch, batch_skip, k=self.k)
        if x_skip is not None:
            x = torch.cat([x, x_skip], dim=1)
        x = self.nn(x)
        return x, pos_skip, batch_skip


class Net(torch.nn.Module):
    def __init__(self, num_classes):
        super(Net, self).__init__()
        self.sa1_module = SAModule(0.2, 0.2, MLP([3 + 3, 64, 64, 128]))
        self.sa2_module = SAModule(0.25, 0.4, MLP([128 + 3, 128, 128, 256]))
        self.sa3_module = GlobalSAModule(MLP([256 + 3, 256, 512, 1024]))

        self.fp3_module = FPModule(1, MLP([1024 + 256, 256, 256]))
        self.fp2_module = FPModule(3, MLP([256 + 128, 256, 128]))
        self.fp1_module = FPModule(3, MLP([128 + 3, 128, 128, 128]))

        self.lin1 = torch.nn.Linear(128, 128)
        self.lin2 = torch.nn.Linear(128, 128)
        self.lin3 = torch.nn.Linear(128, num_classes)

    def forward(self, data):
        sa0_out = (data.x, data.pos, data.batch)
        sa1_out = self.sa1_module(*sa0_out)
        sa2_out = self.sa2_module(*sa1_out)
        sa3_out = self.sa3_module(*sa2_out)

        fp3_out = self.fp3_module(*sa3_out, *sa2_out)
        fp2_out = self.fp2_module(*fp3_out, *sa1_out)
        x, _, _ = self.fp1_module(*fp2_out, *sa0_out)

        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin2(x)
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin3(x)
        return F.log_softmax(x, dim=-1)


class dataloader(data.Dataset):
    def __init__(self, data_path, imageset = 'train',split_ratio=[0.7,0.2,0.1]): # train, validate, test
        import random
        self.imageset = imageset        
        from pathlib import Path
        paths_=list(Path(data_path).glob('**/*.pt'))
        train, validate, test = np.split(paths_, [int(len(paths_)*split_ratio[0]), int(len(paths_)*sum(split_ratio[:2])),])
        if imageset=='train':
            random.shuffle(train)
            self.paths=train
        elif imageset == 'val':
            self.paths=validata
        elif imageset == 'test':
            random.shuffle(test)
            self.paths=test[:1]   #[:10]
        else:
            raise Exception('Split must be train/val/test')        
         
    def __len__(self):
        'Denotes the total number of samples'
        return len(self.paths)
    
    def __getitem__(self, index):
        raw_data =torch.load(self.paths[index])
        return raw_data

def train(model_path=''):
    import os
    # if os.path.exists(model_path):
        # print(model_path)
        # model=torch.load(model_path)    
        # model.eval()
    
    model.train()

    total_loss = correct_nodes = total_nodes = 0
    for i, data in enumerate(train_loader):
        data = data.to(device)
        optimizer.zero_grad()
        out = model(data)
        # print(out.shape)
        # print(data.y.shape)
        loss = F.nll_loss(out, data.y.reshape(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        correct_nodes += out.argmax(dim=1).eq(data.y).sum().item()
        total_nodes += data.num_nodes
        
        
        if (i + 1) % 50== 0:
            torch.save(model,model_save_path+f'skitti_PyTorchGeo_epoch_%s_Acc_{correct_nodes / total_nodes:.4f}.pth'%i)        

        if (i + 1) % 10 == 0:
            print(f'[{i+1}/{len(train_loader)}] Loss: {total_loss / 10:.4f} '
                  f'Train Acc: {correct_nodes / total_nodes:.4f}')
            total_loss = correct_nodes = total_nodes = 0    
            

            
            
            
            
            
@torch.no_grad()
def test(loader, model_path=''):
    import os
    if os.path.exists(model_path):
        # print(model_path)
        model=torch.load(model_path)    
    
    model.eval()
    # print("_"*50)
    j=0
    ious=[]
    for data in loader:
        data = data.to(device)
        pred = model(data).argmax(dim=1)
        print("_"*50)
        print(np.unique(pred.cpu().numpy()))
        print(np.unique(data.y.cpu().numpy()))
        
        # print("+"*50)
        i, u = i_and_u(pred, data.y, 34, data.batch)
        # print("/"*50)
        iou = i.cpu().to(torch.float) / u.cpu().to(torch.float)
        # print("#"*50)
        iou[torch.isnan(iou)] = 1
        
        # print(iou[0])
        print("_"*10,j)
        j+=1
        ious.append(iou[0])        
        
        # print(ious)
    # Compute mean IoU.
    ious = [torch.stack(iou).mean(0).mean(0) for iou in [ious]]
    # print("#"*50)
    # print(ious)
    return torch.tensor(ious).mean().item()
    # return torch.tensor(ious).mean().item() 

@torch.no_grad()
def test_o3dVisualization(loader, model_path=''):
    import pandas as pd
    if model_path:
        # print(model_path)
        model=torch.load(model_path)    
    else:
        print("need to give the mode path.")
    
    model.eval()
    # print("_"*50)
    j=0
    ious=[]
    print("#"*5,len(loader))
    for data in loader:
        print("_"*5,j)
        data = data.to(device)
        pred = model(data).argmax(dim=1)
        pred_=pred.cpu().numpy()
        # print(pred_.shape)
        # print(data.pos.shape)
        print(np.unique(pred_))
        print("/"*10)
        print(np.unique(data.y.cpu()))
        
        # unique_digitize=np.unique(pred_)
        # random_color_dict=[{k:np.random.randint(low=0,high=255,size=1)for k in unique_digitize} for i in range(3)]
        # print(random_color_dict)
        # data_color=[pd.DataFrame(pred_).replace(random_color_dict[i]).to_numpy() for i in range(3)]
        # print(data_color)
        # data_rgb=np.concatenate([np.expand_dims(i,axis=-1) for i in data_color],axis=-1)
        # print(data_rgb)
        
        classification_color={
                             0:(255,255,1), # "unlabeled", and others ignored
                             1:(246,30,30), # "car"
                             2:(246,30,239), # "bicycle"
                             3:(97,20,313), # "motorcycle"
                             4:(206,55,141),  # "truck"
                             5:(157,29,189), # "other-vehicle"
                             6:(38,103,201), # "person"
                             7:(38,146,201), # "bicyclist"
                             8:(58,168,185), # "motorcyclist"
                             9:(105,111,112), # "road"
                             10:(65,115,109), # "parking"
                             11:(129,134,133), # "sidewalk"
                             12:(71,74,74), # "other-ground"
                             13:(168,156,50), # "building"
                             14:(168,117,50), # "fence"
                             15:(50,168,113), # "vegetation"
                             16:(18,90,49), # "trunk"
                             17:(215,201,147), # "terrain"
                             18:(218,120,34), # "pole"
                             19:(218,64,34),  # "traffic-sign"
                                }
        
        color_dict=[{key:val[i]for key,val in classification_color.items()} for  i in range(3)]
        data_color=[pd.DataFrame(pred_).replace(color_dict[i]).to_numpy() for i in range(3)]
        data_rgb=np.concatenate([np.expand_dims(i,axis=-1) for i in data_color],axis=-1)
        # print(data_color)
        
                
        # print("#"*50) 
        # print(data_rgb.reshape(-1,3))
        # print(pred_)
        #o3d-visulization
        import open3d as o3d
        pcd=o3d.geometry.PointCloud()
        pcd.points=o3d.utility.Vector3dVector(data.pos.cpu().numpy())  
        
        pcd.colors=o3d.utility.Vector3dVector(data_rgb.reshape(-1,3)/255)    
        
        o3d.visualization.draw_geometries([pcd],point_show_normal=False)
        
        
        # o3d.io.write_point_cloud(r"E:\dataset\results\PyTorchGeo_poiNet_pcd_img\pcd\%s.pcd"%j, pcd)
        j+=1
        
            

if __name__ == '__main__':
    dataset_path="E:/dataset/results/graph_dataset_KITTI"
    train_loader=dataloader(data_path=dataset_path, imageset = 'train',split_ratio=[0.7,0.2,0.1])
    
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Net(num_classes=50).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    model_save_path=r'./model_save/'
    for epoch in range(1, 36): #31
        train(model_path=model_save_path)
    
    
        # iou = test(test_loader)
        # print('Epoch: {:02d}, Test IoU: {:.4f}'.format(epoch, iou))    
 


    #test
    test_loader=dataloader(data_path=dataset_path, imageset = 'test',split_ratio=[0.7,0.2,0.1])    #[0.7,0.2,0.1]
    model_path=r'C:\Users\richi\omen-richiebao\omen-code\Chicago_code\dcp_cloudPoints_processing\model_save\skitti_PyTorchGeo_1199.pth'
    # for epoch in range(1,2):
    #     iou = test(test_loader,model_path=model_path)
    #     print('Epoch: {:02d}, Test IoU: {:.4f}'.format(epoch, iou))


    #visualization
    
    # test_o3dVisualization(test_loader,model_path=model_path)

    
    '''    
    #temp
    for i, data in enumerate(train_loader):
        print(data)
        print(data.batch.type())
        print(data.pos.type())
        print(data.y.type())
        print(data.x.type())
        if i ==0:break   
        
        
    #     print(np.unique(data.y))
    #     # print(data.y.numpy())
    #     # print(data.category)
    #     # print(data.x.numpy())
    #     # print(i)
        
        
    #     import open3d as o3d
    #     pcd=o3d.geometry.PointCloud()
    #     pcd.points=o3d.utility.Vector3dVector(data.pos)       
    #     pcd.normals=o3d.utility.Vector3dVector(data.x.numpy())
        
    #     aa=data.y.numpy().astype(np.float)/19
    #     bb=aa.reshape(-1,1)
    #     cc=np.insert(bb, 1, 0, axis=1)
    #     dd=np.insert(cc, 2, 0, axis=1)
    #     pcd.colors=o3d.utility.Vector3dVector(dd)
    #     o3d.visualization.draw_geometries([pcd],point_show_normal=False)
        # print(data.num_nodes)
        
        if i ==0:break    
    '''