import sqlite3

# def initiate_db():
#     connection = sqlite3.connect('telegram_database.db')
#     cursor = connection.cursor()
#
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Products(
#     id INTEGER PRIMARY KEY,
#     title TEXT NOT NULL,
#     description TEXT NOT NULL,
#     price INTEGER
#     )
#     ''')
#
#     connection.commit()
#     connection.close()


def initiate_db():
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (username, email, age, 1000))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    username_list = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if username_list.fetchone() is None:
        return False
    else:
        return True


def get_all_products():
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    all_products = cursor.fetchall()
    connection.commit()
    return all_products


def create_users():
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    for i in range(1, 5):
        age = 10 * i
        cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                       (f'username {i}', f'email{i}@.com', age, 1000))
    connection.commit()
    connection.close()


initiate_db()
# create_users()
