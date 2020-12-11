from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow
from qtwidgets import PasswordEdit
import sys
#from PySide2.QtGui import QMainWindow
from PySide2.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        # init some elements
        self.setFixedSize(300, 400)
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.setWindowTitle('Shutdown Tool Login')
        self.verticalLayout_1 = QVBoxLayout(self)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        # Elements
        self.label_1 = QLabel(self)
        self.label_1.setObjectName(u"label")
        self.label_1.setText('Main window')
