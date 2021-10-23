from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from . import dp, logger

from keyboards import all_dictionaries_keyboard, all_words_keyboard, yes_no_answer
from states import DeleteWord
from db import delete_row


@dp.message_handler(text='Delete Word')
async def delete_word(message: Message):

    logger.info('Entered delete word stage')
    await message.answer('Searching for dictionaries', reply_markup=ReplyKeyboardRemove())
    await message.answer('Choose dictionary from which you want to delete a word',
                         reply_markup=all_dictionaries_keyboard())
    await DeleteWord.choose_pair.set()


@dp.callback_query_handler(state=DeleteWord.choose_pair)
async def get_dictionary(call: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['dictionary name'] = call.data
    await call.message.answer('Choose which word you want to delete', reply_markup=all_words_keyboard(call.data))
    await DeleteWord.confirm.set()


@dp.callback_query_handler(state=DeleteWord.confirm)
async def confirm(call: CallbackQuery, state: FSMContext):

    word = call.data
    async with state.proxy() as data:
        data['word'] = word
    await call.message.answer(f'Translation for {word} will be deleted, proceed?', reply_markup=yes_no_answer)
    await DeleteWord.delete.set()


@dp.callback_query_handler(state=DeleteWord.delete)
async def delete(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    dictionary, word = data.get('dictionary name'), data.get('word')

    if call.data == 'yes':
        delete_row(dictionary, 'russian', word)
        await call.message.answer('Word has been deleted')

    else:
        await call.message.answer('Canceled')

    await state.finish()
