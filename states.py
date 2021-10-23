from aiogram.dispatcher.filters.state import StatesGroup, State


class AddWord(StatesGroup):
    choose_dictionary = State()
    create_new = State()
    get_dictionary = State()
    get_translation_pair = State()


class ShowWords(StatesGroup):
    choose_dictionary = State()


class DeleteWord(StatesGroup):
    choose_pair = State()
    confirm = State()
    delete = State()


class CreateDictionary(StatesGroup):
    get_dictionary_name = State()
    add_words = State()


class UpdateDictionary(StatesGroup):
    get_translation_to_update = State()
    update = State()


class DeleteDictionary(StatesGroup):
    get_dictionary = State()
    confirm = State()
    delete = State()
