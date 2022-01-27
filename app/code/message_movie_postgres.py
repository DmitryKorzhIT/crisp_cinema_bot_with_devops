from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hcode, hunderline
from aiogram.dispatcher.filters import Text
from pprint import pprint
import pandas as pd
import numpy as np
import psycopg2

from code.config import APP_BOT_TOKEN


# Telegram bot settings.
bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# PostgreSQL database settings.
conn = psycopg2.connect('dbname=telegram_bot_db user=postgres password=1 host=localhost')
cursor = conn.cursor()


def random_movie_value():
    """Gives a random movie with all neccessary data.
    Return of this function uses to show a movie card
    message.
    """

    # Set a length of file value.
    cursor.execute(f"SELECT COUNT(year) FROM telegram_bot_good_quality_movies_db;")
    file_len = cursor.fetchall()[0][0]

    # Implemented filters to show good quality random movies.
    while True:

        # Generate a random number.
        random_value = np.random.randint(1, file_len+1)

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
        print("Image link:", image_link)

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
        print("Movie type:", movie_type)

        # # Rating kinopoisk vote count.
        # if file['ratingKinopoiskVoteCount'][random_value] < 1000:
        #     rating_kinopoisk_vote_count = '%.1f' %(file['ratingKinopoiskVoteCount'][random_value]/1000)
        # else:
        #     rating_kinopoisk_vote_count = '%.0f' % (file['ratingKinopoiskVoteCount'][random_value] / 1000)
    #
    #     # Movie length.
    #     film_length = file['filmLength'][random_value]
    #     if film_length >= 60:
    #             film_length_hours = film_length // 60
    #             film_length_minutes = film_length % 60
    #             film_length = f"{film_length_hours}ч {film_length_minutes}мин"
    #     else:
    #         film_length = f"{film_length} мин"
    #
    #     # Description.
    #     description = str()
    #     description_list = list(file['description'][random_value].split())
    #
    #     if len(description_list) > 30:
    #         for word in description_list[0:30]:
    #             description += word + ' '
    #         description = f"\n\n\U0001F4D6{hcode(' Описание:')} {description}..."
    #
    #     elif len(description_list) == 0:
    #         description = ''
    #
    #     else:
    #         description = f"\n\n\U0001F4D6{hcode(' Описание:')} {file['description'][random_value]}"
    #
    #
    #     # Message view using aiogram markdown.
    #     text_value = f"{hbold(file['nameRu'][random_value])} " \
    #                  f"{hbold('(')}{hbold(file['year'][random_value])}{hbold(')')}" \
    #                  f"{hbold(movie_type)}\n\n" \
    #                  f"\U0001F31F{hcode(' Рейтинг:')}   {hbold(file['ratingKinopoisk'][random_value])}\n" \
    #                  f"\U0001F440{hcode(' Оценило:')}   {hbold(rating_kinopoisk_vote_count)}{hbold('K')}\n" \
    #                  f"\U0000231B{hcode(' Время:  ')}   {hbold(film_length)}" \
    #                  f"{description}"
    #
    #     # Name with year in one string for search trailers.
    #     name_year = f"{file['nameRu'][random_value]} {file['year'][random_value]}"
    #     name_year = name_year.replace(" ", "+")
    #
    #     # Return movie poster, movie text and name with year in list format.
    #     message_list = [image_link, text_value, name_year]
    #
    #     return message_list
    #
    #
    # def random_movie_buttons(name_year):
    #     """Two inline buttons: "Trailer" and ">" (next movie).
    #     These two buttons uses with a movie message.
    #
    #     The "Trailer" button direct User on youtube.com page
    #     with a trailer for a particular movie.
    #
    #     The ">" (next movie) button updates a movie message.
    #     """
    #
    #     # Message inline buttons.
    #     buttons = [types.InlineKeyboardButton('Трейлер', url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
    #                types.InlineKeyboardButton(text=">", callback_data="next_movie")]
    #     keyboard = types.InlineKeyboardMarkup(row_width=2)
    #     keyboard.add(*buttons)
    #     return keyboard
        break



random_movie_value()

