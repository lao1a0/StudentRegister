'''
@Time : 2020/8/14 23:24
@Author : laolao
@FileName: 测温.py
'''
'''
@Time : 2020/8/5 18:53
@Author : laolao
@FileName: 超声波传感器demo.py
'''

while (1):
    distance = mydev.distance()
    # 判定距离是否在合适拍照的范围
    if distance > 10:
        dis_cnt += 1
    else:
        dis_cnt = 0
        print("请靠近“)
    # 连续检测到三次符合距离要求，跳出循环准备开始人脸检测
    if (dis_cnt == 3):
        break
    # 每隔0.5秒钟进行一次测距
    time.sleep(0.5)

temperature = ""
for j in range(7):
    temperature = sensor.getObjTemp()
    time.sleep(0.8)
    if (temperature > 35):
        # 测温正常结束循环
        mydev.killLED()
        break

# 温度判断
if (temperature > 35 and temperature < 37.2):
    # 温度正常
    print("温度正常" + str(temperature))
else:
    # 温度异常
    print("温度异常" + str(temperature))
