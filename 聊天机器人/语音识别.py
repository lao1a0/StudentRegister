'''
@Time : 2020/7/20 14:19
@Author : laolao
@FileName: 语音识别.py
'''
from 一些全局变量 import *

def Get_File_Content(FilePath):
    '''
    录音转字节码
    :param FilePath:
    :return:
    '''
    with open(FilePath,'rb') as f:
        return f.read()

def Record_To_Text():
    '''
    录音转文字
    :return:
    '''
    res = client.asr(Get_File_Content(WAVE_OUTPUT_FILENAME),'wav',16000,{
        'dev_pid':1537,
    })
    return res

if __name__ == '__main__':
    Record_To_Text()
