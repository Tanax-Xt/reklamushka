import os

from telebot import TeleBot

token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(token)

api_url = "http://backend:8080"
