from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hcode, hunderline
from aiogram.dispatcher.filters import Text
from pprint import pprint
import pandas as pd
import numpy as np
import psycopg2

from code.config import APP_BOT_TOKEN
from code.config import DB_DBNAME, DB_USER, DB_PASSWORD, DB_HOST


# Telegram bot settings.
bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# PostgreSQL database settings.
conn = psycopg2.connect(f'dbname={DB_DBNAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}')
cursor = conn.cursor()


def my_movies_list_buttons():
    """Two inline buttons: "Trailer" and ">" (next movie).
    These two buttons uses with a movie message.

    The "Trailer" button direct User on youtube.com page
   with a trailer for a particular movie.

    The ">" (next movie) button updates a movie message.
    """

    # Message inline buttons.
    buttons = [types.InlineKeyboardButton(text="<", callback_data="my_movies_list_buttons_previous_page"),
               types.InlineKeyboardButton(text="2", callback_data="my_movies_list_buttons_current_page"),
               types.InlineKeyboardButton(text=">", callback_data="my_movies_list_buttons_next_page")]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard


# def add_to_my_movies_list():
#




