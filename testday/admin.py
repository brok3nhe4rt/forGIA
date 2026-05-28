from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import fromBD, os, product_dialog


class ClickableFrame(QFrame): # функции нужны для того, чтобы пользователь нажал и ему вылезло окно редактирвоания
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, articul):
        super().__init__()
        self.articul = articul

    def mousePressEvent(self, event):
        self.clicked.emit(self.articul)


class Ui_Form(object):
    def __init__(self):
        self.user_fio = "Администратор"
        self.edit_window_open = False  # Защита от открытия более одного окна


    def setupUi(self, Form): # интерфейс программы
        self.window = Form
        Form.resize(1000, 750)
        Form.setWindowTitle("Панель Управления Администратора")
        Form.setWindowIcon(QIcon("ahegao.jpg"))

        main_layout = QVBoxLayout(Form)
        self.db = fromBD.sql1()

        header = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("ahegao.jpg").scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        header.addWidget(logo)

        self.btn_add = QPushButton("Добавить новый товар")
        self.btn_add.clicked.connect(lambda: self.open_dialog(None))
        header.addWidget(self.btn_add)
        header.addStretch()

        header.addWidget(QLabel(f"Админ: {self.user_fio}"))
        self.btn_back = QPushButton("Выйти")
        self.btn_back.clicked.connect(self.go_back)
        header.addWidget(self.btn_back)
        main_layout.addLayout(header)

        # Поиск / Сортировка
        ctrl_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Быстрый поиск товаров...")
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

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.menu_layout = QVBoxLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        self.load_data()

    def load_data(self): # Отображение списка товаров в виде кастомных кликабельных фреймов для  редактирования
        for i in reversed(range(self.menu_layout.count())):
            self.menu_layout.itemAt(i).widget().setParent(None)

        products = self.db.show_menu()
        search_text = self.search_input.text().lower()
        selected_supplier = self.filter_box.currentText()


        #Фильтрация
        filtered = []
        for i in products:
            if search_text and (search_text not in i.get('name_tovara', '').lower() and search_text not in i.get('huy',
                                                                                                                 '').lower()):
                continue
            if selected_supplier != "Все поставщики" and i.get('supplier', '') != selected_supplier:
                continue
            filtered.append(i)

        if self.sort_box.currentIndex() == 1:
            filtered.sort(key=lambda x: int(x.get('tovar_na_sklade', 0)))
        elif self.sort_box.currentIndex() == 2:
            filtered.sort(key=lambda x: int(x.get('tovar_na_sklade', 0)), reverse=True)

        # Получаем путь к папке с изображениями
        img_dir = os.path.join(os.path.dirname(__file__), 'test')

        for i in filtered:
            frame = ClickableFrame(i['articul'])
            frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            frame.clicked.connect(self.open_dialog)
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
                    # Если картинки нет, ставим заглушку
                    photo.setPixmap(QPixmap("picture.png").scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            else:
                photo.setPixmap(QPixmap("picture.png").scaled(320, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            l_frame2.addWidget(photo)

            text = QLabel(
                f"{i['name_tovara']} (Клик для ред.)\nАртикул: {i['articul']}\nПоставщик: {i.get('supplier', '-')}\nЦена: {i['price']} руб.\nНа складе: {i['tovar_na_sklade']} шт.")
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

    def open_dialog(self, articul): # Открытие диалогового окна редактирования/добавления товара с системным запретом на открытие дубликатов окон
        try:
            if self.edit_window_open:
                QMessageBox.warning(None, "Ограничение системы","Разрешено открывать только одно окно редактирования одновременно!")
                return
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', str(e))


        self.edit_window_open = True
        self.diag = QDialog()
        self.ui_diag = product_dialog.Ui_ProductDialog(articul, self)
        self.ui_diag.setupUi(self.diag)
        self.diag.show()

    def go_back(self): #функция для возвращения пользователя в окно регистарции при нажатии кнопки "Выйти" в интерфейсе
        import reg
        self.reg_win = QWidget()
        self.ui = reg.Ui_Form()
        self.ui.setupUi(self.reg_win)
        self.reg_win.show()
        self.window.close()