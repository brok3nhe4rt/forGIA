from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import fromBD, os, shutil
import traceback


class Ui_ProductDialog(object):
    def __init__(self, articul, parent_ui):
        self.articul = articul
        self.parent_ui = parent_ui
        self.db = fromBD.sql1()
        self.img_name = ""

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 550)
        Dialog.setWindowTitle("Управление свойствами товара")

        layout = QVBoxLayout(Dialog)

        self.lbl_id = QLabel()
        layout.addWidget(self.lbl_id)

        layout.addWidget(QLabel("Наименование товара:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Описание товара:"))
        self.desc_input = QLineEdit()
        layout.addWidget(self.desc_input)

        layout.addWidget(QLabel("Поставщик:"))
        self.supplier_input = QLineEdit()
        layout.addWidget(self.supplier_input)

        layout.addWidget(QLabel("Цена товара (руб.):"))
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999.99)
        layout.addWidget(self.price_input)

        layout.addWidget(QLabel("Количество на складе (шт.):"))
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(99999)
        layout.addWidget(self.stock_input)

        layout.addWidget(QLabel("Действующая скидка (%):"))
        self.disc_input = QSpinBox()
        self.disc_input.setMaximum(100)
        layout.addWidget(self.disc_input)

        # Выбор изображения
        img_layout = QHBoxLayout()
        self.btn_img = QPushButton("Выбрать изображение товара")
        self.btn_img.clicked.connect(self.choose_image)
        img_layout.addWidget(self.btn_img)
        self.img_label = QLabel("Нет изображения")
        img_layout.addWidget(self.img_label)
        layout.addLayout(img_layout)

        # Кнопки сохранения и удаления
        self.btn_save = QPushButton("Сохранить изменения")
        self.btn_save.clicked.connect(self.save_data)
        layout.addWidget(self.btn_save)

        self.btn_delete = QPushButton("Удалить данный товар")
        self.btn_delete.setStyleSheet("color: red;")
        self.btn_delete.clicked.connect(self.delete_data)
        layout.addWidget(self.btn_delete)

        if self.articul:
            self.lbl_id.setText(f"Редактирование товара ID: {self.articul}")
            self.load_product_info()
        else:
            self.lbl_id.setText(f"Регистрация нового товара")
            self.btn_delete.setVisible(False)

        Dialog.finished.connect(self.on_close)

    def load_product_info(self): #Загружает данные товара в поля формы (для редактирования)
        try:
            products = self.db.show_menu()
            for p in products:
                if str(p['articul']) == str(self.articul):
                    self.name_input.setText(p.get('name_tovara', ''))
                    self.desc_input.setText(p.get('description', ''))
                    self.supplier_input.setText(p.get('supplier', ''))
                    self.price_input.setValue(float(p.get('price', 0)))
                    self.stock_input.setValue(int(p.get('tovar_na_sklade', 0)))
                    self.disc_input.setValue(int(p.get('disc', 0)))
                    self.img_name = p.get('img', '')
                    self.img_label.setText(self.img_name if self.img_name else "Нет изображения")
                    break
        except Exception as e:
            QMessageBox.warning(self.dialog, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def choose_image(self): #выбирает изображение для товара через окно выбора файла
        try:
            file_path, _ = QFileDialog.getOpenFileName(self.dialog, "Выберите фото", "", "Images (*.jpg *.png *.jpeg)")
            if file_path:
                # Ограничение размера 300х200 по ТЗ
                img = QImage(file_path)
                if img.width() > 300 or img.height() > 200:
                    QMessageBox.warning(self.dialog, "Ошибка размера",
                                        "Изображение превышает лимит размера 300x200 пикселей!")
                    return

                # Создаем папку в ТОЙ ЖЕ директории, где и программа
                img_dir = os.path.join(os.path.dirname(__file__), 'test')
                os.makedirs(img_dir, exist_ok=True)

                # Сохраняем с оригинальным именем или генерируем новое
                original_name = os.path.basename(file_path)
                dest_path = os.path.join(img_dir, original_name)
                shutil.copy(file_path, dest_path)
                self.img_name = original_name
                self.img_label.setText(self.img_name)
        except Exception as e:
            QMessageBox.warning(self.dialog, "Ошибка", str(e))

    def save_data(self): #Сохраняет товар в базу данных (добавление или обновление)
        try:
            # Проверка обязательных полей
            if not self.name_input.text().strip():
                QMessageBox.warning(self.dialog, "Внимание", "Заполните поле наименования товара!")
                return

            # Получаем артикул
            if self.articul:
                articul = self.articul
            else:
                articul = str(self.db.get_max_id())

            # Формируем данные для сохранения
            data = {
                'articul': articul,
                'name_tovara': self.name_input.text().strip(),
                'description': self.desc_input.text().strip(),
                'supplier': self.supplier_input.text().strip(),
                'price': self.price_input.value(),
                'tovar_na_sklade': self.stock_input.value(),
                'disc': self.disc_input.value(),
                'img': self.img_name if self.img_name else "picture.png"
            }

            # Сохраняем в БД
            if self.articul:
                success = self.db.update_product(self.articul, data)
            else:
                success = self.db.add_product(data)

            if success:
                QMessageBox.information(self.dialog, "Успех", "Данные товара сохранены!")
                # Проверяем, существует ли метод load_data у родителя
                if hasattr(self.parent_ui, 'load_data'):
                    self.parent_ui.load_data()
                self.dialog.close()
            else:
                QMessageBox.warning(self.dialog, "Ошибка", "Не удалось сохранить данные в БД!")

        except Exception as e:
            QMessageBox.critical(self.dialog, "Ошибка", f"Сбой при сохранении:\n{str(e)}\n{traceback.format_exc()}")

    def delete_data(self): #Удаляет товар из базы данных
        reply = QMessageBox.question(self.dialog, "Подтверждение", "Вы уверены, что хотите безвозвратно удалить товар?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success = self.db.delete_product(self.articul)
            if success:
                QMessageBox.information(self.dialog, "Успех", "Товар успешно удален.")
                if hasattr(self.parent_ui, 'load_data'):
                    self.parent_ui.load_data()
                self.dialog.close()
            else:
                QMessageBox.critical(self.dialog, "Ошибка удаления",
                                     "Невозможно удалить товар: присутствует в активных заказах!")

    def on_close(self): #Сбрасывает флаг открытого окна при закрытии. ЧТобы короче только 1 окно открыто было
        if hasattr(self.parent_ui, 'edit_window_open'):
            self.parent_ui.edit_window_open = False