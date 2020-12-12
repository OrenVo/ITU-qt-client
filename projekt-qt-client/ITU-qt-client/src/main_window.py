from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, \
    QMainWindow, QTabWidget, QTimeEdit, QComboBox, QDateTimeEdit
from qtwidgets import PasswordEdit
import datetime
import sys
from PySide2.QtCore import Qt, QTime


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
        self.actions.addItems(['Poweroff', 'Reboot', 'Script'])

        self.start = QPushButton('Start', self)
        self.start.clicked.connect(self.start_timer)
        self.vbox.addWidget(self.tabs)
        self.vbox.addWidget(self.actions)
        self.vbox.addWidget(self.start, Qt.AlignVCenter)

        self.setLayout(self.vbox)

    def start_timer(self):  # Starts Timer or Hours
        qtime = self.timer.time_in.time()
        hour = qtime.hour()
        minute = qtime.minute()
        sec = qtime.second()
        seconds = hour * 60 * 60 + minute * 60 + sec
        script = ''
        self.parent.client.start_timer(seconds, self.actions.itemText(self.actions.currentIndex()), script)

    def change_hours(self):  # Will be called on timer change to change hours time
        qtime = self.timer.time_in.time()
        hour = qtime.hour()
        minute = qtime.minute()
        sec = qtime.second()
        now = QTime.currentTime()
        seconds = hour * 60 * 60 + minute * 60 + sec
        now_plus_seconds = now.addSecs(seconds)
        self.hours.date_time_in.setDateTime(now_plus_seconds)

    def change_timer(self):  # Will be called on hours change to change timer time
        qtime = self.timer.time_in.time()

        hour = qtime.hour()
        minute = qtime.minute()
        sec = qtime.second()


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
        self.time_in.setDisplayFormat('hh:mm:ss')
        self.time_in.setMinimumTime(QTime(0, 0))
        self.time_in.setMaximumTime(QTime(23, 0))
        self.time_in.timeChanged.connect(self.parent.change_hours)
        self.verticalLayout.addWidget(self.time_in, Qt.AlignVCenter)


class HoursTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.verticalLayout = QVBoxLayout(self)

        self.date_time_in = QDateTimeEdit(self)
        self.date_time_in.dateTimeChanged.connect(self.parent.change_timer)
        self.verticalLayout.addWidget(self.date_time_in, Qt.AlignVCenter)


class MonitorsTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent


class SettingsTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
