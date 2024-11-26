import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        print(f"Соединение с базой данных '{self.db_name}' установлено.")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"Соединение с базой данных '{self.db_name}' закрыто.")

    def execute(self, query, params=None):
        if not self.conn:
            raise Exception("Нет соединения с базой данных.")
        cursor = self.conn.cursor()
        cursor.execute(query, params or [])
        self.conn.commit()
        return cursor


class User:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def setup_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL
        )
        """
        self.db_manager.execute(query)
        print("Таблица 'users' создана или уже существует.")

    def add(self):
        username = input("Введите имя пользователя: ")
        email = input("Введите email пользователя: ")

        query = "INSERT INTO users (username, email) VALUES (?, ?)"
        self.db_manager.execute(query, (username, email))
        print(f"Пользователь '{username}' добавлен.")

    def get_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = ?"
        cursor = self.db_manager.execute(query, (user_id,))
        return cursor.fetchone()

    def delete(self, user_id):
        query = "DELETE FROM users WHERE id = ?"
        self.db_manager.execute(query, (user_id,))
        print(f"Пользователь с ID {user_id} удален.")


class Admin(User):
    def setup_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            permissions TEXT NOT NULL
        )
        """
        self.db_manager.execute(query)
        print("Таблица 'admins' создана или уже существует.")

    def add(self):
        username = input("Введите имя администратора: ")
        email = input("Введите email администратора: ")
        permissions = input("Введите уровень прав (например, full_access): ")

        query = "INSERT INTO admins (username, email, permissions) VALUES (?, ?, ?)"
        self.db_manager.execute(query, (username, email, permissions))
        print(f"Администратор '{username}' добавлен.")


class Customer(User):
    def setup_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """
        self.db_manager.execute(query)
        print("Таблица 'customers' создана или уже существует.")

    def add(self):
        username = input("Введите имя клиента: ")
        email = input("Введите email клиента: ")
        address = input("Введите адрес клиента: ")

        query = "INSERT INTO customers (username, email, address) VALUES (?, ?, ?)"
        self.db_manager.execute(query, (username, email, address))
        print(f"Клиент '{username}' добавлен.")


if __name__ == "__main__":
    db_manager = DatabaseManager("example.db")
    db_manager.connect()

    user_manager = User(db_manager)
    user_manager.setup_table()

    admin_manager = Admin(db_manager)
    admin_manager.setup_table()

    customer_manager = Customer(db_manager)
    customer_manager.setup_table()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить пользователя")
        print("2. Добавить администратора")
        print("3. Добавить клиента")
        print("4. Показать пользователя по ID")
        print("0. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            user_manager.add()
        elif choice == "2":
            admin_manager.add()
        elif choice == "3":
            customer_manager.add()
        elif choice == "4":
            user_id = int(input("Введите ID пользователя: "))
            user = user_manager.get_by_id(user_id)
            print(f"Пользователь: {dict(user) if user else 'не найден'}")
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    db_manager.disconnect()
