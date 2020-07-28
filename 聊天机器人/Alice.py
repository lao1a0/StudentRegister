'''
@Time : 2020/7/20 15:37
@Author : laolao
@FileName: Alice.py
'''
import threading
import time

from 项目.StudentRegister.聊天机器人.图灵机器人 import Tuling_Respond
from 项目.StudentRegister.聊天机器人.语音合成 import Baidu_Speak
from 项目.StudentRegister.聊天机器人.语音识别 import Record_To_Text
from 项目.StudentRegister.聊天机器人.键盘监听_录音 import Recoder, run, check_input

if __name__ == '__main__':
    t1 = threading.Thread(target=check_input, args=())  # 监听键盘
    t1.start()
    Baidu_Speak("主人好，这里是Alice")
    # try:
    count=1
    while True:
        if run is True:
            print("{}:按空格停止说话>>".format(count))
            Recoder()
            text2 = Record_To_Text()
            while text2['err_msg'] != "success.":
                time.sleep(1)
                print("\t{}:没听清，请再说一遍，按空格停止说话>>".format(count))
                Recoder()
                text2 = Record_To_Text()
            # print("\t>>{}".format(text2))
            text1 = text2['result'][0]
            print('\r{}>>:'.format(count), text1)
            speaking,URL=Tuling_Respond(text1)
            Baidu_Speak(speaking)
            if URL !="":
                print(URL)
            count += 1
    # except Exception as e:
    #     print(e)

