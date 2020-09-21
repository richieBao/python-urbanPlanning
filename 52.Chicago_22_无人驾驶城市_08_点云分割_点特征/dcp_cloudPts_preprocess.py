# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:02:05 2020

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

#show 3d pts with open3d 
def show_pts_array(pts_array,pts_color=None):
    import open3d as o3d
    '''show cloud points usinf open3d'''
    # o3d_pts=o3d.geometry.PointCloud()
    # o3d_pts.points=o3d.utility.Vector3dVector(pts_array)
    # o3d.visualization.draw_geometries([o3d_pts])
    
    pcd=o3d.geometry.PointCloud()
    pcd.points=o3d.utility.Vector3dVector(pts_array)
    
    if pts_color is not None:
        pcd.colors=o3d.utility.Vector3dVector(pts_color)
    o3d.visualization.draw_geometries([pcd])


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


'''C - voxel dataset'''
class voxel_dataset(data.Dataset):
    def __init__(self,in_dataset,rotate_aug=False,voxel_size=0.5,grid_size=[200,200,32],ignore_value=0,fixed_volume_space=False, max_volume_space=[25,np.pi,15], min_volume_space=[-25,-np.pi,-15]):
        self.point_cloud_dataset=in_dataset        
        self.rotate_aug=rotate_aug
        self.voxel_size=voxel_size
        
        #method_B
        self.grid_size = np.asarray(grid_size)
        self.fixed_volume_space=fixed_volume_space
        self.max_volume_space=max_volume_space
        self.min_volume_space=min_volume_space
        self.ignore_value=ignore_value
        
    def __len__(self):
        'Denotes the total number of samples'
        return len(self.point_cloud_dataset)
    
    def __getitem__(self,index):
        data=self.point_cloud_dataset[index]
        # print(data)
        if len(data)==2:
            o3d_object,xyz=data
        elif len(data)==3:
            o3d_object,xyz,normal=data
        elif len(data)==4:
            o3d_object,xyz,normal,cluster=data            
        else:
            raise Exception('Return invalid data tuple')        
        # print(xyz.shape)        
        
        '''A - open3d method'''
        if self.rotate_aug:                      
            R=o3d_object.get_rotation_matrix_from_xyz((np.pi*np.random.random(),np.pi*np.random.random(),np.pi*np.random.random()))           
            o3d_object.rotate(R,center=(0,0,0))
        
        voxel_grid=o3d.geometry.VoxelGrid.create_from_point_cloud(o3d_object,voxel_size=self.voxel_size)       
        # print(help(voxel_grid))
        '''
        check_if_included(...)
        create_from_octree(...)
        get_voxel(...)
        get_voxels(...)
        
        has_colors(...)
        has_voxels(...)
        to_octree(...)
        
        create_dense(...)
        
        origin
        voxel_size
        '''
        print(len(voxel_grid.get_voxels()))
        print(voxel_grid.get_voxels()[0].grid_index,voxel_grid.get_voxels()[0].color)
        o3d.visualization.draw_geometries([o3d_object])
        o3d.visualization.draw_geometries([voxel_grid])      
        # print(voxel_grid.get_center())
        
        grid_idx=np.array([val.grid_index for val in voxel_grid.get_voxels()])
        voxel_color=np.array([val.color for val in voxel_grid.get_voxels()])
        data_tuple=(xyz,normal,cluster,grid_idx,voxel_color)    #o3d_object,    
        # print(data_tuple)
        
        # data_tuple=()
        '''B - ref: https://github.com/edwardzhou130/PolarSeg'''
        max_bound=np.percentile(xyz,100,axis=0)
        min_bound=np.percentile(xyz,0,axis = 0)
        # print(max_bound,min_bound)
        if self.fixed_volume_space:
            max_bound=np.asarray(self.max_volume_space)
            min_bound=np.asarray(self.min_volume_space)       
        # print(max_bound,min_bound)    
        # get grid index
        crop_range=max_bound-min_bound
        cur_grid_size=self.grid_size            

        intervals=crop_range/(cur_grid_size-1)
        if (intervals==0).any(): print("Zero interval!")            
        grid_ind=(np.floor((np.clip(xyz,min_bound,max_bound)-min_bound)/intervals)).astype(np.int)
        # print(np.unique(grid_ind))    
        # process voxel position
        voxel_position=np.zeros(self.grid_size,dtype = np.float32)
        dim_array=np.ones(len(self.grid_size)+1,int)
        dim_array[0]=-1 
        voxel_position=np.indices(self.grid_size)*intervals.reshape(dim_array) + min_bound.reshape(dim_array)
   
        # process feature//labels
        processed_feature=np.ones(self.grid_size,dtype=np.uint8)*self.ignore_value
        feature_voxel_pair=np.concatenate([grid_ind,normal,cluster],axis=1)
        feature_voxel_pair=feature_voxel_pair[np.lexsort((grid_ind[:,0],grid_ind[:,1],grid_ind[:,2])),:]
        # print(feature_voxel_pair.shape)
        # data_tuple += (voxel_position,feature_voxel_pair)
        # print(voxel_position.shape,feature_voxel_pair.shape)
        # center data on each voxel for PTnet
        voxel_centers=(grid_ind.astype(np.float32) + 0.5)*intervals + min_bound
        return_xyz=xyz - voxel_centers
        return_xyz=np.concatenate((return_xyz,xyz),axis = 1)
        # print(return_xyz.shape)
        
        # data_tuple += (grid_ind,return_xyz)
        
        '''
        data_tuple=(o3d_object,xyz,normal,cluster,                              #original data
                    grid_idx,voxel_color,                                       #A - using open3d-voxel method
                    voxel_position,feature_voxel_pair,grid_ind,return_xyz,      #B - ref                    
                       )
        '''
        print([i.shape for i in data_tuple])    
        return data_tuple

