from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text
from pprint import pprint
import psycopg2
import pandas as pd
import numpy as np
import os

from code.random_movies import random_movie_value, current_movie_to_db, random_movie_buttons
from code.start_menu import start_menu_buttons
from code.my_movies_list import my_movies_list_buttons


APP_BOT_TOKEN = os.getenv("APP_BOT_TOKEN")

bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


#
#
# Handler for pressing a "type of movies" button.
# @dp.message_handler(commands='start')
# async def type_of_movies_button(message: types.Message):
#     buttons = ['Фильмы / Сериалы', 'Пропустить Ф/С']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     type_of_movies_value = ('(1/4) Пожалуйста, выберите из списка ниже' + u'\U0001F447')
#     await message.answer(type_of_movies_value, reply_markup=keyboard)
#
#
# # Handler for type of movies.
# @dp.message_handler(Text(equals="Фильмы / Сериалы"))
# async def type_of_movies(message: types.Message):
#     type_of_movies_value = ("Фильмы (/4j51b)\n"
#                             "Мультфильмы (/8ba8o)\n"
#                             "Сериалы (/3l51v)\n"
#                             "Аниме (/jas82)\n")
#     await message.answer(type_of_movies_value)
#
#
# # Handler for pressing a "genre" button.
# @dp.message_handler(Text(equals="Пропустить Ф/С"))
# @dp.message_handler(commands='4j51b')
# @dp.message_handler(commands='8ba8o')
# @dp.message_handler(commands='3l51v')
# @dp.message_handler(commands='jas82')
# async def genre_button(message: types.Message):
#     buttons = ['Жанры', 'Пропустить жанры']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     genre_value = ('(2/4) Выберите жанры' + u'\U0001F447')
#     await message.answer(genre_value, reply_markup=keyboard)
#
#
# # Handler for choosing a genre.
# @dp.message_handler(Text(equals="Жанры"))
# async def genre(message: types.Message):
#     genre_value = ("Фантастика (/4j851b)\n"
#                    "Мюзикл (/3l851v)\n")
#     await message.answer(genre_value)
#
#
# # Handler for pressing a "year" button.
# @dp.message_handler(Text(equals="Пропустить жанры"))
# @dp.message_handler(commands='4j851b')
# @dp.message_handler(commands='3l851v')
# async def year_button(message: types.Message):
#     buttons = ['Года', 'Пропустить года']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     year_value = ('(3/4) Выберите года:' + u'\U0001F447')
#     await message.answer(year_value, reply_markup=keyboard)
#
#
# # Handler for choosing a year.
# @dp.message_handler(Text(equals="Года"))
# async def year(message: types.Message):
#     year_value = ("До 2000 (/XCNpkmy5)\n"
#                   "2000 - 2010 (/HFUyun2u)\n"
#                   "2011 - 2020 (/vCJ0Dn9z)\n"
#                   "2021 - 2022 (/tkpn4YUf)\n")
#     await message.answer(year_value)
#
#
# # Handler for pressing a "kinopoisks raiting" button.
# @dp.message_handler(Text(equals="Пропустить года"))
# @dp.message_handler(commands='XCNpkmy5')
# @dp.message_handler(commands='HFUyun2u')
# @dp.message_handler(commands='vCJ0Dn9z')
# @dp.message_handler(commands='tkpn4YUf')
# async def kinopoisk_raiting_button(message: types.Message):
#     buttons = ['Рейтинг Кинопоиска', 'Пропустить рейтинг']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add(*buttons)
#     kinopoisk_raiting = ('(4/4) Выберите рейтинг:' + u'\U0001F447')
#     await message.answer(kinopoisk_raiting, reply_markup=keyboard)
#
#
# # Handler for choosing a kinopoisk raiting.
# @dp.message_handler(Text(equals="Рейтинг Кинопоиска"))
# async def kinopoisk_raiting(message: types.Message):
#     raiting_value = ("До 6.0 (/Fi3ocz8K)\n"
#                     "6.0 - 6.9 (/X2sqFxj9)\n"
#                     "7.0 - 7.5 (/AhdFB2e4)\n"
#                     "7.6 - 7.9 (/Fi5az1kq)\n"
#                     "8.0 и более (/C31BjQyY)")
#     await message.answer(raiting_value)
#
#
# # Handler for showing a movie with inline buttons.
# @dp.message_handler(Text(equals="Пропустить рейтинг"))
# @dp.message_handler(commands='Fi3ocz8K')
# @dp.message_handler(commands='X2sqFxj9')
# @dp.message_handler(commands='AhdFB2e4')
# @dp.message_handler(commands='Fi5az1kq')
# @dp.message_handler(commands='C31BjQyY')
#
#


# Menu after '/start' command.
@dp.message_handler(commands='start')
async def start_menu(message: types.Message):
    """Show a menu after "/start" command."""

    await bot.send_message(message.from_user.id,
                           text='Выберите ниже:',
                           reply_markup=start_menu_buttons())


# Show a random movie message.
@dp.callback_query_handler(text="show_random_movies")
async def random_movie(message: types.Message):
    """Show a random movie card with inline buttons."""

    message_list = random_movie_value()
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]
    kinopoisk_id = message_list[3]

    # Function to write inforamtion into the database about the last users movie.
    current_movie_to_db(user_id=message.from_user.id,
                        kinopoisk_id=kinopoisk_id)

    await bot.send_photo(chat_id=message.from_user.id,
                         parse_mode=types.ParseMode.HTML,
                         photo=image_link,
                         caption=text_value,
                         reply_markup=random_movie_buttons(name_year))
    await bot.delete_message(message.from_user.id, message.message.message_id)


@dp.callback_query_handler(text="next_movie")
async def update_random_movie(callback_query: types.CallbackQuery):
    """Update a random movie card with inline buttons.
    This function activates after pressing an inline
    button "next movie".
    """

    message_list = random_movie_value()
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]
    kinopoisk_id = message_list[3]

    # Function to write inforamtion into the database about the last users movie.
    current_movie_to_db(user_id=callback_query.message.chat.id,
                        kinopoisk_id=kinopoisk_id)

    await bot.edit_message_media(media=types.InputMediaPhoto(image_link, caption=text_value),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 reply_markup=random_movie_buttons(name_year))


# Show my movies list.
@dp.callback_query_handler(text="show_my_movies_list")
async def my_movies_list(callback_query: types.CallbackQuery):
    """Show my movie list with inline buttons."""

    await callback_query.answer()
    await callback_query.message.answer('My movies list!\n\nYou have no movies yet.',
                                        reply_markup = my_movies_list_buttons())


@dp.callback_query_handler(text='to_my_movies_list')
async def to_my_movies_list_function(kinoposk_id, callback_query: types.CallbackQuery):
    """This function shows random movies and adds
    a movie to my movies list in the database."""
    a = update_random_movie.text_value
    user_id = callback_query.message.chat.id
    await callback_query.answer(cache_time=0)
    await callback_query.message.answer(f'Answer on my movies list. Your_id is "{a}".')





if __name__ == '__main__':
    print('\nIt is working!\n')
    executor.start_polling(dp, skip_updates=True)
