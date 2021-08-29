from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)

inline_menu = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text='create new dictionary'),
            InlineKeyboardButton(text='update dictionary'),
        ],
        [
            InlineKeyboardButton(text='delete dictionary'),
            InlineKeyboardButton(text='show dictionary'),
        ],
        [
            InlineKeyboardButton(text='show learned words'),
            InlineKeyboardButton(text='learn new words'),
        ],
    ],
    resize_keyboard=True
)