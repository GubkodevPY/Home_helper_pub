import telebot
from telebot import types
from telebot.types import InlineKeyboardButton
import config
import sqlite3

bot = telebot.TeleBot(config.TOKEN)
purchasesName = None

import telebot
from telebot import types
from telebot.types import InlineKeyboardButton
import config
import sqlite3

bot = telebot.TeleBot(config.TOKEN)
purchasesName = None



@bot.message_handler()
def start(message):
    conn = sqlite3.connect('storege.db')
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Purchases (id INTEGER NOT NULL PRIMARY KEY,purchasesName varchar(50) NOT NULL,status INTEGER NOT NULL DEFAULT 1,createdOn DATATIME NOT NULL DEFAULT (DATETIME('now')))""")
    # """CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50))""")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Сейчас добавим')
    bot.register_next_step_handler(message, create_prod)


def create_prod(message):
    purchasesName = message.text.strip()

    conn = sqlite3.connect('storege.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO Purchases (purchasesName) VALUES ('%s')" % (purchasesName))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Cписок товаров', callback_data='show_products'))
    bot.send_message(message.chat.id, 'Успешно добавили', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'show_products')
def show_products(call):
    conn = sqlite3.connect('storege.db')
    cursor = conn.cursor()

    cursor.execute("SELECT purchasesName FROM Purchases")
    Purchases = cursor.fetchall()

    if not Purchases:
        bot.send_message(call.message.chat.id, "Список товаров:\nВ базе данных нет заметок.")
    else:
        response = "Список товаров:\n"
        for product in Purchases:
            response += f"- {product[0]}\n"
    bot.send_message(call.message.chat.id, response)

    keyboard = types.InlineKeyboardMarkup()
    btn_add_product = types.InlineKeyboardButton('Добавить товар', callback_data='create_prod')
    btn_del_product = types.InlineKeyboardButton('Удалить товар', callback_data='del_product')
    keyboard.add(btn_add_product, btn_del_product)

    bot.send_message(call.message.chat.id, "Что делаем со списком:", reply_markup=keyboard)



bot.polling(none_stop=True)

# def create_item(message):
#     item = message.text.strip()
#     bot.send_message(message.chat.id, 'введите название')
#     bot.register_next_step_handler(message, create_prod)


# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#         keyboard = types.InlineKeyboardMarkup()
#         btn_products = types.InlineKeyboardButton('Товары', callback_data='show_products')
#         btn_notes = types.InlineKeyboardButton('Заметки', callback_data='show_notes')
#         keyboard.add(btn_products, btn_notes)
#
#         # Отправка сообщения с клавиатурой
#         bot.send_message(message.chat.id, 'Нажмите на кнопку для просмотра функций:', reply_markup=keyboard)


# @bot.callback_query_handler(func=lambda call: call.data == 'show_products')
# def show_products(call):
#     conn = sqlite3.connect('Home_help.db')
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT purchasesName FROM Purchases")
#     Purchases = cursor.fetchall()
#
#     if not Purchases:
#         bot.send_message(call.message.chat.id, "Список товаров:\nВ базе данных нет заметок.")
#     else:
#         response = "Список товаров:\n"
#         for product in Purchases:
#             response += f"- {product[0]}\n"
#     bot.send_message(call.message.chat.id, response)
#
#     keyboard = types.InlineKeyboardMarkup()
#     btn_add_product = types.InlineKeyboardButton('Добавить товар', callback_data='add_product')
#     btn_del_product = types.InlineKeyboardButton('Удалить товар', callback_data='del_product')
#     keyboard.add(btn_add_product, btn_del_product)
#
#     bot.send_message(call.message.chat.id, "Что делаем со списком:", reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: call.data == 'add_product')
# def handle_add_product(call):
#     bot.send_message(call.message.chat.id, "Введите наименование товара:")
#
#
# # Функция добавления товара в базу данных
# #@bot.callback_query_handler(func=lambda call: call.data == 'add_product_to_db')
# def add_product_to_db(product_name):
#     conn = sqlite3.connect('Home_help.db')
#     cursor = conn.cursor()
#    cursor.execute("INSERT INTO purchases (purchasesName) VALUES (?)", (product_name,))
#     conn.commit()
#     conn.close()
#
# @bot.message_handler(func=lambda message: True)
# def handle_add_product(message):
#     product_name = message.text  # Получаем наименование товара из сообщения пользователя
#     add_product_to_db # Вызываем функцию для добавления товара в БД
#     bot.send_message(message.chat.id, f"Товар '{product_name}' успешно добавлен в базу данных.")  # Отправляем подтверждение пользователю
#
# # Заметки .... Не тогать
# @bot.callback_query_handler(func=lambda call: call.data == 'show_notes')
# def show_products(call):
#     conn = sqlite3.connect('Home_help.db')
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT NotesName FROM Notes")
#     Notes = cursor.fetchall()
#
#     if not Notes:
#         bot.send_message(call.message.chat.id, "Список заметок:\nВ базе данных нет заметок.")
#     else:
#         response = "Список заметок:\n"
#         for note in Notes:
#             response += f"- {note[0]}\n"
#         bot.send_message(call.message.chat.id, response)
#
#     cursor.close()
#     conn.close()

# bot.polling() # настройка бота на постоянное выполнение прапра
