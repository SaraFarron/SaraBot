from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from . import dp
from . import logger

from keyboards import all_dictionaries_keyboard

from states import AddWords

from db import add_row, is_table


@dp.callback_query_handler(text='add word')
async def add_word(message: Message):
    logger.info(f'{message.from_user.username} is adding new words')
    keyboard = all_dictionaries_keyboard()
    logger.info(f'Message type - {type(message)},\ntext - {message.text},\nmethods - {dir(message)}')

    await message.reply('Please choose dictionary at which words will be added:',
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
