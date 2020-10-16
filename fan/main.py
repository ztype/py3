#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import RPi.GPIO as gpio # 导入Rpi.GPIO库函数命名为GPIO
import time

gpio.setmode(gpio.BOARD) #将GPIO编程方式设置为BOARD模式

pin = 40

gpio.setup(pin, gpio.OUT) #控制pin号引脚

gpio.output(pin, gpio.HIGH) #11号引脚输出高电平
time.sleep(5) #计时0.5秒
gpio.output(pin, gpio.LOW) #11号引脚输出低电平
time.sleep(1) #计时1秒

gpio.cleanup() #释放使用的GPIO引脚