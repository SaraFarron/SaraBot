from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from . import dp
from . import logger

from keyboards import (yes_no_answer, all_dictionaries_keyboard)

from states import UpdateDictionary

from db import get_data, is_table


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
