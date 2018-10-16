import os
source_dataroot = '/home/yf/data/imdb_clean/mtcnn/'
target_dataroot='./imdb_testpic'
def copydata(imagelist,source_root,target_root):
    infile=open(imagelist,'r')
    lines=infile.readlines()
    i=0
    for line in lines:
        i=i+1
        line=source_root+line.split()[0]
        os.system("cp "+line+" "+target_root)
        print "copy..iter:",i
    print "done"

if __name__=="__main__":
    copydata('imdb_test_imagelist.txt',source_dataroot,target_dataroot)
