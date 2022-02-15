import os
from code.config import DB_DBNAME, DB_HOST, DB_PASSWORD, DB_USER
from code.my_movies_cards import (
    add_to_db_users_last_removed_movie_from_my_movies_list,
    add_user_to_db_users_last_removed_movie_from_my_movies_list,
    count_users_movies_in_my_movies_list,
    my_movies_list_in_cards_view_buttons,
    my_movies_list_in_cards_view_buttons_after_deleting,
    my_movies_list_in_cards_view_buttons_after_deleting_and_recovering,
    pull_from_db_users_last_removed_movie_from_my_movies_list,
    remove_users_last_removed_movie_from_my_movies_list,
    set_false_my_movies_list_just_deleted,
    set_false_my_movies_list_just_recovered,
    set_true_my_movies_list_just_recovered,
    show_my_movies_list_in_cards_view_function,
    show_my_movies_list_just_deleted,
    show_my_movies_list_just_recovered,
    show_users_last_movie_in_my_movies_list,
    to_my_movies_list_second_function,
    users_last_movie_in_my_movies_list_equal_zero,
    users_last_movie_in_my_movies_list_minus_one,
    users_last_movie_in_my_movies_list_plus_one,
)
from code.my_movies_list import (
    my_movies_list_buttons,
    show_my_movies_list_in_list_view_function,
)
from code.random_movies import random_movie_buttons, random_movie_value
from code.start_menu import start_menu_buttons
from pprint import pprint

import numpy as np
import pandas as pd
import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hcode, hunderline


# Telegram bot settings.
APP_BOT_TOKEN = os.getenv("APP_BOT_TOKEN")

bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# PostgreSQL database settings.
conn = psycopg2.connect(
    f"dbname={DB_DBNAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}"
)
cursor = conn.cursor()


# 📍Introductory information after '/start' command.
@dp.message_handler(commands="start")
async def start_menu(message: types.Message):
    """Introductory information after '/start' command."""

    # Message view using aiogram markdown.
    text_value = (
        f"{hbold('Вы можете использовать команды:')}\n"
        f"/menu — меню с функциями бота 🤖\n"
        f"/random_movies — случайные фильмы 🎲\n"
        f"/my_movies - мои фильмы 📔\n\n"
        f"{hbold('Или воспользоваться клавиатурой ниже:')}"
    )

    await bot.send_message(
        message.from_user.id, text=text_value, reply_markup=start_menu_buttons()
    )


# 📍Menu after '/menu' command.
@dp.message_handler(commands="menu")
async def start_menu(message: types.Message):
    """Show a menu after "/menu" command."""

    await bot.send_message(
        message.from_user.id,
        text=f"{hbold('Выберите ниже:')}",
        reply_markup=start_menu_buttons(),
    )


# ============================================================================================#
# ==================================👉    Random movie    👈==================================#
# ============================================================================================#

# 📍Show a random movie message.
@dp.message_handler(commands="random_movies")
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
        data["current_movie_id"] = kinopoisk_id

    await bot.send_photo(
        chat_id=message.from_user.id,
        parse_mode=types.ParseMode.HTML,
        photo=image_link,
        caption=text_value,
        reply_markup=random_movie_buttons(name_year),
    )

    # Try to delete a previous message
    try:
        await bot.delete_message(message.from_user.id, message.message.message_id)
    except AttributeError:
        pass


# 📍The "next movie" inline button.
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
        data["current_movie_id"] = kinopoisk_id

    await bot.edit_message_media(
        media=types.InputMediaPhoto(image_link, caption=text_value),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=random_movie_buttons(name_year),
    )


# ============================================================================================#
# =================================👉    My movies list    👈=================================#
# ============================================================================================#

