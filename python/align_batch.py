# -*- coding: utf-8 -*-
import os
import numpy as np
#import matplotlib
#import matplotlib.pylab as plt
import skimage
from skimage import transform as tf
from skimage import io
import sys

ref_p_112_96 = np.float32([30.2946,51.6963, 65.5318,51.5014, 48.0252,71.7366,33.5493,92.3655, 62.7299,92.2041]).reshape((5,2))
ref_p_128_128 = np.float32([43.9736, 51.5082, 86.4005, 52.1159, 66.2167, 79.2851, 46.7114, 101.486, 82.7252, 101.673]).reshape((5,2))
ref_p_256_256 = np.float32([81.1987, 85.5746, 174.157, 85.4161, 126.974, 154.764, 89.5261, 180.875, 170.373, 181.206]).reshape((5,2))

imgSize = (256,256)
DATA_ROOT = '/home/yf/data/umdfaces/umdfaces_batch3/'
TARGET_ROOT= '/home/yf/data/umdfaces/umdfaces_batch3_align_256_256/'

def read_file(path):
    with open(path) as f:
        return list(f)

def alignment(fp_file,image_path,save_path,ref_points = []):   
    point_lines = read_file(fp_file)
    image_lines = read_file(image_path)
    
    if not point_lines or not image_lines:
        print 'empty file'
        return

    if len(ref_points) == 0:
        ref_points = np.float32(point_lines[0].split()).reshape((5,2))

    i = 0
    for (point_line, image_line) in zip(point_lines, image_lines):
        image_line = image_line.strip('\n')
        point_line = point_line.strip('\n')

        img_name = image_line.split()[0]
        dir_name=image_line.split('/')[0]
        exist_dirs = os.listdir(TARGET_ROOT)
        if dir_name not in exist_dirs:
            os.mkdir(TARGET_ROOT + dir_name)
        
        
        img = skimage.io.imread(DATA_ROOT+img_name)
        pts = np.float32(point_line.split()).reshape((5,2))

        tfrom=tf.estimate_transform('similarity',ref_points,pts)
        warpimage=tf.warp(img,inverse_map=tfrom,output_shape=imgSize)     
        skimage.io.imsave(save_path+img_name,warpimage)
        
        i = i+1
        print ('\riter %d' %(i))

    print 'done'

if __name__=='__main__':
    #if len(sys.argv)!=4:
    #    print 'print ',sys.argv[0], 'fp_file image_path save_path'
    #    sys.exit()

    #fp_file = sys.argv[1]
    #image_path = sys.argv[2]
    #save_path = sys.argv[3]
    
    fp_file = '/home/yf/data/umdfaces/umdfaces_batch3_fpoint.txt'
    image_path = '/home/yf/data/umdfaces/umdfaces_batch3_imagelist_all.txt'
    save_path = '/home/yf/data/umdfaces/umdfaces_batch3_align_256_256/'
    

    if save_path.endswith("/") == False:
        save_path += "/"

    alignment(fp_file,image_path,save_path,ref_p_256_256)
    #alignment(fp_file2,image_path2,save_path2,ref_p_256_256)
    #alignment(fp_file3,image_path3,save_path3,ref_p_256_256)
