from aiogram.types import Message, ReplyKeyboardRemove

from . import dp, logger


@dp.message_handler(state='*', commands=['learn'])
@dp.message_handler(lambda message: message.text.lower() == 'learn', state='*')
async def learn_new(message: Message):

    logger.info('Started learning')

    await message.answer('Canceled.', reply_markup=ReplyKeyboardRemove())
