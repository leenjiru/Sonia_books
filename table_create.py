import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table_users = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_table_users)

create_table_books = "CREATE TABLE IF NOT EXISTS books(name text, price real)"
cursor.execute(create_table_books)

connection.commit()

connection.close()

