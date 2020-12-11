from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, \
    QMainWindow, QTabWidget
from qtwidgets import PasswordEdit
import sys
from PySide2.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        # init some elements
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.setWindowTitle('Shutdown Tool')
        self.vbox = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(TimerTab(), "Timer")
        self.tabs.addTab(HoursTab(), "Hours")
        self.tabs.addTab(MonitorsTab(), "Resources")
        self.tabs.addTab(SettingsTab(), "Settings")
        self.vbox.addWidget(self.tabs)
        self.setLayout(self.vbox)

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())


class TimerTab(QWidget):

    def __init__(self):
        super().__init__()


class HoursTab(QWidget):

    def __init__(self):
        super().__init__()


class MonitorsTab(QWidget):

    def __init__(self):
        super().__init__()


class SettingsTab(QWidget):

    def __init__(self):
        super().__init__()
