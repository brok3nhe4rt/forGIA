from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import fromBD, os


class Ui_Form(object): #интерйес
    def setupUi(self, Form):
        self.window = Form
        Form.setObjectName("Form")
        Form.resize(900, 650)
        Form.setWindowTitle("Каталог продукции (Режим гостя)")
        Form.setWindowIcon(QIcon("ahegao.jpg"))

        main_layout = QVBoxLayout(Form)

        # Шапка макета
        header = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("ahegao.jpg").scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        header.addWidget(logo)

        header.addWidget(QLabel("Вы вошли как: Гость"))
        header.addStretch()

        self.btn_back = QPushButton("Назад к авторизации")
        self.btn_back.clicked.connect(self.go_back)
        header.addWidget(self.btn_back)
        main_layout.addLayout(header)

        # Список продукции
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        self.db = fromBD.sql1()
        self.load_data()

    def load_data(self): #фукнцяи для добавления инфомрцции в интерфейс

        # Очистка
        for i in reversed(range(self.menu_layout.count())):
            self.menu_layout.itemAt(i).widget().setParent(None)

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


            # Блок фото
            photo = QLabel()

            # Формируем правильный путь к изображению
            img_name = i.get('img', '')
            if img_name:
                img_path = os.path.join(img_dir, img_name)
                if os.path.exists(img_path):
                    photo.setPixmap(QPixmap(img_path).scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    photo.setPixmap(QPixmap("picture.png").scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            else:
                photo.setPixmap(QPixmap("picture.png").scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            l_frame2.addWidget(photo)

            # Блок описания
            text = QLabel(
                f"{i['name_tovara']}\nАртикул: {i['articul']}\nОписание: {i['description']}\nЦена: {i['price']} руб.\nНа складе: {i['tovar_na_sklade']} шт.")
            l_frame3.addWidget(text, stretch=2)

            # Блок скидки
            disc_lbl = QLabel(f"Скидка:{i['disc']}%")
            l_frame4.addWidget(disc_lbl)

            # Условное форматирование по спецификации ГИА
            if int(i.get('disc', 0)) >= 15:
                frame.setStyleSheet("background-color: #d4edda;")  # Светло-зеленый
            if int(i.get('tovar_na_sklade', 0)) == 0:
                frame.setStyleSheet("background-color: #e2e3e5;")  # Светло-серый

            l_frame.addWidget(frame2)
            l_frame.addWidget(frame3)
            l_frame.addWidget(frame4)


            self.menu_layout.addWidget(frame)

    def go_back(self):
        import reg
        self.reg_win = QWidget()
        self.ui = reg.Ui_Form()
        self.ui.setupUi(self.reg_win)
        self.reg_win.show()
        self.window.close()