from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, \
    QMainWindow, QTabWidget, QTimeEdit, QComboBox, QDateTimeEdit, QHBoxLayout, QSpinBox, QScrollArea, QGridLayout
from qtwidgets import PasswordEdit
import datetime
import sys
from PySide2.QtCore import Qt, QTime, QDateTime, QTimer
from PySide2 import QtGui


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
        self.tabs.currentChanged.connect(self.tab_changed)

        self.actions = QComboBox(self)
        self.actions.addItems(['Poweroff', 'Reboot', 'Suspend', 'Script'])
        self.start = QPushButton('Start timer', self)
        self.start.clicked.connect(self.start_timer)
        self.script_path = QLineEdit(self)
        self.script_label = QLabel("Script path:", self)
        self.logout_btn = QPushButton('Logout', self)
        self.logout_btn.setVisible(False)
        self.logout_btn.clicked.connect(self.logout)
        self.vbox.addWidget(self.tabs)
        self.vbox.addWidget(self.actions)
        self.vbox.addWidget(self.start, Qt.AlignVCenter)
        self.vbox.addWidget(self.script_label, Qt.AlignLeft)
        self.vbox.addWidget(self.script_path)
        self.vbox.addWidget(self.logout_btn)

        self.setLayout(self.vbox)

        self.timer_running = False
        self.monitor_running = False
        self.timers_timer = QTimer()
        self.timers_timer.setInterval(1_000)
        self.timers_timer.timeout.connect(self.timers_timer_tick)
        self.status_timer = QTimer()
        self.status_timer.setInterval(5_000)
        self.status_timer.timeout.connect(self.check_status)
        self.check_init_state()
        self.change_hours()

    def check_init_state(self):
        mon = self.parent.client.stat_monitor()
        timer = self.parent.client.stat_timer()
        if mon:
            self.monitor_running = True
        if timer:
            if timer['running']:
                self.timer.time_in.setTime(QTime(0,0).addSecs(timer['time_left']))
                self.timer.time_in.setEnabled(False)
                self.start.setText('Stop timer')
                self.start.clicked.disconnect()
                self.start.clicked.connect(self.stop_timer)
                self.timers_timer.start()
                self.status_timer.start()
                self.timer_running = True
            else:
                self.timer.time_in.setTime(QTime().addSecs(timer['time_set']))

    def check_status(self):
        timer = self.parent.client.stat_timer()
        mon = self.parent.client.stat_monitor()
        if not mon and self.monitor_running:
            self.stop_monitor()
        sec = timer.get('time_left')
        if timer:
            self.timer.time_in.setTime(QTime(0, 0).addSecs(int(sec)))
        else:
            self.timer_running = False

    def start_timer(self):  # Starts Timer or Hours
        qtime = self.timer.time_in.time()
        hour = qtime.hour()
        minute = qtime.minute()
        sec = qtime.second()
        seconds = hour * 60 * 60 + minute * 60 + sec
        script = self.script_path.text()
        if self.parent.client.start_timer(seconds, self.actions.itemText(self.actions.currentIndex()), script):
            self.timer.time_in.setEnabled(False)
            self.start.setText('Stop timer')
            self.start.clicked.disconnect()
            self.start.clicked.connect(self.stop_timer)
            self.timers_timer.start()
            self.status_timer.start()
            self.timer_running = True

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

    def logout(self):
        self.parent.client.logout()
        self.hide()
        self.parent.show()

    def start_monitor(self):
        request = list()
        # monitor_data['time']
        # Actions[monitor_data['action']]
        # monitor_data['resource']
        # monitor_data.get('value')
        # monitor_data['script']

        if self.resources.cpu_percent.value() > 0 and self.resources.cpu_time.time() > QTime(0, 0):  # CPU
            qtime = self.resources.cpu_time.time()
            hour = qtime.hour()
            minute = qtime.minute()
            sec = qtime.second()
            seconds = hour * 60 * 60 + minute * 60 + sec
            request.append({
                'value': self.resources.cpu_percent.value(),
                'time': seconds,
                'resource': 'CPU',
                'action': self.actions.itemText(self.actions.currentIndex()),
                'script': self.script_path.text()
            })
        if self.resources.net_kbs.value() > 0 and self.resources.net_time.time() > QTime(0, 0):  # NET
            qtime = self.resources.net_time.time()
            hour = qtime.hour()
            minute = qtime.minute()
            sec = qtime.second()
            seconds = hour * 60 * 60 + minute * 60 + sec
            request.append({
                'value': self.resources.net_kbs.value(),
                'time': seconds,
                'resource': 'Network',
                'action': self.actions.itemText(self.actions.currentIndex()),
                'script': self.script_path.text()
            })
        if self.resources.ram_percent.value() > 0 and self.resources.ram_time.time() > QTime(0, 0):  # RAM
            qtime = self.resources.ram_time.time()
            hour = qtime.hour()
            minute = qtime.minute()
            sec = qtime.second()
            seconds = hour * 60 * 60 + minute * 60 + sec
            request.append({
                'value': self.resources.ram_percent.value(),
                'time': seconds,
                'resource': 'RAM',
                'action': self.actions.itemText(self.actions.currentIndex()),
                'script': self.script_path.text()
            })
        if self.resources.audio_time.time() > QTime(0, 0):  # Audio
            qtime = self.resources.audio_time.time()
            hour = qtime.hour()
            minute = qtime.minute()
            sec = qtime.second()
            seconds = hour * 60 * 60 + minute * 60 + sec
            request.append({
                'value': None,
                'time': seconds,
                'resource': 'Sound',
                'action': self.actions.itemText(self.actions.currentIndex()),
                'script': self.script_path.text()
            })
        if self.resources.disp_time.time() > QTime(0, 0):  # Display
            qtime = self.resources.disp_time.time()
            hour = qtime.hour()
            minute = qtime.minute()
            sec = qtime.second()
            seconds = hour * 60 * 60 + minute * 60 + sec
            request.append({
                'value': None,
                'time': seconds,
                'resource': 'Display',
                'action': self.actions.itemText(self.actions.currentIndex()),
                'script': self.script_path.text()
            })
        if self.resources.processes_combobox.itemText(self.resources.processes_combobox.currentIndex()) != 'None':
            request.append({
                'value': int(self.resources.processes_combobox.itemText(self.resources.processes_combobox.currentIndex()).split(':')[1]),
                'time': None,
                'resource': 'Process',
                'action': self.actions.itemText(self.actions.currentIndex()),
                'script': self.script_path.text()
            })
        if not self.parent.client.start_monitor(request):
            print("[Client error]: Error when starting monitor", file=sys.stderr)
            return
        self.resources.cpu_percent.setEnabled(False)
        self.resources.cpu_time.setEnabled(False)
        self.resources.net_horizontal_layout.setEnabled(False)
        self.resources.net_kbs.setEnabled(False)
        self.resources.net_time.setEnabled(False)
        self.resources.ram_percent.setEnabled(False)
        self.resources.ram_time.setEnabled(False)
        self.resources.audio_time.setEnabled(False)
        self.resources.disp_time.setEnabled(False)
        self.status_timer.start()
        self.monitor_running = True
        self.start.clicked.disconnect()
        self.start.setText('Stop monitor')
        self.start.clicked.connect(self.stop_monitor)

    def submit_settings(self):
        translate = {
            "Full access": 0,
            "Actions & Scripts": 1,
            "Scripts only": 2,
            "Login only": 3,
            "Access denied": 4
        }

        for box, user, level in zip(self.settings.box_list, self.settings.user_list, self.settings.level_list):
            box_val = translate[box.itemText(box.currentIndex())]
            if box_val != level:
                self.parent.client.permissions_edit(user, box_val)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.parent.client.logout()
        event.accept()

    def tab_changed(self):
        if self.tabs.currentIndex() == 0:
            self.logout_btn.setVisible(False)
            self.script_path.setVisible(True)
            self.script_label.setVisible(True)
            self.actions.setVisible(True)
            if self.timer_running is False:
                self.start.setText('Start timer')
                self.start.clicked.disconnect()
                self.start.clicked.connect(self.start_timer)
            else:
                self.start.setText('Stop timer')
                self.start.clicked.disconnect()
                self.start.clicked.connect(self.stop_timer)
        elif self.tabs.currentIndex() == 1:
            self.logout_btn.setVisible(False)
            self.script_label.setVisible(True)
            if self.timer_running is False:
                self.start.setText('Start timer')
                self.start.clicked.disconnect()
                self.start.clicked.connect(self.start_timer)
            else:
                self.start.setText('Stop timer')
                self.start.clicked.disconnect()
                self.start.clicked.connect(self.stop_timer)
        elif self.tabs.currentIndex() == 2:
            self.logout_btn.setVisible(False)
            self.script_path.setVisible(True)
            self.actions.setVisible(True)
            self.script_label.setVisible(True)
            if self.monitor_running is False:
                self.resources.processes_combobox.clear()
                self.resources.processes_combobox.addItem('None')
                for pid, name in self.parent.client.get_processes().items():
                    self.resources.processes_combobox.addItem(f'{name} : {pid}')
                self.start.clicked.disconnect()
                self.start.setText('Start monitor')
                self.start.clicked.connect(self.start_monitor)
            else:
                self.start.clicked.disconnect()
                self.start.setText('Stop monitor')
                self.start.clicked.connect(self.stop_monitor)
        elif self.tabs.currentIndex() == 3:
            self.logout_btn.setVisible(True)
            self.start.setText('Submit settings')
            self.script_path.setVisible(False)
            self.actions.setVisible(False)
            self.script_label.setVisible(False)
            self.start.clicked.disconnect()
            self.start.clicked.connect(self.submit_settings)

    def timers_timer_tick(self):
        self.timer.time_in.setTime(self.timer.time_in.time().addSecs(-1))
        if self.timer.time_in.time() == QTime(0, 0):
            self.timers_timer.stop()
            self.status_timer.stop()
            self.start.clicked.disconnect()
            self.start.setText('Start timer')
            self.start.clicked.connect(self.start_timer)
            self.timer.time_in.setEnabled(True)
            self.timer_running = False

    def stop_timer(self):
        self.timer.time_in.setEnabled(True)
        self.timers_timer.stop()
        self.parent.client.stop_timer()
        self.timer_running = False
        self.start.clicked.disconnect()
        self.start.setText('Start timer')
        self.start.clicked.connect(self.start_timer)
        self.start.setText('Start timer')
        self.start.clicked.connect(self.start_timer)
        self.status_timer.stop()

    def stop_monitor(self):
        self.parent.client.stop_monitor()
        self.monitor_running = False
        self.status_timer.stop()
        self.start.clicked.disconnect()
        self.start.setText('Start monitor')
        self.start.clicked.connect(self.start_monitor)
        self.resources.cpu_percent.setEnabled(True)
        self.resources.cpu_time.setEnabled(True)
        self.resources.net_horizontal_layout.setEnabled(True)
        self.resources.net_kbs.setEnabled(True)
        self.resources.net_time.setEnabled(True)
        self.resources.ram_percent.setEnabled(True)
        self.resources.ram_time.setEnabled(True)
        self.resources.audio_time.setEnabled(True)
        self.resources.disp_time.setEnabled(True)

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

        # CPU
        self.cpu_horizontal_layout = QHBoxLayout()
        self.cpu_label = QLabel()
        self.cpu_label.setText('CPU usage')
        self.cpu_percent = QSpinBox()
        self.cpu_percent.setSuffix('%')
        self.cpu_percent.setRange(0, 100)
        self.cpu_time = QTimeEdit()
        self.cpu_horizontal_layout.addWidget(self.cpu_label)
        self.cpu_horizontal_layout.addWidget(self.cpu_percent)
        self.cpu_horizontal_layout.addWidget(self.cpu_time)
        self.verticalLayout.addLayout(self.cpu_horizontal_layout)

        # NET
        self.net_horizontal_layout = QHBoxLayout()
        self.net_label = QLabel()
        self.net_label.setText('Network usage')
        self.net_kbs = QSpinBox()
        self.net_kbs.setSuffix(' kb/s')
        self.net_kbs.setRange(0, 1_000_000)
        self.net_time = QTimeEdit()
        self.net_horizontal_layout.addWidget(self.net_label)
        self.net_horizontal_layout.addWidget(self.net_kbs)
        self.net_horizontal_layout.addWidget(self.net_time)
        self.verticalLayout.addLayout(self.net_horizontal_layout)

        # RAM
        self.ram_horizontal_layout = QHBoxLayout()
        self.ram_label = QLabel()
        self.ram_label.setText('Ram usage')
        self.ram_percent = QSpinBox()
        self.ram_percent.setSuffix('%')
        self.ram_percent.setRange(0, 100)
        self.ram_time = QTimeEdit()
        self.ram_horizontal_layout.addWidget(self.ram_label)
        self.ram_horizontal_layout.addWidget(self.ram_percent)
        self.ram_horizontal_layout.addWidget(self.ram_time)
        self.verticalLayout.addLayout(self.ram_horizontal_layout)

        # Audio
        self.audio_horizontal_layout = QHBoxLayout()
        self.audio_label = QLabel()
        self.audio_label.setText('Audio not playing for:')
        self.audio_time = QTimeEdit()
        self.audio_horizontal_layout.addWidget(self.audio_label)
        self.audio_horizontal_layout.addWidget(self.audio_time)
        self.verticalLayout.addLayout(self.audio_horizontal_layout)

        # Display
        self.disp_horizontal_layout = QHBoxLayout()
        self.disp_label = QLabel()
        self.disp_label.setText('Display off for:')
        self.disp_time = QTimeEdit()
        self.disp_horizontal_layout.addWidget(self.disp_label)
        self.disp_horizontal_layout.addWidget(self.disp_time)
        self.verticalLayout.addLayout(self.disp_horizontal_layout)

        # Processes
        self.processes_combobox = QComboBox()
        self.processes_combobox.addItem('None')
        for pid, name in self.parent.parent.client.get_processes().items():
            self.processes_combobox.addItem(f'{name} : {pid}')
        self.verticalLayout.addWidget(self.processes_combobox)


class SettingsTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.scrollArea = QScrollArea()
        self.scrollWidget = QWidget()
        self.verticalLayout = QVBoxLayout()
        self.box_list = list()
        self.user_list = list()
        self.level_list = list()

        # Users
        for user, level in self.parent.parent.client.permissons_view().items():
            self.user_layout = QHBoxLayout()
            self.user_label = QLabel()
            self.user_label.setText(user)
            self.user_rights = QComboBox()
            self.user_rights.addItem("Full access")
            self.user_rights.addItem("Actions & Scripts")
            self.user_rights.addItem("Scripts only")
            self.user_rights.addItem("Login only")
            self.user_rights.addItem("Access denied")
            self.user_rights.setCurrentIndex(int(level))
            self.user_layout.addWidget(self.user_label)
            self.user_layout.addWidget(self.user_rights)
            self.verticalLayout.addLayout(self.user_layout)
            self.box_list.append(self.user_rights)
            self.user_list.append(user)
            self.level_list.append(level)

        # Scrolling
        self.scrollWidget.setLayout(self.verticalLayout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.addWidget(self.scrollArea)
