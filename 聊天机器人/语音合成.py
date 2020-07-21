'''
@Time : 2020/7/20 13:52
@Author : laolao
@FileName: 语音合成.py
'''
import os
import playsound

from 项目.聊天机器人.一些全局变量 import *
from 项目.聊天机器人.获得Acc_token import get_token


def Baidu_Speak(text):
    '''
    开发文档： https://ai.baidu.com/ai-doc/SPEECH/Qk38y8lrl
    :param text: 让她说的话
    :return:
    '''

    result = client.synthesis(text, "zh", 1, {
        "val":  5 , # 音量
        "spd": 6, # 音速
        "pit":  5, # 语调
        "per":  111, # 度小萌
        "tok": get_token()
    })
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
        playsound.playsound('audio.mp3')  # 播放
        os.remove('audio.mp3')  # 放完后删除音频文件，否则第二次会无法写入

if __name__ == '__main__':
    Baidu_Speak(input(">>"))