# 📍Add movies to my_movies_list.
@dp.callback_query_handler(text="to_my_movies_list")
async def to_my_movies_list_function(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """This handler call a function to_my_movies_list_second_function.

    The function "to_my_movies_list_second_function" - adds
    a random movie to my_movies_list in the database.
    """

    # Get a user_id and call the function.
    user_id = callback_query.message.chat.id
    async with state.proxy() as data:
        kinopoisk_id = data["current_movie_id"]

    text_value = to_my_movies_list_second_function(user_id, kinopoisk_id)

    await callback_query.answer(text=text_value, cache_time=0)


# 📍Show the first movie from my_movies_list in a cards view.
@dp.message_handler(commands="my_movies")
@dp.callback_query_handler(text="show_my_movies_list_in_cards_view")
async def my_movies_list_in_cards_view(message: types.Message):
    """Show the first movie from the my_movie_list
    in a card view with inline buttons.
    """

    # Pull data about user's id.
    user_id = (message.from_user.id,)
    user_id = user_id[0]

    # Count a number of user's movies in my_movies_list.
    count_users_movies = count_users_movies_in_my_movies_list(user_id)

    # If the my_movies_list contains at least one movie.
    if count_users_movies > 0:

        # Set to "0" a number of movies that a user has watched from my_movies_list.
        users_last_movie_in_my_movies_list_equal_zero(user_id)

        # Pull a kinopoisk_id of a movie where a user has stopped.
        kinopoisk_id = show_users_last_movie_in_my_movies_list(user_id)

        # Add a user to the table.
        add_user_to_db_users_last_removed_movie_from_my_movies_list(
            user_id, kinopoisk_id
        )

        # Pull information about a movie from the my_movies_list.
        message_list = show_my_movies_list_in_cards_view_function(kinopoisk_id)
        image_link = message_list[0]
        text_value = message_list[1]
        name_year = message_list[2]

        await bot.send_photo(
            chat_id=message.from_user.id,
            parse_mode=types.ParseMode.HTML,
            photo=image_link,
            caption=text_value,
            reply_markup=my_movies_list_in_cards_view_buttons(name_year),
        )

        # Try to delete a previous message
        try:
            await bot.delete_message(message.from_user.id, message.message.message_id)
        except AttributeError:
            pass

    # If the my_movies_list contains zero movies.
    else:
        await bot.send_message(
            message.from_user.id,
            text="Вы еще не добавили ни одного фильма.",
            reply_markup=start_menu_buttons(),
        )

        # Try to delete a previous message
        try:
            await bot.delete_message(message.from_user.id, message.message.message_id)
        except AttributeError:
            pass


# 📍Update a message with the next movie from my_movies_list in a cards view.
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

    await bot.edit_message_media(
        media=types.InputMediaPhoto(image_link, caption=text_value),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=my_movies_list_in_cards_view_buttons(name_year),
    )


# 📍Update a message with the previous movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_previous_movie")
async def my_movies_list_in_cards_view_previous_movie(
    callback_query: types.CallbackQuery,
):
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

    await bot.edit_message_media(
        media=types.InputMediaPhoto(image_link, caption=text_value),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=my_movies_list_in_cards_view_buttons(name_year),
    )


# 📍Remove a movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_remove_movie")
async def my_movies_list_in_cards_view_remove_movie(
    callback_query: types.CallbackQuery,
):
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

    await bot.edit_message_media(
        media=types.InputMediaPhoto(image_link, caption=text_value),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=my_movies_list_in_cards_view_buttons_after_deleting(name_year),
    )


# 📍Recover after removing a movie from my_movies_list in a cards view.
@dp.callback_query_handler(text="my_movies_list_in_cards_view_recover_movie")
async def my_movies_list_in_cards_view_recover_movie(
    callback_query: types.CallbackQuery,
):
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

    await bot.edit_message_media(
        media=types.InputMediaPhoto(image_link, caption=text_value),
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=my_movies_list_in_cards_view_buttons_after_deleting_and_recovering(),
    )

    await callback_query.answer(text=alert, cache_time=0)


if __name__ == "__main__":
    print("\nIt is working!\n")
    executor.start_polling(dp, skip_updates=True)
