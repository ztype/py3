# -*- coding: UTF-8 -*- 
import sys,os
from PyQt5 import QtWidgets
from src.window import Window
import signal

def checkEvn():
    if os.environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

def main():
    checkEvn()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    app.installEventFilter(window)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()