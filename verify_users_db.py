import sqlite3

conn = sqlite3.connect('prototipo/users.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
table_exists = cursor.fetchone()

if table_exists:
    print("La tabella 'users' esiste.")
else:
    print("La tabella 'users' non esiste.")

conn.close()
