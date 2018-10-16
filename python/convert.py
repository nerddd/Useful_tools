#coding=utf-8
import cv2
import common
import datetime
import os
import numpy as np
CSV_FILE_NAME = '_ultraface.csv'

def relabel(fileName,newfileName):
    inFile=open(fileName,'r')
    outFile=open(newfileName,'w')
    x_lines=inFile.readlines()
    id=0
    before_lable=x_lines[0].split('/')[0]
    for x_line in x_lines:
    	x_0=x_line.split()[0]
        current_lable=x_0.split('/')[0]
        if current_lable!=before_lable:
        	id=id+1
        	outFile.writelines(x_0+' '+np.str(id)+'\n')
        	before_lable=current_lable
        else:
        	outFile.writelines(x_0+' '+np.str(id)+'\n')
    print id,'\nDone'

 
def GetFileList(dir_name,fileList):
    newDir = dir_name
    if os.path.isfile(dir_name):
        fileList.append(dir_name.decode('gbk'))
    elif os.path.isdir(dir_name):  
        for s in os.listdir(dir_name):
            newDir=os.path.join(dir_name,s)
            GetFileList(newDir, fileList)  
    return fileList

def generate_imagelist_from_dir(dir_name,output_filename):
    filelist=GetFileList(dir_name,[])
    outputfile=open('all_imagelist_tmp.txt','w')
    i=0
    for e in filelist:
        line=e.encode('utf-8').split('/')[-3]+'/'+e.encode('utf-8').split('/')[-2]+'/'+e.encode('utf-8').split('/')[-1]+' '+'0'+'\n'
        outputfile.writelines(line)
        print 'generating iter:',i
        i=i+1
    relabel('all_imagelist_tmp.txt',output_filename)
    os.remove('all_imagelist_tmp.txt')
    print 'Generate done\nSave in ',output_filename

 
def check_overlap():
    fa=open('name1_tmp.txt','r')
    a=fa.readlines()
    fa.close()
    fb=open('name4_tmp.txt','r')
    b=fb.readlines()
    fb.close()
    c=[i for i in a if i in b]
    fc=open('over1.txt','w')
    fc.writelines(c)
    fc.close()
    print 'Done'

def generate_frames_fpoint_from_csv():
    df = common.read_from_file('umdfaces_videos_ultraface.csv')
    fpfilename='umdfaces_frames_fpoint.txt'
    outfile=open(fpfilename,'w')
    for row in df.iterrows():
        #Extract Important Imformation
        face_x = float(row[1]['FACE_X'])
        face_y = float(row[1]['FACE_Y'])
            
        P0_x=float(row[1]['P8X'])
        P0_y=float(row[1]['P8Y'])
        P1_x=float(row[1]['P11X'])
        P1_y=float(row[1]['P11Y'])
        P2_x=float(row[1]['P15X'])
        P2_y=float(row[1]['P15Y'])
        P3_x=float(row[1]['P18X'])
        P3_y=float(row[1]['P18Y'])
        P4_x=float(row[1]['P20X'])
        P4_y=float(row[1]['P20Y'])

        line=str(P0_x)+' '+str(P0_y)+' '+str(P1_x)+' '+str(P1_y)+' '+str(P2_x)+' '+str(P2_y)+' '+str(P3_x)+' '+str(P3_y)+' '+str(P4_x)+' '+str(P4_y)+'\n'
        outfile.writelines(line)
    print 'Done!'

def generate_batch_fpoint_from_csv():
    ori = ((common.ORI_BATCH1, common.PROCESSED_BATCH1), (common.ORI_BATCH2, common.PROCESSED_BATCH2), (common.ORI_BATCH3, common.PROCESSED_BATCH3))
    for pairs in ori:
        df = common.read_from_file(pairs[0]+pairs[0].split('/')[1]+CSV_FILE_NAME)
        fpfilename=pairs[0].split('/')[1]+'_fpoint.txt'
        outfile=open(fpfilename,'w')
        for row in df.iterrows():
            #Extract Important Imformation
            face_x = float(row[1]['FACE_X'])
            face_y = float(row[1]['FACE_Y'])
            
            P0_x=float(row[1]['P8X'])
            P0_y=float(row[1]['P8Y'])
            P1_x=float(row[1]['P11X'])
            P1_y=float(row[1]['P11Y'])
            P2_x=float(row[1]['P15X'])
            P2_y=float(row[1]['P15Y'])
            P3_x=float(row[1]['P18X'])
            P3_y=float(row[1]['P18Y'])
            P4_x=float(row[1]['P20X'])
            P4_y=float(row[1]['P20Y'])

            line=str(P0_x)+' '+str(P0_y)+' '+str(P1_x)+' '+str(P1_y)+' '+str(P2_x)+' '+str(P2_y)+' '+str(P3_x)+' '+str(P3_y)+' '+str(P4_x)+' '+str(P4_y)+'\n'
            outfile.writelines(line)
    print 'Done!'

