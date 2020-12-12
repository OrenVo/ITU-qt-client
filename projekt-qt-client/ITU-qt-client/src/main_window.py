from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, \
    QMainWindow, QTabWidget, QTimeEdit, QComboBox, QDateTimeEdit
from qtwidgets import PasswordEdit
import datetime
import sys
from PySide2.QtCore import Qt, QTime, QDateTime


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
        now = QDateTime.currentDateTime()
        seconds = hour * 60 * 60 + minute * 60 + sec
        now_plus_seconds = now.addSecs(seconds)
        self.hours.date_time_in.dateTimeChanged.disconnect()
        self.hours.date_time_in.setDateTime(now_plus_seconds)
        self.hours.date_time_in.dateTimeChanged.connect(self.change_timer)


    def change_timer(self):  # Will be called on hours change to change timer time
        qdatetime = self.hours.date_time_in.dateTime()
        seconds = QDateTime.currentDateTime().secsTo(qdatetime)
        t0 = QTime(0, 0)
        self.timer.time_in.timeChanged.disconnect()
        self.timer.time_in.setTime(t0.addSecs(seconds))
        self.timer.time_in.timeChanged.connect(self.change_hours)

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
        self.verticalLayout = QVBoxLayout(self)
        # self.cpu_label
        # self.cpu_percent
        # self.cpu_time

        # self.net_label
        # self.net_kbs
        # self.net_time

        # self.ram_label
        # self.ram_percent
        # self.ram_time

        # self.audio_label
        # self.audio_time

        # self.disp_label
        # self.disp_time

        # self.processes_combobox


class SettingsTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
