import sqlite3
import pathlib
connection = sqlite3.connect('database.db')
print ('PATH',pathlib.Path())

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Первое сообщение', 'Это первый пост')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Второе сообщение', 'Это второй пост')
            )

connection.commit()
connection.close()
