from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, \
    QMainWindow, QTabWidget, QTimeEdit, QComboBox
from qtwidgets import PasswordEdit
import sys
from PySide2.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        # init some elements
        self.parent = parent
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.setWindowTitle('Shutdown Tool')
        self.vbox = QVBoxLayout(self)

        self.timer = TimerTab(self)
        self.hours = HoursTab(self)
        self.resources = MonitorsTab(self)
        self.settings = SettingsTab(self)

        self.tabs = QTabWidget(self)
        self.tabs.addTab(self.timer, "Timer")
        self.tabs.addTab(self.hours, "Hours")
        self.tabs.addTab(self.resources, "Resources")
        self.tabs.addTab(self.settings, "Settings")

        self.actions = QComboBox(self)
        self.actions.addItems(['Poweroff', 'Reboot', 'Script only'])

        self.start = QPushButton('Start', self)

        self.vbox.addWidget(self.tabs)
        self.vbox.addWidget(self.actions)
        self.vbox.addWidget(self.start, Qt.AlignVCenter)

        self.setLayout(self.vbox)

    def start_timer(self): # Starts timer
        ...

    def change_hours(self): # Will be called on timer change to change hours time
        ...

    def change_timer(self): # Will be called on hours change to change timer time
        ...

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())


class TimerTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.verticalLayout = QVBoxLayout(self)
        self.time_in = QTimeEdit(self)


class HoursTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.verticalLayout = QVBoxLayout(self)


class MonitorsTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent


class SettingsTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
