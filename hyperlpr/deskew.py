#coding=utf-8
import numpy as np
import cv2
import time
from matplotlib import pyplot as plt
import math

from scipy.ndimage import filters
#
# def strokeFiter():
#     pass;

def angle(x,y):
    return int(math.atan2(float(y),float(x))*180.0/3.1415)




def v_rot(img, angel, shape, max_angel):
    size_o = [shape[1],shape[0]]
    size = (shape[1]+ int(shape[0]*np.cos((float(max_angel )/180) * 3.14)),shape[0])
    interval = abs( int( np.sin((float(angel) /180) * 3.14)* shape[0]))
    pts1 = np.float32([[0,0],[0,size_o[1]],[size_o[0],0],[size_o[0],size_o[1]]])
    if(angel>0):
        pts2 = np.float32([[interval,0],[0,size[1]  ],[size[0],0  ],[size[0]-interval,size_o[1]]])
    else:
        pts2 = np.float32([[0,0],[interval,size[1]  ],[size[0]-interval,0  ],[size[0],size_o[1]]])

    M  = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,size)
    return dst,M


def skew_detection(image_gray):
    h, w = image_gray.shape[:2]
    eigen = cv2.cornerEigenValsAndVecs(image_gray,12, 5)
    angle_sur = np.zeros(180,np.uint)
    eigen = eigen.reshape(h, w, 3, 2)
    flow = eigen[:,:,2]
    vis = image_gray.copy()
    vis[:] = (192 + np.uint32(vis)) / 2
    d = 12
    points =  np.dstack( np.mgrid[d/2:w:d, d/2:h:d] ).reshape(-1, 2)
    for x, y in points:
        vx, vy = np.int32(flow[int(y), int(x)]*d)
        # cv2.line(rgb, (x-vx, y-vy), (x+vx, y+vy), (0, 355, 0), 1, cv2.LINE_AA)
        ang = angle(vx,vy)
        angle_sur[(ang+180)%180] +=1

    # torr_bin = 30
    angle_sur = angle_sur.astype(np.float)
    angle_sur = (angle_sur-angle_sur.min())/(angle_sur.max()-angle_sur.min())
    angle_sur = filters.gaussian_filter1d(angle_sur,5)
    skew_v_val =  angle_sur[20:180-20].max()
    skew_v = angle_sur[30:180-30].argmax() + 30
    skew_h_A = angle_sur[0:30].max()
    skew_h_B = angle_sur[150:180].max()
    skew_h = 0
    if (skew_h_A > skew_v_val*0.3 or skew_h_B > skew_v_val*0.3):
        if skew_h_A>=skew_h_B:
            skew_h = angle_sur[0:20].argmax()
        else:
            skew_h = - angle_sur[160:180].argmax()
    return skew_h,skew_v


def fastDeskew(image):
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    skew_h,skew_v = skew_detection(image_gray)
    print("校正角度 h ",skew_h,"v",skew_v)
    deskew,M = v_rot(image,int((90-skew_v)*1.5),image.shape,60)
    return deskew,M



if __name__ == '__main__':
    fn = './dataset/0.jpg'

    img = cv2.imread(fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    skew_h,skew_v = skew_detection(gray)
    img = v_rot(img,(90-skew_v ),img.shape,60)
    # img = h_rot(img,skew_h)
    # if img.shape[0]>img.shape[1]:
    #     img = h_rot(img, -90)

    plt.show()
    cv2.waitKey()
