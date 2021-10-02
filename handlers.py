from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

from app import bot, dp
from app import logger


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)
