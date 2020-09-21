# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 19:45:05 2020

@author: Richie Bao-Chicago.IIT(driverless city project)
data:IIT(driverless city project)
"""
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
    geometry=o3d.io.read_point_cloud(r'E:\dataset\results\PyTorchGeo_poiNet_pcd_img\pcd\0.pcd')

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
            geometry.colors=pcd.colors
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
    
def imgs2GIF_PCL(imgs_path,save_path,):
    from PIL import Image
    import os    
    
    file_names=sorted((fn for fn in os.listdir(imgs_path) if fn.endswith( ('.jpeg', '.png', '.gif','.jpg')))) #[1000:] #[180:1000]
    # print(file_names)
    images=[Image.open(os.path.join(imgs_path,fn)) for fn in file_names]
    # print(images)
    # imageio.mimsave(os.path.join(save_path,'pts_origional.gif'), images, duration = 0.04) # modify duration as needed
    images[0].save(os.path.join(save_path,'skitti_pytorchGeo.gif'), save_all=True, append_images=images[1:], duration=100, loop=0)
    
  
    
if __name__ == '__main__':
    # fileType=["pcd"]    
    # ptClouds_rootPath=r'E:\dataset\results\PyTorchGeo_poiNet_pcd_img\pcd'    
    # save_path=r'E:\dataset\results\PyTorchGeo_poiNet_pcd_img\img'
    # multi_ptClouds_animation_filepath(ptClouds_rootPath,fileType,save_path)     
    
    
 
    imgs_path=r'E:\dataset\results\PyTorchGeo_poiNet_pcd_img\img'    
    imgs2GIF_PCL(imgs_path,save_path=r'E:\dataset\results\gif')
  