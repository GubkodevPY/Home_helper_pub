import sqlite3

conn = sqlite3.connect('Home_help.db')
cursor = conn.cursor()

# Функция для получения товаров
cursor.execute('SELECT * FROM Purchases')
Purchases = cursor.fetchall()

# Выводим результаты
for user in Purchases:
  print(Purchases)

conn.close()


# Функция для добавления нового товара в список
def add_Purchases(purchasesName):
    cursor.execute('INSERT INTO Purchases (purchasesName) VALUES (?)', (purchasesName,))
    conn.commit()

# Функция для добавления заметки
def add_Note(NoteName):
    cursor.execute('INSERT INTO Notes (NoteName) VALUES (?)', (NoteName,))
    conn.commit()


# Функция для обновления статуса задачи
def update_task_status(task_id, status):
  cursor.execute('UPDATE Tasks SET status = ? WHERE id = ?', (status, task_id))
  conn.commit()

# Сохраняем изменения и закрываем соединение
conn.close()
