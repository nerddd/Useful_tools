# -*- coding:utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#计算每个类别的个数
def Count_num(fileName,newfileName):
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
            new_line=person_tmp+" "+str(num)+"\n"
            outFile.writelines(new_line)
            num=0
            person_tmp=x_0 
    new_line=person_tmp+" "+str(num)+"\n"
    outFile.writelines(new_line) 
    print '\nDone'

if __name__ == '__main__':
	Count_num('./vgg2_clean.txt','./clean_list_num.txt')
