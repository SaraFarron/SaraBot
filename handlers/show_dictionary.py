from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from db import get_data
from keyboards import all_dictionaries_keyboard
from states import ShowWords
from . import dp, logger


@dp.message_handler(text='Show Dictionary')
async def delete_word(message: Message):

    logger.info('Entered show dictionary stage')
    await message.answer('Searching for dictionaries', reply_markup=ReplyKeyboardRemove())
    await message.answer('Choose dictionary which you want to see',
                         reply_markup=all_dictionaries_keyboard())
    await ShowWords.choose_dictionary.set()


@dp.callback_query_handler(state=ShowWords.choose_dictionary)
async def get_dictionary(call: CallbackQuery, state: FSMContext):

    dictionary = call.data
    words = get_data(dictionary, field='russian')
    text = f"All words in {dictionary}:\n"

    for word in words:
        text += word[0] + ', '
    text = text[:-2] + '.'
    await call.message.answer(text)
    await state.finish()
