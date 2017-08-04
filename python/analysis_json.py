import json
import os
import sys

#JSON_PATH='/home/yf/megaface/MegaFace/FaceScrub_cropped/'
JSON_PATH='/home/yf/megaface/MegaFace/MegaFace_Challenge1/daniel/FlickrFinal2/'
def analysis(filename,newfilename):
    outfile=open(newfilename,'w')
    with open(filename) as fp:
        feature_file=json.load(fp)
        path_list=feature_file["path"]
        for i in range(len(path_list)):
            line=path_list[i]+'\n'
            outfile.writelines(line)
            print i
    print 'Done'

def json2txt(filename,newfilename):
    infile=open(filename,'r')
    lines=infile.readlines()
    outfile=open(newfilename,'w')
    i=0
    for line in lines:
        line=line.strip()
        json_path=JSON_PATH+line+'.JSON'
        with open(json_path) as fp:
            points=""
            points_file=json.load(fp)
            x_0=str("%.3f" % points_file["landmarks"]["1"]["x"])
            y_0=str("%.3f" % points_file["landmarks"]["1"]["y"])
            x_1=str("%.3f" % points_file["landmarks"]["0"]["x"])
            y_1=str("%.3f" % points_file["landmarks"]["0"]["y"])
            x_2=str("%.3f" % points_file["landmarks"]["2"]["x"])
            y_2=str("%.3f" % points_file["landmarks"]["2"]["y"])
            points_list=x_0+' '+y_0+' '+x_1+' '+y_1+' '+x_2+' '+y_2+'\n'
            outfile.writelines(points_list)
            i=i+1
            print i
    print 'Done'


if __name__=='__main__':
    #analysis('megaface_features_list.json_1000000_1','analysis_megaface_1000000_1.txt')
    #json2txt('facescrub_noface.txt','facescrub_noface_fpoint.txt')
    json2txt('megaface_noface.txt','megaface_noface_fpoint.txt')
