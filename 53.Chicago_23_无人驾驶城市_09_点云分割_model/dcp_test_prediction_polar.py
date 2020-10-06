# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 22:02:15 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
"""
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from torch.utils import data
import yaml,os
import argparse
import numba as nb
import torch
from matplotlib.colors import rgb2hex,hex2color
import matplotlib.pyplot as plt
from sklearn import preprocessing

import torch
from torch_geometric.data import Dataset,InMemoryDataset
from torch_geometric.data import Data



import os
import time
import argparse
import sys
import numpy as np
import torch
import torch.optim as optim
from tqdm import tqdm

# from network.BEV_Unet import BEV_Unet
# from network.ptBEV import ptBEVnet

from BEV_Unet import BEV_Unet
from ptBEV import ptBEVnet

from dataloader.dataset import collate_fn_BEV,collate_fn_BEV_test,SemKITTI,SemKITTI_label_name,spherical_dataset,voxel_dataset
#ignore weird np warning
import warnings
warnings.filterwarnings("ignore")

def fast_hist(pred, label, n):
    k = (label >= 0) & (label < n)
    bin_count=np.bincount(
        n * label[k].astype(int) + pred[k], minlength=n ** 2)
    return bin_count[:n ** 2].reshape(n, n)

def per_class_iu(hist):
    return np.diag(hist) / (hist.sum(1) + hist.sum(0) - np.diag(hist))

def fast_hist_crop(output, target, unique_label):
    hist = fast_hist(output.flatten(), target.flatten(), np.max(unique_label)+1)
    hist=hist[unique_label,:]
    hist=hist[:,unique_label]
    return hist

def SemKITTI2train(label):
    if isinstance(label, list):
        return [SemKITTI2train_single(a) for a in label]
    else:
        return SemKITTI2train_single(label)

def SemKITTI2train_single(label):
    return label - 1 # uint8 trick

def train2SemKITTI(input_label):
    # delete 0 label (uses uint8 trick : 0 - 1 = 255 )
    return input_label + 1

def main(args):
    test_batch_size = args.test_batch_size
    model_save_path = args.model_save_path
    output_path = args.test_output_path
    compression_model = args.grid_size[2]
    grid_size = args.grid_size
    pytorch_device = torch.device('cuda:0')
    model = args.model
    if model == 'polar':
        fea_dim = 8#9
        circular_padding = True
    elif model == 'traditional':
        fea_dim = 7
        circular_padding = False

    # prepare miou fun
    unique_label=np.asarray(sorted(list(SemKITTI_label_name.keys())))[1:] - 1
    unique_label_str=[SemKITTI_label_name[x] for x in unique_label+1]

    # prepare model
    my_BEV_model=BEV_Unet(n_class=len(unique_label), n_height = compression_model, input_batch_norm = True, dropout = 0.5, circular_padding = circular_padding)
    my_model = ptBEVnet(my_BEV_model, pt_model = 'pointnet', grid_size =  grid_size, fea_dim = fea_dim, max_pt_per_encode = 256,
                            out_pt_fea_dim = 512, kernal_size = 1, pt_selection = 'random', fea_compre = compression_model)
    if os.path.exists(model_save_path):
        my_model.load_state_dict(torch.load(model_save_path))
    my_model.to(pytorch_device)

        
    test_dataset_loader = polar_dataset_loader
    val_dataset_loader = polar_dataset_loader

    # validation
    print('*'*80)
    print('Test network performance on validation split')
    print('*'*80)
    pbar = tqdm(total=len(val_dataset_loader))
    my_model.eval()
    hist_list = []
    time_list = []
    
    
    '''
    with torch.no_grad():
        for i_iter_val,(_,val_vox_label,val_grid,val_pt_labs,val_pt_fea,_) in enumerate(val_dataset_loader):
            val_vox_label = SemKITTI2train(val_vox_label)
            val_pt_labs = SemKITTI2train(val_pt_labs)
            val_pt_fea_ten = [torch.from_numpy(i).type(torch.FloatTensor).to(pytorch_device) for i in val_pt_fea]
            val_grid_ten = [torch.from_numpy(i[:,:2]).to(pytorch_device) for i in val_grid]
            val_label_tensor=val_vox_label.type(torch.LongTensor).to(pytorch_device)

            torch.cuda.synchronize()
            start_time = time.time()
            predict_labels = my_model(val_pt_fea_ten, val_grid_ten)
            torch.cuda.synchronize()
            time_list.append(time.time()-start_time)

            predict_labels = torch.argmax(predict_labels,dim=1)
            predict_labels = predict_labels.cpu().detach().numpy()
            for count,i_val_grid in enumerate(val_grid):
                hist_list.append(fast_hist_crop(predict_labels[count,val_grid[count][:,0],val_grid[count][:,1],val_grid[count][:,2]],val_pt_labs[count],unique_label))
            pbar.update(1)
    iou = per_class_iu(sum(hist_list))
    print('Validation per class iou: ')
    for class_name, class_iou in zip(unique_label_str,iou):
        print('%s : %.2f%%' % (class_name, class_iou*100))
    val_miou = np.nanmean(iou) * 100
    del val_vox_label,val_grid,val_pt_fea,val_grid_ten
    pbar.close()
    print('Current val miou is %.3f ' % val_miou)
    print('Inference time per %d is %.4f seconds\n' %
        (test_batch_size,np.mean(time_list)))
    
    # test
    print('*'*80)
    print('Generate predictions for test split')
    print('*'*80)
'''
    
    

    pbar = tqdm(total=len(test_dataset_loader))
    with torch.no_grad():
        for i_iter_test,(_,_,test_grid,_,test_pt_fea,test_index,xyz) in enumerate(test_dataset_loader):
            
                        # print(i_iter_test)
            # print(test_grid,test_pt_fea,test_index)
            # print(len(test_grid),test_grid[0].shape,len(test_pt_fea),test_pt_fea[0].shape,len(test_index))
            # if i_iter_test==0: break
            
            
            
            # predict
            test_pt_fea_ten = [torch.from_numpy(i).type(torch.FloatTensor).to(pytorch_device) for i in test_pt_fea]
            test_grid_ten = [torch.from_numpy(i[:,:2]).to(pytorch_device) for i in test_grid]

            predict_labels = my_model(test_pt_fea_ten,test_grid_ten)
            predict_labels = torch.argmax(predict_labels,1).type(torch.uint8)
            predict_labels = predict_labels.cpu().detach().numpy()
            # write to label file
            for count,i_test_grid in enumerate(test_grid):
                test_pred_label = predict_labels[count,test_grid[count][:,0],test_grid[count][:,1],test_grid[count][:,2]]
                test_pred_label = train2SemKITTI(test_pred_label)
                test_pred_label = np.expand_dims(test_pred_label,axis=1)

                new_save_dir = output_path + '%s'%i_iter_test+'.label'
                if not os.path.exists(os.path.dirname(new_save_dir)):
                    try:
                        os.makedirs(os.path.dirname(new_save_dir))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                test_pred_label = test_pred_label.astype(np.uint32)
                test_pred_label.tofile(new_save_dir)
            pbar.update(1)
            
            print("/n")
            print("_"*50)
            print(xyz[0].shape)
            print( len(test_pred_label))      
            # print(np.array(test_pred_label).reshape(-1))
            label_classi=np.array(test_pred_label).reshape(-1)
            print(np.unique(label_classi))
            import open3d as o3d
            pcd=o3d.geometry.PointCloud()
            pcd.points=o3d.utility.Vector3dVector(xyz[0])   
            
            # aa=np.array(test_pred_label/18)
            # bb=aa.reshape(-1,1)
            # cc=np.insert(bb, 1, 0, axis=1)
            # dd=np.insert(cc, 2, 0, axis=1)     
            
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
            
            # print(pred_)
            import pandas as pd
            pred_=np.array(test_pred_label)
            color_dict=[{key:val[i]for key,val in classification_color.items()} for  i in range(3)]
            data_color=[pd.DataFrame(pred_).replace(color_dict[i]).to_numpy() for i in range(3)]
            data_rgb=np.concatenate([np.expand_dims(i,axis=-1) for i in data_color],axis=-1)            
            
            
            
            
            
            
            
            
            pcd.colors=o3d.utility.Vector3dVector(data_rgb.reshape(-1,3)/255)
            o3d.visualization.draw_geometries([pcd],point_show_normal=False)            
            
            
            
            if i_iter_test==3:break
            
    del test_grid,test_pt_fea,test_index
    pbar.close()
    print('Predicted test labels are saved in %s. Need to be shifted to original label format before submitting to the Competition website.' % output_path)
    print('Remapping script can be found in semantic-kitti-api.')







def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

'''A - could points preprocessing-All data locates in one folder.'''
class dcp_cpts(data.Dataset):
    def __init__(self,data_path,config_path,ref_feature=[],set_selection='set_a',return_ref=False):
        self.return_ref=return_ref
        with open(config_path,'r') as stream:
            self.dcp_configuration=yaml.safe_load(stream)
        self.data_set=self.dcp_configuration['set']
        self.set_selection=set_selection
        if set_selection=='set_a':
            split=self.data_set['set_a']
        elif set_selection=='set_b':
            split=self.data_set['set_b']
        else:
            raise Exception('Split must be set_a/set_b')
        self.pts_idx=list(absoluteFilePaths(data_path))[split[0]:split[1]]
        
        import random
        random.shuffle(self.pts_idx)
        
        self.ref_feature_list=self.dcp_configuration['pts_process']
        # print(self.ref_feature_list)
        self.ref_feature=ref_feature
        
        
    def __len__(self):
        '''Denotes the total number of samples'''
        return len(self.pts_idx)
    
    def __getitem__(self,index):        
        # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Info) #o3d.utility.VerbosityLevel.Debug/Warning/Error
        
        raw_data=o3d.io.read_point_cloud(self.pts_idx[index])
        pts_array=np.asarray(raw_data.points)
        if self.return_ref:
            ref_handle=pts_utility(raw_data,) 
            data_dic={'o3d_object':None,"pts_array":None,"normal":None,"cluster":None}
            for f in self.ref_feature:
                if f in self.ref_feature_list and f=='remove_byRadius':                    
                    #clean the outlier    
                    remove_radius=self.dcp_configuration['remove_byRadius']['radius']
                    remove_center_coordi=self.dcp_configuration['remove_byRadius']['center_coordi']
                    ref_handle.remove_byRadius(radius=remove_radius,center_coordi=remove_center_coordi)  
                    
                                     
                elif f in self.ref_feature_list and f=='vertex_normal_estimation': 
                    #estimate normals
                    normal_radius=self.dcp_configuration['vertex_normal_estimation']['radius']
                    normal_max_nn=self.dcp_configuration['vertex_normal_estimation']['max_nn']
                    ref_handle.vertex_normal_estimation(radius=normal_radius, max_nn=normal_max_nn)
                    # print(np.asarray(ref_handle.cloudPts.normals))

                    
                elif f in self.ref_feature_list and f=='cluster_dbscan':     
                    #cluster_dbscan
                    dbscan_eps=self.dcp_configuration['cluster_dbscan']['eps']
                    dbscan_min_points=self.dcp_configuration['cluster_dbscan']['min_points']
                    ref_handle.cluster_dbscan(eps=dbscan_eps,min_points=dbscan_min_points,)
                    
                    
                elif f in self.ref_feature_list and f=='vertex_downsample':  
                    #voxel downsample
                    down_voxel_size=self.dcp_configuration['vertex_downsample']['voxel_size']
                    ref_handle.voxel_down_sample(voxel_size=down_voxel_size)
            
            # o3d.visualization.draw_geometries([ref_handle.cloudPts],point_show_normal=True) #point_show_normal=True
            data_dic.update({'o3d_object':ref_handle.cloudPts,"pts_array":np.asarray(ref_handle.cloudPts.points)})
            if ref_handle.cloudPts.has_normals():
                data_dic.update({"normal":np.asarray(ref_handle.cloudPts.normals)})
            if  ref_handle.cloudPts.has_colors():
                data_dic.update({"cluster":np.asarray(ref_handle.cloudPts.colors)})
          
            data_tuple=tuple(v for v in data_dic.values())
       
        else:
            data_tuple=(raw_data,pts_array)
        # o3d.visualization.draw_geometries([data_tuple[0]])
        return data_tuple     

'''B - open3d-utility'''
class pts_utility:
    def __init__(self,cloudPts):     
        self.cloudPts=cloudPts        


    def update(self,value):
        self.cloudPts=value

    #remove data with radius
    def remove_byRadius(self,radius,center_coordi=[0,0,0]):    
        center_pt=o3d.geometry.PointCloud()
        center_pt.points=o3d.utility.Vector3dVector(np.array([center_coordi]))    
        c_distance=self.cloudPts.compute_point_cloud_distance(center_pt)
        c_d_mask=np.array(c_distance)<radius
        # print(np.asarray(self.cloudPts.points).shape)
        self.cloudPts.points=o3d.utility.Vector3dVector(np.asarray(self.cloudPts.points)[c_d_mask])
        # print(np.asarray(self.cloudPts.points).shape)
        # o3d.visualization.draw_geometries([self.cloudPts])
        # return self.cloudPts
        # self.updata(self.cloudPts)

    #remove_radius_outlier(...) 
    #remove_statistical_outlier(...)
            
    #cluster_dbscan(...)
    def cluster_dbscan(self,eps=1,min_points=10):
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            labels=np.array(self.cloudPts.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))
        max_label=labels.max()                      
        print(f"point cloud has {max_label + 1} clusters")                      
        colors=plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0]=0
        self.cloudPts.colors = o3d.utility.Vector3dVector(colors[:, :3])
        # o3d.visualization.draw_geometries([self.cloudPts])
        return self.cloudPts
        
    #compute_mahalanobis_distance(...)
    #compute_nearest_neighbor_distance(...)   
    #compute_point_cloud_distance(...)  
    
    #estimate_normals(...)/normalize_normals(...)
    def vertex_normal_estimation(self,radius=1, max_nn=30):
        self.cloudPts.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=max_nn))
        # o3d.visualization.draw_geometries([self.cloudPts],point_show_normal=True)
        return self.cloudPts
        
        
    #voxel_down_sample(...)/voxel_down_sample_and_trace(...)
    def voxel_down_sample(self,voxel_size=0.05):
        cloudPts_downSample=self.cloudPts.voxel_down_sample(voxel_size=voxel_size)
        self.update(cloudPts_downSample)
        # o3d.visualization.draw_geometries([cloudPts_downSample])
        return cloudPts_downSample

    #rotate(...)    
    #scale(...)    
    #transform(...)    
    #translate(...)

'''E-polar dataset'''
# transformation between Cartesian coordinates and polar coordinates
def cart2polar(input_xyz):
    rho = np.sqrt(input_xyz[:,0]**2 + input_xyz[:,1]**2)
    phi = np.arctan2(input_xyz[:,1],input_xyz[:,0])
    return np.stack((rho,phi,input_xyz[:,2]),axis=1)

def polar2cat(input_xyz_polar):
    x = input_xyz_polar[0]*np.cos(input_xyz_polar[1])
    y = input_xyz_polar[0]*np.sin(input_xyz_polar[1])
    return np.stack((x,y,input_xyz_polar[2]),axis=0)

#@nb.jit('u1[:,:,:](u1[:,:,:],i8[:,:])',nopython=True,cache=True,parallel = False)
# @nb.jit(nopython=True,cache=True,parallel =False)
def nb_process_label(processed_label,sorted_label_voxel_pair):
    label_size = 256
    counter = np.zeros((label_size,),dtype = np.uint16)
    counter[sorted_label_voxel_pair[0,3]] = 1
    cur_sear_ind = sorted_label_voxel_pair[0,:3]
    for i in range(1,sorted_label_voxel_pair.shape[0]):
        cur_ind = sorted_label_voxel_pair[i,:3]
        if not np.all(np.equal(cur_ind,cur_sear_ind)):
            processed_label[cur_sear_ind[0],cur_sear_ind[1],cur_sear_ind[2]] = np.argmax(counter)
            counter = np.zeros((label_size,),dtype = np.uint16)
            cur_sear_ind = cur_ind
        counter[sorted_label_voxel_pair[i,3]] += 1
    processed_label[cur_sear_ind[0],cur_sear_ind[1],cur_sear_ind[2]] = np.argmax(counter)
    return processed_label
        
class polar_projection_dataset_skitti(data.Dataset):    
    def  __init__(self,in_dataset,grid_size=[200,200,32],rotate_aug=False,ignore_value=0,fixed_volume_space=False, max_volume_space=[25,np.pi,15], min_volume_space=[-25,-np.pi,-15]):  #
        'Initialization'
        self.point_cloud_dataset=in_dataset            
        self.grid_size=np.asarray(grid_size)
        self.rotate_aug=rotate_aug
        self.ignore_value=ignore_value
        self.fixed_volume_space=fixed_volume_space
        self.max_volume_space=max_volume_space
        self.min_volume_space=min_volume_space

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.point_cloud_dataset)

    def __getitem__(self, index):
        'Generates one sample of data'        
        data=self.point_cloud_dataset[index]
        if len(data)==2:
            o3d_object,xyz=data
        elif len(data)==3:
            o3d_object,xyz,normal=data
        elif len(data)==4:
            o3d_object,xyz,normal,cluster=data            
        else:
            raise Exception('Return invalid data tuple')       
            
        # check scan makes sense
        if not isinstance(xyz, np.ndarray):
            raise TypeError("Scan should be numpy array")

        # check feature makes sense
        if normal is not None and not isinstance(normal, np.ndarray):
            raise TypeError("normal should be numpy array")
        if cluster is not None and not isinstance(cluster, np.ndarray):
            raise TypeError("cluster should be numpy array")

        '''A - open3d method'''
        if self.rotate_aug:                      
            R=o3d_object.get_rotation_matrix_from_xyz((np.pi*np.random.random(),np.pi*np.random.random(),np.pi*np.random.random()))           
            o3d_object.rotate(R,center=(0,0,0))
        
        '''B - convert coordinate into polar coordinates'''
        xyz_pol=cart2polar(xyz)            
        # o3d.visualization.draw_geometries([o3d_object])     

        max_bound_r=np.percentile(xyz_pol[:,0],100,axis = 0)
        min_bound_r=np.percentile(xyz_pol[:,0],0,axis = 0)
        max_bound=np.max(xyz_pol[:,1:],axis = 0)
        min_bound=np.min(xyz_pol[:,1:],axis = 0)
        max_bound=np.concatenate(([max_bound_r],max_bound))
        min_bound=np.concatenate(([min_bound_r],min_bound))
        if self.fixed_volume_space:
            max_bound=np.asarray(self.max_volume_space)
            min_bound=np.asarray(self.min_volume_space)            
    
        # get grid index
        crop_range=max_bound - min_bound
        cur_grid_size=self.grid_size
        intervals=crop_range/(cur_grid_size-1)
        # print(intervals)
        
        if (intervals==0).any(): print("Zero interval!")
        grid_ind=(np.floor((np.clip(xyz_pol,min_bound,max_bound)-min_bound)/intervals)).astype(np.int)
        # print(grid_ind)

        # process voxel position
        voxel_position=np.zeros(self.grid_size,dtype = np.float32)
        dim_array=np.ones(len(self.grid_size)+1,int)
        dim_array[0]=-1 
        voxel_position=np.indices(self.grid_size)*intervals.reshape(dim_array) + min_bound.reshape(dim_array)
        # print(voxel_position.shape)
        voxel_position=polar2cat(voxel_position)        
        # print(voxel_position.shape)
        
        cluster_hex=np.array([rgb2hex(rgb) for rgb in cluster])
        le=preprocessing.LabelEncoder()
        le.fit(cluster_hex)
        cluster_hex_le=le.transform(cluster_hex)
        # print(cluster_hex_le.shape)
        # process labels
        processed_label=np.ones(self.grid_size,dtype=np.uint8)*self.ignore_value   
        # print(processed_label.shape,cluster_hex_le.reshape(-1,1).shape) 
        
        label_voxel_pair=np.concatenate([grid_ind,cluster_hex_le.reshape(-1,1)],axis = 1)
        label_voxel_pair=label_voxel_pair[np.lexsort((grid_ind[:,0],grid_ind[:,1],grid_ind[:,2])),:]
        # print(label_voxel_pair)      
        
        processed_label=nb_process_label(np.copy(processed_label),label_voxel_pair)        
        # print(processed_label.shape)

        # label_shape=processed_label.shape
        # processed_label=le.inverse_transform(processed_label.reshape(-1))
        # processed_labe=processed_labe.reshape(label_shape)
        
        data_tuple=(voxel_position,processed_label)
        # print(voxel_position.shape,processed_label.shape)

        # center data on each voxel for PTnet
        voxel_centers=(grid_ind.astype(np.float32) + 0.5)*intervals + min_bound
        return_xyz=xyz_pol - voxel_centers
        return_xyz=np.concatenate((return_xyz,xyz_pol,xyz[:,:2]),axis = 1)  
        
        # print("#_"*50)
        # print(return_xyz.shape)
        
        # print(voxel_position)
        return_fea = return_xyz
        labels=cluster_hex_le
        data_tuple += (grid_ind,labels,return_fea,index,xyz)
        
        
        return data_tuple

'''
def collate_fn_BEV(data):
    import numpy as np
    # print(data)
    # data2stack=np.stack([d[0] for d in data]).astype(np.float32)
    # label2stack=np.array([d[1] for d in data])
    # grid_ind_stack=[d[2] for d in data]
    # point_label=[d[3] for d in data]
    # xyz = [d[4] for d in data]
    # return torch.from_numpy(data2stack),torch.from_numpy(label2stack),grid_ind_stack,point_label,xyz
    
    d0=np.array([d[0] for d in data])
    d1=np.array([d[1] for d in data])
    # d2=np.array([d[2] for d in data])
    # d3=np.array([d[3] for d in data])
    
    
    
    # return data2stack,label2stack,grid_ind_stack,point_label  #torch.from_numpy(data2stack)
    return d0,d1,# d2,d3        
'''       

def collate_fn_BEV_test(data):    
    data2stack=np.stack([d[0] for d in data]).astype(np.float32)
    # print(d[1])
    label2stack=np.stack([d[1] for d in data])
    
    grid_ind_stack = [d[2] for d in data]
    point_label = [d[3] for d in data]
    xyz = [d[4] for d in data]
    index = [d[5] for d in data]
    pos=[d[6] for d in data]
    return torch.from_numpy(data2stack),torch.from_numpy(label2stack),grid_ind_stack,point_label,xyz,index,pos



if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='')
    parser.add_argument('-c', '--config', default='.\config\dcp_configuration.yaml',help='configuration')
    parser.add_argument('-dp', '--data_path', default=r'E:\dataset\driverlessCity\pcds',help='simulaiton or actural scan cloud points,.pcd')
    # parser.add_argument('-s', '--grid_size', nargs='+', type=int, default=[200,200,32], help='grid size of BEV representation (default: [480,360,32])')
    parser.add_argument('--batch_size', type=int, default=1, help='batch size for training (default: 2)') #default=2
    
    parser.add_argument('-p', '--model_save_path', default='./SemKITTI_PolarSeg.pt')
    parser.add_argument('-o', '--test_output_path', default='./out/')
    parser.add_argument('-m', '--model', choices=['polar','traditional'], default='polar', help='training model: polar or traditional (default: polar)')
    parser.add_argument('-s', '--grid_size', nargs='+', type=int, default = [100,100,36], help='grid size of BEV representation (default: [480,360,32])') # [480,360,32]  [240,180,16]
    parser.add_argument('--test_batch_size', type=int, default=1, help='batch size for training (default: 1)')
        
    
    
    
    
    
    args=parser.parse_args()    
    print("staring...")
    ref_feature=['remove_byRadius','vertex_normal_estimation','cluster_dbscan',] #'vertex_downsample'
    dcp_dataset=dcp_cpts(args.data_path,args.config,ref_feature=ref_feature,set_selection='set_b', return_ref=True) 
    # dcp_dataset.__getitem__(0)
    
    #default = [480,360,32], [240,180,16],[100,100,36]
    polar_pts=polar_projection_dataset_skitti(in_dataset=dcp_dataset,grid_size=args.grid_size,rotate_aug=False,ignore_value=255,fixed_volume_space=False, max_volume_space=[25,np.pi,15], min_volume_space=[-25,-np.pi,-15])
    polar_pts.__getitem__(0)
    
    polar_batch_size=args.batch_size    
    polar_dataset_loader=torch.utils.data.DataLoader(dataset=polar_pts,
                                                      batch_size=polar_batch_size,
                                                      collate_fn=collate_fn_BEV_test ,   #collate_fn_BEV
                                                      shuffle=False,
                                                      num_workers=0)         
    
    
    
    
    if not len(args.grid_size) == 3:
        raise Exception('Invalid grid size! Grid size should have 3 dimensions.')

    print(' '.join(sys.argv))
    print(args)
    main(args)    
    
    
    
