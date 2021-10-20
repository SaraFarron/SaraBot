from aiogram.types import Message, ReplyKeyboardRemove

from db import get_all_tables
from . import dp, logger


@dp.message_handler(text='Show All Dictionaries')
async def show_all_dictionaries(message: Message):

    logger.info('Showed all dictionaries')
    dictionaries = get_all_tables()
    text = "Here is all your dictionaries:\n"

    for dictionary in dictionaries:
        text += f"{dictionary}, "
    text = text[:-2] + '.'

    await message.answer(text, reply_markup=ReplyKeyboardRemove())
