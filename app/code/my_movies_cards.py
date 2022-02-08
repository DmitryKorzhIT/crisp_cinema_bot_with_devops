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



#============================================================================================#
#===================================👉    Keyboards    👈===================================#
#============================================================================================#

# 📍Inline buttons for my_movies_list in cards view.
def my_movies_list_in_cards_view_buttons(name_year):
    """Inline buttons for my_movies_list in cards view:
    • Remove from my_movies_list.
    • Trailer.
    • Previous movie.
    • Next movie.
    """

    # Inline keyboard.
    buttons = [types.InlineKeyboardButton(text="Удалить из \U0001F4D4",
                                          callback_data="my_movies_list_in_cards_view_remove_movie"),
               types.InlineKeyboardButton('Трейлер',
                                          url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
               types.InlineKeyboardButton(text="<", callback_data="my_movies_list_in_cards_view_previous_movie"),
               types.InlineKeyboardButton(text=">", callback_data="my_movies_list_in_cards_view_next_movie")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    # Return an inline keyboard.
    return keyboard


# 📍Inline buttons for my_movies_list in cards view after deleting a movie.
def my_movies_list_in_cards_view_buttons_after_deleting(name_year):
    """Inline buttons for my_movies_list in cards view after
    a user has been deleted a movie from my_movies_list.
    It contains a button with the ability to add a removed movie
    back to my_movies_list.
    """

    # Inline keyboard.
    buttons = [types.InlineKeyboardButton(text="Добавить в \U0001F4D4",
                                          callback_data="my_movies_list_in_cards_view_recover_movie"),
               types.InlineKeyboardButton('Трейлер',
                                          url=f"https://www.youtube.com/results?search_query={name_year}+трейлер"),
               types.InlineKeyboardButton(text="<", callback_data="my_movies_list_in_cards_view_previous_movie"),
               types.InlineKeyboardButton(text=">", callback_data="my_movies_list_in_cards_view_next_movie")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    # Return an inline keyboard.
    return keyboard


# 📍Inline buttons for my_movies_list in cards view after deleting a movie and recovering a movie.
def my_movies_list_in_cards_view_buttons_after_deleting_and_recovering():
    """Inline buttons for my_movies_list in cards view after
    a user has been deleted a movie from my_movies_list and after
    a user has been recovered this movie.
    """

    # Inline keyboard.
    buttons = [types.InlineKeyboardButton(text="<", callback_data="my_movies_list_in_cards_view_previous_movie"),
               types.InlineKeyboardButton(text=">", callback_data="my_movies_list_in_cards_view_next_movie")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    # Return an inline keyboard.
    return keyboard



#============================================================================================#
#=====================================👉    Other    👈=====================================#
#============================================================================================#

# 📍Add a movie to my movies list.
def to_my_movies_list_second_function(user_id, kinopoisk_id):
    """This function adds a random movie
    to my_movies_list in the database."""

    # # Pull data about movie's kinopoisk_id.
    # cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_users_last_movie WHERE user_id='{user_id}'")
    # kinopoisk_id = cursor.fetchall()[0][0]

    # Check if the movie already in my_movies_list.
    cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_my_movies_list "
                   f"WHERE user_id='{user_id}' AND kinopoisk_id='{kinopoisk_id}';")
    movie_existence = cursor.fetchall()

    # Get data about current date and time.
    datetime_now = datetime.now(tz=None)

    # If the movie not in my_movies_list - add it!
    if len(movie_existence) == 0:
        cursor.execute(f"INSERT INTO telegram_bot_my_movies_list "
                       f"VALUES ('{user_id}', '{kinopoisk_id}', '{datetime_now}');")
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
     all his movies in range from "0" to the last movie.
     This function uses when a user presses the button my_movies_list and
     it resets data about the last movie a user has seen to "0".
     Because of this function, a user watches movies, not from the
     last movie he or she is stopped, but from the beginning.
     """

    # Pull user's id from the table "telegram_bot_users_last_movie_in_my_movies_list".
    cursor.execute(f"SELECT user_id FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    number_of_movie_from_my_movies_list = cursor.fetchall()

    # Add or update number of a movie to zero.
    if len(number_of_movie_from_my_movies_list) == 0:
        cursor.execute(f"INSERT INTO telegram_bot_users_last_movie_in_my_movies_list VALUES ('{user_id}', '0');")
        conn.commit()

    else:
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number = '0' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()


# 📍Update to "+1" a number of movies that a user has watched from my_movies_list.
def users_last_movie_in_my_movies_list_plus_one(user_id):
    """This function is an additional function for watching my_movies_list.
     When a user watches my_movies_list I have decided to count
     all his movies in range from "0" to the last movie.
     This function uses when a user presses the button
     "my_movies_list_in_cards_view_next_movie" and it updates
     data about the last movie a user has seen on "+1".
     """

    # Pull user's last movie number.
    cursor.execute(f"SELECT users_last_movie_number FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    number_of_movie_from_my_movies_list = cursor.fetchall()
    number_of_movie_from_my_movies_list = number_of_movie_from_my_movies_list[0][0]

    # Count a number of user's movies in my_movies_list.
    cursor.execute(f"SELECT COUNT (user_id) FROM telegram_bot_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    count_amount_of_movies_in_my_movies_list = cursor.fetchall()[0][0]

    # If we have the last movie in a queue and want to go forward,
    # it sends us to the first movie.
    if number_of_movie_from_my_movies_list >= count_amount_of_movies_in_my_movies_list - 1:
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number='0' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()

    # If we have NOT the last movie in a queue and want to go forward.
    else:
        # "+1" to user's last movie number.
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number='{number_of_movie_from_my_movies_list + 1}' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()


# 📍Update to "-1" a number of movies that a user has watched from my_movies_list.
def users_last_movie_in_my_movies_list_minus_one(user_id):
    """This function is an additional function for watching my_movies_list.
     When a user watches my_movies_list I have decided to count
     all his movies in range from "0" to the last movie.
     This function uses when a user presses the button
     "my_movies_list_in_cards_view_next_movie" and it updates
     data about the last movie a user has seen on "-1".
     """

    # Pull user's last movie number.
    cursor.execute(f"SELECT users_last_movie_number FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    number_of_movie_from_my_movies_list = cursor.fetchall()[0][0]

    # Count a number of user's movies in my_movies_list.
    cursor.execute(f"SELECT COUNT (user_id) FROM telegram_bot_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    count_amount_of_movies_in_my_movies_list = cursor.fetchall()[0][0]

    # If we have the first movie in a queue and want to go back,
    # this condition send us to the last movie.
    if number_of_movie_from_my_movies_list <= 0:
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number='{count_amount_of_movies_in_my_movies_list-1}' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()

    # If we have NOT the first movie in a queue and want to go back.
    else:
        # "-1" to user's last movie number.
        cursor.execute(f"UPDATE telegram_bot_users_last_movie_in_my_movies_list "
                       f"SET users_last_movie_number='{number_of_movie_from_my_movies_list-1}' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()


# 📍Pull a kinopoisk_id of a movie where user has stopped.
def show_users_last_movie_in_my_movies_list(user_id):
    """This function pull number of a movie where user has stopped
    while has been listing my_movies_list. Then it uses this number
    to pull a kinopoisk id of this movie."""

    # Pull user's last movie number.
    cursor.execute(f"SELECT users_last_movie_number FROM telegram_bot_users_last_movie_in_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    number_of_movie_from_my_movies_list = cursor.fetchall()
    number_of_movie_from_my_movies_list = number_of_movie_from_my_movies_list[0][0]

    # Pull a list of user's movies from my_movies_list.
    cursor.execute(f"SELECT kinopoisk_id FROM telegram_bot_my_movies_list WHERE user_id='{user_id}' "
                   f"ORDER BY date_time DESC;")
    all_users_movies_list = cursor.fetchall()

    # Kinopoisk id of a movie where user has stopped.
    kinopoisk_id = all_users_movies_list[number_of_movie_from_my_movies_list][0]

    return kinopoisk_id


# 📍Add data to a table with the last movie that a user deleted from my_movies_list.
def add_to_db_users_last_removed_movie_from_my_movies_list(user_id, kinopoisk_id):
    """While a user is listing his my_movies_list, he might want to delete
    a specific movie from his movies library. If a user wants to do it,
    he presses the button "Remove from my library" and kinopoisk_id of
    this movie temporarily adds to a special table.
    I need this function to have the ability to recover the kinopoisk_id
    of the last deleted movie."""

    # Check is user already exist in the table.
    cursor.execute(f"SELECT user_id FROM telegram_bot_my_movies_list_last_removed_movie "
                   f"WHERE user_id='{user_id}';")
    user_existance = cursor.fetchall()

    # Insert or update kinopoisk_id of the last movie that a user deleted from my_movies_list.
    if len(user_existance) == 0:
        cursor.execute(f"INSERT INTO telegram_bot_my_movies_list_last_removed_movie "
                       f"VALUES ('{user_id}', '{kinopoisk_id}', 'true');")
        conn.commit()

    else:
        cursor.execute(f"UPDATE telegram_bot_my_movies_list_last_removed_movie "
                       f"SET kinopoisk_id='{kinopoisk_id}', just_deleted='true' "
                       f"WHERE user_id='{user_id}';")
        conn.commit()


# 📍Pull data from a table with the last movie that a user deleted from my_movies_list.
def pull_from_db_users_last_removed_movie_from_my_movies_list(user_id):
    """While a user is listing his my_movies_list, he might want to delete
    a specific movie from his movies library. If a user wants to do it,
    he presses the button "Remove from my library" and kinopoisk_id of
    this movie temporarily adds to a special table.
    I need this function to recover the kinopoisk_id of the last deleted movie.
    """

    cursor.execute(f"SELECT kinopoisk_id "
                   f"FROM telegram_bot_my_movies_list_last_removed_movie "
                   f"WHERE user_id='{user_id}';")
    kinopoisk_id = cursor.fetchall()[0][0]

    return kinopoisk_id


# 📍Delete a movie from the my_movies_list DB table.
def remove_users_last_removed_movie_from_my_movies_list(user_id, kinopoisk_id):
    """Remove a movie that a user has just deleted from the my_movies_list DB table."""

    cursor.execute(f"DELETE FROM telegram_bot_my_movies_list "
                   f"WHERE user_id='{user_id}' AND kinopoisk_id='{kinopoisk_id}';")
    conn.commit()


# 📍Check is a movie has been just deleted.
def show_my_movies_list_just_deleted(user_id):
    """Check, is a user just deleted a movie from my_movies_list.
    It returns a True or a False value.
    """

    cursor.execute(f"SELECT just_deleted "
                   f"FROM telegram_bot_my_movies_list_last_removed_movie "
                   f"WHERE user_id='{user_id}';")
    just_deleted = cursor.fetchall()[0][0]

    return just_deleted


# 📍Set False that the movie is not just deleted.
def set_false_my_movies_list_just_deleted(user_id):
    """This function set a False value in the DB table and tell,
    that the last thing that a user has done IS NOT deleted
    a movie from my_movies_list.
    """

    cursor.execute(f"UPDATE telegram_bot_my_movies_list_last_removed_movie "
                   f"SET just_deleted='false' "
                   f"WHERE user_id='{user_id}';")
    conn.commit()


# 📍Check is a movie has been just recovered.
def show_my_movies_list_just_recovered(user_id):
    """This function check a value in the DB table and tell,
    was the last thing that user has done was recovered a movie
    or not from my_movies_list.
    """

    cursor.execute(f"SELECT just_recovered "
                   f"FROM telegram_bot_my_movies_list_last_removed_movie "
                   f"WHERE user_id='{user_id}';")
    just_recovered = cursor.fetchall()[0][0]

    return just_recovered


# 📍Set True that the movie is just recovered.
def set_true_my_movies_list_just_recovered(user_id):
    """This function set a True value in the DB table and tell,
    that the last thing that a user has done is recovered
    a movie after deleting it in my_movies_list.
    """

    cursor.execute(f"UPDATE telegram_bot_my_movies_list_last_removed_movie "
                   f"SET just_recovered='true' "
                   f"WHERE user_id='{user_id}';")
    conn.commit()


# 📍Set False that the movie is not just recovered.
def set_false_my_movies_list_just_recovered(user_id):
    """This function set a False value in the DB table and tell,
    that the last thing that a user has done IS NOT recovered
    a movie after deleting it in my_movies_list.
    """

    cursor.execute(f"UPDATE telegram_bot_my_movies_list_last_removed_movie "
                   f"SET just_recovered='false' "
                   f"WHERE user_id='{user_id}';")
    conn.commit()


# 📍Count a number of user's movies in my_movies_list.
def count_users_movies_in_my_movies_list(user_id):
    """Count a number of user's movies in my_movies_list."""

    cursor.execute(f"SELECT COUNT (user_id) FROM telegram_bot_my_movies_list "
                   f"WHERE user_id='{user_id}';")
    count_amount_of_movies_in_my_movies_list = cursor.fetchall()[0][0]

    return count_amount_of_movies_in_my_movies_list




