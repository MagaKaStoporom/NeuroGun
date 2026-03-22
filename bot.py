import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot("8557401774:AAHRL-jED1L8SBAHF1gfDSt29rlFO361lA0") # токен бота
admin_id = 7563327336  # айди админа

# клавиатура
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton('Частые вопросы'), types.KeyboardButton('Написать нам! 📰')) # две кнопки







class DataBase:
    @bot.message_handler(func=lambda m: True)
    def all_messages(message):
        # база данных
        db = sqlite3.connect('data.db', check_same_thread=False)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS quests (id INTEGER PRIMARY KEY, user_id INTEGER, text TEXT)')
        db.commit()


        if message.text == 'Частые вопросы':
                bot.send_message(message.chat.id, 'частые вопросы')
        elif message.text == 'Написать нам! ':
                bot.send_message(message.chat.id, 'Напиши свой вопрос!')
        else:
                # сохраняем вопрос
                cur.execute('INSERT INTO quests (user_id, text) VALUES (?, ?)', (message.from_user.id, message.text))
                db.commit()
                bot.send_message(message.chat.id, 'в базу данных пришел вопрос!')


class Handler:

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        # проверяем, что нажали пользователя
        if message.text == 'Частые вопросы':
            try:
                with open("photo.png", 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption='частые вопросы!')
            except Exception as e:
                bot.reply_to(message, f'ошибка: {e}')  # если ошибка

        elif message.text == 'Написать нам! 📰':
            bot.send_message(message.chat.id, 'напиши свой вопрос или жалобу!')

        elif message.from_user.id == admin_id:  # для админа
            bot.send_message(message.chat.id, 'вы в режиме администратора')

        else:
            # обычный пользователь
            card = f"""
            твой вопрос принят!

            имя: {message.from_user.last_name if message.from_user.last_name else 'нет'}
            твой id: {message.from_user.id}
            твой вопрос: {message.text}
            """
            
            print(f"поступил новый вопрос! {message.text}")
            bot.send_message(message.chat.id, card)  # отправляем карточку


class Main(Handler): # наследование
     @bot.message_handler(commands=['start'])
     def func(message):
          bot.send_message(f"Привет! Мы - техническая поддержка. Воспользуйся кнопками ниже...")



        

if __name__ == "__main__":
    print('бот запущен')
    bot.polling(none_stop=True)  # запускаем бота
