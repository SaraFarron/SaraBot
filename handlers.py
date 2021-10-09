from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from main import dp
from main import logger

from keyboards import (menu, yes_no_answer, all_dictionaries_keyboard)

from states import (AddWords, UpdateDictionary,
                    DeleteDictionary, CreateDictionary)

from db import (
    create_table, add_row, update_row,
    delete_row, get_data, is_table)


@dp.message_handler(Command('menu'))
async def send_menu(message: Message):
    """Menu, shows all bot functionality"""

    logger.info(f'sent menu to {message.from_user.username}')

    await message.answer("Please choose an action", reply_markup=menu)


# Add words
@dp.callback_query_handler(text='add word')
async def add_word(message: Message):

    logger.info(f'{message.from_user.username} is adding new words')
    keyboard = all_dictionaries_keyboard()

    await message.answer('Please choose dictionary at which words will be added:',
                         reply_markup=keyboard)
    await AddWords.get_dictionary.set()  # more readable then await AddWords.first()


@dp.callback_query_handler(state=AddWords.get_dictionary)
async def get_dictionary(message: Message, state: FSMContext, call: CallbackQuery):

    dictionary_name = call.data

    if not is_table(dictionary_name):  # TODO might not be necessary
        await message.answer('No such dictionary')
        await state.finish()

    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name

    await message.answer('Provide a pair of words in this format:\n русский english')
    await AddWords.next()


@dp.message_handler(state=AddWords.get_translation_pair)
async def get_translation_pair(message: Message, state: FSMContext):

    pair = message.text.split(' ')
    data = state.get_data()
    add_row(data.get('dictionary name'), {pair[0]: pair[1]})  # TODO test this

    await message.answer(f'translation for {pair[1]} added to {data.get("dictionary name")}')
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

    await message.answer('Do you want add words to new dictionary right now?', reply_markup=yes_no_answer)
    await CreateDictionary.next()


@dp.callback_query_handler(state=CreateDictionary.add_words)
async def add_words(message: Message, call: CallbackQuery, state: FSMContext):

    await call.answer(cache_time=30)
    callback_data = call.data

    if callback_data == 'yes':

        async with state.proxy() as data:
            data['dictionary name'] = callback_data  # Wasn't tested

        await AddWords.get_translation_pair.set()  # TODO send dictionary name

    else:
        await message.answer('New dictionary has been created!')
        await state.finish()


# Update dictionary
@dp.callback_query_handler(text='update dict')
async def update_dictionary(message: Message, call: CallbackQuery):

    await call.answer(cache_time=60)  # seconds
    callback_data = call.data
    keyboard = all_dictionaries_keyboard()

    logger.info(f'call = {callback_data} to update dictionary from  {call.from_user.username}')

    await message.answer('Select dictionary to update', reply_markup=keyboard)
    await UpdateDictionary.get_dictionary.set()


@dp.callback_query_handler(state=UpdateDictionary.get_translation_to_update)
async def get_translation_to_update(message: Message, call: CallbackQuery, state: FSMContext):

    await call.answer(cache_time=60)
    callback_data = call.data

    if not is_table(callback_data):
        await message.answer('No such dictionary')
        await state.finish()

    await message.answer(
        'Send an old word and new version of word that you want to update like this:\n old word_new word')
    await UpdateDictionary.next()


@dp.message_handler(state=UpdateDictionary.confirm)
async def confirm(message: Message, state: FSMContext, call: CallbackQuery):

    # TODO search for word and if exists continue, otherwise go to previous state
    old_word, new_word = message.text.split('_')
    old_pair = get_data(message.from_user.username, old_word)

    if not old_pair:
        await message.answer('No such word found in dictionary')
        await UpdateDictionary.previous()

    else:
        await message.answer(f'You are changing {old_word} to {new_word}, proceed?', reply_markup=yes_no_answer)
        await call.answer(cache_time=30)
        callback_data = call.data

        if callback_data == 'yes':
            new_pair = ''  # TODO
            # update_row(callback_data, )
            await state.finish()  # TODO update dictionary
            await message.answer('Dictionary updated!')
        else:
            await message.answer('Canceled')

        await state.finish()


# Delete dictionary


# Show learned words


# Learn new words


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)
