from code.config import APP_BOT_TOKEN, DB_DBNAME, DB_HOST, DB_PASSWORD, DB_USER
from datetime import datetime

import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hbold, hcode

# Telegram bot settings.
bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# PostgreSQL database settings.
conn = psycopg2.connect(
    f"dbname={DB_DBNAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}"
)
cursor = conn.cursor()


# 📍Show my_movies_list.
def show_my_movies_list_in_list_view_function(user_id):
    """Show user's my_movies_list."""

    # Text of the my_movies_list message.
    my_movies_string = str(f"{hbold('My movies list:')}\n\n")

    # Pull movies from my_movies_list.
    cursor.execute(
        f"SELECT kinopoisk_id FROM telegram_bot_my_movies_list WHERE user_id='{user_id}' "
        f"ORDER BY date_time DESC;"
    )
    all_user_movies_list = cursor.fetchall()

    # For each movie from my_movies_list.
    for i in all_user_movies_list:
        kinopoisk_id = i[0]

        # Pull data about one movie.
        cursor.execute(
            f"SELECT * FROM telegram_bot_good_quality_movies_db WHERE kinopoisk_id={kinopoisk_id};"
        )
        movie_list = list(cursor.fetchall())

        # Put data about one movie into a dictionary.
        movie_dict = {
            "my_index": movie_list[0][0],
            "name_ru": movie_list[0][1],
            "rating_kinopoisk": movie_list[0][2],
            "rating_kinopoisk_vote_count": movie_list[0][3],
            "film_length": movie_list[0][4],
            "rating_age_limits": movie_list[0][5],
            "kinopoisk_id": movie_list[0][6],
            "type": movie_list[0][7],
            "year": movie_list[0][8],
            "poster_url": movie_list[0][9],
            "countries": movie_list[0][10],
            "genres": movie_list[0][11],
            "description": movie_list[0][12],
        }

        # String with one movie.
        text_value = f"• {movie_dict['name_ru']}\n"

        # Append a movie to string with other movies.
        my_movies_string += str(text_value)

    # Return a string with all movies from the my_movies_list.
    return my_movies_string


# 📍Show my_movies_list inline buttons.
def my_movies_list_buttons():
    """Inline buttons for "my_movies_list":
    • Previous movie.
    • Trailer.
    • Next movie.
    • Remove from my_movies_list
    """

    # Inline keyboard.
    buttons = [
        types.InlineKeyboardButton(
            text="<", callback_data="my_movies_list_buttons_previous_page"
        ),
        types.InlineKeyboardButton(
            text="Трейлер", url="https://www.youtube.com"
        ),  # url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
        types.InlineKeyboardButton(
            text=">", callback_data="my_movies_list_buttons_next_page"
        ),
        types.InlineKeyboardButton(
            text="Удалить из \U0001F4D4",
            callback_data="my_movies_list_buttons_next_page",
        ),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    # Return an inline keyboard.
    return keyboard
