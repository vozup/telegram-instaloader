import telebot
from common.config import Config

token = Config().get_telegram_token()
bot = telebot.TeleBot(token)