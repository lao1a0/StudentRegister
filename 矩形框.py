# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'First.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
import cv2
import requests
import json
import urllib
import base64
import pymysql
import os

from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_FirstForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1069, 767)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("B.jpg")))
        Form.setPalette(palette)

        self.timer_camera = QtCore.QTimer()
        self.timer_camera2 = QtCore.QTimer()

        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0

        self.show_camera = QtWidgets.QLabel(Form)
        self.show_camera.setGeometry(QtCore.QRect(194, 160, 681, 481))
        self.show_camera.setAlignment(QtCore.Qt.AlignCenter)
        self.show_camera.setObjectName("show_camera")
        self.show_camera.setPixmap(QPixmap("image.jpg"))
        self.open_camera = QtWidgets.QPushButton(Form)
        self.open_camera.setGeometry(QtCore.QRect(414, 680, 241, 51))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.open_camera.setFont(font)
        self.open_camera.setObjectName("open_camera")
        self.label = QtWidgets.QLabel(Form)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(399, 50, 271, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QtCore.QRect(286, 95, 500, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")

        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.open_camera.clicked.connect(self.button_open_camera_clicked)  # 若该按键被点击，则调用button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.label_show_camera)  # 若定时器结束，则调用show_camera()
        # self.button_close.clicked.connect(self.close)  # 若该按键被点击，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "相识"))
        self.open_camera.setText(_translate("Form", "打开相机"))

        self.label.setText(_translate("Form", "新生报道系统"))
        # self.label_2.setText(_translate("Form", "人脸识别度低，请寻找工作人员！"))

    def get_Token(self):
        # 动态获取Access Token
        AK = 'zu3BEDWdNEV5cvCNg8Ctmb7D'
        SK = 'GFeWyalISBM139W95lMVpMH22xkBOBWe'
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK, SK)
        response = requests.get(host)
        return response.json()['access_token']


    def button_open_camera_clicked(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                msg = QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QMessageBox.Ok)
            else:
                self.timer_camera.start(500)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示

                # self.open_camera.setText('关闭相机')
                self.open_camera.hide()

    def label_show_camera(self):
        flag, self.image = self.cap.read()  # 从视频流中读取
        num = 1

        cv2.imwrite("F:\Face_picture2\image" + str(num) + ".jpg", self.image)  # 保存一张图像
        strnum = str(num)
        imagenumber = 'image' + strnum
        with open("F:\Face_picture2\\" + imagenumber + ".jpg", 'rb') as f:
            base64_data = base64.b64encode(f.read())
            codee = base64_data.decode()
            num += 1

        access_token = self.get_Token()

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        request_url = request_url + "?access_token=" + access_token
        headers = {'Content-Type': 'application/json'}
        params = {"image": codee, "image_type": "BASE64", "face_field": "age,beauty,expression,face_shape,gender"}
        response = requests.post(request_url, data=params, headers=headers)

        result = response.json()['result']
        print(result)


        face_list = result['face_list'][0]
        location = face_list['location']  # 获得人脸的大小

        img = cv2.imread("F:\Face_picture2\\" + imagenumber + ".jpg", cv2.IMREAD_COLOR)

        leftTopX = int(location['left'])
        leftTopY = int(location['top'])
        rightBottomX = int(leftTopX + int(location['width']))
        rightBottomY = int(leftTopY + int(location['height']))
        # 绘制矩形
        cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (0, 255, 0), 2)
        gender = face_list['gender']['type']
        age = face_list['age']
        cv2.putText(img, "{}:{}".format(gender, age),(leftTopX, rightBottomY-20), fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=0.5, color=(255, 0, 0))

        show = cv2.resize(img, (640, 480))  # 把读到的帧的大小重新设置为 640x480

        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色

        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.show_camera.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImag

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("人脸识别.png"))

    mainWindows = QMainWindow()
    mainWindows2 = QMainWindow()

    ui = Ui_FirstForm()

    #向主窗口添加控件
    ui.setupUi(mainWindows)

    mainWindows.show()

    sys.exit(app.exec_())