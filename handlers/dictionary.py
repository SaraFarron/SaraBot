from aiogram.types import Message

from main import bot, dp
from main import logger
from keyboards import inline
from aiogram.dispatcher.filters import Command, Text


@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer("Here are your buttons", reply_markup=inline.inline_menu)


@dp.message_handler()
async def echo(message: Message):
    logger.info(f'echoed user {message.from_user.username}')
    await message.answer(text=message.text)  # Should do the same thing
