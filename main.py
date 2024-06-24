from telebot import TeleBot
from config.config import DATABASE_URL, TELEGRAM_API_TOKEN
from data.database import DataBase
from handlers.post_statistics_handler import post_statistics_handler
from handlers.car_selection_handler import car_selection_handler
from handlers.start_handler import handle_start
from handlers.menu_handler import menu_handler, users_choice_handler
from utils.logging import init_logger
# importing UserState model so sqlalchemy can create the table
from data.models import UserState


def init_telebot():
    logger.info("Bot started")
    bot = TeleBot(TELEGRAM_API_TOKEN)
    handle_start(bot)
    menu_handler(bot)
    users_choice_handler(bot)
    car_selection_handler(bot)
    post_statistics_handler(bot)
    bot.polling()

def init_database():
    DataBase.initialize(DATABASE_URL)
    DataBase.create_all_tables()

if __name__ == "__main__":
    logger = init_logger()
    init_database()
    init_telebot()
