#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys
import os
import signal

from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from src.client import Client
from src.login_window import LoginWindow


def signal_handler(sig, frame):
    QApplication.quit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LoginWindow()
    widget.center()
    widget.show()
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(app.exec_())
