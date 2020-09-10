# StudentRegister
暑假的工作记录
## 主项目——新生注册
#### 工具
百度AI:人脸检测、人脸识别
#### 使用方法
- 可检测并识别人脸，查询本地的sql数据库回显用户的个人信息
- 可以支持打印机，打印出个人信息
- 红外探测，量体温 **(30-37.2正常)**，语音交互提示测温结果
- 可导出体温在**30-37.2**的学生的个人信息，并用excel表格显示，并打印表格
#### 说明
- 拍照获得的图片保存地址：/home/pi/Pictures
- 数据库录入图片保存地址：/home/pi/Pictures/Face_picture/
- mysql数据库名：test 数据表名:user
- 头像 ：/home/pi/Pictures/Face_local/  
- 地图 ：/home/pi/Pictures/map_local/  
- 摄像头拍摄保存照片：/home/pi/Pictures/Face_picture/
- excel表格：/home/pi/Documents/
- 人脸库在ydjhlsz这个账号里，语音识别
#### 第三方库安装
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

## 主项目——树莓派（自带open-cv）

#### 登录账号密码：

pi  yahboom

#### mysql账号密码：
本地：root 123
云端：root 相识学生报道系统base64
APP_TOKEN：AT_8B6A2kdNHmNo7oYcPpsbgeQlK7l06KDm
UID_wL85bprwzyAigwmf61FnVHWLbP1N

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
