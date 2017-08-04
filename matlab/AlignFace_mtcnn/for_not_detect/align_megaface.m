addpath('~/caffe-rc5-triplet/matlab')

img_root = '/home/yf/megaface/MegaFace/FaceScrub_cropped';
save_root = '/home/yf/megaface/MegaFace/FaceScrub_v2-align';
image_list = '/home/yf/align/facescrub_noface.txt';
fpoint_list = '/home/yf/align/facescrub_noface_fpoint.txt';
coord3points = [30.2946, 65.5318, 48.0252; ...
                51.6963, 51.5014, 71.7366];
imgSize = [112, 96];
            

%three steps threshold
threshold=[0.6 0.7 0.7];
minsize = 100;
factor=0.709;

image_fid=fopen(image_list,'r');
fpoint_fid=fopen(fpoint_list,'r');

[x_0,y_0,x_1,y_1,x_2,y_2]=textread(fpoint_list,'%f %f %f %f %f %f');
i=1;
while ~feof(image_fid);
    image_line=fgetl(image_fid);
    image_path=fullfile(img_root,image_line);
    save_path =fullfile(save_root,image_line);
    [save_folder, save_name, save_ext] = fileparts(save_path);
    if exist(save_folder,'dir') == 0
        mkdir(save_folder);
    end;

    fpoint_vector=[x_0(i) y_0(i) x_1(i) y_1(i) x_2(i) y_2(i)];
    fpoint=double(reshape(fpoint_vector,[2,3]));
    
    img = imread(image_path);
    if size(img, 3) < 3
        img(:,:,2) = img(:,:,1);
        img(:,:,3) = img(:,:,1);
    end


    Tfm =  cp2tform(fpoint', coord3points', 'similarity');
    cropImg = imtransform(img, Tfm, 'XData', [1 imgSize(2)],...
                                'YData', [1 imgSize(1)], 'Size', imgSize);

    imwrite(cropImg, save_path);
    disp(i)
    i=i+1;
end
