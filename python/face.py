#!/usr/bin/python2
# -*- coding:utf-8 -*-
"""
Verify.py: Created by YangFan on 17-6-22
Companion: verify_configs.json
* Verify cosine similarity with two given facial images
* Python API embedding to Java through JPY
"""

import sys, os
# os.environ["GLOG_minloglevel"] = "4"
os.environ["GLOG_minloglevel"] = "2"
sys.path.insert(0, '/usr/local/jpy')
import caffe    # extract feature
import mtcnn    # detect facial points
import jpy, jpyutil # java python bridge
import json         # configs loader
import numpy as np  # image container 
import skimage.io   # image reader
from skimage import transform as tf # align: affine transform
from numpy import linalg as la  # linear transformation
from sklearn.externals import joblib   # load pca model

jpyutil.init_jvm(jvm_maxmem='256M')
FloatArray = jpy.get_type('[F')

"""
Details of MTcnn from c++ explosion
python module: mtcnn
 + set_device(int)  # set gpu id used for detection
 * MTcnn(str)       # handle face detection with given model_dir
   * factor      float  read write 0.709 
   * minSize     int    read write 40
   * threshold   list   read write [0.5, 0.6, 0.6]
   + detect(np)  list   detected face information
"""

"""
Wrapper for instantiation of FACE in Java
"""
def FACE(config_path, mtcnn_id, center_id):
    return Face(config_path, mtcnn_id, center_id)

class Face:
    """
    Face API : Python Object to be Embedded in Java
        * mtcnn       brief handle mtcnn face detection
        * center      handle center feature similarity
        + verify      compute similarity of two given images 
        + detect      detect face information
        + extract     extract face features in given image
    """

    def __init__(self, config_path, mtcnn_id, center_id):
        with open(config_path) as f:
            configs = json.load(f)

        ## init mtcnn
        mtcnn.set_device(mtcnn_id)
        self.mtcnn = mtcnn.MTcnn(str(configs['mtcnn']['model_dir'])) 
        self.mtcnn.factor = configs['mtcnn']['factor']
        self.mtcnn.minSize = configs['mtcnn']['minSize']
        self.mtcnn.threshold = configs['mtcnn']['threshold']

        ## init center
        self.center = Center(configs['center'], center_id)

    def _listToNp(self, image, height, width):
        """
        Convert byte list to numpy OpenCV like: BGR uint8
        """
        image = np.array(image).reshape(height, width, 3).astype(np.uint8)  # OpenCV like
        return image
    
    def _detect(self, image):
        """
        Detect face informations of given numpy OpenCV like: BGR uint8
        """
        raw_infos = self.mtcnn.detect(image)
        num = len(raw_infos) / 18

        infos = []
        for i in xrange(num):
            infos.append({})
            raw_info = raw_infos[18*i:18*(i+1)]
            infos[i]['bbox'] = raw_info[:4]
            infos[i]['fpoints'] = raw_info[4:14]
            infos[i]['score'] = raw_info[15]
            infos[i]['rotations'] = raw_info[-3:]
        return infos
    
    def verify(self, image1, height1, width1, image2, height2, width2):
        """
        Compute facial similarity with given two image byte list
        return cos similar: float to java
        """
        # convert to numpy OpenCV like
        image1 = self._listToNp(image1, height1, width1)
        image2 = self._listToNp(image2, height2, width2)
        # detect face informations
        faceInfo1 = self._detect(image1)
        faceInfo2 = self._detect(image2)
        # verify similarity
        if len(faceInfo1) == 0:  
            if len(faceInfo2) == 0: # both no face
                sim = -3
            else:   # only image1 no face
                sim = -1
        else:
            if len(faceInfo2) == 0:  # only image2 no face
                sim = -2
            else:   # both have face
                fpoints1 = faceInfo1[0]['fpoints']
                fpoints2 = faceInfo2[0]['fpoints']
                #sim==4 means image1 is a fake face,otherwise ,return the simiarity.
                sim = self.center.verify(image1, fpoints1, image2, fpoints2)
        return sim

    def detect(self, image, height, width):
        """
        Detect face informations of given numpy OpenCV like: BGR uint8
        return faceInfos : float[][18] to java
        [
          x1, y1, x2, y2,   # bounding box 
          xy,xy,xy,xy,xy,   # facial points 
          score,            # confidence
          - roll,           # Z axis 翻转角:歪着脸  * NotImplemented
          - pitch,          # X axis 俯仰角:上下看  * NotImplemented
          - yaw             # Y axis 偏航角:左右看  * NotImplemented
        ]
        """
        image = self._listToNp(image, height, width)
        raw_infos = self.mtcnn.detect(image)
        infos = []
        num = len(raw_infos) / 18
        # print num,
        for i in xrange(num):
            info = []
            for f in raw_infos[18*i:18*(i+1)]:
                info.append(round(f, 3))
            infos.append(jpy.array('float', info)) # float[]
        return jpy.array(FloatArray, infos) # flaot[][]

    def extract(self, image, height, width):
        """
        Extract facial features in given image
        return faceFeatures: float[][] to java
        [
          x1, y1, x2, y2,   # bounding box
          score,            # confidence
          feature           # center feature
        ]
        """
        image = self._listToNp(image, height, width)
        face_infos = self._detect(image)
        feat_infos = []
        fpoints = []

        for face_info in face_infos:
            feat_info = face_info['bbox']
            feat_info.append(face_info['score'])
            feat_infos.append(feat_info)
            fpoints.append(face_info['fpoints'])

        features = self.center.extract(image, fpoints)
        for i in xrange(features.shape[0]):
            feat_infos[i].extend(list(features[i]))
            # print feat_infos[i][:6]
            feat_infos[i] = jpy.array('float', feat_infos[i]) # float[]
        return jpy.array(FloatArray, feat_infos)    # float[][]

