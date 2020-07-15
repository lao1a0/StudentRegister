# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'First.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import cv2
import requests
import json
import urllib
import base64
import pymysql
import os

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
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

        self.loop = 0

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
        self.timer_camera2.timeout.connect(self.hi)
        # self.button_close.clicked.connect(self.close)  # 若该按键被点击，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "相识"))
        self.open_camera.setText(_translate("Form", "打开相机"))
        self.label.setText(_translate("Form", "新生报道系统"))

    def button_open_camera_clicked(self):
        '''
         单击打开摄像头
        :return:
        '''
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                msg = QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QMessageBox.Ok)
            else:
                self.timer_camera.start(1)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
                self.timer_camera2.start(1500)
                # self.open_camera.setText('关闭相机')
                self.open_camera.hide()

    def label_show_camera(self):
        #
        # 在label中显示摄像头拍摄到的信息
        #
        flag, self.image = self.cap.read()  # 从视频流中读取

        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.show_camera.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def faceDetect(self,imgBase64,token):
        '''
        人脸检测与属性分析
        '''
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        request_url = request_url + "?access_token=" + token
        headers = {'Content-Type': 'application/json'}
        params = {"image": imgBase64, "image_type": "BASE64", "face_field": "age,beauty,expression,face_shape,gender"}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()

    def getToken(self):
        '''
        动态获得access_token
        :return:
        '''
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        AK = 'zu3BEDWdNEV5cvCNg8Ctmb7D'  # API Key
        SK = 'GFeWyalISBM139W95lMVpMH22xkBOBWe'  # Secret Key
        host = 'https://aip.baidubce.com/oauth/2.0/token'
        head = {'Content-Type': 'application/json; charset=UTF-8'}
        key = {'grant_type': 'client_credentials', 'client_id': AK, "client_secret": SK}
        request = requests.get(url=host, params=key, headers=head)
        content = request.json()
        # print( content['access_token'])
        if (content):
           return content['access_token']

    def Get_img_base64(self,imgPath):
        '''
        将图片进行base64编码
        :param imgPath:
        :return: 一串base64
        '''
        with open(imgPath, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            codee = base64_data.decode()
        return codee

    def Zh_cn(self,string):
        return string.encode("gbk").decode(errors="ignore")

    def Face_detection(self,imgPath):
        '''
        绘制人脸检测框
        :param imgPath:图片的地址
        :return:
        '''
        access_token = self.getToken()
        codee=self.Get_img_base64(imgPath=imgPath)
        result = self.faceDetect(imgBase64=codee, token=access_token)['result']
        face_list = result['face_list'][0]
        location = face_list['location']  # 获得人脸的大小
        img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
        leftTopX = int(location['left'])
        leftTopY = int(location['top'])
        rightBottomX = int(leftTopX + int(location['width']))
        rightBottomY = int(leftTopY + int(location['height']))
        # 绘制矩形
        cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (0, 255, 0), 2)
        cv2.imshow(self.Zh_cn('识别成功'), img)
        cv2.waitKey(0)

    def Get_a_shot(self):
        '''
        从视频流中获得一张图片
        :return:imgPath,flag
        '''
        flag, self.image = self.cap.read()  # 从视频流中读取
        num = 1
        cv2.imwrite("F:\Fac_picture\image" + str(num) + ".jpg", self.image)  # 保存一张图像
        strnum = str(num)
        imagenumber = 'image' + strnum
        imgPath = "F:\Fac_picture\\" + imagenumber + ".jpg"
        return imgPath,flag

    def Face_identification(self):
        '''
       人脸识别
           开启摄像头，相机自动捕获人脸照片保存到本地
           调用百度云api用本地的照片与云端的照片进行比对
           group_id_list:要更换为自己设置的人脸库中的组id
       :return:人脸识别后返回的json数据
       '''
        access_token = self.getToken()
        imgPath = self.Get_a_shot()[0]
        codee = self.Get_img_base64(imgPath=imgPath)
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search" + "?access_token=" + access_token
        params = "{\"image\":\"" + codee + "\",\"image_type\":\"BASE64\",\"group_id_list\":\"01\",\"quality_control\":\"LOW\",\"liveness_control\":\"NORMAL\"}"
        request = urllib.request.Request(url=request_url, data=params.encode(encoding='UTF8'))
        request.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(request)
        content = response.read()
        return content

    def label_show_camera2(self):
        #
        # 在label中显示摄像头拍摄到的信息
        #
        try:
            while True:
                imgPath, flag = self.Get_a_shot()
                print(flag)
                if not flag:
                    break
                self.Face_detection(imgPath)
                if  cv2.waitKey(1):
                    break
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)

        flag, self.image = self.cap.read()  # 从视频流中读取

        show = cv2.resize(self.image, (640, 480))
        # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        # 把读取到的视频数据变成QImage形式
        self.show_camera.setPixmap(QPixmap.fromImage(showImage))
        # 往显示视频的Label里 显示QImage

    def hi(self):
        '''
        检测人脸
        识别人脸
        :return:
        '''

        imgPath, flag = self.Get_a_shot()
        self.Face_detection(imgPath)
        cv2.destroyAllWindows()

        content = self.Face_identification()

        if content:
            temp = json.loads(content)
            print(temp)
            flag = temp["error_code"]
            if flag != 0:
                print("错误！")
                self.label_2.setAlignment(Qt.AlignCenter)
                self.label_2.setText("<font color=red>人脸识别度低，请寻找工作人员！</font>")
            else:
                print(temp["result"]['user_list'][0]['group_id'])
                print(temp["result"]['user_list'][0]['user_id'])
                print(temp["result"]['user_list'][0]['score'])

                self.label_2.clear()
                number = temp["result"]['user_list'][0]['user_id']
                # 获得自己设定的用户id-->学号
                numm = temp["result"]['user_list'][0]['score']
                # 获得匹配度
                if numm >= 80:  # 匹配度大于80就算是匹配成功
                    mainWindows.close()
                    self.timer_camera.stop()  # 关闭定时器
                    self.timer_camera2.stop()
                    self.cap.release()  # 释放视频流
                    self.show_camera.clear()  # 清空视频显示区域

                    Second.label.setPixmap(QPixmap("F:\Fac_picture\\" + number + ".jpg")) # 拿出本地库里的图片进行回显
                    Second.label.setScaledContents(True)  # 让图片自适应label大小

                    # 使用MySQL数据库
                    conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='test')
                    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                    cursor.execute("SELECT * FROM user WHERE 学号={}".format(number))

                    # print("SELECT * FROM user WHERE 学号={}".format(number))

                    p = cursor.fetchone()

                    Second.label_3.setText(p['学号'])
                    Second.label_7.setText(p['姓名'])
                    Second.label_9.setText(p['班级'])
                    Second.label_5.setText(p['学院'])

                    conn.commit()
                    cursor.close()
                    conn.close()

                    mainWindows2.show()
        else:
            print("未获得数据！")


