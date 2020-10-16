#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#author: zfq

import tkinter as tk
import os
import time
import psutil

from app import device_pi as pi

class app():
    def __init__(self, title):
        self.root = tk.Tk()
        self.init()
    @staticmethod
    def getDateTime():
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        return now
    @staticmethod
    def getDate():
        now = time.strftime("%Y-%m-%d")
        return now
    @staticmethod
    def getTime():
        now = time.strftime("%H:%M:%S")
        return now

    def event_info(self, event):
        super.event_info(self, event) 
    
    def maximize(self):
        h = self.root.winfo_screenheight()-100
        w = self.root.winfo_screenwidth()-100
        print("screen height:", h,"width:", w)
        self.root.geometry("%dx%d"%(w, h))
    
    def fullscreen(self, full=True): 
        self.root.attributes("-fullscreen", full)

    def isFullscreen(self):
        return self.root.attributes("-fullscreen")

    def hideCursor(self):
        self.root.config(cursor="none")

    def onTimeClick(self, event):
        fc = self.isFullscreen()
        self.fullscreen(not fc)
    def onSlide(self,event):
        value = self.scale.get()
        self.screen.set_brightness(value)


    def init(self):
        self.screen = pi.PiGpioScreen()
        if self.root.title() == "":
            self.root.title("info")

        self.maximize()
        self.fullscreen()
        self.root.config(background="black")
        self.hideCursor()
       
        btm_fg_color="gray"
        mid_fg_color="#D3D3D3"
        #380x220
        sh = self.root.winfo_screenheight()
        # layouts
        # top layout
        tls = tk.LabelFrame(self.root, bg="gray", borderwidth=0)
        self.top_labels = tls
        '''
        self.scale = tk.Scale(tls, from_=1, to=100, resolution=1,
                        orient=tk.HORIZONTAL, show=0, command=self.onSlide,
                        highlightbackground="black", highlightcolor="black",
                        bg="black", activebackground="black",fg="black",troughcolor="black",
                        width=int(sh/6))
                        '''
        self.scale = tk.Label(tls,bg="gray", height=int(sh/80))
        #self.scale.set(15)
        self.scale.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=0)
        #self.scale.bind("<B1-Motion>",self.onSlide)
        self.top_labels.pack(side=tk.TOP)
        # middle layout
        mls = tk.LabelFrame(self.root, bg="black", borderwidth=0)
        self.mid_labels = mls

        self.time_label = tk.Label(mls, bg="black", fg=mid_fg_color)
        self.time_label.bind("<Button-1>", self.onTimeClick)
        self.update_time()

        self.date_label = tk.Label(mls, bg="black", fg=mid_fg_color, borderwidth=1, relief="solid")
        self.update_date()

        self.time_label.pack(side=tk.TOP)
        self.date_label.pack(side=tk.TOP, pady=5)
        mls.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        # bottom layout
        bls = tk.LabelFrame(self.root, bg="black", borderwidth=0)
        self.bottom_labels = bls 

        self.mem_label = tk.Label(bls, bg="black", fg=btm_fg_color, borderwidth=0)
        self.update_mem_usage()
        self.mem_label.pack(side=tk.LEFT)

        self.ip_label = tk.Label(bls, bg="black", fg=btm_fg_color, borderwidth=0, relief="solid")
        self.updateIpAddress()

        self.cpu_label = tk.Label(bls, bg="black", fg=btm_fg_color, borderwidth=0, relief="solid")
        self.update_cpu()

        self.time_label.config(font=("Courier", int(sh/5)-10))
        self.date_label.config(font=("Courier", int(sh/5)-30))

        self.cpu_label.pack(padx=15, side=tk.LEFT, fill=tk.X)
        self.ip_label.pack(ipadx=3, anchor=tk.S, side=tk.RIGHT)
        bls.pack(side=tk.BOTTOM)

    def update_mem_usage(self):
        mems = psutil.virtual_memory()
        #totalg = mems.total/(1024*1024*1024)
        usedg = mems.used/(1024*1024*1024)
        s = "MEM:{:.2f}G-{:.1f}%".format(usedg, mems.percent)
        self.mem_label.config(text=s)
    def updateIpAddress(self, ips=""):
        if ips == "":
            ips = self.get_ip_address()
        ipstr = ",".join(ips)
        ipstr = "IP:"+ipstr
        print(ipstr)
        self.ip_label.config(text=ipstr)

    def update_date(self):
        now = app.getDate()
        self.date_label.config(text=now)
    def update_time(self):
        now = app.getTime()
        self.time_label.config(text=now)

    def update_cpu(self):
        per = psutil.cpu_percent()
        cpu = pi.get_cpu_temp()
        cpustr = "CPU:{:.1f}%-{:.2f}℃".format(per, cpu)
        self.cpu_label.config(text=cpustr)
        
    def second_timer_update(self):
        self.update_time()
        self.update_date()
        self.update_cpu()
        self.update_mem_usage()
        self.root.after(1000, self.second_timer_update)
    # the window main entrance
    def run(self):
        self.root.after(1000, self.second_timer_update)
        self.root.mainloop()
    def get_ip_address(self):
        return pi.get_wan_ip_address()
   
        