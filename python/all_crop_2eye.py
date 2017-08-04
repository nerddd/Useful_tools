import sys
import os
import numpy as np
import skimage
from skimage import io
import matplotlib.pyplot as plt

DATA_ROOT = 'mscelebv1_crop/'

def read_file(path):
    with open(path) as f:
        return list(f)


def crop(fp_file,image_path,save_path):   
    point_lines = read_file(fp_file)
    image_lines = read_file(image_path)
    
    if not point_lines or not image_lines:
        print 'empty file'
        return

    i = 0
    for (point_line, image_line) in zip(point_lines, image_lines):
        image_line = image_line.strip('\n')
        point_line = point_line.strip('\n')

        img_name = image_line.split()[0]

        img = skimage.io.imread(DATA_ROOT+img_name)
        
        eye_width=np.float32(point_line.split()[2])-np.float32(point_line.split()[0])*0.78
        eye_height=eye_width*0.4
        x1= np.float32(point_line.split()[0])-0.5*eye_width
        x2= np.float32(point_line.split()[0])+0.5*eye_width
        y1= np.float32(point_line.split()[1])-0.5*eye_height
        y2= np.float32(point_line.split()[1])+0.5*eye_height
        crop_image=img[y1:y2,x1:x2]    
        skimage.io.imsave(save_path+img_name,crop_image)
        
        i = i+1
        sys.stdout.write('\riter %d\n' %(i))
        sys.stdout.flush()

    print 'done'

if __name__=='__main__':

    fp_file = 'list_clean_allimage_fpoint.txt'
    image_path = 'list_clean_allimage_align.txt'
    save_path = './mscelebv1_crop_eye/'

    if save_path.endswith("/") == False:
        save_path += "/"

    crop(fp_file,image_path,save_path)