'''D-spherical(3d->2d) projection dataset'''
class spherical_projection_dataset(data.Dataset):
    def __init__(self,in_dataset,project=False, H=64, W=1024, fov_up=3.0, fov_down=-25.0):
        self.point_cloud_dataset=in_dataset 
        self.project=project
        self.proj_H=H
        self.proj_W=W
        self.proj_fov_up=fov_up
        self.proj_fov_down=fov_down       
        self.reset()

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.point_cloud_dataset)    
    
    def __getitem__(self,index):
        self.reset()
        data=self.point_cloud_dataset[index]
        # print(data)
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


        # o3d.visualization.draw_geometries([o3d_object])
        '''do range projection'''
        self.points=xyz
        # laser parameters
        fov_up=self.proj_fov_up / 180.0 * np.pi      # field of view up in rad
        fov_down=self.proj_fov_down / 180.0 * np.pi  # field of view down in rad
        fov=abs(fov_down) + abs(fov_up)  # get field of view total in rad        
        # print(fov_up,fov_down,fov)
        # get depth of all points
        depth=np.linalg.norm(self.points, 2, axis=1)        
        # print(depth)
        # get scan components
        scan_x=self.points[:, 0]
        scan_y=self.points[:, 1]
        scan_z=self.points[:, 2]
        # get angles of all points
        yaw=-np.arctan2(scan_y, scan_x)
        pitch=np.arcsin(scan_z / depth)        
        # print(yaw,pitch)
        # get projections in image coords
        proj_x=0.5 * (yaw / np.pi + 1.0)          # in [0.0, 1.0]
        proj_y=1.0 - (pitch + abs(fov_down)) / fov        # in [0.0, 1.0]        
        # print(proj_x,proj_y)
        # scale to image size using angular resolution
        proj_x *= self.proj_W                              # in [0.0, W]
        proj_y *= self.proj_H                              # in [0.0, H]        
        # round and clamp for use as index
        proj_x=np.floor(proj_x)
        proj_x=np.minimum(self.proj_W - 1, proj_x)
        proj_x=np.maximum(0, proj_x).astype(np.int32)   # in [0,W-1]
        self.proj_x=np.copy(proj_x)  # store a copy in orig order
    
        proj_y=np.floor(proj_y)
        proj_y=np.minimum(self.proj_H - 1, proj_y)
        proj_y=np.maximum(0, proj_y).astype(np.int32)   # in [0,H-1]
        self.proj_y=np.copy(proj_y)  # stope a copy in original order       .
        
        # copy of depth in original order
        self.unproj_range=np.copy(depth)        

        # order in decreasing depth
        indices=np.arange(depth.shape[0])
        order=np.argsort(depth)[::-1]
        depth=depth[order]
        indices=indices[order]
        points=self.points[order]
        cluster_=cluster[order] #feature
        proj_y=proj_y[order]
        proj_x=proj_x[order]        
        
        # assing to images
        self.proj_range[proj_y, proj_x]=depth
        self.proj_xyz[proj_y, proj_x]=points
        # print(self.proj_feature.shape,cluster_.shape)
        cluster_hex=np.array([rgb2hex(rgb) for rgb in cluster_])
        # print(cluster_hex)
        self.proj_feature[proj_y, proj_x]=cluster_hex
        # print(self.proj_feature)
        self.proj_idx[proj_y, proj_x]=indices
        self.proj_mask=(self.proj_idx > 0).astype(np.float32)        

        data_tuple=(self.proj_feature,)
        return data_tuple

    def reset(self):
        """ Reset scan members. """
        self.points=np.zeros((0, 3), dtype=np.float32)        # [m, 3]: x, y, z
        self.feature=np.zeros((0, 3), dtype=np.float32)    # [m ,1]: remission
        
        # projected range image - [H,W] range (-1 is no data)
        self.proj_range=np.full((self.proj_H, self.proj_W), -1, dtype=np.float32)
        
        # unprojected range (list of depths for each point)
        self.unproj_range=np.zeros((0, 1), dtype=np.float32)
        
        # projected point cloud xyz - [H,W,3] xyz coord (-1 is no data)
        self.proj_xyz=np.full((self.proj_H, self.proj_W, 3), -1,dtype=np.float32)
        
        # projected feature - [H,W] intensity (-1 is no data)
        self.proj_feature=np.full((self.proj_H, self.proj_W), '#000000',dtype=np.dtype('U25')) #dtype=np.float3
        # print(self.proj_feature)
        
        # projected index (for each pixel, what I am in the pointcloud)
        # [H,W] index (-1 is no data)
        self.proj_idx=np.full((self.proj_H, self.proj_W), -1,dtype=np.int32)
        
        # for each point, where it is in the range image
        self.proj_x=np.zeros((0, 1), dtype=np.float32)        # [m, 1]: x
        self.proj_y=np.zeros((0, 1), dtype=np.float32)        # [m, 1]: y
        
        # mask containing for each pixel, if it contains a point or not
        self.proj_mask=np.zeros((self.proj_H, self.proj_W), dtype=np.int32)       # [H,W] mask
      

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

