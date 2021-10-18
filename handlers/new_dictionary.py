from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import (yes_no_answer)
from . import dp
from . import logger
from states import (AddWords, CreateDictionary)


@dp.callback_query_handler(text="add dict")
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
