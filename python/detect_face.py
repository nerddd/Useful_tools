#!/usr/bin/env python
# coding=utf-8

import sys
# sys.path.append('./build')
sys.path.append('/home/yf/data/umdfaces/python-lib')

import mtcnn
from mtcnn import MTcnn,init_log
from skimage.io import imread

sys.path.append('/home/yf/caffe-rc5/python')
import caffe
init_log(2)
# init model
mt = MTcnn('../../../MTmodel')

DATA_PATH='/home/yf/data/umdfaces_batch'

def detect_fp():
    for i in xrange(1,4):
        print 'Detect landmark in batch',i,'starting...'
        ImgDataPath=DATA_PATH+str(i)+'/'
        imagelist='/home/yf/data/umdfaces/umdfaces_batch'+str(i)+'_imagelist.txt'
        infile=open(imagelist,'r')
        fpfilename='/home/yf/data/umdfaces/umdfaces_batch'+str(i)+'_fpoint.txt'
        outfile=open(fpfilename,'w')
        imagelist_clean='/home/yf/data/umdfaces/umdfaces_batch'+str(i)+'_imagelist_clean.txt'
        outfile2=open(imagelist_clean,'w')
        lines=infile.readlines()
        for line in lines:
            print 'batch',i,':',line.split()[0]
            img_path=ImgDataPath+line.split()[0]
            #print 'read image: %s' %img_path
            img = imread(img_path)
            img = img[:,:,(2,1,0)]  # OpenCV like BGR uint8
            
            # detect fpoints
            fps = mt.detect(img)
            if len(fps)!=0:
                fpoint=''
                for k in xrange(13):
                    fps[k]='%.3f' % fps[k]
                    fpoint=fpoint+str(fps[k])+' '
                fps[13]='%.3f' % fps[13]
                fpoint=fpoint+str(fps[13])+'\n'
                outfile.writelines(fpoint)
                outfile2.writelines(line)

        print 'over'
    print 'Done'

if __name__=="__main__":
    detect_fp()

