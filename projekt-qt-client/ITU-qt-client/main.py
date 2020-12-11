#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget
# import qtwidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from src.client import Client
from src.login_window import LoginWindow


# def center(self):
#     qRect = self.frameGeometry()
#     center_point = QDesktopWidget().availableGeometry().center()
#     qRect.moveCenter(center_point)
#     self.move(qRect.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LoginWindow()
    # widget.center()
    widget.show()
    sys.exit(app.exec_())
