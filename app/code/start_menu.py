from aiogram import types

def start_menu_buttons():
    """Buttons for menu after "/start" command."""

    buttons = [types.InlineKeyboardButton('\U0001F3B2Random movies', callback_data="show_random_movies"),
               types.InlineKeyboardButton('\U0001F4D2My movies', callback_data="show_my_movies_list")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
