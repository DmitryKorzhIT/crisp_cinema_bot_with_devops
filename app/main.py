from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hcode, hunderline
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pprint import pprint
import psycopg2
import pandas as pd
import numpy as np
import os

from code.random_movies import random_movie_value, random_movie_buttons
from code.start_menu import start_menu_buttons
from code.my_movies_list import my_movies_list_buttons, show_my_movies_list_in_list_view_function
from code.my_movies_cards import to_my_movies_list_second_function, users_last_movie_in_my_movies_list_equal_zero
from code.my_movies_cards import users_last_movie_in_my_movies_list_plus_one
from code.my_movies_cards import users_last_movie_in_my_movies_list_minus_one
from code.my_movies_cards import add_to_db_users_last_removed_movie_from_my_movies_list
from code.my_movies_cards import remove_users_last_removed_movie_from_my_movies_list
from code.my_movies_cards import show_users_last_movie_in_my_movies_list
from code.my_movies_cards import my_movies_list_in_cards_view_buttons
from code.my_movies_cards import my_movies_list_in_cards_view_buttons_after_deleting
from code.my_movies_cards import show_my_movies_list_in_cards_view_function
from code.my_movies_cards import show_my_movies_list_just_deleted
from code.my_movies_cards import set_false_my_movies_list_just_deleted
from code.my_movies_cards import pull_from_db_users_last_removed_movie_from_my_movies_list
from code.my_movies_cards import my_movies_list_in_cards_view_buttons_after_deleting_and_recovering
from code.my_movies_cards import show_my_movies_list_just_recovered
from code.my_movies_cards import set_true_my_movies_list_just_recovered
from code.my_movies_cards import set_false_my_movies_list_just_recovered
from code.my_movies_cards import count_users_movies_in_my_movies_list
from code.config import DB_DBNAME, DB_USER, DB_PASSWORD, DB_HOST


# Telegram bot settings.
APP_BOT_TOKEN = os.getenv("APP_BOT_TOKEN")

bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# PostgreSQL database settings.
conn = psycopg2.connect(f'dbname={DB_DBNAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}')
cursor = conn.cursor()


