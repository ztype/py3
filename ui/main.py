#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author:zfq

import os,time,sys
import threading
import tkinter as tk
from app import app as myapp

global app
app = None

def checkEvn():
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

def handleSignal():
    global app
    while app is not None:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("exiting")
            #app.destroy()
            sys.exit()
            break
def checkAlive():
    thd = threading.Thread(target=handleSignal,name="handleSignal")
    thd.start()

def main():
    checkEvn()
    global app
    app = myapp.app(title="info")
    app.run()

if __name__ == "__main__":
    #sys.path.append(r'./app')
    main()