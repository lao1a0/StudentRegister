'''
@Time : 2020/8/14 23:24
@Author : laolao
@FileName: 测温.py
'''
from 超声波 import *
from  红外 import *
from 语音合成 import *


def thermometry():
    '''
        返回0代表温度异常
    '''
    dis_cnt = 0
    sensor = MLX90614()

    while (1):
        dist = distance()
        # 判定距离是否在合适拍照的范围
        print("［debug］当前距离为{:.2f}cm ".format(dist))
        if dist <= 30:
            dis_cnt += 1
        else:
            dis_cnt = 0
            Baidu_Speak("请靠近")
            print("\t\t请靠近")
        # 连续检测到三次符合距离要求，跳出循环准备开始人脸检测
        if (dis_cnt == 3):
            break
        # 每隔1秒钟进行一次测距
        time.sleep(1)

    temperature = ""
    for j in range(7):
        temperature = sensor.getObjTemp()
        time.sleep(0.8)
        if (temperature > 35):
            # 测温正常结束循环
            break
    tag=1
    # 温度判断
    if (temperature > 35 and temperature < 37.2):
        # 温度正常
        speak = "温度正常" + str(temperature)
    else:
        # 温度异常
        speak = "温度异常" + str(temperature)
        tag =0
    Baidu_Speak(speak)
    print(speak)
    return  tag

if __name__ == '__main__':
    try:
        thermometry()
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