class Ui_SecondForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(876, 550)

        # 添加显示照片的label
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 110, 161, 201)) # 设置画布
        self.label.setAlignment(QtCore.Qt.AlignCenter) # 文本居中
        self.label.setObjectName("label")

        # 添加重新拍拍照按钮
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(100, 430, 212, 51)) #设置按钮的大小和位置

        # 设置按钮的样式
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        # 添加打印按钮
        self.pushButton2 =QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(500,430,212,51))
            # 设置按钮的样式
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton2.setFont(font)
        self.pushButton2.setObjectName("pushButton2")


        # 新建一个画布
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(430, 60, 351, 311))
        self.widget.setObjectName("widget")
        # 添加网格布局
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName("gridLayout")
        # 在网格布局中添加label
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)

        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)

        self.label_8 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_9 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 1, 1, 1)

        # 设置背景图片
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("B.jpg")))
        Form.setPalette(palette)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 绑定信号与槽
        self.pushButton.clicked.connect(self.shut)
        self.pushButton2.clicked.connect(self.Print)

    def retranslateUi(self, Form):
        '''
        前端设置
        :param Form:
        :return:
        '''
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "相识"))

        self.pushButton2.setText(_translate("Form","打印"))
        self.pushButton.setText(_translate("Form", "重新拍照"))
        self.label_2.setText(_translate("Form", "学\t\t\t号："))

        self.label_4.setText(_translate("Form", "学\t\t\t院："))

        self.label_6.setText(_translate("Form", "姓\t\t\t名："))

        self.label_8.setText(_translate("Form", "班\t\t\t级："))

    def shut(self):
        '''
        重新拍照
        :return:
        '''
        mainWindows2.close()
        flag = ui.cap.open(ui.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
        if flag == False:  # flag表示open()成不成功
            msg = QMessageBox.warning(ui, 'warning', "请检查相机于电脑是否连接正确", buttons=QMessageBox.Ok)
        else:
            ui.timer_camera.start(1)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
            ui.timer_camera2.start(1500)
            # ui.button_open_camera.setText('关闭相机')
            mainWindows.show()

    def Print(self):
        '''
        打印信息
        :return:
        '''
        print("打开打印机")
        printer = QtPrintSupport.QPrinter()  # 创建一个打印对象
        painter = QtGui.QPainter()

        # 将绘制的目标重定向到打印机
        painter.begin(printer)
        screen = self.widget.grab()  # 获得打印屏幕
        painter.drawPixmap(10, 10, screen)
        painter.end()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("人脸识别.png"))

    mainWindows = QtWidgets.QMainWindow()
    mainWindows2 = QtWidgets.QMainWindow()

    ui = Ui_FirstForm()
    Second = Ui_SecondForm()
    #向主窗口添加控件
    ui.setupUi(mainWindows)
    Second.setupUi(mainWindows2)
    mainWindows.show()

    sys.exit(app.exec_())