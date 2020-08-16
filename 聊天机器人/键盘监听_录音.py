'''
@Time : 2020/7/20 14:06
@Author : laolao
@FileName: 键盘监听_录音.py
'''
import threading

from pynput.keyboard import Listener
import pyaudio
import wave

from 一些全局变量 import WAVE_OUTPUT_FILENAME

run = True
CHUNK = 1024  # 数据包或者数据片段
FORMAT = pyaudio.paInt16  # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
CHANNELS = 1  # 声道，1为单声道，2为双声道
RATE = 16000  # 采样率，每秒钟16000次
# RECORD_SECONDS = 5  # 录音时间


def Recoder():
    '''
    录音并保存为wav文件
    :return:
    '''
    global run
    _frames = []
    p = pyaudio.PyAudio()
    # 打开数据流
    stream = p.open(channels=CHANNELS,
                    format=FORMAT,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    while run:
        # 读取数据
        data = stream.read(CHUNK)
        _frames.append(data)

    # 停止数据流
    stream.stop_stream()
    stream.close()
    # 关闭PyAudio
    p.terminate()

    # 保存wav文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(_frames))
    wf.close()
    # print("Saved")


def press(key):
    '''
    获得键盘输入，判断是否为空格，空格停止录音
    :param key:监听的键盘输入
    :return:
    '''
    global run
    try:
        if str(key) == 'Key.space':
            run = not run
            # print(run)
    except AttributeError as e1:
        print(e1)
        pass


def check_input():
    '''
    监听键盘的输入
    :return:
    '''

    with Listener(on_press=press) as listener:
        listener.join()
        print(listener)


if __name__ == '__main__':
    t1 = threading.Thread(target=check_input, args=())  # 监听键盘
    print("开始录音：")
    t1.start()
    Recoder()