from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


def help_keybord():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = KeyboardButton('/predict')
    buttons_2 = KeyboardButton('/start')
    markup = markup.add(buttons_2, buttons)
    return markup