import pickle
import numpy as np
import cv2
import os

labels20 = ["aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable", "dog",
    "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
    "train", "tvmonitor"]

# 8, 14, 15, 19

voc_models = ['yolo-full', 'yolo-tiny', 'yolo-small',  # <- v1
              'yolov1', 'tiny-yolov1', # <- v1.1 
              'tiny-yolo-voc', 'yolo-voc'] # <- v2

coco_models = ['tiny-coco', 'yolo-coco',  # <- v1.1
               'yolo', 'tiny-yolo'] # <- v2

coco_names = 'coco.names'
nine_names = '9k.names'

def labels(meta, FLAGS):    
    model = os.path.basename(meta['name'])
    if model in voc_models: 
        print("Model has a VOC model name, loading VOC labels.")
        meta['labels'] = labels20
    else:
        file = FLAGS.labels
        if model in coco_models:
            print("Model has a coco model name, loading coco labels.")
            file = os.path.join(FLAGS.config, coco_names)
        elif model == 'yolo9000':
            print("Model has name yolo9000, loading yolo9000 labels.")
            file = os.path.join(FLAGS.config, nine_names)

        meta['labels'] =["car"]
        # with open(file, 'r') as f:
        #     meta['labels'] = list()
        #
        #     labs = [l.strip() for l in f.readlines()]
        #
        #     for lab in labs:
        #         if lab == '----': break
        #         meta['labels'] += [lab]
    if len(meta['labels']) == 0: 
        meta['labels'] = labels20





