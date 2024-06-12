from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telebot import TeleBot

def menu_handler(bot: TeleBot):
    @bot.message_handler(commands=['menu'])
    def show_menu(message: Message):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Search Car", callback_data="search_car"),
                InlineKeyboardButton("Price Trends", callback_data="price_trends"),
                InlineKeyboardButton("Car Details", callback_data="car_details"))
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)