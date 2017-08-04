# -*- coding:utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#将每个类别减少thres个
def reduce_num(fileName,newfileName,thres=30):
    inFile=open(fileName,'r')
    outFile=open(newfileName,'w')
    x_lines=inFile.readlines()
   
    num=0
    person_tmp=x_lines[0].split('/')[0]
    for x_line in x_lines:
        x_0=x_line.split('/')[0]
        if person_tmp==x_0:
            num+=1
            if num>thres:
                outFile.writelines(x_line)
        else:
            num=0
            person_tmp=x_0
    print "Reduce done"


if __name__ == '__main__':
    reduce_num('train-balanced.txt','train-reduced.txt')
