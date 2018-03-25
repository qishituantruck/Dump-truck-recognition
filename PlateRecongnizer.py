#coding=utf-8
import numpy
import cv2
import time
import os
# from hyperlpr import pipline
from util.uploadimg import ftp_upload
from hyperlpr import pipline as pp
from hyperlpr import e2emodel as model


if __name__=="__main__":
    pred_model = model.construct_model("./model/ocr_plate_all_w_rnn_2.h5", )
    path = "./image/10.jpg"
    image=cv2.imread(path)
    # ftp_upload(path, "test.jpg")
    image,result=pp.RecognizePlateDict(image,pred_model)
    # result=recognize(path)
    print(result)


    if len(result)==0:
        print("未检测到车牌！")
    else:
        for i in range(len(result)):
            plate=result[i]
            platenumber=plate["Name"]
            x=plate["x"]
            y=plate["y"]
            w=plate["w"]
            h=plate["h"]
            cv2.rectangle(image, (x, y), (x+w, y+h), (55, 255, 155), 5)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, platenumber, (x, y-10), font, 1, (55, 255, 155), 2, cv2.LINE_AA)


    cv2.imshow("result",image)
    cv2.waitKey(0)
