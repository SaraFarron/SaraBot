from db import (
    create_table, add_row, update_row,
    delete_row, get_data, is_table)

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor

from logging import basicConfig, getLogger, INFO
from dotenv import load_dotenv
from os import environ
import asyncio


def bot():
    basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=INFO)
    logger = getLogger(__name__)
    load_dotenv()

    loop = asyncio.get_event_loop()
    bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
    dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

    executor.start_polling(dp)


if __name__ == '__main__':
    bot()
