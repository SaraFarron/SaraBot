from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from . import dp

from keyboards import all_dictionaries_keyboard, yes_no_answer
from states import AddWords, CreateDictionary
from db import add_row, get_all_tables


@dp.message_handler(state=AddWords.choose_dictionary)
@dp.message_handler(text='Add New Word')
async def add_word(message: Message):

    await message.reply('Searching for your dictionaries', reply_markup=ReplyKeyboardRemove())
    keyboard = all_dictionaries_keyboard()

    if keyboard:
        await message.reply('Please choose dictionary at which words will be added:',
                            reply_markup=keyboard)
        await AddWords.get_dictionary.set()

    else:
        await message.reply("You don't have any dictionaries yet, do you want to create one?",
                            reply_markup=yes_no_answer)
        await AddWords.create_new.set()


@dp.message_handler(state=AddWords.create_new)
async def create_new_dictionary(message: Message, state: FSMContext):

    if message.text == 'Yes':
        await state.finish()
        await CreateDictionary.get_dictionary_name.set()

    else:
        await message.reply('Okay, canceled')
        await state.finish()


@dp.callback_query_handler(text=get_all_tables(), state=AddWords.get_dictionary)
async def get_dictionary(call: CallbackQuery, state: FSMContext):

    dictionary_name = call.data
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name

    await call.message.answer('Provide a pair of words in this format:\n русский english')
    await AddWords.next()


@dp.message_handler(state=AddWords.get_translation_pair)
async def get_translation_pair(message: Message, state: FSMContext):

    pair = message.text.split(' ')
    data = await state.get_data()
    add_row(data.get('dictionary name'), {'Russian': pair[0], 'English': pair[1]})

    await message.answer(f'Translation for {pair[1]} added to {data.get("dictionary name")}')
    await state.finish()
