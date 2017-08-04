import sys
import os
import numpy as np
import skimage
from skimage import io,transform
import matplotlib.pyplot as plt
import cv2

def read_file(path):
    with open(path) as f:
        return list(f)


def make_dir(image_path):   
    image_lines = read_file(image_path)
    if not image_lines:
        print 'empty file'
        return
    i = 0
    for image_line in image_lines:
        image_line = image_line.strip('\n')
        subdir_name = image_line.split('/')[0]
        print subdir_name
        isExists=os.path.exists(subdir_name)
        if not isExists:
            os.mkdir(subdir_name)
            #print subdir_name+"created successfully!"      
        i = i+1
        sys.stdout.write('\riter %d\n' %(i))
        sys.stdout.flush()

    print 'Done'

if __name__=='__main__': 
    image_path='./list_clean_allimage_align.txt'
    make_dir(image_path)
