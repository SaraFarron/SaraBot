from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor

from logging import basicConfig, getLogger, INFO
from os import environ
import asyncio
from dotenv import load_dotenv
from db import get_all_tables, create_table


basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=INFO)
logger = getLogger(__name__)
load_dotenv()
loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())


def on_startup():
    """Function that launches on startup"""

    tables = get_all_tables()

    if 'leaned' not in tables:
        create_table('learned', {'Russian': 'TEXT', 'English': 'TEXT'})
    if 'learning' not in tables:
        create_table('learning', {
            'Russian': 'TEXT', 'English': 'TEXT', 'times_learned': 'SMALLINT', 'date_last_learned': 'TIMESTAMP'}
                     )


if __name__ == '__main__':
    from handlers import dp
    on_startup()
    executor.start_polling(dp)
