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
async def update_dictionary(message: Message, call: CallbackQuery):
    await call.answer(cache_time=60)  # seconds
    callback_data = call.data
    logger.info(f'call = {callback_data} to update dictionary from  {call.from_user.username}')
    await message.answer('Select dictionary to update', reply_markup=inline.all_dictionaries_keyboard)
    await UpdateDictionary.get_dictionary.set()


@dp.callback_query_handler(state=UpdateDictionary.get_translation_to_update)
async def get_translation_to_update(message: Message, call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    # TODO check if dictionary exists in db
    await message.answer(
        'Send an old word and new version of word that you want to update like this:\n old-word new-word')
    await UpdateDictionary.next()


@dp.message_handler(state=UpdateDictionary.confirm)
async def confirm(message: Message, state: FSMContext, call: CallbackQuery):
    # TODO search for word and if exists continue, otherwise go to previous state
    old_word = 'old'
    new_word = 'new'

    await message.answer(f'You are changing {old_word} to {new_word}, proceed?', reply_markup=inline.yes_no)
    await call.answer(cache_time=30)
    callback_data = call.data
    if callback_data == 'yes':
        await state.finish()  # TODO update dictionary
        await message.answer('Dictionary updated!')
    else:
        await message.answer('Canceled')
        await state.finish()


# Delete dictionary


# Show learned words


# Learn new words


@dp.message_handler()
async def error(message: Message):

    logger.info(f'did not understand user {message.from_user.username}')
    await message.answer('Excuse me, i didnt understand your request')
