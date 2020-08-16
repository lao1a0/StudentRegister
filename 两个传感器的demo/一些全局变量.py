'''
@Time : 2020/7/20 14:46
@Author : laolao
@FileName: 一些全局变量.py
'''
from aip import AipSpeech

count = 1

# 录音文件的名字
WAVE_OUTPUT_FILENAME='output.wav'

# 百度AI
# APP_ID = '21462872'
# API_KEY = 'iz0BRgE2xVk8Yech2lBViwwg'
# SECRET_KEY = 'QYM4Zf4WaRD77kApL7nH6YrMVmny3VdK'
# client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
APP_ID = '22041775'
API_KEY = 'iU7uCQiU1Ko47bHjtNf3DaUE'
SECRET_KEY = 'QYM4Zf4WaRD77kApL7nH6YrMVmny3VdK'
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

# 图灵机器人的错误码
ERROR_CODE = ['5000', '6000', '4000', '4001', '4002', '0'
                     '4003', '4005', '4007', '4100', '4200', '4300',
                    '4400', '4500', '4600', '4602', '7002', '8008']
# 图灵机器人的API
api_key = "c493bd693289422e89ed33b62d542aae"
urls = 'http://openapi.tuling123.com/openapi/api/v2'  # 图灵接口的url