class polar_projection_dataset(data.Dataset):    
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
        
        # print(voxel_position)
        
        
        return data_tuple
        
        
    
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
        return [r'E:\dataset\results\graph_dataset\kitti_graph.dataset']

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
            y=cluster_hex_le
            

        
            # print(o3d_object.points)
            import copy
            o3d_object_copy=copy.deepcopy(o3d_object)
            o3d_object_copy.paint_uniform_color([0.5, 0.5, 0.5])
            o3d_object_tree = o3d.geometry.KDTreeFlann(o3d_object_copy)
        
            ss=1700
            o3d_object_copy.colors[ss] = [1, 0, 0]
            [k, idx, _] = o3d_object_tree.search_radius_vector_3d(o3d_object_copy.points[ss], 2)
            np.asarray(o3d_object_copy.colors)[idx[1:], :] = [0, 1, 0]
            o3d.visualization.draw_geometries([o3d_object_copy],)
            # print(k)
            # print(idx)     
            
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
            print(edge_index)
            data = Data(pos=pos, x=x, y=y, edge_index=edge_index)
            # data_list.append(data)   
            
            torch.save(data, os.path.join(self.processed_fp,r'graph_{}.pt'.format(i_iter)))
            
            
            if i_iter==0:break
            
        # data, slices = self.collate(data_list)
        # torch.save((data, slices), self.processed_file_names[0])     #InMemoryDataset
        
        
    def get(self, idx):
        data=torch.load(os.path.join(self.processed_fp,r'graph_{}.pt'.format(idx)))
        return data        

            

        

        
        
        














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

