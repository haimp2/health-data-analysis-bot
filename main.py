from telebot import TeleBot
from config.config import TELEGRAM_API_TOKEN
from handlers.start_handler import handle_start

if __name__ == '__main__':
    bot = TeleBot(TELEGRAM_API_TOKEN)
    handle_start(bot)
    bot.polling()
