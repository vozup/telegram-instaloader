import telebot
from telebot import types
from common.config import Config
from common.common import site_name
from loader.main_loader import Loader

token = Config().get_telegram_token()
bot = telebot.TeleBot(token)
L = Loader()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Show available files")
    btn2 = types.KeyboardButton('Button 1')
    btn3 = types.KeyboardButton('Button 2')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "Hello!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.startswith('http'):
        full_site, site = site_name(message.text)
        if site == 'instagram':
            post = L.get_post(message.text)
            post_type = post.typename
            author = post.owner_username
            if L.download_post(message.text, message.from_user.username):
                bot.send_message(message.from_user.id, f"{post_type} by {author} downloaded!")
            else:
                bot.send_message(message.from_user.id, "Maybe file already exist")
        elif site == 'tiktok':
            bot.send_message(message.from_user.id, f"I still do not know how to download files from {full_site}")
        else:
            bot.send_message(message.from_user.id, f"Unknown site {full_site}")
    else:
        bot.send_message(message.from_user.id, "Unknown command")

    # elif message.text == '👋 Поздороваться':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    #     btn1 = types.KeyboardButton('Как стать автором на Хабре?')
    #     btn2 = types.KeyboardButton('Правила сайта')
    #     btn3 = types.KeyboardButton('Советы по оформлению публикации')
    #     markup.add(btn1, btn2, btn3)
    #     bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)  # ответ бота


def pooling():
    bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
