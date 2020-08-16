'''
@Time : 2020/7/20 13:56
@Author : laolao
@FileName: 语音合成_图灵Bot.py
'''
from 图灵机器人 import Tuling_Respond
from 语音合成 import Baidu_Speak

count = 1

if __name__ == '__main__':
    while True:
        data = input('{}>>：'.format(count))  # 输入对话内容
        res = Tuling_Respond(data)
        print(res)
        # Baidu_Speak(Tuling_Respond(data))
        count += 1