from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from . import dp, logger

from keyboards import all_dictionaries_keyboard, yes_no_answer
from states import AddWord, CreateDictionary
from db import add_row


@dp.message_handler(state=AddWord.choose_dictionary)
@dp.message_handler(text='Add New Word')
async def add_word(message: Message):

    logger.info('Entered add word stage')
    await message.answer('Searching for your dictionaries', reply_markup=ReplyKeyboardRemove())
    keyboard = all_dictionaries_keyboard()

    if keyboard:
        await message.answer('Please choose dictionary at which words will be added:',
                             reply_markup=keyboard)
        await AddWord.get_dictionary.set()

    else:
        await message.answer("You don't have any dictionaries yet, do you want to create one?",
                             reply_markup=yes_no_answer)
        await AddWord.create_new.set()


@dp.callback_query_handler(state=AddWord.create_new)
async def create_new_dictionary(call: CallbackQuery, state: FSMContext):

    if call.message.text == 'yes':
        await state.finish()
        await CreateDictionary.get_dictionary_name.set()

    else:
        await call.message.answer('Okay, canceled')
        await state.finish()


@dp.callback_query_handler(state=AddWord.get_dictionary)
async def get_dictionary(call: CallbackQuery, state: FSMContext):

    dictionary_name = call.data
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name

    await call.message.answer('Provide a pair of words in this format:\n русский english')
    await AddWord.next()


@dp.message_handler(state=AddWord.get_translation_pair)
async def get_translation_pair(message: Message, state: FSMContext):

    pair = message.text.split(' ')
    data = await state.get_data()
    add_row(data.get('dictionary name'), {'Russian': pair[0], 'English': pair[1]})

    await message.answer(f'Translation for {pair[1]} added to {data.get("dictionary name")}')
    await state.finish()
