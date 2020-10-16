from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QLabel,QWidget,QPushButton
from PyQt5.QtCore import QDateTime,QDate
from PyQt5.QtGui import QCursor, QWindow,QPalette

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
    def init(self):
        self.setObjectName("mainwindow")
        self.resize(300,200)
        self.setWindowTitle("timer")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.setupUI()
    def setupUI(self):
        # layout
        vbox = QVBoxLayout()
        vbox.setObjectName("mainlayout")
        self.root = QWidget(self)
        
        # center widget

        self.timelabel = QPushButton(self.root)
        self.timelabel.setText("now")
        self.timelabel.setBackgroundRole(QPalete.)
        vbox.addWidget(self.timelabel)
        # set layout
        self.root.setLayout(vbox)
        self.setCentralWidget(self.root)
        
        self.timelabel.clicked.connect(self.maxmin)
    def maxmin(self):
        ws = self.windowState()
        self.setWindowState(ws)
        if not self.isMaximized() :
            self.setWindowState(ws | QWindow.FullScreen)
        else:
            self.setWindowState(ws ^ QWindow.FullScreen)
        
        