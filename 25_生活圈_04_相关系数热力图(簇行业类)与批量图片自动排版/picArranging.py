# -*- coding: utf-8 -*-
"""
Created on Wed May  1 23:02:21 2019

@author:Richie Bao-caDesign设计(cadesign.cn)
参考源于网络
"""
import numpy as np
from PIL import Image
import cv2
from os.path import dirname as ospdn
import os
import os.path as osp
import re

def may_make_dir(path):
  """
  Args:
    path: a dir, or result of `osp.dirname(osp.abspath(file_path))`
  Note:
    `osp.exists('')` returns `False`, while `osp.exists('.')` returns `True`!
  """
  # This clause has mistakes:
  # if path is None or '':

  if path in [None, '']:
    return
  if not osp.exists(path):
    os.makedirs(path)

'''读取图片数据'''  
def read_im(im_path):
  # shape [H, W, 3]
  im = np.asarray(Image.open(im_path.rstrip()))
  # Resize to (im_h, im_w) = (128, 64)
  resize_h_w = (864,1296) #调整图像大小
  if (im.shape[0], im.shape[1]) != resize_h_w:
    im = cv2.resize(im, resize_h_w[::-1], interpolation=cv2.INTER_LINEAR) 
  im=im[20:,0:1100,:] #根据图像情况，进一步调整图像大小，例如去除白边等
  im = im.transpose(2, 0, 1) #转置
  if (im.shape[0] is not 3):
      im = im[0:3,:,:]
  return im

def save_im(im, save_path):
  """im: shape [3, H, W]"""
  may_make_dir(ospdn(save_path))
  im = im.transpose(1, 2, 0)
  Image.fromarray(im).save(save_path)
  
def make_im_grid(ims, n_rows, n_cols, space, pad_val):
  """Make a grid of images with space in between.
  Args:
    ims: a list of [3, im_h, im_w] images
    n_rows: num of rows
    n_cols: num of columns
    space: the num of pixels between two images
    pad_val: scalar, or numpy array with shape [3]; the color of the space
  Returns:
    ret_im: a numpy array with shape [3, H, W]
  """
  assert (ims[0].ndim == 3) and (ims[0].shape[0] == 3)
  assert len(ims) <= n_rows * n_cols
  h, w = ims[0].shape[1:]
  H = h * n_rows + space * (n_rows - 1)
  W = w * n_cols + space * (n_cols - 1)
  if isinstance(pad_val, np.ndarray):
    # reshape to [3, 1, 1]
    pad_val = pad_val.flatten()[:, np.newaxis, np.newaxis]
  ret_im = (np.ones([3, H, W]) * pad_val).astype(ims[0].dtype)
  for n, im in enumerate(ims):
    r = n // n_cols
    c = n % n_cols
    h1 = r * (h + space)
    h2 = r * (h + space) + h
    w1 = c * (w + space)
    w2 = c * (w + space) + w
    ret_im[:, h1:h2, w1:w2] = im
  return ret_im


if __name__=="__main__":
    images_dir = r'C:\Users\Richi\sf_richiebao\sf_monograph\25_socialAttribute_04_partialCorrle_picArranging\results\single'
    save_path = r'C:\Users\Richi\sf_richiebao\sf_monograph\25_socialAttribute_04_partialCorrle_picArranging\results\merged\results.png'
    n_rows = 5
    n_cols = 10
    
    dirs_files = os.listdir(images_dir)  #返回指定的文件夹包含的文件或文件夹的名字的列表，按字母-数字顺序
    dirs_files.sort()
    pattern=re.compile(r'[_](.*?)[.]', re.S)
    fn_numExtraction=[(int(re.findall(pattern, fName)[0]),fName) for fName in dirs_files] #提取文件名中的数字，即聚类距离。并对应文件名
    fn_sort=sorted(fn_numExtraction)
#    print(fn_sort)
    fn_sorted=[i[1] for i in fn_sort]
#    print(fn_sorted)
    
    image_names = []
    for dir_file in fn_sorted:
        image_path = os.path.join(images_dir, dir_file)
        if image_path.endswith('.png'):
            image_names.append(image_path)
    q_im_paths = image_names[0:n_rows*n_cols] #保证提取的图片数量与所配置的n_rows*n_cols数量同

    ims = []
    for q_im_path in q_im_paths:
        im = read_im(q_im_path)
        ims.append(im)
    im = make_im_grid(ims, n_rows, n_cols,1, 255)
    save_im(im, save_path.rstrip())