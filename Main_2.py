import telebot
from telebot import types
import config
import sqlite3

bot = telebot.TeleBot(config.TOKEN)
purchasesName = None

# Создание таблицы, если она не существует
def initialize_db():
    conn = sqlite3.connect('storege.db')
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS Purchases (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            purchasesName VARCHAR(50) NOT NULL,
            status INTEGER NOT NULL DEFAULT 1,
            createdOn DATETIME NOT NULL DEFAULT (DATETIME('now'))
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS Notes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            noteText TEXT NOT NULL,
            createdOn DATETIME NOT NULL DEFAULT (DATETIME('now'))
        )"""
    )
    conn.commit()
    cur.close()
    conn.close()

initialize_db()


# Стартовое сообщение и выбор действий
@bot.message_handler(commands=['start', 'help'])
def start(message):
    show_main_menu(message.chat.id)

# Функция для отображения главного меню
def show_main_menu(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    btn_show_products = types.InlineKeyboardButton('Список товаров', callback_data='show_products')
    btn_show_notes = types.InlineKeyboardButton('Список заметок', callback_data='show_notes')

    keyboard.add(btn_show_products, btn_show_notes)
    bot.send_message(chat_id, "Что хотите сделать?", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Добавить товар"
@bot.callback_query_handler(func=lambda call: call.data == 'add_product')
def handle_add_product(call):
    bot.send_message(call.message.chat.id, "Введите наименование товара:")
    bot.register_next_step_handler(call.message, create_prod)

# Обработчик ввода наименования товара
def create_prod(message):
    purchasesName = message.text.strip()
    if purchasesName:
        conn = sqlite3.connect('storege.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Purchases (purchasesName) VALUES (?)", (purchasesName,))
            conn.commit()
            bot.send_message(message.chat.id, f"Товар '{purchasesName}' успешно добавлен.")
            ask_for_another_product(message)
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, f"Ошибка при добавлении товара: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        bot.send_message(message.chat.id, "Вы не ввели название товара. Попробуйте еще раз.")

def ask_for_another_product(message):
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='add_product')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='show_products')
    keyboard.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, "Хотите добавить еще товар?", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Список товаров"
@bot.callback_query_handler(func=lambda call: call.data == 'show_products')
def show_products(call):
    conn = sqlite3.connect('storege.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, purchasesName FROM Purchases")
    purchases = cursor.fetchall()
    cursor.close()
    conn.close()

    if not purchases:
        bot.send_message(call.message.chat.id, "Список товаров:\nВ базе данных нет товаров.")
    else:
        response = "Список товаров:\n"
        for product in purchases:
            response += f"- {product[1]}\n"
        bot.send_message(call.message.chat.id, response)

    keyboard = types.InlineKeyboardMarkup()
    btn_add_product = types.InlineKeyboardButton('Добавить товар', callback_data='add_product')
    btn_del_product = types.InlineKeyboardButton('Удалить товар', callback_data='confirm_delete')
    btn_main_menu = types.InlineKeyboardButton('На главный экран', callback_data='main_menu')
    keyboard.add(btn_add_product, btn_del_product, btn_main_menu)

    bot.send_message(call.message.chat.id, "Что делаем со списком:", reply_markup=keyboard)

# Подтверждение удаления товара
@bot.callback_query_handler(func=lambda call: call.data == 'confirm_delete')
def confirm_delete(call):
    conn = sqlite3.connect('storege.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, purchasesName FROM Purchases")
    purchases = cursor.fetchall()
    cursor.close()
    conn.close()

    if not purchases:
        bot.send_message(call.message.chat.id, "Список товаров:\nВ базе данных нет товаров.")
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for product in purchases:
            btn_del_product = types.InlineKeyboardButton(f'Удалить {product[1]}', callback_data=f'del_product_{product[0]}')
            keyboard.add(btn_del_product)
        btn_main_menu = types.InlineKeyboardButton('На главный экран', callback_data='main_menu')
        keyboard.add(btn_main_menu)
        bot.send_message(call.message.chat.id, "Выберите товар для удаления:", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Удалить товар"
@bot.callback_query_handler(func=lambda call: call.data.startswith('del_product_'))
def del_product(call):
    product_id = int(call.data.split('_')[2])
    conn = sqlite3.connect('storege.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Purchases WHERE id = ?", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(call.message.chat.id, f"Товар с ID {product_id} удален.")
    confirm_delete(call)

# Обработчик нажатия на кнопку "На главный экран"
@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def go_to_main_menu(call):
    show_main_menu(call.message.chat.id)


# # работа с заметками
# # Обработчик нажатия на кнопку "Добавить заметку"
# @bot.callback_query_handler(func=lambda call: call.data == 'show_notes')
# def handle_show_notes(call):
#     bot.send_message(call.message.chat.id, "Введите наименование товара:")
#     bot.register_next_step_handler(call.message, show_notes)
#
# # Обработчик нажатия на кнопку "Список товаров"
# @bot.callback_query_handler(func=lambda call: call.data == 'show_notes')
# def show_notes(call):
#     conn = sqlite3.connect('storege.db')
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT id, noteText FROM Notes")
#     noteText = cursor.fetchall()
#     cursor.close()
#     conn.close()
#
#     if not noteText:
#         bot.send_message(call.message.chat.id, "Список товаров:\nВ базе данных нет товаров.")
#     else:
#         response = "Список товаров:\n"
#         for product in noteText:
#             response += f"- {product[1]}\n"
#         bot.send_message(call.message.chat.id, response)
#
#     keyboard = types.InlineKeyboardMarkup()
#     btn_add_product = types.InlineKeyboardButton('Добавить товар', callback_data='add_product')
#     btn_del_product = types.InlineKeyboardButton('Удалить товар', callback_data='confirm_delete')
#     btn_main_menu = types.InlineKeyboardButton('На главный экран', callback_data='main_menu')
#     keyboard.add(btn_add_product, btn_del_product, btn_main_menu)
#
#     bot.send_message(call.message.chat.id, "Что делаем со списком:", reply_markup=keyboard)

# Запуск бота
bot.polling(none_stop=True)
