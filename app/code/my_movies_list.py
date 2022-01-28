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


def