class Center:
    """
    Handle center feature similarity.
    + verify            compute similarity of two image with facial key points
    - _merge_factory    create merge function with given merge type
    - _align            align face in image with fpoints list
    - _extract          extract center feature with given batch faces
    - _similar          compute cosine similarity of given features
    """
    def __init__(self, configs, device_id):
        # caffe environment settings
        caffe.set_mode_gpu()
        caffe.set_device(device_id)

        # basic settings
        self._ref_points = np.float32(configs['ref_points']).reshape((5,2))
        self._mode = configs['mode']
        self._mirror = configs['mirror']
        self._pca_model = configs['pca_model']

        if self._mode == 'verify':
            self._batch_face = 2
            if self._mirror:
                self._batch_size = self._batch_face * 2
            else:
                self._batch_size = self._batch_face
        else:
            if self._mirror:
                self._batch_face = configs['batch_size'] / 2  # each batch contains face num
                self._batch_size = self._batch_face * 2
            else:
                self._batch_face = configs['batch_size']
                self._batch_size = self._batch_face
       
        if self._pca_model:
            self._pca = joblib.load(str(self._pca_model))

        # load center model
        self._net = caffe.Net(
                str(configs['deploy']),
                str(configs['model']),
                caffe.TEST) 
        self._in = self._net.inputs[0]
        self._layer = self._net.outputs[0]    # feature layer name
        self._image_size = self._net.blobs[self._in].data.shape[2:]
        self._data_shape = (self._batch_size, 3) + self._image_size
        self._net.blobs[self._in].reshape(*self._data_shape)
        self._feature_length = self._net.blobs[self._layer].data.shape[1]
       
        # data container
        self._input = np.zeros(self._data_shape, dtype=np.float32)
        if self._mirror:
            if str(self._mirror) == 'concatenate':
                self._merge = np.zeros((self._batch_face, self._feature_length*2), dtype=np.float32)
            else:
                self._merge = np.zeros((self._batch_face, self._feature_length), dtype=np.float32)
        self._merge_function = self._merge_factory(str(self._mirror))

        # init transfomer
        self._transformer = caffe.io.Transformer({self._in: self._data_shape})
        self._transformer.set_transpose(self._in, (2,0,1)) # HWC to CHW
        self._transformer.set_raw_scale(self._in, 255)     # [0,1] to [0,255]
        self._transformer.set_mean(self._in, np.array((127.5, 127.5, 127.5)))  # substract mean
        # self._transformer.set_channel_swap(self._in, (2,1,0))    # RGB to BGR
        self._transformer.set_input_scale(self._in, 0.0078125)   # to [-1, 1]
        self.anti_init_net()

    def _merge_factory(self, merge_type):
        """
        Use closure to save 'if' check every time we merge mirror feature
        """
        if merge_type == 'concatenate':
            def merge_feature(features):
                for i in xrange(self._batch_face):
                    self._merge[i] = np.concatenate((features[2*i], features[2*i+1]))
        elif merge_type == 'add': # elem-wise add
            def merge_feature(features):
                for i in xrange(self._batch_face):
                    self._merge[i] = features[2*i] + features[2*i+1]
        elif merge_type == 'max': # elem-wise max
            def merge_feature(features):
                for i in xrange(self._batch_face):
                    for j in xrange(self._feature_length):
                        self._merge[i][j] = max(features[2*i][j], features[2*i+1][j])
        elif merge_type == 'min': # elem-wise min
            def merge_feature(features):
                for i in xrange(self._batch_face):
                    for j in xrange(self._feature_length):
                        self._merge[i][j] = min(features[2*i][j], features[2*i+1][j])
        else:    # None: Disable mirror
            def merge_feature(features):
                self._merge = features

        return merge_feature

    def _align(self, image, fpoints):
        """
        Align Face with given facial key points.
        Affine transformation to reference standard key points
        """
        fpoints = np.float32(fpoints).reshape((5,2))
        tfrom = tf.estimate_transform('similarity', self._ref_points, fpoints)
        warp_image = tf.warp(image, inverse_map=tfrom, 
                output_shape=self._image_size)
        return warp_image

    def _extract(self, batch_faces):
        """
        Extract feature with given batch faces using center model 
        Enable batch to extract feature simultaneously
        """
        assert(len(batch_faces) <= self._batch_face)
        if self._mirror:
           for i in xrange(len(batch_faces)):
               self._input[2*i] = self._transformer.preprocess(self._in, batch_faces[i])
               self._input[2*i+1] = self._transformer.preprocess(self._in, np.fliplr(batch_faces[i]))
        else:
            for i in xrange(len(batch_faces)):
                self._input[i] = self._transformer.preprocess(self._in, batch_faces[i])
        self._net.blobs[self._in].data[...] = self._input
        self._net.forward()
        self._merge_function(self._net.blobs[self._layer].data)
        
    def extract(self, image, fpoints):
        """
        Extract feature with given faces using center model
        """
        num = len(fpoints)
        faces = []
        for i in xrange(num):
            faces.append(self._align(image, fpoints[i]))
        features = np.zeros((num, self._feature_length), np.float32)
        for begin in xrange(0, num, self._batch_face):
            end = min(begin+self._batch_face, num)
            self._extract(faces[begin:end])
            features[begin:end] = self._merge[:end-begin]
        
        if self._pca_model:
            return self._pca.transform(features)
        else:
            return features

    def _similar(self, features):
        """
        Compute cosine similarity between two features
        """
        feat1 = np.mat(features[0])
        feat2 = np.mat(features[1])
        inp = float(feat1 * feat2.T)
        denom = la.norm(feat1) * la.norm(feat2)
        return 0.5 + 0.5 * (inp / denom)

    #def anti_init_net(self):
    #    anti_spoofing_model='./python/center/model/anti_iter_120000.caffemodel'
    #    anti_spoofing_deploy='./python/center/model/anti_deploy.prototxt'
    #    anti_spoofing_net=caffe.Classifier(anti_spoofing_deploy,anti_spoofing_model,
    #            mean=np.array((127.5, 127.5, 127.5)),
    #            channel_swap=(2,1,0),
    #            raw_scale=255,
    #            image_dims=(112,96))#(112,96)
    #    return anti_spoofing_net

    #def anti_spoofing(self, net, img):
    #    #print 'pic shape is:',img.shape[0],img.shape[1]
    #    prediction=(net.predict([img],oversample=False))[0].argmax()
    #    return prediction
    #
    def anti_init_net(self):
        anti_spoofing_model='./python/center/model/anti_iter_120000.caffemodel'
        anti_spoofing_deploy='./python/center/model/anti_deploy.prototxt'
        self._anti_net=caffe.Net(anti_spoofing_deploy,anti_spoofing_model,caffe.TEST)

    def anti_spoofing(self,_anti_net, img):
        _anti_in = _anti_net.inputs[0]
        _anti_layer = _anti_net.outputs[0]    # feature layer name
        _anti_input = self._transformer.preprocess(_anti_in, img)
        _anti_net.blobs[_anti_in].data[...] = _anti_input
        _anti_net.forward()
        prediction=_anti_net.blobs[_anti_layer].data.argmax()
        return prediction
    
    def verify(self, image1, fpoints1, image2, fpoints2):
        """
        Verify similarity of given two image
        * argv   : numpy  OpenCV like BGR uint8
                   list   Facial key points
        * return : float  Cosine similarity
        """
        face1 = self._align(image1, fpoints1)
        face2 = self._align(image2, fpoints2)
        
        #anti_net=self.anti_init_net()
        anti_pred=self.anti_spoofing(self._anti_net,face1)
        if anti_pred==0:#face1 is real
            self._extract([face1, face2])
            if self._pca_model:
                return self._similar(self._pca.transform(self._merge))
            else:
                return self._similar(self._merge)
        else:
            return -4
        '''
        self._extract([face1, face2])
        if self._pca_model:
            return self._similar(self._pca.transform(self._merge))
        else:
            return self._similar(self._merge)
        '''
if __name__ == "__main__":
    caffe.init_log(2)
    test_main()