def batch_work():
    ori = ((common.ORI_BATCH1, common.PROCESSED_BATCH1), (common.ORI_BATCH2, common.PROCESSED_BATCH2), (common.ORI_BATCH3, common.PROCESSED_BATCH3))
    for pairs in ori:
        df = common.read_from_file(pairs[0]+pairs[0].split('/')[1]+CSV_FILE_NAME)
        for row in df.iterrows():
            #Extract Important Imformation
            file_name = row[1]['FILE']
            roi_x = int(row[1]['FACE_X'])
            roi_y = int(row[1]['FACE_Y'])
            roi_w = int(row[1]['FACE_WIDTH'])
            roi_h = int(row[1]['FACE_HEIGHT'])
            #Create Dir if not Exist
            file_name = file_name.strip()
            dir_name = file_name.split('/')[0]
            if not os.path.isdir(pairs[1]+dir_name):
                os.makedirs(pairs[1]+dir_name)
            #Crop And Resize Image
            img = cv2.imread(pairs[0]+file_name)
            img_roi = img[roi_y:(roi_y+roi_h+1), roi_x:(roi_x+roi_w+1)]
            img_roi_resize = cv2.resize(img_roi, (roi_w,roi_h))
            #print img.size()
            cv2.imwrite(pairs[1]+file_name,img_roi_resize)
            LOG.info('Process %s Done!'%(file_name))

def generate_frames_imagelist():
    csvfilename='/home/yf/data/umdfaces/umdfaces_videos_ultraface.csv'
    df = common.read_from_file(csvfilename)
    imagelist_name='umdfaces_frames_imagelist_tmp.txt'
    imagelist=open(imagelist_name,'w')
    id=0
    for row in df.iterrows():
        #Extract Important Imformation
        file_name = row[1]['FILE']
         #Create Dir if not Exist
        file_name = file_name.strip()
        dir_name = file_name.split('/')[0]
        image_name=file_name.split(',')[0]
        line_content=image_name+' '+str(id)+'\n'
        imagelist.writelines(line_content)
    print 'imagelist done!'

def generate_batch_imagelist_from_csv():
    ori = ((common.ORI_BATCH1, common.PROCESSED_BATCH1), (common.ORI_BATCH2, common.PROCESSED_BATCH2), (common.ORI_BATCH3, common.PROCESSED_BATCH3))
    for pairs in ori:
        df = common.read_from_file(pairs[0]+pairs[0].split('/')[1]+CSV_FILE_NAME)
        imagelist_name=pairs[0].split('/')[1]+'_imagelist_tmp.txt'
        imagelist=open(imagelist_name,'w')
        id=0
        for row in df.iterrows():
            #Extract Important Imformation
            file_name = row[1]['FILE']
            #Create Dir if not Exist
            file_name = file_name.strip()
            dir_name = file_name.split('/')[0]
            image_name=file_name.split(',')[0]
            line_content=image_name+' '+str(id)+'\n'
            imagelist.writelines(line_content)
            LOG.info('Process %s Done!'%(file_name))
    print 'imagelist done!'

def check_clear():
    data_path='/home/yf/data/umdfaces/umdfaces_frames/'
    infile=open('/home/yf/data/umdfaces/frames_imagelist_tmp.txt','r')
    outfile=open('./umdfaces_frames_imagelist_tmp.txt','w')
    lines=infile.readlines()
    for line in lines:
        img_path=data_path+line.split()[0]
        if os.path.exists(img_path):
            outfile.writelines(line)
    print 'Done'

        

if __name__ == '__main__':
    LOG = common.init_my_logger()
    start_time = datetime.datetime.now()
    #batch_work()
    #generate_fpoint_from_csv()
    #generate_frames_imagelist()
    #check_clear()
    #check_overlap()
    #generate_frames_fpoint_from_csv()
    #relabel('umdfaces_frames_imagelist_tmp.txt','umdfaces_frames_imagelist.txt')
    generate_imagelist_from_dir('/home/yf/data/umdfaces/all_umdfaces/','all_imagelist_tmp.txt')
    end_time = datetime.datetime.now()
    LOG.info('Cost %d Seconds!'%((end_time-start_time).seconds))
