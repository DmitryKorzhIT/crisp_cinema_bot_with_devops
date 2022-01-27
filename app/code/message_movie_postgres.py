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





# cursor.execute(f"SELECT COUNT(year) FROM telegram_bot_db;")
# pprint(cursor.fetchall())
#
# auto_links_db = cursor.fetchall()
# for link in auto_links_db:
#     print(link[12])







def random_movie_value():
    """Gives a random movie with all neccessary data.
    Return of this function uses to show a movie card
    message.
    """


    # Read a csv file and create a random number.
    # file = pd.read_csv('../.data/data_v.3.0.csv')
    # file_len = file[file.columns[0]].count() - 1
    # print(file_len)

    cursor.execute(f"SELECT COUNT(year) FROM telegram_bot_db;")
    file_len = cursor.fetchall()[0][0]

    # Implemented filters to show good quality random movies.
    while True:
        random_value = np.random.randint(0, file_len)

        # # Remove from adult bad quality movies.
        # if (file['ratingAgeLimits'][random_value] == 'r' or 'age18') and \
        #    (file['ratingKinopoiskVoteCount'][random_value] >= 2000) and \
        #    (file['ratingKinopoisk'][random_value] >= 5.5) and \
        #    (file['year'][random_value] >= 2000):
        #     break

        # cursor.execute(f"SELECT year FROM telegram_bot_db WHERE myIndex = {random_value};")
        # cursor.execute(f"SELECT kinopoiskId FROM telegram_bot_db;")
        cursor.execute(f"SELECT * FROM telegram_bot_db WHERE my_index='{random_value}';")
        # cursor.execute(f"SELECT my_index FROM telegram_bot_db;")
        item = cursor.fetchall()
        print(item)
        break



        # # Remove from bad quality movies.
        # elif (file['ratingKinopoiskVoteCount'][random_value] >= 1000) and \
        #      (file['ratingKinopoisk'][random_value] >= 5.0) and \
        #      (file['year'][random_value] >= 2000):
        #     break
        #
        # else:
        #     continue
#
#
#     # Get link of the poster.
#     image_link = file['posterUrl'][random_value]
#
#     # Movie type.
#     movie_type_eng = file['type'][random_value]
#     if movie_type_eng == 'TV_SERIES':
#         movie_type = ' (cериал)'
#     elif movie_type_eng == 'MINI_SERIES':
#         movie_type = ' (мини-сериал)'
#     elif movie_type_eng == 'TV_SHOW':
#         movie_type = ' (ток-шоу)'
#     else:
#         movie_type = ''
#
#     # Rating kinopoisk vote count.
#     if file['ratingKinopoiskVoteCount'][random_value] < 1000:
#         rating_kinopoisk_vote_count = '%.1f' %(file['ratingKinopoiskVoteCount'][random_value]/1000)
#     else:
#         rating_kinopoisk_vote_count = '%.0f' % (file['ratingKinopoiskVoteCount'][random_value] / 1000)
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
#
#
#
random_movie_value()

