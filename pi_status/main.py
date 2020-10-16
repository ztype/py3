#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import psutil

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def get_mem_usage():
    return psutil.virtual_memory().percent

def get_blk():
    tf = open("/usr/bin/python")
    blk = tf.read()
    tf.close()
    return blk

def keep_get_cpu_temp():
    blks = []
    b = get_blk()
    print("blk size:",len(b))
    while True:
        temp = get_cpu_temp()
        musage = get_mem_usage()
        print("CPU TEMP:{:.2f},MEM USAGE:{}".format(temp,musage))
        #time.sleep(0.5)
        blks.append(psutil.virtual_memory())
        blks.append(b)


if __name__ == "__main__":
    try:
        keep_get_cpu_temp()
    except Exception as e:
        print(e)
    