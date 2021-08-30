from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
)


all_dictionaries = []  # TODO get all dictionaries from db
keyboard = [[KeyboardButton(text=name)] for name in all_dictionaries]
all_dictionaries_keyboard = ReplyKeyboardMarkup(
    keyboard=keyboard,
    resize_keyboard=True,
    row_width=2)
