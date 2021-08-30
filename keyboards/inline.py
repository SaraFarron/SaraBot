from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)


menu = InlineKeyboardMarkup(row_width=2)  # row_width=2 is ignored for whatever reason

# Adding buttons via list-in-list results in error, temporary this solution
menu.add(InlineKeyboardButton(text='create new dictionary', callback_data='create_dictionary'))
menu.add(InlineKeyboardButton(text='update dictionary', callback_data='update_dictionary'))
menu.add(InlineKeyboardButton(text='delete dictionary', callback_data='delete_dictionary'))
menu.add(InlineKeyboardButton(text='show dictionary', callback_data='show_dictionary'))
menu.add(InlineKeyboardButton(text='add new words', callback_data='add_word'))  # TODO move to update dictionary
menu.add(InlineKeyboardButton(text='show learned words', callback_data='show_learned_words'))
menu.add(InlineKeyboardButton(text='learn new words', callback_data='learn_new_words'))
