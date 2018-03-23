from darkflow.net.build import TFNet
import cv2
import numpy as np
import json
import time
from util.CarLocation import getCarLoc
options = {"model": "cfg/tiny-yolo-voc.cfg", "load": "model/tiny-yolo-voc.weights", "threshold": 0.1,"gpu":0.7}



# ipaddress='http://10.6.12.241:8080/'
# cap=cv2.VideoCapture(ipaddress)
cap = cv2.VideoCapture('test.mp4')
c = 0
tfnet = TFNet(options) #初始化

while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # cv2.waitKey(0)
    if c%15==0:
        starttime=time.time()
        result = tfnet.return_predict(frame)
        print(result)
        endtime=time.time()
        print(endtime-starttime)

        carnum,carLocationList=getCarLoc(result)
        if carnum>0:
            print(carnum)
            # cv2.imwrite('C:/Users/chezh/Documents/GitHub/Dump-truck-recognition/image/' + str(c) + '.jpg', frame)
            for item in carLocationList:
                cv2.rectangle(frame, item["topleft"], item["bottomright"], (55, 255, 155), 5)
                #上传文件到服务器
                cv2.imshow("capture", frame)
                # cv2.imwrite('C:/Users/chezh/PycharmProjects/opencv_project/image/' + str(c) + '.jpg', frame)
                # cv2.imwrite('C:/Users/chezh/Documents/GitHub/Dump-truck-recognition/image/' + str(c) + '.jpg', frame)

        # print(getCarLoc(result))
    cv2.imshow("capture", frame)
    c = c + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()