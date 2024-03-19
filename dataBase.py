import sqlite3

conn = sqlite3.connect('Home_help.db')
cursor = conn.cursor()


# Создаем таблицу purchases
cursor.execute('''
CREATE TABLE IF NOT EXISTS Purchases (
id INTEGER NOT NULL PRIMARY KEY,
purchasesName varchar(50) NOT NULL,
status INTEGER NOT NULL DEFAULT 1,
createdOn DATATIME NOT NULL DEFAULT (DATETIME('now'))
)
''')

# Создаем таблицу Заметки
cursor.execute('''
CREATE TABLE IF NOT EXISTS Notes (
id INTEGER NOT NULL PRIMARY KEY,
NotesName TEXT NOT NULL,
NoteDescription TEXT,
status INTEGER NOT NULL DEFAULT 1,
createdOn DATATIME NOT NULL DEFAULT (DATETIME('now'))
)
''')



