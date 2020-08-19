# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.13.0
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
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from 语音合成 import *

from 测温 import thermometry

UserNumber=""
class Ui_FirstForm(object):
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1069, 767)

        # 窗口背景设置
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("B.jpg")))
        Form.setPalette(palette)

        self.timer_camera = QtCore.QTimer()         # 定时器timer_camear为每次从摄像头取画面的间隔
        self.timer_camera2 = QtCore.QTimer()        # 定时器timer_camear2从摄像头取画面进行"人脸识别"的时间

        self.cap = cv2.VideoCapture()               #打开摄像头，若参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
        self.CAM_NUM = 0

        # Qt Designer自动生成控件及布局代码

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

        # 信号与槽进行绑定
        self.open_camera.clicked.connect(self.button_open_camera_clicked)     # 若该按键被点击，则调用button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.label_show_camera)             # 若定时器结束，则调用show_camera()
        self.timer_camera2.timeout.connect(self.recognition)
        # self.button_close.clicked.connect(self.close)                       # 若该按键被点击，则关闭程序
    
    # 一些固定文字控件的标题的设定
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "相识"))
        self.open_camera.setText(_translate("Form", "打开相机"))

        self.label.setText(_translate("Form", "新生报道系统"))
        # self.label_2.setText(_translate("Form", "人脸识别度低，请寻找工作人员！"))

    # 获取你的access_token
    def get_Token(self):
        # AK = 'P6pS6GX1ke3PcfvG4wmU1s2l'                # 填写的你API Key
        # SK = 'T8K1m9wpFvgT8xCOVO05WpnaM5ubnF8w'        # 填写你的Secret Key
        AK = 'zu3BEDWdNEV5cvCNg8Ctmb7D'  # API Key
        SK = 'GFeWyalISBM139W95lMVpMH22xkBOBWe'  # Secret Key
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK, SK)
        response = requests.get(host)
        return response.json()['access_token']

    def start_camera(self):
        flag = self.cap.open(self.CAM_NUM)      # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
        if flag == False:                       # 如果打开摄像头不成功
            msg = QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QMessageBox.Ok)
        else:
            self.timer_camera.start(30)         # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
            self.timer_camera2.start(3000)


    def button_open_camera_clicked(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            self.start_camera()
            # 加载人脸数据(人脸特征)，用于绘制人脸框
            self.face_cascase = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

            # self.open_camera.setText('关闭相机')
            self.open_camera.hide()              # 隐藏这个button

    # 绘制人脸框
    def paint_rectangle(self, image):
        # 得到每一帧->图像计算
        # 灰度转换：转换成灰度的图计算强度得以降低
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 对比 摄像头采集到的数据 -> 人脸特征训练集
        faces = self.face_cascase.detectMultiScale(gray, 1.3, 3)

        for (x, y, w, h) in faces:
            # 在窗口当中标识人脸 画一个矩形
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

        return image

    def label_show_camera(self):
        flag, self.image = self.cap.read()  # 从视频流中读取一帧图像给self.image

        show = cv2.resize(self.image, (640, 480))  # 把读到的帧的大小重新设置为 640x480

        imag = self.paint_rectangle(show)

        imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色

        showImage = QImage(imag.data, imag.shape[1], imag.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.show_camera.setPixmap(QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImag

    # 利用WxPusher公众号发送信息
    def Get_Uid(self,name):
        p = self.use_mysql("SELECT * FROM teacher WHERE 姓名='{}'".format(name))
        uid = p['UID']
        return uid
        
    def message_send(self, s_name,t_name):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        url = 'http://wxpusher.zjiecode.com/api/send/message'
        # //内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown
        params = {
            "appToken": "AT_8B6A2kdNHmNo7oYcPpsbgeQlK7l06KDm", # 消息发送方
            "content": "{}同学已完成报到".format(s_name) + '\n' + '时间:' + now_time,
            "contentType": 1,
            "uids": [self.Get_Uid(t_name)], # 指定的消息接收方
            "url": ""
        }
        params = json.dumps(params)

        # print(type(params))

        headers = {
            'Content-Type': "application/json",
        }

        html = requests.post(url, data=params, headers=headers)
        # print(html.text)

    # 借助百度智能云api完成人脸识别(搜索)
    def baidu_search(self, codee):
        url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        request_url = url + "?access_token=" + self.get_Token()

        params = {
            "image": codee,
            "image_type": "BASE64",
            "group_id_list": "1",
            "quality_control": "LOW",
            "liveness_control": "NORMAL"
        }

        headers = {
            'Content-Type': "application/json",
        }

        response = requests.post(url=request_url, data=params, headers=headers)
        return response.json()

    # 关闭摄像头，清空第一个窗口显示的图像
    def close_area(self):
        self.timer_camera.stop()  # 关闭定时器
        self.timer_camera2.stop()
        self.cap.release()  # 释放视频流
        self.show_camera.clear()  # 清空视频显示区域

    def use_mysql(self, sql):
        # 使用MySQL数据库
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='123', db='test')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        p = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()

        return p

    def recognition(self):
        global UserNumber
        flag, self.image = self.cap.read()  # 从视频流中读取
        num = 1

        cv2.imwrite("/home/pi/Pictures/Face_picture/image" + str(num) + ".jpg", self.image)  # 保存一张图像
        strnum = str(num)
        imagenumber = 'image' + strnum
        with open("/home/pi/Pictures/Face_picture/" + imagenumber + ".jpg", 'rb') as f:
            base64_data = base64.b64encode(f.read())
            codee = base64_data.decode()
            num += 1

        content = self.baidu_search(codee)

        if content:
            self.label_2.clear()         # 清理上一次的警告信息
            print(content)             # content为返回信息
            flag = content["error_code"]

            if flag != 0:
                if flag == 223114:
                    Baidu_Speak("人脸模糊")
                if flag == 223120:
                    Baidu_Speak("活体检测未通过")
                if flag == 223122:
                    Baidu_Speak("请勿遮挡右眼")
                if flag == 223121:
                    Baidu_Speak("请勿遮挡左眼")
                self.label_2.setText("<font color=red>人脸识别度低，请寻找工作人员！</font>")
            else:
                number = content["result"]['user_list'][0]['user_id']
                numm = content["result"]['user_list'][0]['score']
                if numm >= 80:
                    mainWindows.close()

                    self.close_area()

                    Second.label.setPixmap(QPixmap("/home/pi/Pictures/Face_local/" + number + ".jpg"))
                    Second.label.setScaledContents(True)  # 让图片自适应label大小

                    Second.label_14.setPixmap(QPixmap("/home/pi/Pictures/map_local/" + number + ".png"))
                    Second.label_14.setScaledContents(True)  # 让图片自适应label大小


                    p = self.use_mysql("SELECT * FROM user WHERE 学号 ={}".format(number))

                    Second.label_3.setText(p['姓名'])
                    Second.label_5.setText(p['学号'])
                    Second.label_7.setText(p['班级'])
                    Second.label_9.setText(p['学院'])
                    Second.label_11.setText(p['宿舍'])
                    Second.label_13.setText(p['辅导员'])

                    self.message_send(p['姓名'],p['辅导员'])
                    UserNumber=p['学号']
                    mainWindows2.show()
        else:
            print("未正确调用百度云api,请检查相关代码!")


class Ui_SecondForm(object):
    global UserNumber
    def Set_Background(self,Form,image):
        # 设置窗口背景
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(image)))
        Form.setPalette(palette)
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 640)

        self.Set_Background(Form,"B2.jpg")
        
        # 照片
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(80, 220, 171, 201))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(300, 180, 351, 311))
        self.layoutWidget.setObjectName("layoutWidget")
        
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        
        # 【学院】
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 1, 1, 1)
        
        # 【宿舍】
        self.label_11 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 1, 1, 1)
        
        # 学院：
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        
        # 【学号】
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)
        
        # 姓名：
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        
        # 班级：
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        
        # 【姓名】
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        
        # 宿舍：
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)
        
        # 学号：
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        
        # 【班级】
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        
        # 辅导员
        self.label_12 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 1)
        
        # 【辅导员】
        self.label_13 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 5, 1, 1, 1)
        
         # 1
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(620, 150, 631, 511))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        
         # 显示温度
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(250, 120, 361, 51))
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_14")
        
        # 您的信息如下
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(250, 30, 361, 51))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(21)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        
        # 重新扫描
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 520, 169, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        # 打印个人信息
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 520, 169, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        
        # 测温
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(420, 520, 169, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        
        # 打印表格
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(620, 520, 169, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        
        print("13")
        # 将信号与槽绑定
        self.pushButton.clicked.connect(self.shut)
        self.pushButton_2.clicked.connect(lambda:self.Print(Form))
        self.pushButton_3.clicked.connect(self.GetTemperature)
        self.pushButton_4.clicked.connect(self.Print_Table)     
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def Print_Table(self):
        #打印结果表
        print("打印结果表")
        pass

    def GetTemperature(self):
        global UserNumber
        # 测温
        try:
            t = thermometry()
            font = QtGui.QFont()
            font.setFamily("微软雅黑")
            font.setPointSize(15)
            self.label_16.setFont(font)
            if t>30 and t<37.2:
                self.label_16.setText("<font color='green'>当前体温："+str(t)+"</font>")
            else:
                self.label_16.setText("<font color='red'>当前体温："+str(t)+"</font>") 
            # 体温写入数据库
            print("update user set 体温={} where 学号={}".format(t,UserNumber))
            p = Ui_FirstForm().use_mysql("update user set 体温={} where 学号={}".format(t,UserNumber))
        except KeyboardInterrupt:
            print("[Error]:GetTemperature") 
            self.shut()
        
    # 一些固定文字控件的标题的设定
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        
        self.pushButton.setText(_translate("Form", "重新扫描"))
        self.label_8.setText(_translate("Form", "学    院："))
        self.label_2.setText(_translate("Form", "姓    名："))
        self.label_6.setText(_translate("Form", "班    级："))
        self.label_10.setText(_translate("Form", "宿    舍："))
        self.label_4.setText(_translate("Form", "学    号："))
        self.label_12.setText(_translate("Form", "辅导员："))
        self.pushButton_2.setText(_translate("Form", "打印信息"))
        self.label_14.setText(_translate("Form", "1"))
        self.label_15.setText(_translate("Form", "您的信息如下"))
        self.pushButton_2.setText(_translate("Form", "打印信息"))
        self.pushButton_3.setText(_translate("Form", "测    温"))
        self.pushButton_4.setText(_translate("Form", "打印表格"))
        
    # 关闭窗口，返回原窗口
    def shut(self):
        mainWindows2.close()
        ui.start_camera()
        mainWindows.show()
        
    def Hide_Button(self,Tag):
        self.pushButton.setVisible(Tag)
        self.pushButton_2.setVisible(Tag)
        self.pushButton_3.setVisible(Tag)
        self.pushButton_4.setVisible(Tag)   
        
    # 打印整个窗口
    def Print(self,Form):
        self.printer = QPrinter()
        # 将打印页面设置为横向
        self.printer.setOrientation(QPrinter.Landscape)
        self.Set_Background(Form,"white.jpg")
        self.Hide_Button(False)
        
        printdialog = QPrintDialog(self.printer, mainWindows2)
        
        if QDialog.Accepted == printdialog.exec():
            painter = QtGui.QPainter()
            # 将绘制目标重定向到打印机
            painter.begin(self.printer)
            screen = mainWindows2.grab(QRect(100, 80, 760, 330))
            
            screen = mainWindows2.grab()
            painter.drawPixmap(40, 60, screen)
            painter.end()
            
        self.Set_Background(Form,"B2.jpg")    
        self.Hide_Button(True)

if __name__=='__main__':
    # 人脸识别
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("face.png"))

    mainWindows = QMainWindow()
    mainWindows2 = QMainWindow()

    ui = Ui_FirstForm()
    Second = Ui_SecondForm()

    #向主窗口添加控件
    ui.setupUi(mainWindows)
    Second.setupUi(mainWindows2)

    mainWindows.show()

    sys.exit(app.exec_())
