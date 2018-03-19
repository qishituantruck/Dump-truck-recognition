#coding=utf-8


import numpy
import cv2
import time
import os
from hyperlpr_py3 import pipline
from util.uploadimg import ftp_upload
# def recognize(filename):
#     image = cv2.imread(filename)
    #通过文件名读入一张图片 放到 image中
    # return pipline.RecognizePlateJson(image)

    #识别一张图片并返回json结果
if __name__=="__main__":
    path = "C:/Users/chezh/Documents/GitHub/Dump-truck-recognition/image/2.jpg"
    image=cv2.imread(path)
    img,res=pipline.SimpleRecognizePlate(image)
    # result=recognize(path)
    print(res)
    cv2.waitKey(0)
    # ftp_upload(path,str(i)+".jpg")
    # print(result)
    # for i in range(1,11):
    #     path="C:/Users/chezh/Documents/GitHub/Dump-truck-recognition/image/"+str(i)+".jpg"
    #     result=recognize(path)
    #     ftp_upload(path,str(i)+".jpg")
    #     print(result)