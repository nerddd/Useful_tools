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
%img_root = '/home/yf/megaface/MegaFace/FaceScrub_cropped';
%save_root = '/home/yf/megaface/MegaFace/FaceScrub_v2-align';
image_list = get_image_list_in_folder(img_root);
fnoface=fopen('noface.txt','a');
fface=fopen('aligned.txt','a')
    

if exist(save_root, 'dir') == 0
    mkdir(save_root);
end;

for image_id = 389212:length(image_list);
    find=align_face(image_list{image_id}, PNet, RNet, ONet, LNet);
    disp([num2str(image_id) '/' num2str(length(image_list)) image_list{image_id}]);
    line=strrep(image_list{image_id},'/home/yf/megaface/MegaFace/MegaFace_Challenge1/daniel/FlickrFinal2/','');
    %line=strrep(image_list{image_id},'/home/yf/megaface/MegaFace/FaceScrub_cropped/','');
    if find == 0
        fprintf(fnoface,'%s\n',line);
    else
        fprintf(fface,'%s\n',line);
    end;
end

