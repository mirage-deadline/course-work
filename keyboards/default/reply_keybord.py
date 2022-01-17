from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


def help_keybord():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = KeyboardButton('/predict')
    markup = markup.add(buttons)
    return markup