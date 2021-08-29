from aiogram import Bot, Dispatcher, executor
import asyncio
import logging
from dotenv import load_dotenv
from os import environ


load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()
bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)
