import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def loadData(fileName):
    inFile=open(fileName,'r')
    x_lines=inFile.readlines()
    x_distribute=[0]*20
    for x_line in x_lines:
        x_point=x_line.split()[0]
        i=np.int(np.float32(x_point)/10)
        x_distribute[i]+=1
    print x_distribute


if __name__ == '__main__':
    loadData('dis.txt')