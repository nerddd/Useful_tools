import skimage
from skimage.io import imread
import os

def clean(filename,newfilename):
    infile=open(filename,'r')
    outfile=open(newfilename,'w')
    x_lines=infile.readlines()

    for x_line in x_lines:
        img_path='/home/yf/data/umdfaces/all_umdfaces_256_256/'+x_line.split()[0]
        #print img_path
        if os.path.isfile(img_path):
            outfile.writelines(x_line)
    print 'Done'

if __name__ == '__main__':
    clean('all_imagelist.txt','clean.txt')
        
    
