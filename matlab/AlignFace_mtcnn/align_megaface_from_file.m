pdollar_toolbox_path='pdollar-toolbox';
addpath(genpath(pdollar_toolbox_path));
addpath('~/caffe-rc5-triplet/matlab')
MTCNN_path = 'MTCNN_face_detection_alignment/code/codes/MTCNNv2';
addpath(genpath(MTCNN_path));

caffe.set_mode_gpu();   
caffe.set_device(0);
caffe.reset_all();

caffe_model_path=[MTCNN_path , '/model'];
prototxt_dir = strcat(caffe_model_path,'/det1.prototxt');
model_dir = strcat(caffe_model_path,'/det1.caffemodel');
PNet=caffe.Net(prototxt_dir,model_dir,'test');
prototxt_dir = strcat(caffe_model_path,'/det2.prototxt');
model_dir = strcat(caffe_model_path,'/det2.caffemodel');
RNet=caffe.Net(prototxt_dir,model_dir,'test');  
prototxt_dir = strcat(caffe_model_path,'/det3.prototxt');
model_dir = strcat(caffe_model_path,'/det3.caffemodel');
ONet=caffe.Net(prototxt_dir,model_dir,'test');
prototxt_dir =  strcat(caffe_model_path,'/det4.prototxt');
model_dir = strcat(caffe_model_path,'/det4.caffemodel');
LNet=caffe.Net(prototxt_dir,model_dir,'test');

img_root = '/home/yf/megaface/MegaFace/MegaFace_Challenge1/daniel/FlickrFinal2';
save_root = '/home/yf/megaface/MegaFace/MegaFace_v2-align';
fnoface=fopen('megaface_file_noface.txt','a');
fface=fopen('megaface_file_aligned.txt','a')
    
image_list_filename='/home/yf/megaface/tests/MegaFace_align_list_image.txt';
fid=fopen(image_list_filename,'r'); 

if exist(save_root, 'dir') == 0
    mkdir(save_root);
end;

i=1;
while ~feof(fid);
    image_line=fgetl(fid);
    image_path=fullfile(img_root,image_line);
    disp(['iter:' num2str(i) '\t' image_line]);
    if(i>410827);
        find=align_face(image_path, PNet, RNet, ONet, LNet);
        line=strrep(image_path,'/home/yf/megaface/MegaFace/MegaFace_Challenge1/daniel/FlickrFinal2/','');
        if find == 0
            fprintf(fnoface,'%s\n',line);
        else
            fprintf(fface,'%s\n',line);
        end;
    end;
    i=i+1;
end

