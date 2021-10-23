from aiogram.types import Message, ReplyKeyboardRemove

from . import dp, logger
from db import get_data


@dp.message_handler(state='*', commands=['learn'])
@dp.message_handler(lambda message: message.text.lower() == 'learn', state='*')
async def learn_new(message: Message):

    logger.info('Started learning')

    get_data('learning', order_by='date_last_learned')
#     TODO