#show visualizing  multiple point clouds as an animation/use Open3D Non-blocking visualization.
def filePath_extraction(dirpath,fileType):
    import os
    '''funciton-以所在文件夹路径为键，值为包含该文件夹下所有文件名的列表。文件类型可以自行定义 '''
    filePath_Info={}
    i=0
    for dirpath,dirNames,fileNames in os.walk(dirpath): #os.walk()遍历目录，使用help(os.walk)查看返回值解释
       i+=1
       if fileNames: #仅当文件夹中有文件时才提取
           tempList=[f for f in fileNames if f.split('.')[-1] in fileType]
           if tempList: #剔除文件名列表为空的情况,即文件夹下存在不为指定文件类型的文件时，上一步列表会返回空列表[]
               filePath_Info.setdefault(dirpath,tempList)
    return filePath_Info
def multi_ptClouds_animation_filepath(ptClouds_rootPath,fileType,save_path=None):
    pcd_list=filePath_extraction(ptClouds_rootPath,fileType)
    # print(pcd_list)
    import open3d as o3d
    import os
    import time
    import numpy as np
    # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

    # geometry is the point cloud used in your animaiton
    # geometry=o3d.geometry.PointCloud()
    geometry=o3d.io.read_point_cloud(r'E:\dataset\driverlessCity\pcds\000000.pcd')

    vis=o3d.visualization.Visualizer()
    vis.create_window(width=1920,height=1080,visible=True) #width=1920,height=1080    
    vis.add_geometry(geometry)   
    
    ctr=vis.get_view_control()
    ctr.rotate(60.0, 45.0,45)
    opt=vis.get_render_option()
    opt.background_color=np.asarray([0, 0, 0])
    
    i=0
    for root,fn in pcd_list.items():
        for f in fn:            
            pts_fp=os.path.join(root,f)
            # print(pts_fp)
            pcd=o3d.io.read_point_cloud(pts_fp)
            # vis.add_geometry(pts)
                        
            # print(o3d.io.read_point_cloud(pts_fp).points)
            geometry.points=pcd.points 
            vis.update_geometry(geometry)
            vis.poll_events()
            vis.update_renderer()  
            time.sleep(2/ 20)
            
            if save_path:
                vis.capture_screen_image(os.path.join(save_path,"original_%06d.jpg" % i))
                
            
            # print(i)
            i+=1
            # if i==50:break
            
    vis.destroy_window()   


