from aiogram.dispatcher.filters.state import StatesGroup, State


class AddWords(StatesGroup):
    choose_dictionary = State()
    create_new = State()
    get_dictionary = State()  # todo make get_dictionary a reusable state
    get_translation_pair = State()


class CreateDictionary(StatesGroup):
    get_dictionary_name = State()
    add_words = State()


class UpdateDictionary(StatesGroup):
    get_dictionary = State()
    get_translation_to_update = State()
    confirm = State()


class DeleteDictionary(StatesGroup):
    get_dictionary = State()
    confirm = State()
    delete = State()
