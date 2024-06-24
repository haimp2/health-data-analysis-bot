from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telebot import TeleBot
import pandas as pd
from data.models import UserState
from data.user import update_user
from utils.api import get_search_filed, search_recent_car_posts
from utils.tranformers import create_car_post, filter_search_response

def car_selection_handler(bot: TeleBot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith('manufacturer_'))
    def select_manufacturer(call: CallbackQuery):
        manufacturer = call.data.split('_')[1]
        update_user(call.message.chat.id, user_state=UserState.MODEL.value, manufacturer=manufacturer)

        models = get_search_filed('model', { 'manufacturer': manufacturer })

        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        keyboard_markups = [InlineKeyboardButton(model['text'], callback_data=f"model_{model['value']}") for model in models]
        markup.add(*keyboard_markups)

        bot.send_message(call.message.chat.id, "Select the car model:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('model_'))
    def select_model(call: CallbackQuery):
        model = call.data.split('_')[1]
        user = update_user(call.message.chat.id, user_state=UserState.YEAR.value, model=model)

        year = get_search_filed('year', { 'manufacturer': user['manufacturer'], 'model': model })
        min_year = year['from']
        max_year = year['to']

        bot.send_message(call.message.chat.id, f"Select the car year between {min_year} and {max_year}: (for example 2010-2018)")

    @bot.message_handler(func=lambda message: message.text and message.text.count('-') == 1 and message.text.replace('-', '').isdigit())
    def select_year(message: Message):
        user = update_user(message.chat.id, year=message.text)

        recent_posts = search_recent_car_posts({ 'manufacturer': user['manufacturer'], 'model': user['model'], 'year': user['year']})
        recent_posts = filter_search_response(recent_posts)

        pd.DataFrame(recent_posts).to_csv(f'user-datasets/{message.chat.id}.csv')
    
        message_to_send = ""

        for post in recent_posts[:5]:
            message_to_send += f"{create_car_post(post)}\n\n"

        bot.send_message(message.chat.id, message_to_send)

        # send markup for the user to choose search statistics
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Posts by city", callback_data="posts_by_city"),
                InlineKeyboardButton("Price trend by year", callback_data="price_trend_by_year"),
                InlineKeyboardButton("Kilometers trend by year", callback_data="kilometers_trend_by_year"),
                InlineKeyboardButton("Price by kilometers", callback_data="price_by_kilometers"),
                InlineKeyboardButton("Price trend by city", callback_data="price_trend_by_city"))
        bot.send_message(message.chat.id, "Would you like to see some statistics:", reply_markup=markup)
