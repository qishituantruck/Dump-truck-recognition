#coding=utf-8

from . import  finemapping  as  fm
import cv2
from . import typeDistinguish as td
from . import e2e
from . import finemapping_vertical as fv
from . import detect
import os
import numpy
from . import segmentation

def SimpleRecognizePlateWithGui(image,model):


    images = detect.detectPlateRough(
        image, image.shape[0], top_bottom_padding_rate=0.1)

    res_set = []
    for j, plate in enumerate(images):
        plate, rect, origin_plate = plate
        plate = cv2.resize(plate, (136, 36 * 2))


        plate_color = "蓝"
        plate_type = td.SimplePredict(plate)

        if (plate_type > 0) and (plate_type < 5):
            plate = cv2.bitwise_not(plate)
            plate_color = "黄"

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)

        image_rgb = fv.finemappingVertical(image_rgb)


        e2e_plate, e2e_confidence = e2e.recognizeOne(image_rgb,model)
        #print("e2e:", e2e_plate, e2e_confidence)

        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        #print("校正", time.time() - t1, "s")


        val = segmentation.slidingWindowsEval(image_gray)
        # print val
        #print("分割和识别", time.time() - t2, "s")
        # block_
        if len(val) == 3:
            blocks, res, confidence = val
            if confidence / 7 > 0.7:

                for i, block in enumerate(blocks):

                    block_ = cv2.resize(block, (24, 24))
                    block_ = cv2.cvtColor(block_, cv2.COLOR_GRAY2BGR)
                    # print(block_.shape)
                    image[j * 24:(j * 24) + 24, i * 24:(i * 24) + 24] = block_
                    if image[j * 24:(j * 24) + 24,
                             i * 24:(i * 24) + 24].shape == block_.shape:
                        pass

                res_set.append([res,
                                confidence / 7,
                                rect,
                                plate_color,
                                e2e_plate,
                                e2e_confidence,
                                len(blocks)])
    #print(time.time() - t0, "s")

    return image, res_set



def RecognizePlateDict(image,model):

    images = detect.detectPlateRough(image,image.shape[0],top_bottom_padding_rate=0.1)
    # cv2.imshow("images0",images[0])
    jsons = []
    randomByteArray = bytearray(os.urandom(14688))
    # 把数组赋值给OpenCV类型矩阵
    flatNumpyArray = numpy.array(randomByteArray)

    # 矩阵变维, 1维变维2维(灰度), 1维变为3维(彩色)

    image_rgb = flatNumpyArray.reshape(36, 136, 3)


    for j,plate in enumerate(images):
        plate,rect,origin_plate =plate

        # cv2.imshow("origin_plate",origin_plate)

        # cv2.imshow("plate",plate)
        # cv2.waitKey(0)
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
        print(image_rgb.shape)
        # cv2.imshow("image_rgb",image_rgb)
        # print time.time() - t1,"校正"
        # print("e2e:",e2e.recognizeOne(image_rgb,model)[0])
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




