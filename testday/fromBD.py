import pymysql
import os
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

class sql1():
    def __init__(self): #Функция подключения бд
        self.conn = pymysql.connect(
            host = os.getenv('DB_HOST', '127.0.0.1'),
            user = os.getenv('DB_USER', 'root'),
            password = os.getenv('DB_PASSWORD', '12345'),
            db = os.getenv('DB_NAME', 'db1'),
            cursorclass = DictCursor
        )
        self.cursor = self.conn.cursor()

    def vhod_v_sys(self, login, password): # Фкнция для входа (регистрация)
        self.cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (login, password))
        return self.cursor.fetchone()

    def show_menu(self): #показывает все товары из табилцы
        self.cursor.execute('SELECT * FROM Tovar')
        return self.cursor.fetchall()

    def get_suppliers(self): #получает поставщика товаров для того чтобы в комбобоксе его норм отобразить
        try:
            self.cursor.execute('SELECT DISTINCT supplier FROM Tovar WHERE supplier IS NOT NULL AND supplier != ""')
            return [row['supplier'] for row in self.cursor.fetchall()]
        except Exception:
            return ["Поставщик 1", "Поставщик 2"] # Заглушка, если базы нет

    def get_max_id(self): # генерирует новый уникальный ID (артикул) для добавляемого товара
        try:
            self.cursor.execute('SELECT MAX(CAST(articul AS SIGNED)) as max_id FROM Tovar')
            res = self.cursor.fetchone()
            return int(res['max_id']) + 1 if res and res['max_id'] else 1
        except Exception:
            return 1000

    def add_product(self, data): #фунция для добавления нового товара
        try:
            sql = """INSERT INTO Tovar (articul, name_tovara, description, price, tovar_na_sklade, disc, img, supplier) 
                     VALUES (%(articul)s, %(name_tovara)s, %(description)s, %(price)s, %(tovar_na_sklade)s, %(disc)s, %(img)s, %(supplier)s)"""
            self.cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении товара: {e}")
            return False

    def update_product(self, articul, data):
        try:
            # Переписываем запрос на полностью именованные параметры
            sql = """
                UPDATE Tovar 
                SET name_tovara = %(name_tovara)s, 
                    description = %(description)s, 
                    price = %(price)s, 
                    tovar_na_sklade = %(tovar_na_sklade)s, 
                    disc = %(disc)s, 
                    img = %(img)s, 
                    supplier = %(supplier)s 
                WHERE articul = %(current_articul)s
            """
            # Добавляем артикул прямо в словарь с данными
            data['current_articul'] = articul

            self.cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении товара в БД: {e}")
            return False

    def delete_product(self, articul): #функция удаления товара
        try:
            # Проверка связи с заказами (если таблица существует)
            self.cursor.execute('SELECT * FROM Order_Tovar WHERE tovar_articul = %s', (articul,))
            if self.cursor.fetchone():
                return False
        except Exception:
            pass
        self.cursor.execute('DELETE FROM Tovar WHERE articul = %s', (articul,))
        self.conn.commit()
        return True

    def insert_tovar(self, articul, name, description, price, sklad, disc, img, supplier): #редактирование товара
        try:
            sql = """
                INSERT INTO Tovar (articul, name_tovara, description, price, tovar_na_sklade, disc, img, supplier)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (articul, name, description, price, sklad, disc, img, supplier))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении нового товара в БД: {e}")
            return False

