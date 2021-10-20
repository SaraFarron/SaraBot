from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from . import dp, logger
from db import create_table, is_table
from states import CreateDictionary


@dp.message_handler(state=CreateDictionary.get_dictionary_name)
@dp.message_handler(text="Add Dictionary")
async def create_dictionary(message: Message):

    logger.info('Entered new dictionary stage')
    await message.answer('How new dictionary will be named?', reply_markup=ReplyKeyboardRemove())
    await CreateDictionary.add_words.set()


@dp.message_handler(state=CreateDictionary.add_words)
async def get_dictionary_name(message: Message, state: FSMContext):

    dictionary_name = message.text
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name

    if not is_table(dictionary_name):
        create_table(dictionary_name, {'Russian': 'TEXT', 'English': 'TEXT'})

    await message.answer('New dictionary has been created!')
    await state.finish()
