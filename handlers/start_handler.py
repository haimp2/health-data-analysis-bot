from telebot import TeleBot
from telebot.types import Message
import logging

logger = logging.getLogger('logger')

def handle_start(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        logger.info("User started the bot")
        bot.send_message(message.chat.id, "Welcome to the Second-Hand Car Search Bot! Use /menu to see options.")
