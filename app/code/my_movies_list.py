from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import hbold, hcode
from datetime import datetime
import psycopg2

from code.config import APP_BOT_TOKEN
from code.config import DB_DBNAME, DB_USER, DB_PASSWORD, DB_HOST


# Telegram bot settings.
bot = Bot(token=APP_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# PostgreSQL database settings.
conn = psycopg2.connect(f'dbname={DB_DBNAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}')
cursor = conn.cursor()


# 📍Add a movie to my movies list.
def to_my_movies_list_second_function(user_id, kinopoisk_id):
    """This function adds a random movie
    to my_movies_list in the database."""

    # # Pull data about movie's kinopoisk_id.
    # cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_users_last_movie WHERE user_id='{user_id}'")
    # kinopoisk_id = cursor.fetchall()[0][0]

    # Check if the movie already in my_movies_list.
    cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_my_movies_list "
                   f"WHERE user_id='{user_id}' AND kinopoisk_id='{kinopoisk_id}'")
    movie_existence = cursor.fetchall()

    # Get data about current date and time.
    datetime_now = datetime.now(tz=None)

    # If the movie not in my_movies_list - add it!
    if len(movie_existence) == 0:
        cursor.execute(f"INSERT INTO telegram_bot_my_movies_list VALUES ('{user_id}', '{kinopoisk_id}', '{datetime_now}')")
        conn.commit()
        text_value='Фильм добавлен в вашу библиотеку!'

    # If the movie already in my_movies_list - update date_time of this movie!
    else:
        cursor.execute(f"UPDATE telegram_bot_my_movies_list "
                       f"SET date_time = '{datetime_now}' "
                       f"WHERE user_id='{user_id}' AND kinopoisk_id='{kinopoisk_id}';")
        conn.commit()
        text_value='Этот фильм уже находится в вашей библиотеке!'

    # Return a message for user.
    return text_value


# 📍 Set to "0" a number of movies that a user has watched from my_movies_list.
def users_last_movie_in_my_movies_list_equal_zero(user_id):
    """This function is an additional function for watching my_movies_list.
     When a user watches my_movies_list I have decided to count
     all his movies in a range from "0" to the last movie.
     This function uses when a user presses the button my_movies_list and
     it resets data about the last movie a user has seen to "0".
     Because of this function, a user watches movies, not from the
     last movie he or she is stopped but from the beginning.
     """

    cursor.execute(f"SELECT user_id FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}'")
    number_of_movie_from_my_movies_list = cursor.fetchall()

    print(f"\tMovie existence: {number_of_movie_from_my_movies_list}.\n")


    if len(number_of_movie_from_my_movies_list) == 0:
        cursor.execute(f"INSERT INTO telegram_bot_users_last_movie_in_my_movies_list VALUES ('{user_id}', '1')")
        conn.commit()
        print(f"\tMovie existence: User id was added with 1 value.\n")

    else:
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number = '1' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()
        print(f"\tMovie existence: users_last_movie_number updated to 1.\n")


# 📍Show my_movies_list.
def show_my_movies_list_in_list_view_function(user_id):
    """Show user's my_movies_list."""

    # Text of the my_movies_list message.
    my_movies_string = str(f"{hbold('My movies list:')}\n\n")

    # Pull movies from my_movies_list.
    cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_my_movies_list WHERE user_id='{user_id}' "
                   f"ORDER BY date_time DESC;")
    all_user_movies_list = cursor.fetchall()
    print('All users movies list:', all_user_movies_list)

    # For each movie from my_movies_list.
    for i in all_user_movies_list:
        kinopoisk_id = i[0]

        # Pull data about one movie.
        cursor.execute(f"SELECT * FROM telegram_bot_good_quality_movies_db WHERE kinopoisk_id={kinopoisk_id};")
        movie_list = list(cursor.fetchall())

        # Put data about one movie into a dictionary.
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
    buttons = [types.InlineKeyboardButton(text="<", callback_data="my_movies_list_buttons_previous_page"),
               types.InlineKeyboardButton(text="Трейлер", url='https://www.youtube.com'),  # url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
               types.InlineKeyboardButton(text=">", callback_data="my_movies_list_buttons_next_page"),
               types.InlineKeyboardButton(text="Удалить из \U0001F4D4", callback_data="my_movies_list_buttons_next_page")]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    # Return an inline keyboard.
    return keyboard





