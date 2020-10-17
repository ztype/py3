from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLayout, QMainWindow, QApplication
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QSizePolicy
from PyQt5.QtWidgets import QLabel,QWidget,QPushButton,QSlider
from PyQt5.QtCore import QDateTime,QDate,QTime, Qt,QTimer
from PyQt5.QtGui import QCursor, QFont, QWindow,QPalette
from PyQt5 import QtGui

import pi.device as pi 
import psutil

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.piscreen = pi.PiGpioScreen()
        self.init()
    def init(self):
        self.setObjectName("mainwindow")
        self.oldsize = QtCore.QSize(300,200)
        self.resize(self.oldsize)
        self.setWindowTitle("timer")
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setupUI()
    def setupUI(self):
        # layout
        vbox = QVBoxLayout()
        self.root = QWidget(self)
        self.root.setObjectName("main")
        # head layout
        hhead = QVBoxLayout()
        self.brightslider = QSlider(self.root,orientation=Qt.Horizontal)
        self.brightslider.setMinimum(1)
        self.brightslider.setMaximum(100)
        self.brightslider.valueChanged.connect(self.onSlide)
        hhead.addWidget(self.brightslider)
        hhead.setSpacing(0)
        vbox.addLayout(hhead)
        # center layout
        vbody = QVBoxLayout()
        self.timelabel = QPushButton(self.root)
        self.timelabel.setObjectName("time")
        vbody.addStretch(1)
        vbody.addWidget(self.timelabel,alignment=Qt.AlignHCenter,stretch=2)
        self.datelabel = QPushButton(self.root)
        self.datelabel.setObjectName("date")
        self.datelabel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        vbody.addSpacing(5)
        vbody.addWidget(self.datelabel,alignment=Qt.AlignHCenter,stretch=2)
        vbody.addStretch(1)

        vbody.setSpacing(0)
        vbody.setContentsMargins(0,0,0,0)
        vbox.addLayout(vbody,stretch=1)
        # foot layout
        hfoot = QHBoxLayout()
        self.memlabel = QLabel(self.root)
        self.updateMemInfo()
        hfoot.addWidget(self.memlabel)
        self.cpulabel = QLabel(self.root)
        self.updateCpuInfo()
        hfoot.addWidget(self.cpulabel)
        self.iplabel = QLabel(self.root)
        self.updateIpAddress()
        hfoot.addWidget(self.iplabel)
        hfoot.setSpacing(0)
        vbox.addLayout(hfoot)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0,0,0,0)
        # set layout
        self.root.setLayout(vbox)
        self.setCentralWidget(self.root)
        
        self.timelabel.clicked.connect(self.maxmin)
        self.updateDatetime()
        self.allWithBorder()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateUi)
        self.timer.start(1000)
        #cursor
        self.ctimer = QTimer(self)
        self.ctimer.timeout.connect(self.hideCursor)
        self.ctimer.start(5000)
    def hideCursor(self):
        #print("cursor hide")
        self.setCursor(Qt.BlankCursor)
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            #print(event.pos())
            self.setCursor(Qt.ArrowCursor)
            self.ctimer.start(5000)
        return super().eventFilter(source, event)
    def onSlide(self):
        v = self.brightslider.value()
        self.piscreen.set_brightness(v)
    def allWithBorder(self):
        self.setStyleSheet('''
        *{
            margin: 0px 0px 0px 0px;
            padding: 0px 0px 0px 0px;
            border-style:solid;
            border-width: 1px;
            border-color: gray;
            background-color: #101010;
        }
        QLabel,QPushButton,QSlider{
            
        }
        QPushButton{
            color: #EDEDED;
            font-family: Arial;
            font-size: 80pt;
        }
        QPushButton#date{
            font-size: 60pt;
        }
        QLabel{
            color: #E0E0E0;
            font-family: Arial;
        }
        QSlider{
        }
        ''')
    
    def updateUi(self):
        self.updateDatetime()
        self.updateMemInfo()
        self.updateCpuInfo()
    def updateDatetime(self):
        now = QTime().currentTime().toString(QtCore.Qt.ISODate)
        self.timelabel.setText(now)
        date = QDate().currentDate().toString(QtCore.Qt.ISODate)
        self.datelabel.setText(date)
    def updateIpAddress(self):
        ips = pi.get_wan_ip_address()
        ipstr = ",".join(ips)
        ipstr = "IP:"+ipstr
        self.iplabel.setText(ipstr)
    def updateCpuInfo(self):
        per = psutil.cpu_percent()
        cpu = pi.get_cpu_temp()
        cpustr = "CPU:{:.1f}%-{:.2f}℃".format(per, cpu)
        self.cpulabel.setText(cpustr)
    def updateMemInfo(self):
        if hasattr(self,"memlabel") and self.memlabel is not None:
            mems = psutil.virtual_memory()
            usedg = mems.used/(1024*1024*1024)
            s = "MEM:{:.2f}G-{:.1f}%".format(usedg, mems.percent)
            self.memlabel.setText(s)
    #override
    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        if not self.isMaximized() and e.oldSize().isValid():
            self.oldsize = e.oldSize()
        return super().resizeEvent(e)

    def maxmin(self):
        ws = self.windowState()
        self.setWindowState(ws)
        if not self.isMaximized() :
            self.setWindowState(ws | QWindow.FullScreen)
        else:
            #self.setWindowState(ws ^ QWindow.FullScreen)
            self.resize(self.oldsize)
            
        
        