from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import menu
from . import dp
from . import logger


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """Allow user to cancel any action"""

    logger.info('Canceled stage')

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer('Canceled.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command('menu'))
async def send_menu(message: Message):
    """Menu, shows all bot functionality"""

    logger.info(f'sent menu to {message.from_user.username}')

    await message.answer("Please choose an action", reply_markup=menu)


@dp.message_handler(state='*', commands=['help'])
@dp.message_handler(lambda message: message.text.lower() == 'help', state='*')
async def help_command(message: Message):

    logger.info('Sent help')
    await message.answer(f"To get menu with all actions you can do type /menu\n"
                         f"If you want to upload a file with many words from google translator just send a file\n"
                         f"You can cancel any action type /cancel command\n"
                         f"This menu is called via /help command.")