#
#
# Handler for pressing a "type of movies" button.
# @dp.message_handler(commands='start')
# async def type_of_movies_button(message: types.Message):
#     buttons = ['???????????? / ??????????????', '???????????????????? ??/??']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     type_of_movies_value = ('(1/4) ????????????????????, ???????????????? ???? ???????????? ????????' + u'\U0001F447')
#     await message.answer(type_of_movies_value, reply_markup=keyboard)
#
#
# # Handler for type of movies.
# @dp.message_handler(Text(equals="???????????? / ??????????????"))
# async def type_of_movies(message: types.Message):
#     type_of_movies_value = ("???????????? (/4j51b)\n"
#                             "?????????????????????? (/8ba8o)\n"
#                             "?????????????? (/3l51v)\n"
#                             "?????????? (/jas82)\n")
#     await message.answer(type_of_movies_value)
#
#
# # Handler for pressing a "genre" button.
# @dp.message_handler(Text(equals="???????????????????? ??/??"))
# @dp.message_handler(commands='4j51b')
# @dp.message_handler(commands='8ba8o')
# @dp.message_handler(commands='3l51v')
# @dp.message_handler(commands='jas82')
# async def genre_button(message: types.Message):
#     buttons = ['??????????', '???????????????????? ??????????']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     genre_value = ('(2/4) ???????????????? ??????????' + u'\U0001F447')
#     await message.answer(genre_value, reply_markup=keyboard)
#
#
# # Handler for choosing a genre.
# @dp.message_handler(Text(equals="??????????"))
# async def genre(message: types.Message):
#     genre_value = ("???????????????????? (/4j851b)\n"
#                    "???????????? (/3l851v)\n")
#     await message.answer(genre_value)
#
#
# # Handler for pressing a "year" button.
# @dp.message_handler(Text(equals="???????????????????? ??????????"))
# @dp.message_handler(commands='4j851b')
# @dp.message_handler(commands='3l851v')
# async def year_button(message: types.Message):
#     buttons = ['????????', '???????????????????? ????????']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#     year_value = ('(3/4) ???????????????? ????????:' + u'\U0001F447')
#     await message.answer(year_value, reply_markup=keyboard)
#
#
# # Handler for choosing a year.
# @dp.message_handler(Text(equals="????????"))
# async def year(message: types.Message):
#     year_value = ("???? 2000 (/XCNpkmy5)\n"
#                   "2000 - 2010 (/HFUyun2u)\n"
#                   "2011 - 2020 (/vCJ0Dn9z)\n"
#                   "2021 - 2022 (/tkpn4YUf)\n")
#     await message.answer(year_value)
#
#
# # Handler for pressing a "kinopoisks raiting" button.
# @dp.message_handler(Text(equals="???????????????????? ????????"))
# @dp.message_handler(commands='XCNpkmy5')
# @dp.message_handler(commands='HFUyun2u')
# @dp.message_handler(commands='vCJ0Dn9z')
# @dp.message_handler(commands='tkpn4YUf')
# async def kinopoisk_raiting_button(message: types.Message):
#     buttons = ['?????????????? ????????????????????', '???????????????????? ??????????????']
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add(*buttons)
#     kinopoisk_raiting = ('(4/4) ???????????????? ??????????????:' + u'\U0001F447')
#     await message.answer(kinopoisk_raiting, reply_markup=keyboard)
#
#
# # Handler for choosing a kinopoisk raiting.
# @dp.message_handler(Text(equals="?????????????? ????????????????????"))
# async def kinopoisk_raiting(message: types.Message):
#     raiting_value = ("???? 6.0 (/Fi3ocz8K)\n"
#                     "6.0 - 6.9 (/X2sqFxj9)\n"
#                     "7.0 - 7.5 (/AhdFB2e4)\n"
#                     "7.6 - 7.9 (/Fi5az1kq)\n"
#                     "8.0 ?? ?????????? (/C31BjQyY)")
#     await message.answer(raiting_value)
#
#
# # Handler for showing a movie with inline buttons.
# @dp.message_handler(Text(equals="???????????????????? ??????????????"))
# @dp.message_handler(commands='Fi3ocz8K')
# @dp.message_handler(commands='X2sqFxj9')
# @dp.message_handler(commands='AhdFB2e4')
# @dp.message_handler(commands='Fi5az1kq')
# @dp.message_handler(commands='C31BjQyY')
#
#

# ????Introductory information after '/start' command.
@dp.message_handler(commands='start')
async def start_menu(message: types.Message):
    """Introductory information after '/start' command."""

    # Message view using aiogram markdown.
    text_value = f"{hbold('???? ???????????? ???????????????????????? ??????????????:')}\n" \
                 f"/menu ??? ???????? ?? ?????????????????? ???????? ????\n" \
                 f"/random_movies ??? ?????????????????? ???????????? ????\n" \
                 f"/my_movies - ?????? ???????????? ????\n\n" \
                 f"{hbold('?????? ?????????????????????????????? ?????????????????????? ????????:')}"


    await bot.send_message(message.from_user.id,
                           text=text_value,
                           reply_markup=start_menu_buttons())


# ????Menu after '/menu' command.
@dp.message_handler(commands='menu')
async def start_menu(message: types.Message):
    """Show a menu after "/menu" command."""

    await bot.send_message(message.from_user.id,
                           text=f"{hbold('???????????????? ????????:')}",
                           reply_markup=start_menu_buttons())



#============================================================================================#
#==================================????    Random movie    ????==================================#
#============================================================================================#

# ????Show a random movie message.
@dp.message_handler(commands='random_movies')
@dp.callback_query_handler(text="show_random_movies")
async def random_movie(message: types.Message, state: FSMContext):
    """The function shows the first message with a random movie.

    1. The function pulls data about a movie.
    2. Each time the function update information in the database
    about a last user's movie.
    3. It shows a random movie card with inline buttons.
    """

    # Pull data from function random_movie_value with
    # information about a movie.
    message_list = random_movie_value()
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]
    kinopoisk_id = message_list[3]

    async with state.proxy() as data:
        data['current_movie_id']=kinopoisk_id

    await bot.send_photo(chat_id=message.from_user.id,
                         parse_mode=types.ParseMode.HTML,
                         photo=image_link,
                         caption=text_value,
                         reply_markup=random_movie_buttons(name_year))
    await bot.delete_message(message.from_user.id, message.message.message_id)


