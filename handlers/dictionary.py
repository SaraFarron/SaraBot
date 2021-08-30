from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

from app import bot, dp
from app import logger
from keyboards import inline, reply
from states.dictionary import AddWords, CreateDictionary, UpdateDictionary, DeleteDictionary


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    """Menu, shows all bot functionality"""

    logger.info(f'sent menu to {message.from_user.username}')
    await message.answer("Your menu, sir", reply_markup=inline.menu)


# Add words
@dp.callback_query_handler(text='add_word')
async def add_word(message: Message):

    logger.info(f'{message.from_user.username} is adding new words')
    await message.answer('Please choose dictionary at which words will be added:',
                         reply_markup=inline.all_dictionaries_keyboard)  # TODO error
    await AddWords.get_dictionary.set()  # more readable then await AddWords.first()


@dp.message_handler(state=AddWords.get_dictionary)
async def get_dictionary(message: Message, state: FSMContext):

    dictionary_name = message.text
    # TODO search in db for dictionary_name
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name
    await message.answer('Provide a pair of words in this format:\n русский english')
    await AddWords.next()


@dp.message_handler(state=AddWords.get_translation_pair)
async def get_translation_pair(message: Message, state: FSMContext):

    pair = message.text.split(' ')
    # TODO put pair in db
    state_data = state.get_data()
    await message.answer(f'translation for {pair[1]} added to {state_data.get("dictionary name")}')
    await state.finish()  # if need to save data then await state.reset_state(with_data=False)


# Create new dictionary
@dp.callback_query_handler(text="create_dictionary")
async def create_dictionary(message: Message, call: CallbackQuery):

    await call.answer(cache_time=60)  # seconds
    callback_data = call.data
    logger.info(f'call = {callback_data} to create new dictionary from  {call.from_user.username}')
    await message.answer('How new dictionary will be named?')
    await CreateDictionary.get_dictionary_name.set()


@dp.message_handler(state=CreateDictionary.get_dictionary_name)
async def get_dictionary_name(message: Message, state: FSMContext):
    dictionary_name = message.text
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name
    await message.answer('Do you want add words to new dictionary right now?', reply_markup=inline.yes_no)
    await CreateDictionary.next()


@dp.callback_query_handler(state=CreateDictionary.add_words)
async def add_words(message: Message, call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=30)
    callback_data = call.data
    if callback_data == 'yes':
        await AddWords.get_translation_pair.set()  # TODO send dictionary name
    else:
        await message.answer('New dictionary has been created!')
        await state.finish()


# Update dictionary
@dp.callback_query_handler(text='update_dictionary')
async def update_dictionary(message: Message):
    pass


@dp.callback_query_handler()
async def get_translation_to_update(message: Message, state: FSMContext):
    pass


@dp.message_handler()
async def confirm(message: Message):
    pass


# Delete dictionary


# Show learned words


# Learn new words


@dp.message_handler()
async def error(message: Message):

    logger.info(f'did not understand user {message.from_user.username}')
    await message.answer('Excuse me, i didnt understand your request')
