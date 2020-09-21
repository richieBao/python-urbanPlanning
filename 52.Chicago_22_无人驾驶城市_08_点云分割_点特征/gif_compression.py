# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:57:15 2020

@author: Richie Bao-caDesign (cadesign.cn)
"""
from PIL import Image
from tqdm import tqdm


gif_path=r'E:\temp\pts_cluster_A.gif'
save_path=r'E:\temp\01.gif'

imageObject=Image.open(gif_path)
# print("if is animated gif? ",imageObject.is_animated)
# print("gif_frames number: ",imageObject.n_frames)


width_ratio=0.1
height_ratio=0.1

images=[]
for frame in tqdm(range(0,imageObject.n_frames)):
    imageObject.seek(frame)
    # print(imageObject.width, imageObject.height)
    # imageObject.show() 
    # print(imageObject)
    img_resize=imageObject.resize((round(imageObject.size[0] *width_ratio), round(imageObject.size[1] * height_ratio)), Image.ANTIALIAS) 
    # print(img_resize.width, img_resize.height)
    # img_resize.show()
    images.append(img_resize)
    
    # if frame==10:
        # break
    
images[0].save(save_path,save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)    