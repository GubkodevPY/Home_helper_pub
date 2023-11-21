import telebot
import config
from telebot import types
import sqlite3

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
        keyboard = types.InlineKeyboardMarkup()
        btn_products = types.InlineKeyboardButton('Товары', callback_data='show_products')
        btn_notes = types.InlineKeyboardButton('Заметки', callback_data='show_notes')
        keyboard.add(btn_products, btn_notes)

        # Отправка сообщения с клавиатурой
        bot.send_message(message.chat.id, 'Нажмите на кнопку для просмотра функций:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'show_products')
def show_products(call):
    conn = sqlite3.connect('Home_help.db')
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
    btn_add_product = types.InlineKeyboardButton('Добавить товар', callback_data='add_product')
    btn_del_product = types.InlineKeyboardButton('Удалить товар', callback_data='del_product')
    keyboard.add(btn_add_product, btn_del_product)

    cursor.close()
    conn.close()

    bot.send_message(call.message.chat.id, "Что делаем со списком:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'add_product')
def handle_add_product(call):
    bot.send_message(call.message.chat.id, "Введите наименование товара:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print("Получено сообщение:", message.text)  # Добавьте это отладочное сообщение
    if message.text:
        result = add_product(message.text)
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "Вы не передали название товара.")

def add_product(product_name):
    # Подключение к базе данных
    conn = sqlite3.connect('Home_help.db')
    cursor = conn.cursor()

    try:
        # Добавление товара в базу данных
        cursor.execute("INSERT INTO purchases (purchasesName) VALUES (?)", (product_name,))
        conn.commit()
        return f"Товар '{product_name}' успешно добавлен в базу данных!"
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении товара: {e}")
        return f"Ошибка при добавлении товара: {e}"
    finally:
        conn.close()


# Заметки .... Не тогать
@bot.callback_query_handler(func=lambda call: call.data == 'show_notes')
def show_products(call):
    conn = sqlite3.connect( 'Home_help.db')
    cursor = conn.cursor()

    cursor.execute("SELECT NotesName FROM Notes")
    Notes = cursor.fetchall()

    if not Notes:
        bot.send_message(call.message.chat.id, "Список заметок:\nВ базе данных нет заметок.")
    else:
        response = "Список заметок:\n"
        for note in Notes:
            response += f"- {note[0]}\n"
        bot.send_message(call.message.chat.id, response)

    cursor.close()
    conn.close()

bot.polling() # настройка бота на постоянное выполнение прапра

