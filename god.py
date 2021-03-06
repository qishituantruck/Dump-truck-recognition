from darkflow.net.build import TFNet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QDir,QThread,pyqtSignal
import sys
import cv2
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from hyperlpr import pipline as pp
import numpy as np
import numpy
import time
from util.CarLocation import getCarLoc,getproperplatenum
from util.uploadimg import ftp_upload

from hyperlpr import e2emodel as model

fontC = ImageFont.truetype("./Font/platech.ttf", 14, 0);


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.timer_plate=QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.setupUi(Ui_MainWindow)
        self.plateRecong=self.initPlateRecongizer()
        self.tfnet=self.initYolo2()
        self.number=0
        self.platenum=0

    def setupUi(self, QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1302, 603)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 50, 931, 531))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 54, 12))
        self.label.setObjectName("label")


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(970, 70, 54, 12))
        self.label_3.setObjectName("label_3")

        # 显示车牌图
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1040, 60, 191, 51))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(970, 310, 54, 20))
        self.label_5.setObjectName("label_5")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 9, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(1040, 300, 191, 41))

        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_2.setFont(QtGui.QFont("黑体", 24, QtGui.QFont.Bold))

        self.lineEdit_2.setStyleSheet("color:red")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 10, 75, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_3.clicked.connect(self.button_recongnizer_click)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton.setGeometry(QtCore.QRect(430, 10, 81, 31))

        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.select_new_dir)

        self.timer_camera.timeout.connect(self.show_camera)

        self.timer_plate.timeout.connect(self.deal_pictures)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton_2.setGeometry(QtCore.QRect(550, 10, 75, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.button_open_camera_click)
        # self.pushButton_2.clicked.connect(self.button_open_camera_click)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(970, 200, 54, 12))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1040, 190, 191, 51))

        self.label_7.setObjectName("label_7")


        self.video_path = ""

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def initPlateRecongizer(self):
        pred_model = model.construct_model("./model/ocr_plate_all_w_rnn_2.h5", )
        return pred_model
    def initYolo2(self):
        # options = {"model": "cfg/tiny-yolo-voc.cfg", "load": "model/tiny-yolo-voc.weights", "threshold": 0.1,
        #            "gpu": 0.7}
        options = {"model": "cfg/tiny-yolo-voc-truck.cfg", "load": "model/tiny-yolo-voc-truck_8000.weights", "threshold": 0.4,
                   "gpu": 0.7}
        tfnet = TFNet(options)
        return tfnet
    def select_new_dir(self):

        # self.lineEdit.setText(QFileDialog.getExistingDirectory(self, "读取文件夹", QDir.currentPath()))
        filepath,filetype=QFileDialog.getOpenFileName(self,"读取文件",QDir.currentPath(),'Image Files(*.mp4)')

        self.lineEdit.setText(filepath)

        self.video_path=filepath

        # print(filepath)

    def deal_pictures(self):


        if self.platenum<len(self.image_filename_list):
            print(self.platenum)
            path = self.imagefilepath + "/" + self.image_filename_list[self.platenum]
            print("路径：" + path)
            showimage=cv2.imread(path)
            fullimage = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)

            image, res_set = pp.SimpleRecognizePlateWithGui(fullimage, self.plateRecong)

            print(res_set)
            img = QtGui.QImage(
                showimage.data,
                showimage.shape[1],
                showimage.shape[0],
                showimage.shape[1] *
                showimage.shape[2],
                QtGui.QImage.Format_RGB888)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(img.rgbSwapped()))

            if len(res_set) > 0:

                curr_rect = res_set[0][2]
                image_crop = image[int(curr_rect[1]):int(
                    curr_rect[1] + curr_rect[3]), int(curr_rect[0]):int(curr_rect[0] + curr_rect[2])]
                curr_plate = cv2.resize(image_crop, (136, 72))
                plate_img = QtGui.QImage(
                    curr_plate.data,
                    curr_plate.shape[1],
                    curr_plate.shape[0],
                    curr_plate.shape[1] *
                    curr_plate.shape[2],
                    QtGui.QImage.Format_RGB888)
                self.label_4.setPixmap(
                    QtGui.QPixmap.fromImage(plate_img.rgbSwapped()))

                # print(res_set[0][6])
                block_crop = image[0:24, 0:(24 * int(res_set[0][6]))]
                curr_block = cv2.resize(
                    block_crop, (24 * int(res_set[0][6]), 24))
                block_image = QtGui.QImage(
                    curr_block.data,
                    curr_block.shape[1],
                    curr_block.shape[0],
                    curr_block.shape[1] *
                    curr_block.shape[2],
                    QtGui.QImage.Format_RGB888)
                self.label_7.setPixmap(
                    QtGui.QPixmap.fromImage(block_image.rgbSwapped()))
                platenum=getproperplatenum(res_set)
                self.lineEdit_2.setText(platenum)
                print("开始上传服务器！")
                ftp_upload('./image/'+self.image_filename_list[self.platenum],platenum+'/'+self.image_filename_list[self.platenum])
                # if os.path.exists('./image/'+self.image_filename_list[self.platenum]):
                #
                #     os.remove('./image/'+self.image_filename_list[self.platenum])
                #         # os.unlink(my_file)
                # else:
                #     print('no such file!')
            else:
                print("未检测到！")
                randomByteArray = bytearray(os.urandom(14688))
                # 把数组赋值给OpenCV类型矩阵
                flatNumpyArray = numpy.array(randomByteArray)

                # 矩阵变维, 1维变维2维(灰度), 1维变为3维(彩色)

                image_rgb = flatNumpyArray.reshape(36, 136, 3)

                curr_plate = cv2.resize(image_rgb, (136, 72))
                plate_img = QtGui.QImage(
                    curr_plate.data,
                    curr_plate.shape[1],
                    curr_plate.shape[0],
                    curr_plate.shape[1] *
                    curr_plate.shape[2],
                    QtGui.QImage.Format_RGB888)
                self.label_4.setPixmap(
                    QtGui.QPixmap.fromImage(plate_img.rgbSwapped()))

                # print(res_set[0][6])
                print("here!")
                curr_block = cv2.resize(
                    image_rgb, (136, 72))
                block_image = QtGui.QImage(
                    curr_block.data,
                    curr_block.shape[1],
                    curr_block.shape[0],
                    curr_block.shape[1] *
                    curr_block.shape[2],
                    QtGui.QImage.Format_RGB888)
                self.label_7.setPixmap(
                    QtGui.QPixmap.fromImage(block_image.rgbSwapped()))
                self.lineEdit_2.setText("未检测到！")

                # self.license_plate_widget.clear()
                # self.block_plate_widget.clear()
                # self.segmentation_recognition_edit.setText("")
                # self.filename_edit.setText("")
                # self.confidence_edit.setText("")
                # self.plate_color_edit.setText("")
                # self.e2e_recognization_edit.setText("")
                # self.e2e_confidence_edit.setText("")

            # show = cv2.resize(image, (924, 520))
            #
            # show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            # showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            # self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))
            #
            # image_rgb = cv2.resize(image_rgb, (191, 51))
            # plate_img = QtGui.QImage(
            #     image_rgb.data,
            #     image_rgb.shape[1],
            #     image_rgb.shape[0],
            #     image_rgb.shape[1] *
            #     image_rgb.shape[2],
            #     QtGui.QImage.Format_RGB888)
            # self.label_4.setPixmap(
            #     QtGui.QPixmap.fromImage(plate_img.rgbSwapped()))

            # if len(res_set)!=0:
            #
            #     plate = res_set[0]
            #     platenumber = plate["Name"]
            #     x = plate["x"]
            #     y = plate["y"]
            #     w = plate["w"]
            #     h = plate["h"]
            #     cv2.rectangle(image, (x, y), (x + w, y + h), (55, 255, 155), 5)
            #     # font = cv2.FONT_HERSHEY_SIMPLEX
            #
            #     img = Image.fromarray(image)
            #     draw = ImageDraw.Draw(img)
            #     # draw.text((int(rect[0]+1), int(rect[1]-16)), addText.decode("utf-8"), (255, 255, 255), font=fontC)
            #     draw.text((x, y-10), platenumber, (255, 255, 255), font=fontC)
            #     imagex = np.array(img)
            #     # cv2.putText(image, platenumber, (x, y - 10), font, 1, (55, 255, 155), 2, cv2.LINE_AA)

            #     cv2.imwrite('./cache/'+self.image_filename_list[self.platenum], imagex)
            #     ftp_upload('./cache/'+self.image_filename_list[self.platenum],platenumber+'/'+self.image_filename_list[self.platenum])
            #
            #     if os.path.exists('./cache/'+self.image_filename_list[self.platenum]):
            #         # 删除文件，可使用以下两种方法。
            #         os.remove('./cache/'+self.image_filename_list[self.platenum])
            #         # os.unlink(my_file)
            #     else:
            #         print('no such file!')
            #     # 上传
            #     self.lineEdit_2.setText(res_set[0]["Name"])
            # else:
            #     self.lineEdit_2.setText("未检测到！")


            self.platenum += 1

        else:
            self.timer_plate.stop()
            self.platenum = 0


    def button_recongnizer_click(self):

        if self.timer_plate.isActive()==False:
            self.timer_plate.start(1000)
            self.imagefilepath = "./image"
            self.image_filename_list = []
            name_list = os.listdir(self.imagefilepath)  # 列出文件夹下所有的目录与文件
            for i in range(0, len(name_list)):
                if name_list[i].endswith(".jpg"):
                    self.image_filename_list.append(name_list[i])
            self.image_filename_list.sort()
            print(self.image_filename_list)
        else:
            self.timer_plate.stop()

    def button_open_camera_click(self):

        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.video_path)
            self.timer_camera.start(33)


        else:
            self.timer_camera.stop()
            self.cap.release()


    def show_camera(self):


        flag, self.image = self.cap.read()
        # face = self.face_detect.align(self.image)
        # if face:
        #     pass
        if flag:
            self.image = cv2.resize(self.image, (924, 520))

            result = self.tfnet.return_predict(self.image)
            carnum, carLocationList = getCarLoc(result)

            if carnum > 0:
                currenttimes=0
                topleft_x=0
                topleft_y=0
                bottomright_x=0
                bottomright_y=0
                    # cv2.imwrite('./image/' + currenttime + '.jpg', self.image)
                for item in carLocationList:
                    topleft_x = item["topleft"][0]
                    topleft_y = item["topleft"][1]
                    bottomright_x = item["bottomright"][0]
                    bottomright_y = item["bottomright"][1]
                    currenttimes = (bottomright_x - topleft_x)/(bottomright_y - topleft_y)
                    cv2.rectangle(self.image, item["topleft"], item["bottomright"], (0, 0, 255), 5)

                #     # 上传文件到服务器
                #     # cv2.imshow("capture", self.image)
                #     cv2.imwrite('./image/' + str(self.number) + '.jpg', self.image)



                # if self.number%15==0 and currenttimes<2 and topleft_x >= 40 and topleft_y >= 0 and bottomright_x <= 700 and bottomright_y <= 400 :
                if self.number % 15 == 0 and currenttimes<2 and topleft_x>=10 and bottomright_y<450:
                    currenttime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                    cv2.imwrite('./image/' + currenttime + '.jpg', self.image)
                    # cv2.imwrite('C:/Users/chezh/Documents/GitHub/Dump-truck-recognition/image/' + str(c) + '.jpg', frame)
            # print(getCarLoc(result))
            # print("目标检测")
        # print("here!!")
        #     show = cv2.resize(self.image, (804, 452))
            show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))
            self.number += 1
        else:
            self.timer_camera.stop()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "视频目录："))
        self.pushButton.setText(_translate("MainWindow", "选择新的视频"))
        self.pushButton_2.setText(_translate("MainWindow", "开始检测"))
        self.label_3.setText(_translate("MainWindow", "粗定位："))
        self.label_5.setText(_translate("MainWindow", "识别结果："))
        self.pushButton_3.setText(_translate("MainWindow", "批量识别"))
        self.label_6.setText(_translate("MainWindow", "精定位："))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())