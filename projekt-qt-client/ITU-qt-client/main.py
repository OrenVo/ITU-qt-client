#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget
# import qtwidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from src.client import Client


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.client = Client()
        self.setFixedSize(200, 210)
        self.ui.login_btn.clicked.connect(self.login)
        self.ui.password.setEchoMode(QLineEdit.Password)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        if not ui:
            print("Error loading file", file=sys.stderr)
            exit(1)
        ui_file.close()
        return ui

    def login(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        if not self.client.connect(username, password):



    def center(self):
        qRect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(center_point)
        self.move(qRect.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWindow()
    widget.center()
    widget.show()
    sys.exit(app.exec_())
