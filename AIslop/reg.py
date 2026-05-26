import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QWidget, QApplication
import fromBD
import guest, client, manager, admin


class Ui_Form(object):
    def setupUi(self, Form):
        self.current_window = Form
        self.db = fromBD.sql1()

        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setWindowIcon(QtGui.QIcon("ahegao.jpg"))
        Form.setWindowTitle("Авторизация системы")

        layout = QtWidgets.QVBoxLayout(Form)

        self.lbl_login = QtWidgets.QLabel("Логин:")
        layout.addWidget(self.lbl_login)

        self.login_pole = QtWidgets.QLineEdit()
        layout.addWidget(self.login_pole)

        self.lbl_pass = QtWidgets.QLabel("Пароль:")
        layout.addWidget(self.lbl_pass)

        self.password_pole = QtWidgets.QLineEdit()
        self.password_pole.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_pole)

        self.vhodButton = QtWidgets.QPushButton("Войти в систему")
        layout.addWidget(self.vhodButton)

        self.GuestButton = QtWidgets.QPushButton("Продолжить как гость")
        layout.addWidget(self.GuestButton)

        self.vhodButton.clicked.connect(self.vhod)
        self.GuestButton.clicked.connect(self.window_guest)

    def vhod(self):
        login = self.login_pole.text().strip()
        password = self.password_pole.text().strip()

        if not login or not password:
            QMessageBox.warning(None, "Внимание", "Заполните все поля формы!")
            return

        try:
            data = self.db.vhod_v_sys(login, password)
            if data:
                role = str(data.get('role_id', '3'))
                fio = data.get('name', 'Авторизованный пользователь')

                self.new_window = QWidget()
                if role == '1':
                    self.ui = manager.Ui_Form()
                elif role == '2':
                    self.ui = admin.Ui_Form()
                else:
                    self.ui = client.Ui_Form()

                self.ui.user_fio = fio
                self.ui.setupUi(self.new_window)
                self.new_window.show()
                self.current_window.close()
            else:
                QMessageBox.warning(None, "Ошибка", "Неверный логин или секретный пароль!")
        except Exception as e:
            QMessageBox.critical(None, "Критическая ошибка", f"Ошибка БД: {str(e)}")

    def window_guest(self):
        self.new_window = QWidget()
        self.ui = guest.Ui_Form()
        self.ui.setupUi(self.new_window)
        self.new_window.show()
        self.current_window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())