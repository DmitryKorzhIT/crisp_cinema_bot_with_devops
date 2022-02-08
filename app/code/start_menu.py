from aiogram import types


# 📍Inline buttons for start menu.
def start_menu_buttons():
    """Buttons for menu after "/start" command."""

    buttons = [types.InlineKeyboardButton('\U0001F3B2Случайные фильмы', callback_data="show_random_movies"),
               types.InlineKeyboardButton('\U0001F4D2Мои фильмы', callback_data="show_my_movies_list_in_cards_view")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
