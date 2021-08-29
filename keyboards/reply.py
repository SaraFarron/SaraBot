from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
)


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='create new dictionary'),
            KeyboardButton(text='update dictionary'),
        ],
        [
            KeyboardButton(text='delete dictionary'),
            KeyboardButton(text='show dictionary'),
        ],
        [
            KeyboardButton(text='show learned words'),
            KeyboardButton(text='learn new words'),
        ],
    ],
    resize_keyboard=True
)