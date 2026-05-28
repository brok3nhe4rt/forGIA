from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import fromBD, os


class Ui_Form(object):
    def __init__(self):
        self.user_fio = "Пользователь"

    def setupUi(self, Form): # интерфейс программы
        self.window = Form
        Form.setObjectName("Form")
        Form.resize(900, 650)
        Form.setWindowTitle("Каталог продукции (Клиент)")
        Form.setWindowIcon(QIcon("ahegao.jpg"))

        main_layout = QVBoxLayout(Form)

        header = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("ahegao.jpg").scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        header.addWidget(logo)
        header.addStretch()

        # Правый верхний угол: ФИО + кнопка выхода
        header.addWidget(QLabel(f"Вы вошли как: <b>{self.user_fio}</b> (Клиент)"))
        self.btn_back = QPushButton("Выйти")
        self.btn_back.clicked.connect(self.go_back)
        header.addWidget(self.btn_back)
        main_layout.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        self.db = fromBD.sql1()
        self.load_data()

    def load_data(self): # Отображение списка товаров в виде кастомных кликабельных фреймов для  редактирования
        products = self.db.show_menu()

        # Получаем путь к папке с изображениями
        img_dir = os.path.join(os.path.dirname(__file__), 'test')

        for i in products:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            l_frame = QHBoxLayout(frame)

            frame2 = QFrame()
            frame2.setFrameStyle(QFrame.Shape.Box)
            l_frame2 = QVBoxLayout(frame2)

            frame3 = QFrame()
            frame3.setFrameStyle(QFrame.Shape.Box)
            l_frame3 = QVBoxLayout(frame3)

            frame4 = QFrame()
            frame4.setFrameStyle(QFrame.Shape.Box)
            l_frame4 = QVBoxLayout(frame4)


            photo = QLabel()

            # Формируем правильный путь к изображению
            img_name = i.get('img', '')
            if img_name:
                img_path = os.path.join(img_dir, img_name)
                if os.path.exists(img_path):
                    photo.setPixmap(QPixmap(img_path).scaled(150, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    photo.setPixmap(QPixmap("picture.png").scaled(150, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            else:
                photo.setPixmap(QPixmap("picture.png").scaled(150, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            l_frame2.addWidget(photo)

            text = QLabel(
                f"{i['name_tovara']}\nАртикул: {i['articul']}\nОписание: {i['description']}\nЦена: {i['price']} руб.\nНа складе: {i['tovar_na_sklade']} шт.")
            l_frame3.addWidget(text, stretch=2)

            disc_lbl = QLabel(f"Скидка:{i['disc']}%")
            l_frame4.addWidget(disc_lbl)

            if int(i.get('disc', 0)) >= 15:
                frame.setStyleSheet("background-color: #d4edda;")
            if int(i.get('tovar_na_sklade', 0)) == 0:
                frame.setStyleSheet("background-color: #e2e3e5;")

            l_frame.addWidget(frame2)
            l_frame.addWidget(frame3)
            l_frame.addWidget(frame4)


            self.menu_layout.addWidget(frame)
    def go_back(self): #функция для возвращения пользователя в окно регистарции при нажатии кнопки "Выйти" в интерфейсе
        import reg
        self.reg_win = QWidget()
        self.ui = reg.Ui_Form()
        self.ui.setupUi(self.reg_win)
        self.reg_win.show()
        self.window.close()