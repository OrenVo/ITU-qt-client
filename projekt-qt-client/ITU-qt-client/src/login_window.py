from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QCheckBox
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

        # Vertical layout
        self.verticalLayout_1.addWidget(self.label_1)
        self.verticalLayout_1.addWidget(self.username)
        self.verticalLayout_1.addWidget(self.label_2)
        self.verticalLayout_1.addWidget(self.password)
        self.verticalLayout_1.addWidget(self.login_btn, 0, Qt.AlignHCenter | Qt.AlignVCenter)
        # Label text
        self.label_1.setText('Username:')
        self.label_2.setText('Password:')
        # Connecting slots
        self.login_btn.clicked.connect(self.login)
        self.client = Client()
        self.password.returnPressed.connect(self.login_btn.click)
        self.username.returnPressed.connect(self.login_btn.click)
        # Other
        self.main_window = None

    def login(self):
        user = self.username.text()
        password = self.password.text()
        if not self.client.login(username=user, password=password):
            ...  # show error
        else:
            self.hide()
            self.main_window = MainWindow(self)
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
