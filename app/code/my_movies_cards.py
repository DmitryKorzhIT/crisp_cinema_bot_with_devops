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


# 📍Show my_movies_list in a cards view.
def show_my_movies_list_in_cards_view_function(kinopoisk_id):
    """Show user's my_movies_cards. Mainly style
    has been copied from the random_movies.py,
    random_movie_buttons function.
    """

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
        rating_kinopoisk_vote_count = '%.1f' % (movie_dict['rating_kinopoisk_vote_count'] / 1000)
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
    message_list = [image_link, text_value, name_year]

    return message_list


# 📍Inline buttons for my_movies_list in cards view.
def my_movies_list_in_cards_view_buttons():
    """Inline buttons for my_movies_list in cards view:
    • Previous movie.
    • Trailer.
    • Next movie.
    • Remove from my_movies_list
    """

    # Inline keyboard.
    buttons = [types.InlineKeyboardButton(text="Удалить из \U0001F4D4", callback_data="my_movies_list_buttons_next_page"),
               types.InlineKeyboardButton(text="Трейлер", url='https://www.youtube.com'),  # url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
               types.InlineKeyboardButton(text="<", callback_data="my_movies_list_in_cards_view_previous_movie"),
               types.InlineKeyboardButton(text=">", callback_data="my_movies_list_in_cards_view_next_movie")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    # Return an inline keyboard.
    return keyboard


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


# 📍Set to "0" a number of movies that a user has watched from my_movies_list.
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
        cursor.execute(f"INSERT INTO telegram_bot_users_last_movie_in_my_movies_list VALUES ('{user_id}', '0')")
        conn.commit()
        print(f"\tMovie existence: User id was added with 0 value.\n")

    else:
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number = '0' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()
        print(f"\tMovie existence: users_last_movie_number updated to 0.\n")


# 📍Update to "+1" a number of movies that a user has watched from my_movies_list.
def users_last_movie_in_my_movies_list_plus_one(user_id):
    """This function is an additional function for watching my_movies_list.
     When a user watches my_movies_list I have decided to count
     all his movies in a range from "0" to the last movie.
     This function uses when a user presses the button
     "my_movies_list_in_cards_view_next_movie" and it updates
     data about the last movie a user has seen on "+1".
     """

    cursor.execute(f"SELECT users_last_movie_number FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}'")
    number_of_movie_from_my_movies_list = cursor.fetchall()
    print(f"\t#301: {number_of_movie_from_my_movies_list}\n")
    number_of_movie_from_my_movies_list = number_of_movie_from_my_movies_list[0][0]

    cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                   f"SET users_last_movie_number='{number_of_movie_from_my_movies_list+1}' "
                   f"WHERE user_id='{user_id}';")
    conn.commit()
    print(f"\tMovie existence: users_last_movie_number updated to {number_of_movie_from_my_movies_list+1}.\n")


# 📍
def show_users_last_movie_in_my_movies_list(user_id):

    cursor.execute(f"SELECT users_last_movie_number FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}'")
    number_of_movie_from_my_movies_list = cursor.fetchall()
    number_of_movie_from_my_movies_list = number_of_movie_from_my_movies_list[0][0]
    print(f"\tNumber of movie from my movies list: {number_of_movie_from_my_movies_list}.\n")

    # Pull a list of user's movies from my_movies_list.
    cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_my_movies_list WHERE user_id='{user_id}' "
                   f"ORDER BY date_time DESC;")
    all_users_movies_list = cursor.fetchall()
    kinopoisk_id = all_users_movies_list[number_of_movie_from_my_movies_list][0]
    print(f"\tKinopoisk id: {kinopoisk_id}.\n")

    return kinopoisk_id






