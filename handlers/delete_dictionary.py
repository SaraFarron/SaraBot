from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from db import delete_table
from keyboards import all_dictionaries_keyboard, yes_no_answer
from states import DeleteDictionary
from . import dp, logger


@dp.message_handler(text='Delete Dictionary')
async def get_name(message: Message):

    logger.info('Entered delete stage')
    await message.answer('Searching for dictionaries', reply_markup=ReplyKeyboardRemove())
    await message.answer('Please choose which dictionary you want to be deleted',
                         reply_markup=all_dictionaries_keyboard())
    await DeleteDictionary.confirm.set()


@dp.callback_query_handler(state=DeleteDictionary.confirm)
async def confirm_deletion(call: CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['dictionary name'] = call.data
    await call.message.answer(f"{call.data} will be deleted, proceed?", reply_markup=yes_no_answer)
    await DeleteDictionary.delete.set()


@dp.callback_query_handler(state=DeleteDictionary.delete)
async def delete_dictionary(call: CallbackQuery, state: FSMContext):

    if call.data == 'yes':
        data = await state.get_data()
        delete_table(data.get('dictionary name'))
        await call.message.answer("Dictionary deleted successfully")  # TODO after this bot stops working
    else:
        await call.message.answer('Canceled')
        await state.finish()
