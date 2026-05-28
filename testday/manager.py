from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import fromBD, os


class Ui_Form(object):
    def __init__(self):
        self.user_fio = "Менеджер"

    def setupUi(self, Form):
        self.window = Form
        Form.resize(950, 700)
        Form.setWindowTitle("Панель Менеджера")
        Form.setWindowIcon(QIcon("ahegao.jpg"))

        main_layout = QVBoxLayout(Form)
        self.db = fromBD.sql1()

        # Шапка макета
        header = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("ahegao.jpg").scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        header.addWidget(logo)
        header.addStretch()
        header.addWidget(QLabel(f"Сотрудник: {self.user_fio}"))

        self.btn_back = QPushButton("Выйти")
        self.btn_back.clicked.connect(self.go_back)
        header.addWidget(self.btn_back)
        main_layout.addLayout(header)

        # Панель управления (Поиск, Сортировка, Фильтрация)
        ctrl_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию или описанию...")
        self.search_input.textChanged.connect(self.load_data)
        ctrl_layout.addWidget(self.search_input)

        self.sort_box = QComboBox()
        self.sort_box.addItems(["Без сортировки", "Остаток: по возрастанию", "Остаток: по убыванию"])
        self.sort_box.currentIndexChanged.connect(self.load_data)
        ctrl_layout.addWidget(self.sort_box)

        self.filter_box = QComboBox()
        self.filter_box.addItem("Все поставщики")
        self.filter_box.addItems(self.db.get_suppliers())
        self.filter_box.currentIndexChanged.connect(self.load_data)
        ctrl_layout.addWidget(self.filter_box)

        main_layout.addLayout(ctrl_layout)

        # Список
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        self.load_data()

    def load_data(self):
        for i in reversed(range(self.menu_layout.count())):
            self.menu_layout.itemAt(i).widget().setParent(None)

        products = self.db.show_menu()
        search_text = self.search_input.text().lower()
        selected_supplier = self.filter_box.currentText()

        filtered_products = []
        for i in products:
            # Поиск
            name = i.get('name_tovara', '').lower()
            desc = i.get('description', '').lower()
            if search_text and (search_text not in name and search_text not in desc):
                continue
            # Фильтрация
            supplier = i.get('supplier', '')
            if selected_supplier != "Все поставщики" and supplier != selected_supplier:
                continue
            filtered_products.append(i)

        # Сортировка по количеству на складе
        if self.sort_box.currentIndex() == 1:
            filtered_products.sort(key=lambda x: int(x.get('tovar_na_sklade', 0)))
        elif self.sort_box.currentIndex() == 2:
            filtered_products.sort(key=lambda x: int(x.get('tovar_na_sklade', 0)), reverse=True)

        # Получаем путь к папке с изображениями
        img_dir = os.path.join(os.path.dirname(__file__), 'test')

        for i in filtered_products:
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
                    photo.setPixmap(QPixmap(img_path).scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    photo.setPixmap(QPixmap("picture.png").scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            else:
                photo.setPixmap(QPixmap("picture.png").scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            l_frame2.addWidget(photo)

            text = QLabel(
                f"{i['name_tovara']}\nАртикул: {i['articul']}\nПоставщик: {i.get('supplier', '-')}\nЦена: {i['price']} руб.\nНа складе: {i['tovar_na_sklade']} шт.")
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

    def go_back(self):
        import reg
        self.reg_win = QWidget()
        self.ui = reg.Ui_Form()
        self.ui.setupUi(self.reg_win)
        self.reg_win.show()
        self.window.close()