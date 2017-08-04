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


def crop(fp_file,image_path):   
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

        if np.float32(point_line.split()[2])> np.float32(point_line.split()[0]):
            eye_left_x=np.float32(point_line.split()[0])
            eye_right_x=np.float32(point_line.split()[2])
            eye_left_y=np.float32(point_line.split()[1])
            eye_right_y=np.float32(point_line.split()[3])
        else:
            eye_left_x=np.float32(point_line.split()[2])
            eye_right_x=np.float32(point_line.split()[0])
            eye_left_y=np.float32(point_line.split()[3])
            eye_right_y=npfloat32(point_line.split()[1])
        left_eye_width=(eye_right_x-eye_left_x)*0.78
        right_eye_width=left_eye_width
        if left_eye_width*0.5>eye_left_x:
            left_eye_width=eye_left_x*2
        if right_eye_width*0.5+eye_right_x>img.shape[1]:
            right_eye_width=(img.shape[1]-eye_right_x)*2
        crop_right=np.int32(eye_right_x+right_eye_width*0.5)
        crop_left=np.int32(eye_left_x-left_eye_width*0.5)
        crop_width=crop_right-crop_left
        #y_tmp=max(eye_left_y,eye_right_y)
        crop_height=crop_width*0.3
        #crop_down=np.int32(y_tmp-crop_height*0.5)
        #crop_up=np.int32(y_tmp+crop_height*0.5)
        '''
        if eye_width>40 and eye_width<140:   
            x1= np.int(eye_left_x-0.5*eye_width)
            x2= np.int(eye_left_x+0.5*eye_width)
            y1= np.int(eye_left_y-0.5*eye_height)
            if y1<0:
                y1=0
            y2= np.int(eye_left_y+0.5*eye_height)
        '''
        dx=str("%.2f"%crop_width)
        dy=str("%.2f"%crop_height)
        c=dx+' '+dy+'\n'
        fc=open('2eye_dis.txt','a')
        fc.writelines(c)
        
        i = i+1
        sys.stdout.write('\riter %d\n' %(i))
        sys.stdout.flush()

    print 'done'

if __name__=='__main__':
    
    fp_file = 'list_clean_allimage_fpoint.txt'
    image_path = 'list_clean_allimage_align.txt'

    crop(fp_file,image_path)
