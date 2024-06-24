from telebot.types import CallbackQuery
from telebot import TeleBot
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from bidi.algorithm import get_display

matplotlib.use('Agg')

def set_hebrew_labels(ax, title, xlabel, ylabel):
    ax.set_title(get_display(title), fontsize=14)
    ax.set_xlabel(get_display(xlabel), fontsize=12)
    ax.set_ylabel(get_display(ylabel), fontsize=12)
    plt.xticks(rotation=45)

def save_and_send_plot(bot: TeleBot, chat_id):
    plt.tight_layout()
    plt.savefig(f'user-figs/{chat_id}.png')
    bot.send_photo(chat_id, open(f'user-figs/{chat_id}.png', 'rb'))

def load_dataset(chat_id):
    return pd.read_csv(f'user-datasets/{chat_id}.csv')

def transform_dataset(df):
    df['city'] = df['city'].apply(get_display)
    df['year'] = df['year'].astype(int)
    df['price'] = df['price'].str.replace(' ₪', '').str.replace(',', '').astype(float)
    df['kilometers'] = df['kilometers'].str.replace(',', '').astype(float)
    return df

def load_and_transform_dataset(chat_id):
    df = load_dataset(chat_id)
    return transform_dataset(df)


def post_statistics_handler(bot: TeleBot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith('posts_by_city'))
    def plot_posts_by_city(call: CallbackQuery):
        df = load_and_transform_dataset(call.message.chat.id)
        ads_by_city = df['city'].value_counts()
        fig, ax = plt.subplots()
        ads_by_city.plot(kind='bar', ax=ax)
        set_hebrew_labels(ax, 'מספר המודעות לפי עיר', 'עיר', 'מספר מודעות')
        save_and_send_plot(bot, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('price_trend_by_year'))
    def plot_price_trend_by_year(call: CallbackQuery):
        df = load_and_transform_dataset(call.message.chat.id)
        price_trends = df.groupby('year')['price'].mean()
        fig, ax = plt.subplots()
        price_trends.plot(kind='line', ax=ax)
        set_hebrew_labels(ax, 'מגמות מחירים לפי שנה', 'שנה', 'מחיר ממוצע (₪)')
        save_and_send_plot(bot, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('kilometers_trend_by_year'))
    def plot_kilometers_trend_by_year(call: CallbackQuery):
        df = load_and_transform_dataset(call.message.chat.id)
        kilometers_trend = df.groupby('year')['kilometers'].mean()
        fig, ax = plt.subplots()
        kilometers_trend.plot(kind='line', ax=ax)
        set_hebrew_labels(ax, 'מגמות קילומטרים לפי שנה', 'שנה', 'קילומטרים ממוצעים')
        save_and_send_plot(bot, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('price_by_kilometers'))
    def plot_price_by_kilometers(call: CallbackQuery):
        df = load_and_transform_dataset(call.message.chat.id)
        fig, ax = plt.subplots()
        ax.scatter(df['kilometers'], df['price'])
        set_hebrew_labels(ax, 'מחיר לפי קילומטרים', 'קילומטרים', 'מחיר (₪)')
        save_and_send_plot(bot, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('price_trend_by_city'))
    def plot_price_trend_by_city(call: CallbackQuery):
        df = load_and_transform_dataset(call.message.chat.id)
        average_price_by_city = df.groupby('city')['price'].mean()
        fig, ax = plt.subplots()
        average_price_by_city.plot(kind='line', ax=ax)
        set_hebrew_labels(ax, 'מגמות מחירים לפי עיר', 'עיר', 'מחיר ממוצע (₪)')
        save_and_send_plot(bot, call.message.chat.id)

    
        