from aiogram.types import Message

from db import get_data
from . import dp, logger


@dp.message_handler(text='Show Learned')
async def show_learned_words(message: Message):

    logger.info('Showed learned words')

    words = get_data('learned', field='russian')
    text = "All learned words:\n"

    for word in words:
        text += word[0] + ', '
    text = text[:-2] + '.'
    await message.answer(text)
