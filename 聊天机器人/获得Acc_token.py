'''
@Time : 2020/7/20 14:32
@Author : laolao
@FileName: 获得Acc_token.py
'''
import requests

def get_token():
    '''
    获得认证
    client_id 为官网获取的AK， client_secret 为官网获取的SK
    :return:
    '''
    client_id = 'iz0BRgE2xVk8Yech2lBViwwg'
    client_secret = 'T4opIIehyfyo8c7oQ1p3NOg5js2m8PtE'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        return response.json()