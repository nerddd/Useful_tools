# -*- coding:utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def read_file(path):
    with open(path) as f:
        return list(f)

#将标签重新按顺序生成，写入新的文件中
def Relabel(fileName,newfileName):
    inFile=open(fileName,'r')
    outFile=open(newfileName,'w')
    x_lines=inFile.readlines()
    #x_distribute=[0]*20
    id=0
    before_lable=x_lines[0].split('/')[0]
    for x_line in x_lines:
    	x_0=x_line.split()[0]
        #x_1=x_line.split()[1]
        current_lable=x_0.split('/')[0]
        if current_lable!=before_lable:
        	id=id+1
        	outFile.writelines(x_0+' '+np.str(id)+'\n')
        	before_lable=current_lable
        else:
        	outFile.writelines(x_0+' '+np.str(id)+'\n')
    print id,'\nDone'

#计算每个类别的个数,返回小于thre的类别有多少个
def Count_num(fileName,newfileName,thre=10):
    inFile=open(fileName,'r')
    outFile=open(newfileName,'w')
    x_lines=inFile.readlines()
   
    count=0
    num=0
    person_tmp=x_lines[0].split('/')[0]
    print person_tmp
    for x_line in x_lines:
        x_0=x_line.split('/')[0]
        if person_tmp==x_0:
            num+=1
        else:
            if num<thre:
                count+=1
                print count,x_0,num
            num=0
            person_tmp=x_0 
    if num<thre:
            count+=1   
    print count,'\nDone'

if __name__ == '__main__':
    #loadData('eye_image_clean.txt','image_clean.txt')
    Relabel('all_imagelist.txt','all_umdfaces_clean.txt')
    #Relabel('umdfaces_batch1_imagelist_tmp.txt','umdfaces_batch1_imagelist.txt')
    #Relabel('umdfaces_batch2_imagelist_tmp.txt','umdfaces_batch2_imagelist.txt')
    #Relabel('umdfaces_batch3_imagelist_tmp.txt','umdfaces_batch3_imagelist.txt')

