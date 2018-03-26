from darkflow.net.build import TFNet
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QDir,QThread,pyqtSignal
import sys
import cv2
import os
from hyperlpr import pipline as pp
import numpy as np
import time
from util.CarLocation import getCarLoc

from hyperlpr import e2emodel as model

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
        MainWindow.resize(1110, 623)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 50, 741, 511))
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
        self.label_3.setGeometry(QtCore.QRect(800, 70, 54, 12))
        self.label_3.setObjectName("label_3")

        #显示车牌图
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(880, 70, 191, 51))
        self.label_4.setObjectName("label_4")


        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(800, 170, 54, 12))
        self.label_5.setObjectName("label_5")


        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 9, 331, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(880, 170, 191, 41))

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

        self.video_path=""



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def initPlateRecongizer(self):
        pred_model = model.construct_model("./model/ocr_plate_all_w_rnn_2.h5", )
        return pred_model
    def initYolo2(self):
        options = {"model": "cfg/tiny-yolo-voc.cfg", "load": "model/tiny-yolo-voc.weights", "threshold": 0.1,
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
        print("处理图片！！")
        if self.platenum<len(self.image_filename_list):
            print(self.platenum)
            path = self.imagefilepath + "/" + self.image_filename_list[self.platenum]
            print("路径：" + path)
            image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
            image_rgb, res_set = pp.RecognizePlateDict(image, self.plateRecong)

            # print(res_set)

            show = cv2.resize(image, (640, 480))

            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))

            image_rgb = cv2.resize(image_rgb, (191, 51))
            plate_img = QtGui.QImage(
                image_rgb.data,
                image_rgb.shape[1],
                image_rgb.shape[0],
                image_rgb.shape[1] *
                image_rgb.shape[2],
                QtGui.QImage.Format_RGB888)
            self.label_4.setPixmap(
                QtGui.QPixmap.fromImage(plate_img.rgbSwapped()))
            if len(res_set)!=0:

                self.lineEdit_2.setText(res_set[0]["Name"])



            else:
                self.lineEdit_2.setText("未检测到！")
            self.platenum += 1
        else:
            self.timer_plate.stop()


    def button_recongnizer_click(self):

        if self.timer_plate.isActive()==False:
            self.timer_plate.start(1000)

            self.imagefilepath = "./image"
            self.image_filename_list = []
            name_list = os.listdir(self.imagefilepath)  # 列出文件夹下所有的目录与文件
            self.image_filename_list.clear()
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

            if self.number%15==0:

                result = self.tfnet.return_predict(self.image)

                carnum, carLocationList = getCarLoc(result)
                if carnum > 0:
                    print(carnum)
                    currenttime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                    cv2.imwrite('./image/' + currenttime + '.jpg', self.image)
                for item in carLocationList:
                    cv2.rectangle(self.image, item["topleft"], item["bottomright"], (55, 255, 155), 5)
                #     # 上传文件到服务器
                #     # cv2.imshow("capture", self.image)
                #     cv2.imwrite('./image/' + str(self.number) + '.jpg', self.image)
                    # cv2.imwrite('C:/Users/chezh/Documents/GitHub/Dump-truck-recognition/image/' + str(c) + '.jpg', frame)
            # print(getCarLoc(result))
            # print("目标检测")
        # print("here!!")
            show = cv2.resize(self.image, (640, 480))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))
            self.number += 1
        else:
            self.timer_camera.stop()



    def closeEvent(self, event):
        print("关闭！！")
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")

        msg.addButton(ok,QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "视频目录："))
        self.pushButton.setText(_translate("MainWindow", "选择新的视频"))
        self.pushButton_2.setText(_translate("MainWindow", "开始检测"))
        self.label_3.setText(_translate("MainWindow", "车牌图片："))
        # self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "识别结果："))
        self.pushButton_3.setText(_translate("MainWindow", "批量识别"))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())