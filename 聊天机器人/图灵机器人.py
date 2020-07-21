'''
@Time : 2020/7/20 13:30
@Author : laolao
@FileName: 图灵机器人.py
'''
import requests

from 项目.聊天机器人.一些全局变量 import ERROR_CODE, api_key, urls

prologue = "主人您好，我是Alice，爱你哦~"  # 定义开场白
count = 1  # 用来计数输入的次数

# 回复
def Tuling_Respond(data):
    '''
    输入的是你的对话内容
    :param data:
    :return: 输出一个二元组，第一个是机器人的回答，第二个是查询的url
    '''
    data_dict = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": data
            },
        },
        "userInfo": {
            "apiKey": api_key,
            "userId": "20183614"
        }
    }

    result = requests.post(urls, json=data_dict)
    content = result.json()
    # print(content)
    if content['intent']['code'] in ERROR_CODE:
        return "Ooops 发生错误"
    else:
        if len(content['results'])==1:
            return content['results'][0]['values']['text'], ""
        else:
            return content['results'][1]['values']['text'], content['results'][0]['values']['url']
if __name__ == "__main__":
    print("Alice:", prologue)
    while True:
        data = input('{}>>：'.format(count))  # 输入对话内容
        speaking,url=Tuling_Respond(data)
        print(speaking,"+",url)
        count += 1

