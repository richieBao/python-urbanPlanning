# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 12:25:40 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
ref: PyTorch Geometric Example
"""
import os.path as osp

import torch
from torch.utils import data
import torch.nn.functional as F

from torch_geometric.datasets import ShapeNet
import torch_geometric.transforms as T
from torch_geometric.data import DataLoader
from torch_geometric.nn import knn_interpolate
from torch_geometric.utils import intersection_and_union as i_and_u
from torch_geometric.data import Dataset,InMemoryDataset
from torch_geometric.data import Data

from sklearn import preprocessing

import open3d as o3d
import numpy as np
import numba as nb
import yaml,os,argparse

from matplotlib.colors import rgb2hex,hex2color
import matplotlib.pyplot as plt


'''dataset'''
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

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))
           
class SemKITTI(data.Dataset):
    def __init__(self, data_path, imageset = 'train', return_ref = False,ref_feature=[],config_path=''):
        self.return_ref = return_ref
        #with open("semantic-kitti.yaml", 'r') as stream:
        with open(r"C:\Users\richi\omen-richiebao\omen-code\code_ref_2020_08\PolarSeg-master\semantic-kitti.yaml", 'r') as stream:
            semkittiyaml = yaml.safe_load(stream)
        self.learning_map = semkittiyaml['learning_map']
        self.imageset = imageset
        if imageset == 'train':
            split = semkittiyaml['split']['train']
        elif imageset == 'val':
            split = semkittiyaml['split']['valid']
        elif imageset == 'test':
            split = semkittiyaml['split']['test']
        else:
            raise Exception('Split must be train/val/test')
        
        self.im_idx = []
        # print(split)
        for i_folder in split:
            # print(i_folder)
            # self.im_idx += absoluteFilePaths('/'.join([data_path,str(i_folder).zfill(2),'velodyne']))
            self.im_idx += absoluteFilePaths('\\'.join([data_path,str(i_folder).zfill(2),'velodyne']))
            # self.im_idx.append(absoluteFilePaths(os.path.join(data_path,str(i_folder).zfill(2),'velodyne')))
            # print(absoluteFilePaths(os.path.join(data_path,str(i_folder).zfill(2),'velodyne')))
        # print(self.im_idx )    
        
        self.ref_feature=ref_feature
        
        with open(config_path,'r') as stream:
            self.dcp_configuration=yaml.safe_load(stream)        
        self.ref_feature_list=self.dcp_configuration['pts_process']
            
         
    def __len__(self):
        'Denotes the total number of samples'
        return len(self.im_idx)
    
    def __getitem__(self, index):
        raw_data = np.fromfile(self.im_idx[index], dtype=np.float32).reshape((-1, 4))
        
        
        pcd=o3d.geometry.PointCloud()
        pcd.points=o3d.utility.Vector3dVector(raw_data[:,:3])     
        # pcd.label=

        # o3d.visualization.draw_geometries([pcd])
        if self.return_ref:
            ref_handle=pts_utility(pcd,) 
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
            # o3d.visualization.draw_geometries([ref_handle.cloudPts])
            data_dic.update({'o3d_object':ref_handle.cloudPts,"pts_array":np.asarray(ref_handle.cloudPts.points)})
            if ref_handle.cloudPts.has_normals():
                data_dic.update({"normal":np.asarray(ref_handle.cloudPts.normals)})
            if  ref_handle.cloudPts.has_colors():
                data_dic.update({"cluster":np.asarray(ref_handle.cloudPts.colors)})       
                
            data_tuple=tuple(v for v in data_dic.values())
        
        else:
            data_tuple=(raw_data,pts_array)

        if self.imageset == 'test':
            annotated_data = np.expand_dims(np.zeros_like(raw_data[:,0],dtype=int),axis=1)
        else:
            annotated_data = np.fromfile(self.im_idx[index].replace('velodyne','labels')[:-3]+'label', dtype=np.int32).reshape((-1,1))
            annotated_data = annotated_data & 0xFFFF #delete high 16 digits binary
            annotated_data = np.vectorize(self.learning_map.__getitem__)(annotated_data)
        data_tuple += (raw_data[:,:3], annotated_data.astype(np.uint8),)
        if self.return_ref:
            data_tuple += (raw_data[:,3],)
        # print(data_tuple)
        
        return data_tuple  #'o3d_object','pts_array","normal","cluster",//////original---raw_data_pos,raw_data_lable,raw_data.normal

'''F-pytorch geometric graph dataset'''
class graph_dataset(Dataset):  #Dataset,InMemoryDataset
    def __init__(self, in_dataset,processed_fp,root, transform=None, pre_transform=None):
        self.in_dataset=in_dataset
        self.processed_fp=processed_fp  

        super(graph_dataset, self).__init__(root, transform, pre_transform)
        # self.data, self.slices = torch.load(self.processed_file_names[0])
      

    @property
    def raw_file_names(self):
        return []
    @property
    def processed_file_names(self):
        return [r'E:\dataset\results\graph_dataset\graph_dataset_KITTI.dataset']

    def download(self):
        pass
    
    def process(self):        
        data_list = []
        # print(data_list)
        # i=0
        for i_iter,data in enumerate(self.in_dataset):        
            print(i_iter)
            if len(data)==2:
                o3d_object,xyz=data
            elif len(data)==3:
                o3d_object,xyz,normal=data
            elif len(data)==4:
                o3d_object,xyz,normal,cluster=data     
            elif len(data)==7:
                o3d_object,xyz,normal,cluster,raw_data_pos,raw_lable,raw_normal=data                 
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
                
            # o3d.visualization.draw_geometries([o3d_object])
            pos=xyz
            # print(pos)
            x=normal
            # print(normal)
            
            cluster_hex=np.array([rgb2hex(rgb) for rgb in cluster])
            le=preprocessing.LabelEncoder()
            le.fit(cluster_hex)
            cluster_hex_le=le.transform(cluster_hex)            
            # print(cluster_hex_le)
            y_=cluster_hex_le
            
            y=raw_lable
            


            # print(o3d_object.points)
            import copy
            o3d_object_copy=copy.deepcopy(o3d_object)
            o3d_object_copy.paint_uniform_color([0.5, 0.5, 0.5])
            o3d_object_tree = o3d.geometry.KDTreeFlann(o3d_object_copy)
        
            ss=1700
            o3d_object_copy.colors[ss] = [1, 0, 0]
            [k, idx, _] = o3d_object_tree.search_radius_vector_3d(o3d_object_copy.points[ss], 2)
            np.asarray(o3d_object_copy.colors)[idx[1:], :] = [0, 1, 0]
            # o3d.visualization.draw_geometries([o3d_object_copy],)
            # print(k)
            # print(idx)     

            '''
            source_nodes=[]
            target_nodes=[]
            # print(help(o3d_object_copy))
            for j in range(len(o3d_object_copy.points)):
                [k, idx, _] = o3d_object_tree.search_radius_vector_3d(o3d_object_copy.points[j], 2)
                for i in idx[1:]:
                    source_nodes.append(j)
                    target_nodes.append(i)

            # print(len(source_nodes))
            edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)
            # print(edge_index)
            '''
            
            #numpay array
            # data = Data(pos=pos, x=x, y=y, ) #edge_index=edge_index
            #tensor
            # print(y.shape)
            data = Data(pos=torch.from_numpy(pos).float(), x=torch.from_numpy(x).float(), y=torch.from_numpy(y.reshape(-1)).long(),batch=torch.from_numpy(np.zeros(len(y),dtype=np.int64) ))
            
            # data_list.append(data)   
            
            torch.save(data, os.path.join(self.processed_fp,r'graph_{}.pt'.format(i_iter)))
            
            
            # if i_iter==10:break
            
        # data, slices = self.collate(data_list)
        # torch.save(data_list, r'E:\dataset\results\graph_dataset_KITTI_merge\graph_dataset_KITTI.dataset')     #InMemoryDataset (data, slices)
        
        
    def get(self, idx):
        data=torch.load(os.path.join(self.processed_fp,r'graph_{}.pt'.format(idx)))
        return data        


if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', '--data_dir', default=r'E:\dataset\semanticKITTI\dataset') #''data'        
    parser.add_argument('-p', '--model_save_path', default='./modelSave/KITTI_PyTorchGeo.pt')
    parser.add_argument('--train_batch_size', type=int, default=2, help='batch size for training (default: 2)')
    parser.add_argument('--val_batch_size', type=int, default=2, help='batch size for validation (default: 2)')
    parser.add_argument('--check_iter', type=int, default=4000, help='validation interval (default: 4000)')    
    parser.add_argument('-c', '--config', default='.\config\dcp_configuration.yaml',help='configuration')
    args = parser.parse_args()
      
    
    #load Semantic KITTI class info
    with open(r"./config/semantic-kitti.yaml", 'r') as stream:
        semkittiyaml = yaml.safe_load(stream)
    SemKITTI_label_name = dict()
    for i in sorted(list(semkittiyaml['learning_map'].keys()))[::-1]:
        SemKITTI_label_name[semkittiyaml['learning_map'][i]] = semkittiyaml['labels'][i]
        

    #
    data_path=r'E:\dataset\semanticKITTI\dataset'
    ref_feature=['remove_byRadius','vertex_normal_estimation','cluster_dbscan',] #'vertex_downsample'
    train_pt_dataset = SemKITTI(data_path + '/sequences/', imageset = 'train', return_ref = True,ref_feature=ref_feature,config_path=args.config) 
    train_pt_dataset.__getitem__(0)    
    
      
    print("graph computing!")
    processed_fp=r'E:\dataset\results\graph_dataset_KITTI'
    graph_pts=graph_dataset(in_dataset=train_pt_dataset,processed_fp=processed_fp,root='') 
    # graph_pts.process()
    # graph_pts.get(0)
        
        