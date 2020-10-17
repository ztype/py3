#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author: zfq

# this module is used to get the raspberry pi's device info
# mainly include:cpu temperature

import socket
import os
import platform
import psutil
import importlib

print(platform.node())
if platform.node() == "raspberrypi":
    gpio = importlib.import_module("RPi.GPIO")


def get_cpu_temp():
    '''get cpu temperature'''
    temp = -1
    try:
        tempFile = open( "/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        temp = float(cpu_temp)/1000
    except FileNotFoundError:
        temp = 0
    return temp

def get_wan_ip_address():
    '''get net wan interace ip'''
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    # check NIC info, get local ip
    ips = []
    # exclude the virtual net
    vset = get_virtual_netiface()
    for k, addr in addrs.items():
        #1.check address family
        #2.check ip address
        if k not in stats or not stats[k].isup or k in vset:
            continue
        for v in addr:
            if v.family == socket.AF_INET and not v.address == "127.0.0.1":
                ips.append(v.address)
    return ips

def get_virtual_netiface():
    '''get virtual network interfaces'''
    vset = set()
    try:
        vinets = os.listdir('/sys/devices/virtual/net/')
        for item in vinets:
            vset.add(item)
    except FileNotFoundError:
        pass
    return vset

def deviceCheck(func):
    def wrapper(*args, **kw):
        if platform.node() != "raspberrypi":
            print(func.__name__,"run without pi")
            return
        return func(*args,**kw)
    return wrapper

class PiGpioScreen():
    @deviceCheck
    def __init__(self):
        self.pin = 18
        self.frequency=1000
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin,gpio.OUT)
        self.pwm = gpio.PWM(self.pin,self.frequency)
        self.pwm.start(0)
        self.pwm.ChangeDutyCycle(30)
    @deviceCheck
    def __del__(self):
        if gpio is None :
            return
        if hasattr(self,"pwm"):
            print("gpio cleanup")
            self.pwm.stop()
            gpio.cleanup()
    @deviceCheck
    def set_brightness(self,b=30):
        '''set screen brightness 0-100'''
        if gpio is None:
            return 
        if b<=0 or b >100 :
            return 
        self.pwm.ChangeDutyCycle(b)
    