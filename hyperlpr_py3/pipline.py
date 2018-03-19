#coding=utf-8
from . import detect
from . import  finemapping  as  fm


import cv2

import time
import numpy as np

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import json

import sys
from . import typeDistinguish as td
import imp





from . import e2e





from . import finemapping_vertical as fv

def RecognizePlateDict(image):
    images = detect.detectPlateRough(image,image.shape[0],top_bottom_padding_rate=0.1)
    jsons = []
    for j,plate in enumerate(images):
        plate,rect,origin_plate =plate
        res, confidence = e2e.recognizeOne(origin_plate)
        print("res",res)

        # cv2.imwrite("./"+str(j)+"_rough.jpg",plate)

        # print "车牌类型:",ptype
        # plate = cv2.cvtColor(plate, cv2.COLOR_RGB2GRAY)
        plate  =cv2.resize(plate,(136,int(36*2.5)))
        t1 = time.time()

        ptype = td.SimplePredict(plate)
        if ptype>0 and ptype<4:
            plate = cv2.bitwise_not(plate)
        # demo = verticalEdgeDetection(plate)

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)
        image_rgb = fv.finemappingVertical(image_rgb)

        # print time.time() - t1,"校正"
        print("e2e:",e2e.recognizeOne(image_rgb)[0])
        image_gray = cv2.cvtColor(image_rgb,cv2.COLOR_BGR2GRAY)

        # cv2.imwrite("./"+str(j)+".jpg",image_gray)
        # image_gray = horizontalSegmentation(image_gray)

        t2 = time.time()
        res, confidence = e2e.recognizeOne(image_rgb)
        res_json = {}
        if confidence  > 0.6:
            res_json["Name"] = res
            res_json["Type"] = td.plateType[ptype]
            res_json["Confidence"] = confidence;
            res_json["x"] = int(rect[0])
            res_json["y"] = int(rect[1])
            res_json["w"] = int(rect[2])
            res_json["h"] = int(rect[3])
            jsons.append(res_json)


    return jsons




