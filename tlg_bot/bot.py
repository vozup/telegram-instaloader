import os
from pathlib import Path
import filetype

import telebot
from telebot import types
from common.config import Config
from common.common import site_name
from loader.main_loader import Loader
from os.path import sep

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
            shortcode = post.shortcode
            if L.download_post(message.text, message.from_user.username):
                bot.send_message(message.from_user.id, f"{post_type} by {author} downloaded!")
                send_media_file(message.from_user, post_type, shortcode)
            else:
                bot.send_message(message.from_user.id, "Maybe file already exist")
        elif site == 'tiktok':
            bot.send_message(message.from_user.id, f"I still do not know how to download files from {full_site}")
        else:
            bot.send_message(message.from_user.id, f"Unknown site {full_site}")
    elif message.text == "Show available files":
        file_list = os.listdir(Path(L.base_download_path + message.from_user.username))
        if file_list:
            bot.send_message(message.from_user.id, f"You have {len(file_list)} downloaded files")
            bot.send_message(message.from_user.id, '\n'.join(file_list))
        else:
            bot.send_message(message.from_user.id, "You dont have downloaded files")
    else:
        bot.send_message(message.from_user.id, "Unknown command")

    # elif message.text == '👋 Поздороваться':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    #     btn1 = types.KeyboardButton('Как стать автором на Хабре?')
    #     btn2 = types.KeyboardButton('Правила сайта')
    #     btn3 = types.KeyboardButton('Советы по оформлению публикации')
    #     markup.add(btn1, btn2, btn3)
    #     bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)  # ответ бота


def send_media_file(message_from_user, media_type: str, shortcode: str):
    """
    Determination of the type of uploaded post
    :param media_type: GraphVideo GraphImage GraphSidecar
    :param message_from_user:
    :param shortcode: shortcode of post to search for a file name
    :return:
    """
    file_path = L.base_download_path + message_from_user.username + sep + shortcode
    if media_type == "GraphVideo":
        video = open(file_path + '.mp4', 'rb')
        bot.send_video(message_from_user.id, video)
    elif media_type == "GraphImage":
        image = open(file_path + '.jpg', 'rb')
        bot.send_photo(message_from_user.id, image)
    # If link on album
    elif media_type == "GraphSidecar":
        files = os.listdir(Path(L.base_download_path + message_from_user.username))
        album = set()
        # Find downloaded files in user directory
        for file in files:
            if file.startswith(shortcode):
                file_path = L.base_download_path + message_from_user.username + sep + file
                kind = filetype.guess(file_path)
                media = open(file_path, 'rb')

                if kind.mime.startswith('image'):
                    album.add(types.InputMediaPhoto(media))
                elif kind.mime.startswith('video'):
                    album.add(types.InputMediaVideo(media))
                # Only 10 item
                if len(album) == 10:
                    bot.send_media_group(message_from_user.id, album)
                    album.clear()
        # Send rest of files
        if len(album) > 0:
            bot.send_media_group(message_from_user.id, album)
    else:
        bot.send_message(message_from_user.id, "Unknown media type")


def pooling():
    bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
