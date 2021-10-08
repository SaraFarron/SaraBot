from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from db import get_all_tables


def add_inline_buttons(buttons: dict[str: str], keyboard: InlineKeyboardMarkup):
    """Return inline keyboard with buttons added"""

    for button_name, button_callback in buttons.items():
        keyboard.add(InlineKeyboardButton(button_name, callback_data=button_callback))

    return keyboard


menu_buttons = {
    'Add Dictionary': 'add dict',
    'Show all dictionaries': 'show dicts',
    'Update Dictionary': 'update dict',
    'Delete Dictionary': 'delete dict'
}
menu = InlineKeyboardMarkup(row_width=2)
menu = add_inline_buttons(menu_buttons, menu)

yes_no_buttons = {
    'Yes': 'yes',
    'No': 'no'
}
yes_no_answer = InlineKeyboardMarkup()
yes_no_answer = add_inline_buttons(yes_no_buttons, yes_no_answer)


def all_dictionaries_keyboard():
    """Return a keyboard with all dictionaries as buttons"""

    dictionaries = get_all_tables()
    dictionaries = {d: d for d in dictionaries}
    keyboard = InlineKeyboardMarkup()
    keyboard = add_inline_buttons(dictionaries, keyboard)

    return keyboard
