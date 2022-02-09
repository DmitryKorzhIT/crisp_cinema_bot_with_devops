# This python code use a PostgreSQL database with movies.
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hcode, hunderline
from aiogram.dispatcher.filters import Text
from pprint import pprint
import pandas as pd
import numpy as np
import psycopg2
import random

from code.config import APP_BOT_TOKEN
from code.config import DB_DBNAME, DB_USER, DB_PASSWORD, DB_HOST


# Telegram bot settings.
bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# PostgreSQL database settings.
conn = psycopg2.connect(f'dbname={DB_DBNAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}')
cursor = conn.cursor()


# 📍Show a random movie.
def random_movie_value():
    """Gives a random movie with all neccessary data.
    This function return a movie card message.
    """

    # Set a length of file value.
    cursor.execute(f"SELECT COUNT(year) FROM telegram_bot_good_quality_movies_db;")
    file_len = cursor.fetchall()[0][0]

    # Generate a random number.
    random_value = random.randint(1, file_len+1)

    # Pull a movie with an index = the random number which we generated earlier.
    cursor.execute(f"SELECT * FROM telegram_bot_good_quality_movies_db WHERE my_index={random_value};")

    # Save a movie data in a list.
    movie_list = list(cursor.fetchall())

    # Save a movie data in a dictionary.
    movie_dict = {'my_index': movie_list[0][0],
                  'name_ru': movie_list[0][1],
                  'rating_kinopoisk': movie_list[0][2],
                  'rating_kinopoisk_vote_count': movie_list[0][3],
                  'film_length': movie_list[0][4],
                  'rating_age_limits': movie_list[0][5],
                  'kinopoisk_id': movie_list[0][6],
                  'type': movie_list[0][7],
                  'year': movie_list[0][8],
                  'poster_url': movie_list[0][9],
                  'countries': movie_list[0][10],
                  'genres': movie_list[0][11],
                  'description': movie_list[0][12]}

    # Get link of the poster.
    image_link = movie_dict['poster_url']

    # Movie type.
    movie_type_eng = movie_dict['type']
    if movie_type_eng == 'TV_SERIES':
        movie_type = ' (cериал)'
    elif movie_type_eng == 'MINI_SERIES':
        movie_type = ' (мини-сериал)'
    elif movie_type_eng == 'TV_SHOW':
        movie_type = ' (ток-шоу)'
    else:
        movie_type = ''

    # Rating kinopoisk vote count.
    if movie_dict['rating_kinopoisk_vote_count'] < 1000:
        rating_kinopoisk_vote_count = '%.1f' %(movie_dict['rating_kinopoisk_vote_count']/1000)
    else:
        rating_kinopoisk_vote_count = '%.0f' % (movie_dict['rating_kinopoisk_vote_count'] / 1000)

    # Movie length.
    film_length = movie_dict['film_length']
    if film_length >= 60:
        film_length_hours = film_length // 60
        film_length_minutes = film_length % 60
        film_length = f"{film_length_hours}ч {film_length_minutes}мин"
    else:
        film_length = f"{film_length} мин"

    # Description.
    description = str()
    description_list = list(movie_dict['description'].split())

    if len(description_list) > 30:
        for word in description_list[0:30]:
            description += word + ' '
        description = f"\n\n\U0001F4D6{hcode(' Описание:')} {description}..."

    elif len(description_list) == 0:
        description = ''

    else:
        description = f"\n\n\U0001F4D6{hcode(' Описание:')} {movie_dict['description']}"


    # Message view using aiogram markdown.
    text_value = f"{hbold(movie_dict['name_ru'])} " \
                 f"{hbold('(')}{hbold(movie_dict['year'])}{hbold(')')}" \
                 f"{hbold(movie_type)}\n\n" \
                 f"\U0001F31F{hcode(' Рейтинг:')}   {hbold(movie_dict['rating_kinopoisk'])}\n" \
                 f"\U0001F440{hcode(' Оценило:')}   {hbold(rating_kinopoisk_vote_count)}{hbold('K')}\n" \
                 f"\U0000231B{hcode(' Время:  ')}   {hbold(film_length)}" \
                 f"{description}"

    # Name with year in one string for search trailers.
    name_year = f"{movie_dict['name_ru']} {movie_dict['year']}"
    name_year = name_year.replace(" ", "+")

    # Return movie poster, movie text and name with year in list format.
    message_list = [image_link, text_value, name_year, movie_dict['kinopoisk_id']]

    return message_list


# 📍Inline buttons for random movie.
def random_movie_buttons(name_year):
    """Two inline buttons: "Trailer" and ">" (next movie).
    These two buttons uses with a movie message.

    The "Trailer" button direct User on youtube.com page
    with a trailer for a particular movie.

    The ">" (next movie) button updates a movie message.
    """

    # Message inline buttons.
    buttons = [types.InlineKeyboardButton('\U0001F4D4', callback_data="to_my_movies_list"),
               types.InlineKeyboardButton('Трейлер', url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
               types.InlineKeyboardButton(text=">", callback_data="next_movie")]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return keyboard