# ????The "next movie" inline button.
@dp.callback_query_handler(text="next_movie")
async def update_random_movie(callback_query: types.CallbackQuery, state: FSMContext):
    """The function updates a random movie card after pressing
    an inline button "next movie".

    1. The function pulls data about a movie.
    2. Each time the function update information in the database
    about a last user's movie.
    3. It shows a random movie card with inline buttons.
    """

    # Pull data from function random_movie_value with
    # information about a movie.
    message_list = random_movie_value()
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]
    kinopoisk_id = message_list[3]

    async with state.proxy() as data:
        data['current_movie_id']=kinopoisk_id

    await bot.edit_message_media(media=types.InputMediaPhoto(image_link, caption=text_value),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 reply_markup=random_movie_buttons(name_year))



#============================================================================================#
#=================================????    My movies list    ????=================================#
#============================================================================================#

# ????Add movies to my_movies_list.
@dp.callback_query_handler(text='to_my_movies_list')
async def to_my_movies_list_function(callback_query: types.CallbackQuery, state: FSMContext):
    """This handler call a function to_my_movies_list_second_function.

    The function "to_my_movies_list_second_function" - adds
    a random movie to my_movies_list in the database.
    """

    # Get a user_id and call the function.
    user_id = callback_query.message.chat.id
    async with state.proxy() as data:
        kinopoisk_id = data['current_movie_id']

    text_value = to_my_movies_list_second_function(user_id, kinopoisk_id)

    await callback_query.answer(text=text_value,
                                cache_time=0)


# ????Show the first movie from my_movies_list in a cards view.
@dp.message_handler(commands='my_movies')
@dp.callback_query_handler(text="show_my_movies_list_in_cards_view")
async def my_movies_list_in_cards_view(message: types.Message):
    """Show the first movie from the my_movie_list
    in a card view with inline buttons.
    """

    # Pull data about user's id.
    user_id = message.from_user.id,
    user_id = user_id[0]

    # Count a number of user's movies in my_movies_list.
    count_users_movies = count_users_movies_in_my_movies_list(user_id)

    # If the my_movies_list contains at least one movie.
    if count_users_movies > 0:

        # Set to "0" a number of movies that a user has watched from my_movies_list.
        users_last_movie_in_my_movies_list_equal_zero(user_id)

        # Pull a kinopoisk_id of a movie where a user has stopped.
        kinopoisk_id = show_users_last_movie_in_my_movies_list(user_id)

        # Pull information about a movie from the my_movies_list.
        message_list = show_my_movies_list_in_cards_view_function(kinopoisk_id)
        image_link = message_list[0]
        text_value = message_list[1]
        name_year = message_list[2]

        await bot.send_photo(chat_id=message.from_user.id,
                             parse_mode=types.ParseMode.HTML,
                             photo=image_link,
                             caption=text_value,
                             reply_markup=my_movies_list_in_cards_view_buttons(name_year))
        await bot.delete_message(message.from_user.id, message.message.message_id)

    # If the my_movies_list contains zero movies.
    else:
        await bot.send_message(message.from_user.id,
                               text='???? ?????? ???? ???????????????? ???? ???????????? ????????????.',
                               reply_markup=start_menu_buttons())
        await bot.delete_message(message.from_user.id, message.message.message_id)


# ????Update a message with the next movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_next_movie")
async def my_movies_list_in_cards_view_next_movie(callback_query: types.CallbackQuery):
    """Update a message with the next movie from the my_movie_list
    in a card view with inline buttons.
    """

    # Pull data about user's id.
    user_id = callback_query.message.chat.id

    # Check is the movie has been just deleted.
    just_deleted = show_my_movies_list_just_deleted(user_id)

    # A movie hasn't been just deleted.
    if just_deleted == False:
        # Update to "+1" a number of movies that a user has watched from my_movies_list.
        users_last_movie_in_my_movies_list_plus_one(user_id)

    # A movie has been just deleted.
    else:
        # Set False value of just_deleted movie in the DB table.
        set_false_my_movies_list_just_deleted(user_id)

    # Set False that the movie is just recovered.
    set_false_my_movies_list_just_recovered(user_id)

    # Pull a kinopoisk_id of a movie where a user has stopped.
    kinopoisk_id = show_users_last_movie_in_my_movies_list(user_id)

    # Pull information about a movie from the my_movies_list.
    message_list = show_my_movies_list_in_cards_view_function(kinopoisk_id)
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]

    await bot.edit_message_media(media=types.InputMediaPhoto(image_link, caption=text_value),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 reply_markup=my_movies_list_in_cards_view_buttons(name_year))


