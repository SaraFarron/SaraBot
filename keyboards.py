from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
)
from db import get_all_tables, get_data


def add_inline_buttons(buttons: dict[str: str], keyboard: InlineKeyboardMarkup):
    """Return inline keyboard with buttons added"""

    for button_name, button_callback in buttons.items():
        keyboard.add(InlineKeyboardButton(button_name, callback_data=button_callback))

    return keyboard


def add_reply_buttons(buttons: list[str, ], keyboard: ReplyKeyboardMarkup):
    """Return inline keyboard with buttons added"""

    for button_name in buttons:
        keyboard.add(button_name)

    return keyboard


menu_buttons = [
    'Add New Word',
    'Delete Word',
    'Add Dictionary',
    'Show All Dictionaries',
    'Update Dictionary',
    'Delete Dictionary',
]
menu = ReplyKeyboardMarkup()
menu = add_reply_buttons(menu_buttons, menu)

yes_no_buttons = {
    'Yes': 'yes',
    'No': 'no'
}
yes_no_answer = InlineKeyboardMarkup()
yes_no_answer = add_inline_buttons(yes_no_buttons, yes_no_answer)


def all_dictionaries_keyboard():
    """
    Return a keyboard with all dictionaries as buttons. If no dictionaries were founded return False
    """

    dictionaries = get_all_tables()

    if not dictionaries:
        return False
    dictionaries = {d: d for d in dictionaries}
    keyboard = InlineKeyboardMarkup()
    keyboard = add_inline_buttons(dictionaries, keyboard)

    return keyboard


def all_words_keyboard(dictionary_name):
    """Return a keyboard with all words from dictionary"""

    words = get_data(dictionary_name, field='russian')
    words = {w: w for w in words}
    keyboard = InlineKeyboardMarkup()
    return add_inline_buttons(words, keyboard)