def ptsCloud_animated(idx,pts_array,pts_color=None,pts_normal=None,save_path=None):
    import open3d as o3d
    import os
    import time
    import numpy as np
    
    global geometry,vis
    
    pcd=o3d.geometry.PointCloud()
    pcd.points=o3d.utility.Vector3dVector(pts_array)
    
    if pts_color is not None:
        pcd.colors=o3d.utility.Vector3dVector(pts_color)        
    if pts_normal is not None:
        pcd.normals=o3d.utility.Vector3dVector(pts_normal)
        
  
    if idx==0:
        vis=o3d.visualization.Visualizer()
        vis.create_window(width=1920,height=1080,visible=True) #width=1920,height=1080  
        geometry=pcd    
        vis.add_geometry(geometry)   
        
        ctr=vis.get_view_control()
        ctr.rotate(60.0, 45.0,45)
        opt=vis.get_render_option()
        opt.background_color=np.asarray([0, 0, 0])  
        
  
           
    geometry.points=pcd.points 
    geometry.colors=pcd.colors 
    geometry.normals=pcd.normals
    
    vis.update_geometry(geometry)
    vis.poll_events()
    vis.update_renderer()  
    time.sleep(2/ 20)
    
    if save_path:
        vis.capture_screen_image(os.path.join(save_path,"original_%06d.jpg" % idx))

    # vis.destroy_window()   




def imgs2GIF(imgs_path,save_path):
    import imageio
    import os
    image_folder=os.fsencode(imgs_path)
    filenames=[]
    for file in os.listdir(image_folder):
        filename=os.fsdecode(file)
        if filename.endswith( ('.jpeg', '.png', '.gif','.jpg') ):
            filenames.append(filename)
    # print(filenames)
    filenames.sort() # this iteration technique has no built in order, so sort the frames
    filenames=[os.path.join(imgs_path,f) for f in filenames][180:]
    images=list(map(lambda filename: imageio.imread(filename), filenames))
    # print(images)
    imageio.mimsave(os.path.join(save_path,'pts_origional.gif'), images, duration = 0.04) # modify duration as needed
    
    
def imgs2GIF_PCL(imgs_path,save_path,):
    from PIL import Image
    import os    
    
    file_names=sorted((fn for fn in os.listdir(imgs_path) if fn.endswith( ('.jpeg', '.png', '.gif','.jpg'))))[1000:] #[180:1000]
    # print(file_names)
    images=[Image.open(os.path.join(imgs_path,fn)) for fn in file_names]
    # print(images)
    # imageio.mimsave(os.path.join(save_path,'pts_origional.gif'), images, duration = 0.04) # modify duration as needed
    images[0].save(os.path.join(save_path,'pts_polar.gif'), save_all=True, append_images=images[1:], duration=100, loop=0)
    
