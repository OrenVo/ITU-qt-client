from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QCheckBox
from PySide2.QtGui import QIcon
from qtwidgets import PasswordEdit
from src.client import Client
from src.main_window import MainWindow
import sys
from PySide2.QtCore import Qt
# from PySide2.QtGui import


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.png'))
        if not self.objectName():
            self.setObjectName(u"LoginWindow")
        self.setWindowTitle('Shutdown Tool Login')
        # Layout
        self.verticalLayout_1 = QVBoxLayout(self)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        # Elements
        self.label_1 = QLabel(self)
        self.label_1.setObjectName(u"label")

        self.username = QLineEdit(self)
        self.username.setObjectName(u"username")

        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")

        self.password = PasswordEdit(self)
        self.password.setObjectName(u"password")
        self.password.setClearButtonEnabled(False)
        self.login_btn = QPushButton('Log in', self)
        self.login_btn.setObjectName(u"login_btn")
        # self.login_btn.setAutoDefault(True)
        self.error_label = QLabel(self)
        self.error_label.setObjectName(u"error_label")
        self.error_label.setStyleSheet('color: red')
        # Vertical layout
        self.verticalLayout_1.addWidget(self.label_1)
        self.verticalLayout_1.addWidget(self.username)
        self.verticalLayout_1.addWidget(self.label_2)
        self.verticalLayout_1.addWidget(self.password)
        self.verticalLayout_1.addWidget(self.login_btn, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        self.verticalLayout_1.addWidget(self.error_label)
        # Label text
        self.label_1.setText('Username:')
        self.label_2.setText('Password:')
        # Connecting slots
        self.login_btn.clicked.connect(self.login)
        self.client = Client()
        self.password.returnPressed.connect(self.login_btn.click)
        self.username.returnPressed.connect(self.login_btn.click)
        # Other
        self.setTabOrder(self.username, self.password)
        self.setTabOrder(self.password, self.login_btn)
        self.main_window = None

    def login(self):
        user = self.username.text()
        password = self.password.text()
        if not self.client.login(username=user, password=password):
            if self.client.code == 403:  # Bad login or password
                self.error_label.setText('Bad username or password')
            elif self.client.code == 401:  # Missing permissions
                self.error_label.setText('Missing permissions')
        else:
            self.error_label.setText('')
            self.hide()
            self.main_window = MainWindow(self)
            self.main_window.setWindowIcon(QIcon('icon.png'))
            self.main_window.center()
            self.main_window.show()

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.center()
    window.show()
    sys.exit(app.exec_())
