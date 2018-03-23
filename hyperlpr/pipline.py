#coding=utf-8

from . import  finemapping  as  fm
import cv2
from . import typeDistinguish as td
from . import e2e
from . import finemapping_vertical as fv
from . import detect
def RecognizePlateDict(image,model):
    images = detect.detectPlateRough(image,image.shape[0],top_bottom_padding_rate=0.1)
    jsons = []

    for j,plate in enumerate(images):
        plate,rect,origin_plate =plate
        cv2.imshow("origin_plate",origin_plate)
        # cv2.imshow("plate",plate)
        cv2.waitKey(0)
        res, confidence = e2e.recognizeOne(origin_plate,model)
        print("res",res)
        # cv2.imshow("origin_plate",origin_plate)
        # cv2.imwrite("./"+str(j)+"_rough.jpg",plate)

        # print "车牌类型:",ptype
        # plate = cv2.cvtColor(plate, cv2.COLOR_RGB2GRAY)
        plate  =cv2.resize(plate,(136,int(36*2.5)))


        ptype = td.SimplePredict(plate)



        if ptype>0 and ptype<4:
            plate = cv2.bitwise_not(plate)
        # demo = verticalEdgeDetection(plate)

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)
        image_rgb = fv.finemappingVertical(image_rgb)
        # print(image_rgb.shape)
        # cv2.imshow("image_rgb",image_rgb)
        # print time.time() - t1,"校正"
        print("e2e:",e2e.recognizeOne(image_rgb,model)[0])
        image_gray = cv2.cvtColor(image_rgb,cv2.COLOR_BGR2GRAY)

        # cv2.imwrite("./"+str(j)+".jpg",image_gray)
        # image_gray = horizontalSegmentation(image_gray)


        res, confidence = e2e.recognizeOne(image_rgb,model)
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
    return image_rgb,jsons




