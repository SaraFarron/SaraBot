from aiogram.types import Message, ReplyKeyboardRemove

from . import dp, logger
from db import get_data


@dp.message_handler(state='*', commands=['learn'])
@dp.message_handler(lambda message: message.text.lower() == 'learn', state='*')
async def learn_new(message: Message):

    logger.info('Started learning')

    get_data('learning', order_by='date_last_learned')
    await message.answer('Looking for words that you need to learn', reply_markup=ReplyKeyboardRemove())

#     TODO


def writing_test(russian: str, english: str):
    """A test in which user needs to write correct translation"""
    pass


def choose_right_test(russian: str, english: str, wrong_russian: list[str, ], wrong_english: list[str, ]):
    """A test in which user needs to choose right translation"""
    pass
