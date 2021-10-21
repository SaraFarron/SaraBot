from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from re import search

from . import dp
from . import logger
from keyboards import all_dictionaries_keyboard
from states import UpdateDictionary
from db import get_data, update_row


@dp.message_handler(text='Update Dictionary')
async def update_dictionary(message: Message):

    await message.answer('Searching for dictionaries', reply_markup=ReplyKeyboardRemove())
    keyboard = all_dictionaries_keyboard()
    logger.info(f'Update dictionary from  {message.from_user.username}')

    await message.answer('Select dictionary to update', reply_markup=keyboard)
    await UpdateDictionary.get_translation_to_update.set()


@dp.callback_query_handler(state=UpdateDictionary.get_translation_to_update)
async def get_translation_to_update(call: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['dictionary name'] = call.data

    await call.message.answer(
        'Send an old and new version of word that you want to update like this:\n old_word-new_word')
    await UpdateDictionary.update.set()


@dp.message_handler(state=UpdateDictionary.update)
async def confirm(message: Message, state: FSMContext):

    data = await state.get_data()
    dictionary_name = data.get('dictionary name')
    old_word, new_word = message.text.split('-')
    response = get_data(dictionary_name)
    words = [x[1] for x in response] + [x[2] for x in response]

    if old_word not in words:
        logger.info(f'{get_data(dictionary_name)}')
        await message.answer('No such word found in dictionary')
        await UpdateDictionary.get_translation_to_update.set()

    else:
        if search('[A-Za-z]', old_word):
            update_row(dictionary_name, {'english': old_word}, {'english': new_word})
            await message.answer('Dictionary updated!')

        elif search('[А-Яа-я]', old_word):
            update_row(dictionary_name, {'russian': old_word}, {'russian': new_word})
            await message.answer('Dictionary updated!')

        else:
            await message.answer('Use english or russian letters')

    await state.finish()
