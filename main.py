import telebot, sqlite3
from telebot import types

token = '2085064048:AAGMJJd6Pwr20WQnjYB0csBZPXm9qk0dx2o'
bot = telebot.TeleBot(token)

markup = types.ReplyKeyboardMarkup(row_width=2)  # Da ili Net
item1 = types.KeyboardButton('Да!')
item2 = types.KeyboardButton('Нет...')
markup.add(item1, item2)

markup2 = types.ReplyKeyboardMarkup()
item = types.KeyboardButton('Проставиться')
markup2.add(item)

def start():

    db = sqlite3.connect('Users.db')

    query_for_users = '''CREATE TABLE IF NOT EXISTS User_info (id INTEGER PRIMARY KEY, name TEXT)'''
    days_for_users = '''CREATE TABLE IF NOT EXISTS User_days (id INTEGER PRIMARY KEY, name TEXT, days INTEGER)'''

    cursor = db.cursor()

    cursor.execute(query_for_users)
    cursor.execute(days_for_users)

    db.commit()
    cursor.close()


@bot.message_handler(commands=['start'])
def welcome(message):

    db = sqlite3.connect('Users.db')
    cursor = db.cursor()

    try:
        cursor.execute(f'''INSERT INTO User_info (id, name) VALUES ({str(message.chat.id)}, "{message.chat.first_name}")''')
    except:
        pass

    db.commit()
    cursor.close()

    bot.send_message(message.chat.id, f'''Приветствую тебя {message.chat.first_name}.
Каждый ноябрь мы устраиваем NNN (Not Nut November). Так мы отдаём честь художникам, которые дают нам такие прекрасные арты.
Готов ли ты к испытанию?''', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == 'Да!':# Получаем ID пользователя и заносим в БД

        db = sqlite3.connect('Users.db')

        cursor = db.cursor()
        try:
            cursor.execute(f'''INSERT INTO User_days (id, name, days) VALUES ({str(message.chat.id)}, "{message.chat.first_name}", "0")''')
        except Exception as e:
            print(e)

        db.commit()
        cursor.close()

        bot.send_message(message.chat.id, 'Good!', reply_markup=markup2)

    elif message.text == 'Нет...':
        bot.send_message(message.chat.id, 'Train your brain', reply_markup=types.ReplyKeyboardRemove())

    elif message.text == 'Проставиться':# + 1 день

        db = sqlite3.connect('Users.db')
        cursor = db.cursor()

        try:
            days = cursor.execute(f'''SELECT days FROM User_days WHERE id = {message.chat.id}''').fetchone()
            days = days[0] + 1
            cursor.execute(f'''UPDATE User_days SET days = {days} WHERE id = {message.chat.id}''')
        except Exception as e:
            print(e)

        db.commit()
        cursor.close()

    else:
        bot.send_message(message.chat.id, 'Сформулируй свой ответ/запрос ещё раз.', reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.send_message(572678552, 'Bot was stared!')
    bot.polling(none_stop=True)