# ????Update a message with the previous movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_previous_movie")
async def my_movies_list_in_cards_view_previous_movie(callback_query: types.CallbackQuery):
    """Update a message with the next movie from the my_movie_list
    in a card view with inline buttons.
    """

    # Pull data about user's id.
    user_id = callback_query.message.chat.id

    # Check is the movie has been just deleted.
    just_deleted = show_my_movies_list_just_deleted(user_id)

    # A movie hasn't been just deleted.
    if just_deleted == True:
        # Set False value of just_deleted movie in the DB table.
        set_false_my_movies_list_just_deleted(user_id)

    # Check is a movie has been just recovered.
    just_recovered = show_my_movies_list_just_recovered(user_id)

    if just_recovered == True:
        # Update to "+1" a number of movies that a user has watched from my_movies_list.
        users_last_movie_in_my_movies_list_plus_one(user_id)

        # Set False that the movie is just recovered.
        set_false_my_movies_list_just_recovered(user_id)

    # Update to "-1" a number of movies that a user has watched from my_movies_list.
    users_last_movie_in_my_movies_list_minus_one(user_id)

    # Pull a kinopoisk_id of a movie where a user has stopped.
    kinopoisk_id = show_users_last_movie_in_my_movies_list(user_id)

    # Pull information about a movie from the my_movies_list.
    message_list = show_my_movies_list_in_cards_view_function(kinopoisk_id)
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]

    await bot.edit_message_media(media=types.InputMediaPhoto(image_link, caption=text_value),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 reply_markup=my_movies_list_in_cards_view_buttons(name_year))


# ????Remove a movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_remove_movie")
async def my_movies_list_in_cards_view_remove_movie(callback_query: types.CallbackQuery):
    """Remove a movie from my_movies_list in a cards view."""

    # Pull data about user's id.
    user_id = callback_query.message.chat.id

    # Pull a kinopoisk_id of a movie where a user has stopped.
    kinopoisk_id = show_users_last_movie_in_my_movies_list(user_id)

    # Pull information about a movie from the my_movies_list.
    message_list = show_my_movies_list_in_cards_view_function(kinopoisk_id)
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]

    # Add data to a table with the last movie that a user deleted from my_movies_list.
    add_to_db_users_last_removed_movie_from_my_movies_list(user_id, kinopoisk_id)

    # Delete a movie from the my_movies_list DB table.
    remove_users_last_removed_movie_from_my_movies_list(user_id, kinopoisk_id)

    await bot.edit_message_media(media=types.InputMediaPhoto(image_link, caption=text_value),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 reply_markup=my_movies_list_in_cards_view_buttons_after_deleting(name_year))


# ????Recover after removing a movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_recover_movie")
async def my_movies_list_in_cards_view_recover_movie(callback_query: types.CallbackQuery):
    """Recover after removing a movie from my_movies_list in a cards view."""

    # Pull data about user's id.
    user_id = callback_query.message.chat.id

    # Pull a kinopoisk_id of a movie where a user has stopped.
    kinopoisk_id = pull_from_db_users_last_removed_movie_from_my_movies_list(user_id)

    # Pull information about a movie from the my_movies_list.
    message_list = show_my_movies_list_in_cards_view_function(kinopoisk_id)
    image_link = message_list[0]
    text_value = message_list[1]
    name_year = message_list[2]

    # Insert a movie from the my_movies_list DB table.
    alert = to_my_movies_list_second_function(user_id, kinopoisk_id)

    # Set False value of just_deleted movie in the DB table.
    set_false_my_movies_list_just_deleted(user_id)

    # Set True that the movie is just recovered.
    set_true_my_movies_list_just_recovered(user_id)

    await bot.edit_message_media(media=types.InputMediaPhoto(image_link, caption=text_value),
                                 chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id,
                                 reply_markup=my_movies_list_in_cards_view_buttons_after_deleting_and_recovering())

    await callback_query.answer(text=alert,
                                cache_time=0)



if __name__ == '__main__':
    print('\nIt is working!\n')
    executor.start_polling(dp, skip_updates=True)
