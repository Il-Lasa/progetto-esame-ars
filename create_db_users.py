import sqlite3

conn = sqlite3.connect('prototipo/users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    user_type TEXT NOT NULL DEFAULT 'base'
)
''')

conn.commit()
conn.close()

print("Tabella 'users' creata con successo.")