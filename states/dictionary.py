from aiogram.dispatcher.filters.state import StatesGroup, State


class AddWords(StatesGroup):
    get_dictionary = State()
    get_translation_pair = State()
    # confirm = State() not necessary