'''  
imgs_path=r'E:\dataset\results\img_04'    
# imgs2GIF(imgs_path,save_path=r'E:\dataset\results\gif')
imgs2GIF_PCL(imgs_path,save_path=r'E:\dataset\results\gif')
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


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='')
    parser.add_argument('-c', '--config', default='.\config\dcp_configuration.yaml',help='configuration')
    parser.add_argument('-p', '--data_path', default=r'E:\dataset\driverlessCity\pcds',help='simulaiton or actural scan cloud points,.pcd')
    parser.add_argument('-s', '--grid_size', nargs='+', type=int, default=[200,200,32], help='grid size of BEV representation (default: [480,360,32])')
    parser.add_argument('--batch_size', type=int, default=1, help='batch size for training (default: 2)') #default=2
    
    args=parser.parse_args()    
    print("staring...")
    ref_feature=['remove_byRadius','vertex_normal_estimation','cluster_dbscan','vertex_downsample'] #'vertex_downsample'
    dcp_dataset=dcp_cpts(args.data_path,args.config,ref_feature=ref_feature,set_selection='set_b', return_ref=True) 
    # dcp_dataset.__getitem__(0)
    
    
    #voxel dataset
    # grid_size=args.grid_size 
    # voxel_pts=voxel_dataset(dcp_dataset,rotate_aug=False,voxel_size=0.5,grid_size=grid_size,ignore_value=0,fixed_volume_space=True)
    # voxel_pts.__getitem__(0)
    
    
    #spherical dataset
    # spherical_pts=spherical_projection_dataset(dcp_dataset,project=True, H=64, W=1024, fov_up=16.0, fov_down=-7) # H=64, W=1024, fov_up=3.0, fov_down=-25.0
    # spherical_pts.__getitem__(0)
    # show_pts_array(spherical_pts.proj_xyz[35])
    # print(spherical_pts.proj_xyz.shape)
    # print(spherical_pts.proj_feature.shape)
       
    '''
    hex2color_=lambda c: hex2color(c)
    hex2color_vec=np.vectorize(hex2color_)   
    
    feature_rgb=hex2color_vec(spherical_pts.proj_feature)
    feature_rgb_stack=np.stack(feature_rgb).T
    feature_rgb_stack_swap=np.swapaxes(feature_rgb_stack,0,1)
    print(feature_rgb_stack_swap.shape)   
    
    fig, ax= plt.subplots(figsize=(30, 20))
    ax.imshow(feature_rgb_stack_swap)
    '''
    
    '''
    hex2color_=lambda c: hex2color(c)
    hex2color_vec=np.vectorize(hex2color_) 
    fig, ax= plt.subplots(figsize=(30, 20))
    
    spherical_dataset_loader=torch.utils.data.DataLoader(dataset=spherical_pts,
                                                         batch_size=args.batch_size,
                                                         collate_fn=collate_fn_BEV,
                                                         shuffle=False,
                                                         num_workers=0) 
    # proj_img=[]
    for i_iter,(pts_color,) in enumerate(spherical_dataset_loader):
        # print(i_iter)
        # print(pts_color.shape)
        feature_rgb=hex2color_vec(pts_color[0])
        feature_rgb_stack=np.stack(feature_rgb).T
        feature_rgb_stack_swap=np.swapaxes(feature_rgb_stack,0,1)
        # print(feature_rgb_stack_swap.shape)         
        plt.figure(figsize=(30, 20))
        plt.imshow(feature_rgb_stack_swap)
        plt.savefig(os.path.join(r'E:\dataset\results\img_03',"spherical_proj_%06d.jpg" % i_iter),bbox_inches='tight')
        
        
        # if i_iter==10:break
    '''

    
    # fileType=["pcd"]    
    # ptClouds_rootPath=r'E:\dataset\driverlessCity\pcds'    
    # save_path=r'E:\dataset\results\img_01'
    # multi_ptClouds_animation_filepath(ptClouds_rootPath,fileType,save_path)   
    
        
    '''
    voxel_batch_size=args.batch_size
    voxel_dataset_loader=torch.utils.data.DataLoader(dataset=voxel_pts,
                                                      batch_size=voxel_batch_size,
                                                      collate_fn=collate_fn_BEV,
                                                      shuffle=False,
                                                      num_workers=0) 
    
    for i_iter,(pts_array,pts_normal,pts_color,d,) in enumerate(voxel_dataset_loader):     #data_tuple=(xyz,normal,cluster,grid_idx,voxel_color) 
        # print(i_iter)
        # print("_"*50)
        # print(pts_array.shape)
        # print(pts_color.shape)
        # print(pts_normal.shape)
        
        ptsCloud_animated(idx=i_iter,pts_array=pts_array[0],pts_color=pts_color[0],pts_normal=pts_normal[0],save_path=r'E:\dataset\results\img_02')
        
        # if i_iter==100:
        #     break
    '''
        
    '''
    rgb2hex_=lambda c: rgb2hex(c)
    rgb2hex_vec=np.vectorize(rgb2hex_) 
        
        
    def uniqueSum(array,val):
        print(array[array==val].sum())
    
    
    polar_pts=polar_projection_dataset(in_dataset=dcp_dataset,grid_size=[100,100,36],rotate_aug=False,ignore_value=255,fixed_volume_space=False, max_volume_space=[25,np.pi,15], min_volume_space=[-25,-np.pi,-15])
    polar_pts.__getitem__(0)
    
    polar_batch_size=args.batch_size    
    polar_dataset_loader=torch.utils.data.DataLoader(dataset=polar_pts,
                                                      batch_size=polar_batch_size,
                                                      collate_fn=collate_fn_BEV,
                                                      shuffle=False,
                                                      num_workers=0)     
    
    import pandas as pd
    
    for i_iter,(pts_array,pts_color) in enumerate(polar_dataset_loader): 
        print(i_iter)
        print("_"*50)
        print(pts_array.shape)
        print(pts_color.shape)
        print(np.unique(pts_color))
        print(np.unique(pts_color[0].reshape(-1)/31))
        
    
    
                
                
        
        plt.figure(figsize=(30, 30))
        # print(pts_array)
        # plt.scatter(pts_array[0][0].reshape(-1), pts_array[0][1].reshape(-1),c=data_rgb/255,alpha=0.5) #pts_color[0]/31
        
        
        x=pts_array[0][0].reshape(-1)
        y=pts_array[0][1].reshape(-1)
        color=pts_color.reshape(-1)
        b=~color==255
        
        c_=color[color!=255]
        unique_digitize=np.unique(c_)
        random_color_dict=[{k:np.random.randint(low=1,high=254,size=1)for k in unique_digitize} for i in range(3)]
        data_color=[pd.DataFrame(c_).replace(random_color_dict[i]).to_numpy() for i in range(3)]
        data_rgb=np.concatenate([i for i in data_color],axis=-1)    
     
        
        
        plt.scatter(x[color!=255],y[color!=255],c=data_rgb/255.,s=200,alpha=1)
        plt.scatter(x[color==255],y[color==255],c='r',s=1)
        
        plt.tick_params(axis='both',labelsize=30)

        
        plt.savefig(os.path.join(r'E:\dataset\results\img_04',"polar_proj_%06d.jpg" % i_iter),bbox_inches='tight')
        plt.show()
        # if i_iter==0:
        #     break
    '''

    print("graph computing!")
    processed_fp=r'E:\dataset\results\graph_dataset'
    graph_pts=graph_dataset(in_dataset=dcp_dataset,processed_fp=processed_fp,root='') 
    # graph_pts=graph_dataset(root='') 
    # graph_pts.process()
    graph_pts.get(0)
    
    
    
    # with open(args.config,'r') as stream:
    #     dcp_configuration=yaml.safe_load(stream)
    # dcp_configuration['pts_process']
    
    
    # dcp_cloudPts_fp=r'E:\dataset\driverlessCity\POINT_CLOUD.ply'    
    # pcd_fp=r'E:\dataset\driverlessCity\pcds\000000.pcd'
    # dcp_cloudPts=o3d.io.read_point_cloud(pcd_fp)
    
    
    
    # aabb = dcp_cloudPts.get_axis_aligned_bounding_box()
    # aabb.color = (1,0,0)
    # obb =dcp_cloudPts.get_oriented_bounding_box()
    # obb.color = (0,1,0)
        
    # o3d.visualization.draw_geometries([dcp_cloudPts, aabb, obb])
    
    
    # #remove_radius_outlier(...)
    # t=dcp_cloudPts
    # a,_=t.remove_radius_outlier(500,25)
    # o3d.visualization.draw_geometries([a])
    
    # #remove_statistical_outlier(...)
    # t=dcp_cloudPts
    # a,_=t.remove_statistical_outlier(100,0.7)
    # o3d.visualization.draw_geometries([a])
    
    '''
    uniform_down_sample(...)
    voxel_down_sample(...)
    voxel_down_sample_and_trace(...)
    
    rotate(...)
    scale(...)
    transform(...)
    translate(...)
    
    get_center(...)
    get_max_bound(...)
    get_min_bound(...)
    
    clear(...)
    dimension(...)
    get_geometry_type(...)
    is_empty(...)
    
    PointCloud = Type.PointCloud
    RGBDImage = Type.RGBDImage
    Unspecified = Type.Unspecified
    VoxelGrid = Type.VoxelGrid
    '''