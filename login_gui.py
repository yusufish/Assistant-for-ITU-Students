from PyQt5.QtWidgets import *

class Login_window(QWidget):

    Username = ""
    Password = ""
    Remember_me = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AFITUS-Login")
        self.resize(350,150)

        login_layout = QGridLayout()

        label_username = QLabel('<font size="4"> Username </font>')
        login_layout.addWidget(label_username, 0 ,0)
        self.username = QLineEdit()
        self.username.setPlaceholderText("SIS Username")
        login_layout.addWidget(self.username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        login_layout.addWidget(label_password, 1, 0)
        self.password = QLineEdit()
        self.password.setPlaceholderText("SIS Password")
        self.password.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.password, 1, 1)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login_control)
        login_layout.addWidget(login_button, 2, 0)

        self.remember_me = QCheckBox("Remember Me")
        self.remember_me.stateChanged.connect(self.remember_state)
        login_layout.addWidget(self.remember_me, 2, 1)

        self.setLayout(login_layout)

    def remember_state(self):
        Login_window.Remember_me = True

    def value_assign(U,P):
        Login_window.Username = U
        Login_window.Password = P
    
    def login_control(self):
        Login_window.value_assign(self.username.text(), self.password.text())
        Login.quit()

Login = QApplication([])
window = Login_window()
window.show()
Login.exec()
