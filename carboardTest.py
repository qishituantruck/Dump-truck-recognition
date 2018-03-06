import cv2
import numpy as np
img=cv2.imread("C:/Users/chezh/PycharmProjects/opencv_project/image/8.jpg")
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray",gray)
gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
median = cv2.medianBlur(gaussian, 5)
# cv2.imshow("median",median)

sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0,  ksize = 3)
# cv2.imshow("sobel",sobel)

ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
# cv2.imshow("binary",binary)

# 膨胀和腐蚀操作的核函数
element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 6))
# 膨胀一次，让轮廓突出
dilation = cv2.dilate(binary, element2, iterations = 1)
# cv2.imshow("dilation",dilation)
# 腐蚀一次，去掉细节
erosion = cv2.erode(dilation, element1, iterations = 1)
# cv2.imshow("erosion",erosion)
# 再次膨胀，让轮廓明显一些
dilation2 = cv2.dilate(erosion, element2,iterations = 3)
cv2.imshow("dilation2",dilation2)

def findPlateNumberRegion(img):
    region = []
    # 查找轮廓

    image,contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    # 筛选面积小的

    for i in range(len(contours)):
        cnt = contours[i]

        # 计算该轮廓的面积

        area = cv2.contourArea(cnt)
        print(area)
        # 面积小的都筛选掉
        if (area < 2000):
            continue

        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        # print("rect is: ")
        # print(rect)

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 车牌正常情况下长高比在2.7-5之间
        ratio =float(width) / float(height)
        if (ratio > 5 or ratio < 2):
            continue

        region.append(box)

    return region

region=findPlateNumberRegion(dilation2)
# print("region:")
# print(region)

for box in region:

    cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
    ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
    xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    x1 = box[xs_sorted_index[0], 0]
    x2 = box[xs_sorted_index[3], 0]

    y1 = box[ys_sorted_index[0], 1]
    y2 = box[ys_sorted_index[3], 1]

    img_org2 = img.copy()
    img_plate = img_org2[y1:y2, x1:x2]
    cv2.imshow('number plate', img_plate)
    cv2.imwrite('number_plate.jpg', img_plate)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)

    # 带轮廓的图片
    cv2.imwrite('contours.png', img)

cv2.waitKey(0)