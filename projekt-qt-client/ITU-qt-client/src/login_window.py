from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow
from qtwidgets import PasswordEdit
from src.client import Client
from src.main_window import MainWindow
import sys
from PySide2.QtCore import Qt
# from PySide2.QtGui import


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        if not self.objectName():
            self.setObjectName(u"LoginWindow")
        self.setWindowTitle('Shutdown Tool Login')
        # Layout
        self.verticalLayout_1 = QVBoxLayout(self)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        # Elements
        self.label_1 = QLabel(self)
        self.label_1.setObjectName(u"label")
        self.verticalLayout_1.addWidget(self.label_1)
        self.username = QLineEdit(self)
        self.username.setObjectName(u"username")
        self.verticalLayout_1.addWidget(self.username)
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        self.verticalLayout_1.addWidget(self.label_2)
        self.password = PasswordEdit(self)
        self.password.setObjectName(u"password")
        self.password.setClearButtonEnabled(False)
        self.verticalLayout_1.addWidget(self.password)
        self.login_btn = QPushButton('Log in', self)
        self.login_btn.setObjectName(u"login_btn")
        self.verticalLayout_1.addWidget(self.login_btn, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        # Label text
        self.label_1.setText('Username:')
        self.label_2.setText('Password:')
        # Connecting slots
        self.login_btn.clicked.connect(self.login)
        self.client = Client()
        self.main_window = None

    def login(self):
        user = self.username.text()
        password = self.password.text()
        if not self.client.login(username=user, password=password):
            ...  # show error
        else:
            self.hide()
            self.main_window = MainWindow(self)
            self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    #widget.center()
    window.show()
    sys.exit(app.exec_())
