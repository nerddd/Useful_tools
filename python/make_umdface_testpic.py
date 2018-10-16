#coding=utf-8
import os
import sys

target_root = "/home/yf/age_gender/v2/testpic/"
source_root1 = '/home/yf/data/umdfaces/umdfaces_batch1_align_256_256/'
source_root2 = '/home/yf/data/umdfaces/umdfaces_batch2_align_256_256/'
source_root3 = '/home/yf/data/umdfaces/umdfaces_batch3_align_256_256/'
def copy_data(source_root,source_imagelist_filename):
    infile=open(source_imagelist_filename,'r')
    lines=infile.readlines()
    person_tmp=lines[0].split('/')[0]
    num=0
    i=0
    for line in lines:
        i=i+1
        class_name = line.split('/')[0]
        if class_name==person_tmp:
            num+=1
            if num<2:
                source_path =source_root+line.split()[0]
                print 'cp ',source_path
                os.system("cp " + source_path + " " + target_root)
        else:
            person_tmp=class_name
            num=0
        print 'copying... iter:',i 
    print 'Copy done'

if __name__=='__main__':
    copy_data(source_root1,'/home/yf/data/umdfaces/umdfaces_batch1_imagelist_all.txt')
    copy_data(source_root2,'/home/yf/data/umdfaces/umdfaces_batch2_imagelist_all.txt')
    copy_data(source_root2,'/home/yf/data/umdfaces/umdfaces_batch2_imagelist_all.txt')
