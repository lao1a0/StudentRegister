'''
@Time : 2020/7/21 17:08
@Author : laolao
@FileName: 录音_语音识别.py
'''
import threading
import time

from 项目.聊天机器人.语音合成 import Baidu_Speak
from 项目.聊天机器人.语音识别 import Record_To_Text
from 项目.聊天机器人.键盘监听_录音 import Recoder, check_input

if __name__ == '__main__':
    t1 = threading.Thread(target=check_input, args=())  # 监听键盘
    t1.start()
    count = 1
    while True:
        print("{}:按空格停止说话>>".format(count))
        Recoder()
        text2 = Record_To_Text()
        while text2['err_msg'] != "success.":
            print("没听清，请再说一遍")
            time.sleep(1)
            print("{}:按空格停止说话>>".format(count))
            Recoder()
            text2 = Record_To_Text()
            print(">>{}" % text2)
        text1=text2['result'][0]
        # print(text1)
        print('\r{}>>:'.format(count), text2)
        Baidu_Speak(text1)
        count+=1
