# StudentRegister
暑假的工作记录
## 主项目——新生注册
#### 工具
百度AI:人脸检测、人脸识别
#### 使用方法
- 可检测并识别人脸，查询本地的sql数据库回显用户的个人信息
- 可以支持打印机，打印出个人信息
- 正在开发：红外探测，量体温

## 主项目——树莓派

#### 学习视频

VMware安装树莓派虚拟机体验：https://blog.csdn.net/wangshuo747/article/details/88948816

新手入门视频教程：https://www.bilibili.com/video/BV15E411r7PV?p=1

设置中文：https://shumeipai.nxez.com/2016/03/13/how-to-make-raspberry-pi-display-chinese.html

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