# StudentRegister
暑假的工作记录
## 主项目——新生注册
#### 工具
百度AI:人脸检测、人脸识别
#### 使用方法
- 可检测并识别人脸，查询本地的sql数据库回显用户的个人信息
- 可以支持打印机，打印出个人信息
- 红外探测，量体温，语音交互提示测温结果
#### 说明
- 拍照获得的图片保存地址：/home/pi/Pictures
- 数据库录入图片保存地址：/home/pi/Pictures/Face_picture/
- mysql数据库名：test 数据表名:user
- 头像 ：/home/pi/Pictures/Face_local/  
- 地图 ：/home/pi/Pictures/map_local/   
- pip3 install playsound
- pip3 install baidu-aip
- playsound报错：

		Traceback (most recent call last):
		  File "/home/pi/Desktop/1.py", line 3, in <module>
		    playsound.playsound('/home/pi/Desktop/Jam - 七月上.mp3')
		  File "/home/pi/.local/lib/python3.5/site-packages/playsound.py", line 92, in _playsoundNix
		    gi.require_version('Gst', '1.0')
		  File "/usr/lib/python3/dist-packages/gi/__init__.py", line 118, in require_version
		    raise ValueError('Namespace %s not available' % namespace)
		ValueError: Namespace Gst not available
- 解决：sudo apt-get install gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 gstreamer1.0-tools
	
数据库的字段类型：

                    Second.label_3.setText(p['姓名'])
                    Second.label_5.setText(p['学号'])
                    Second.label_7.setText(p['班级'])
                    Second.label_9.setText(p['学院'])
                    Second.label_11.setText(p['宿舍'])
                    Second.label_13.setText(p['辅导员'])
		    
		    B2.jpg是什么？

## 主项目——树莓派（自带open-cv）

#### 登录账号密码：

pi  yahboom

#### raspberry部署
- 安装pyqt5:https://blog.csdn.net/lcy1847/article/details/87860046
- 安装pymysql:https://blog.csdn.net/register_2/article/details/79986624
- 安装摄像头：https://blog.csdn.net/damanchen/article/details/85163229
- 开启声音播放：https://www.nousbuild.org/codeu/raspberry-pi-audio-and-video/
- 播放视频：https://shumeipai.nxez.com/2013/09/08/play-video-using-the-command-line.html
- 安装mysql:https://www.jianshu.com/p/b258c5e2335b

#### 学习视频

淘宝店家给的教程：

- https://www.yahboom.com/study/raspberry3B+ 提取码：**16vj**，请复制以后使用

VMware安装树莓派虚拟机体验：

- https://blog.csdn.net/wangshuo747/article/details/88948816

新手入门视频教程：

- https://www.bilibili.com/video/BV15E411r7PV?p=1

设置中文：

- https://shumeipai.nxez.com/2016/03/13/how-to-make-raspberry-pi-display-chinese.html

树莓派入门套件资料客户资料：

- A套餐资料-- https://pan.baidu.com/s/1sIdwQHT5yiCFhXtKf3pzLw 提取码：zmnn
- B套餐资料-- https://pan.baidu.com/s/1n5xhxr5ztIox3P9Vuha_qw     提取码：ah10
- C套资料-- https://pan.baidu.com/s/15_WZQgYH0l_AzPrPsTtzRw   提取码：103o

红外传感器的资料：

- https://pan.baidu.com/s/1V4IX0PKG8vDOionICghSTw
- 淘宝店家：
	- GY-906 这个测试距离是是2CM
		- 说明链接：
		- https://pan.baidu.com/s/1PlaK9DxyONlqvUz7kYYkUA 提取码：57f5
		- 资料下载：
		- https://pan.baidu.com/s/1MXeuWz3VB88AhAGh0qFX8g
	- MLX90614ESF-BAA
		- 链接:
		- https://pan.baidu.com/s/1PEHq8qItdHAuIlr9_pSY2A 提取码：bol6

超声波传感器的资料：

- https://pan.baidu.com/s/1zJYHwi_e2qUNd56RKsf7dw   提取码：kqjo
- 2020款超声波资料 https://pan.baidu.com/s/1miNGWha#list/path=%2F 
- 2020款超声波说明链接：
- https://pan.baidu.com/s/1pMpbh7ps1uOqFeZ1y2lw0Q 提取码：ukbd
- 树莓派上使用HC-SR04超声波测距模块：
- https://shumeipai.nxez.com/2019/01/02/hc-sr04-ultrasonic-ranging-module-on-raspberry-pi.html 
- PS:
- 代码里不要有中文，Echo和Trig可以选择任意接口，这里我选择的是：18 23
- <img src=".\Image\代码里不要有中文.jpg" alt="代码里不要有中文" style="zoom: 80%;" />

3B+引脚原理图：

- https://blog.csdn.net/zz531987464/article/details/100837652
- <img src=".\Image\20181206212711483.jpg" alt="20181206212711483" style="zoom: 80%;" />

GPIO接线图

- https://www.lxx1.com/2639

#### 安装C语言编译环境

- cd /tmp
- 下载这个包：wget https://project-downloads.drogon.net/wiringpi-latest.deb
- 安装这个包：sudo dpkg -i wiringpi-latest.deb
- 查看安装版本：gpio -v

#### 安装python2.7编译环境 

###### 选择安装

- sudo apt-get update
- sudo apt-get install idle-python2.7
- [首选项]-->[Main Menu Editor]-->[编程]-->[IDLE]

## 副项目——聊天机器人

#### 工具
- 百度AI:语音识别，语音合成

- 图灵机器人


#### 使用方法
- 安装**必要的库**后，python环境下运行

- 说话，按空格停止

- 出现“识别失败”按一下空格再次说话，按第二下空格停止

- 支持图灵机器人标准版的各种功能【URL通过界面回显】
- 一些需要自定义的设置在 [一些全局变量.py](https://github.com/thinkforanameissohard/StudentRegister/blob/master/聊天机器人/一些全局变量.py) 里面
