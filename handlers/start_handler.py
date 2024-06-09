from telebot import TeleBot

def handle_start(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Welcome to the Public Health Data Analysis Bot! Use /disease, /vaccination, or /healthcare to get started.")
