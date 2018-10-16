## align_batch.py

批量对齐的脚本，包含四个尺寸的标准脸

### all_dis_2eye.py

对图像存储路径文件和关键点检测文件进行计算,存储图片中眼睛的宽度和高度参数

### all_crop_2eye.py

对图像存储路径文件和关键点检测文件进行计算，对图片中的眼睛进行crop并存储

### all_mkdir.py

针对skimage.io.imsave不能创建新目录，需要首先创建目录，因为图像存储文件中还包括图片的路径，所以在imsave的时候就会出错，需要先创建目录

### analysis_json.py

对json文件进行解析

### clean.py

对imagelist.txt的每一行所代表的文件检测是否真实存在，将不存在的删掉，重新生成imagelist.txt

### compute.py

计算每个类别包含样本个数的区间，比如样本数少于10的有多少类，样本数在10~20之间的有多少类

### _copy.py

改进后的_copy.py批量复制图片，将umdfaces_batch系列的静态图片和umdfaces_frames结合在一起，其中umdfaces_frames的类别是包含于umdfaces_batch1的，将静态图片在对应的类别下新建一个still的子目录放置在混合数据集中

### copy_from_imagelist.py

根据imagelist.txt中图片路径复制图片到目标文件夹

### convert.py

- **generate_imagelist_from_dir**:从目录得到imagelist.txt
- **check_overlap**:检查两个文件中相同的部分
- **generate_fpoint/imagelist_from_csv**:对csv文件进行解析

## count_num.py

输入带标签的文件，输出每一类的数量

### detect_face.py

利用mtcnn对人脸批量进行检测

### draw.py

根据散点画图

### name.py

根据imagelist.txt计算得到每个类别的名字

## face.py

人脸检测，对齐及提取特征和比对

### get_raw_images_list.py

将imagelist.txt分成train.txt和val.txt

### make_umdface_testpic.py

从imagelist.txt中读取，每一类挑选一张(or 几张)图片作为测试集

## plot_training_log.py.example

经过修改的caffe绘制曲线脚本，可以显示中文，生成矢量图

## RandRename.py

批量随机重命名文件夹下文件名

### reduce_num.py

将每个类别减少thres个，对于balance操作的

### relabel.py

- **Relabel**:将混乱的标签重新按顺序生成，写入新的文件中
- **Count_num**:计算每个类别的个数,返回小于thre的类别有多少个

### split_train_test.py

将imagelist.txt分成train.txt和val.txt和test.txt

