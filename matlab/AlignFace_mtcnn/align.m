function find=align(image_path, PNet, RNet, ONet, LNet)
    %three steps threshold
    threshold=[0.6 0.7 0.7];
    minsize = 100;
    factor=0.709;
    imgSize = [112, 96];
    coord5points = [30.2946, 65.5318, 48.0252, 33.5493, 62.7299; ...
                    51.6963, 51.5014, 71.7366, 92.3655, 92.2041];
    %fnoface=fopen('noface.txt','a');
    %fface=fopen('aligned.txt','a')
    find = 0;%inital not finding a face
    img = imread(image_path);
    if size(img, 3) < 3
       img(:,:,2) = img(:,:,1);
       img(:,:,3) = img(:,:,1);
    end
    save_path = strrep(image_path, '/dev/data/txm/home_txm/3caffe/data/msceleb_data/mscelebv1_crop', '/home/yf/data/msdata_v2-align');
    %save_path = strrep(image_path, '/FaceScrub_cropped', '/FaceScrub_v2-align');
    %line=strrep(save_path, '/home/yf/megaface/MegaFace/FaceScrub_v2-align/', '');
    %if exist(save_path, 'file')
        %return;
    %end;
    img = imread(image_path);
    if size(img, 3) < 3
       img(:,:,2) = img(:,:,1);
       img(:,:,3) = img(:,:,1);
    end

    assert(strcmp(image_path, save_path)==0);
    [save_folder, save_name, save_ext] = fileparts(save_path);
    if exist(save_folder,'dir') == 0
        mkdir(save_folder);
    end;

    [boundingboxes points]=detect_face(img,min([minsize size(img,1) size(img,2)]),PNet,RNet,ONet,LNet,threshold,false,factor);

    if isempty(boundingboxes)
        %disp(['******* no face in ' image_path]);
        %return;
        %fprintf(fnoface,'%s\n',line);
        %fclose(fnoface);
        return ;
    end;

    default_face = 1;
    if size(boundingboxes,1) > 1
        for bb=2:size(boundingboxes,1)
            if abs((boundingboxes(bb,1) + boundingboxes(bb,3))/2 - size(img,2) / 2) + abs((boundingboxes(bb,2) + boundingboxes(bb,4))/2 - size(img,1) / 2) < ...
                    abs((boundingboxes(default_face,1) + boundingboxes(default_face,3))/2 - size(img,2) / 2) + abs((boundingboxes(default_face,2) + boundingboxes(default_face,4))/2 - size(img,1) / 2)
                default_face = bb;
            end;
        end;
    end;

    facial5points = double(reshape(points(:,default_face),[5 2])');

    Tfm =  cp2tform(facial5points', coord5points', 'similarity');
    cropImg = imtransform(img, Tfm, 'XData', [1 imgSize(2)],...
                                'YData', [1 imgSize(1)], 'Size', imgSize);

    imwrite(cropImg, save_path);
    %fprintf(fface,'%s\n',line)
    %fclose(fface);
    find =1;
end

