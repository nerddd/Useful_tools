#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
copy umdfaces image from source to target
'''

import os
import sys
import random
import threading

source_root1 = "/home/yf/data/umdfaces/umdfaces_batch1_align_256_256/"
source_root2 = "/home/yf/data/umdfaces/umdfaces_batch2_align_256_256/"
source_root3 = "/home/yf/data/umdfaces/umdfaces_batch3_align_256_256/"
target_root = "/home/yf/data/umdfaces/all_umdfaces/"


#将umdfaces_batch系列的静态图片和umdfaces_frames结合在一起，其中umdfaces_frames的类别是包含于umdfaces_batch1的
#将静态图片在对应的类别下新建一个still的子目录放置在混合数据集中
def copy_data(source_root,source_imagelist_filename):
    infile=open(source_imagelist_filename,'r')
    lines=infile.readlines()
    i=0
    for line in lines:
        i=i+1
        class_name = line.split('/')[0]
        print 'copying... iter:',i
         
        source_path =source_root+line.split()[0]
        if os.path.isfile(source_path):
            exist_dirs = os.listdir(target_root)
            if class_name not in exist_dirs:
                os.makedirs(target_root + class_name+'/still/')
            else:
                exist_subdirs=os.listdir(target_root+class_name)
                subdir_name='still'
                if subdir_name not in exist_subdirs:
                    os.mkdir(target_root+class_name+'/still/')
            target_path=target_root+class_name+'/still/'+line.split()[0].split('/')[1]
            os.system("cp " + source_path + " " + target_path)
    print 'Copy done'

if __name__ == "__main__":
    copy_data(source_root1,'umdfaces_batch1_imagelist_all.txt')
    copy_data(source_root2,'umdfaces_batch2_imagelist_all.txt')
    copy_data(source_root3,'umdfaces_batch3_imagelist_all.txt')

