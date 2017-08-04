import cv2
import common
import datetime
import os

def name2():
    imglistname='umdfaces_frames_imagelist.txt'
    infile=open(imglistname,'r')
    personfile='name4_tmp.txt'
    outfile=open(personfile,'w')
    lines=infile.readlines()
    before=lines[0].split('/')[0]
    print before
    outfile.writelines(before+'\n')
    for line in lines:
        current=line.split('/')[0]
        label=line.split()[1]
        if current!=before:
            outfile.writelines(current+'\n')
            before=current
    print 'Done!'

def name():
    for i in xrange(1,4):
        imglistname='umdfaces_batch'+str(i)+'_imagelist_all.txt'
        infile=open(imglistname,'r')
        personfile='name'+str(i)+'_tmp.txt'
        outfile=open(personfile,'w')
        lines=infile.readlines()
        before=lines[0].split('/')[0]
        print before
        outfile.writelines(before+'\n')
        for line in lines:
            current=line.split('/')[0]
            label=line.split()[1]
            if current!=before:
                outfile.writelines(current+'\n')
                before=current
    print 'Done!'

if __name__=="__main__":
    name()
    name2()
