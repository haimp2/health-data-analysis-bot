import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telebot import TeleBot
from data.models import UserFirstChoice, UserState
from data.user import add_user
from utils.api import get_search_filed

logger = logging.getLogger('logger')

def menu_handler(bot: TeleBot):
    @bot.message_handler(commands=['menu'])
    def show_menu(message: Message):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Search Car", callback_data="search_car"))
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

def users_choice_handler(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data == 'search_car')
    def select_first_choice(call: CallbackQuery):
        user_first_choice = UserFirstChoice.SEARCH_CAR.value
        add_user(call.message.chat.id, UserState.START.value, user_first_choice)
        
        try:
            manufacturers = get_search_filed('manufacturer')
        except Exception as e:
            logger.error(e)
            bot.send_message(call.message.chat.id, "Error occurred while fetching manufacturers")
            return
        
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        keyboard_markups = [InlineKeyboardButton(manufacturer['text'], callback_data=f"manufacturer_{manufacturer['value']}") for manufacturer in manufacturers]
        markup.add(*keyboard_markups)

        bot.send_message(call.message.chat.id, "Select the car manufacturer:", reply_markup=markup)