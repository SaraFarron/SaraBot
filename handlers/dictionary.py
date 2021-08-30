from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

from app import bot, dp
from app import logger
from keyboards import inline, reply
from states.dictionary import AddWords


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    logger.info(f'sent menu to {message.from_user.username}')
    await message.answer("Your menu, sir", reply_markup=inline.menu)


@dp.callback_query_handler(text="create_dictionary")
async def create_dictionary(call: CallbackQuery):
    await call.answer(cache_time=60)  # seconds
    callback_data = call.data
    logger.info(f'call = {callback_data} from  {call.from_user.username}')

    await call.message.answer('How new dictionary will be named?')


@dp.callback_query_handler(text='add_word')
async def add_word(message: Message):
    await message.answer('Please choose dictionary at which words will be added:',
                         reply_markup=reply.all_dictionaries_keyboard)  # TODO error, maybe because kbrd is empty?
    await AddWords.get_dictionary.set()  # more readable then await AddWords.first()


@dp.message_handler(state=AddWords.get_dictionary)
async def get_dictionary(message: Message, state: FSMContext):
    dictionary_name = message.text
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name

    await message.answer('Provide a pair of words in format:\n русский english')
    await AddWords.next()


@dp.message_handler(state=AddWords.get_translation_pair)
async def get_translation_pair(message: Message, state: FSMContext):
    pair = message.text.split(' ')
#     TODO put pair in db
    state_data = state.get_data()
    await message.answer(f'translation for {pair[1]} added to {state_data.get("dictionary name")}')
    await state.finish()  # if need to save data then await state.reset_state(with_data=False)


@dp.message_handler()
async def echo(message: Message):
    logger.info(f'echoed user {message.from_user.username}')
    await message.answer(text=message.text)
