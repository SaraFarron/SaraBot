from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

from main import bot, dp
from main import logger

from db import (
    create_table, add_row, update_row,
    delete_row, get_data, is_table)


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)
