from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import yes_no_answer
from . import dp
from states import AddWords, CreateDictionary


@dp.message_handler(state=CreateDictionary.get_dictionary_name)
@dp.message_handler(text="Add Dictionary'")
async def create_dictionary(message: Message):

    await message.answer('How new dictionary will be named?')
    await CreateDictionary.get_dictionary_name.set()


@dp.message_handler(state=CreateDictionary.add_words)
async def get_dictionary_name(message: Message, state: FSMContext, call: CallbackQuery):
    dictionary_name = message.text
    async with state.proxy() as data:
        data['dictionary name'] = dictionary_name

    await message.answer('Do you want add words to new dictionary right now?', reply_markup=yes_no_answer)
    await call.answer(cache_time=30)

    if call.data == 'yes':

        async with state.proxy() as data:
            data['dictionary name'] = call.data  # Wasn't tested

        await AddWords.get_translation_pair.set()  # TODO send dictionary name

    else:
        await message.answer('New dictionary has been created!')
        await state.finish()

