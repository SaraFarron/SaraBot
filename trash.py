# # --- handlers.py ---
#
# from app import bot, dp
# import logging
# from aiogram.types import (
#     Message, ReplyKeyboardMarkup, KeyboardButton,
#     ReplyKeyboardRemove, InlineKeyboardMarkup,
#     InlineKeyboardButton,
# )
# from aiogram.dispatcher.filters import Command, Text
#
# from dotenv import load_dotenv
# from os import environ
#
# load_dotenv()
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Keyboard buttons
# menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='create new dictionary'),
#             KeyboardButton(text='update dictionary'),
#         ],
#         [
#             KeyboardButton(text='delete dictionary'),
#             KeyboardButton(text='show dictionary'),
#         ],
#         [
#             KeyboardButton(text='show learned words'),
#             KeyboardButton(text='learn new words'),
#         ],
#     ],
#     resize_keyboard=True
# )
#
# # Inline buttons
# inline_menu = InlineKeyboardMarkup(
#     keyboard=[
#         [
#             InlineKeyboardButton(text='create new dictionary'),
#             InlineKeyboardButton(text='update dictionary'),
#         ],
#         [
#             InlineKeyboardButton(text='delete dictionary'),
#             InlineKeyboardButton(text='show dictionary'),
#         ],
#         [
#             InlineKeyboardButton(text='show learned words'),
#             InlineKeyboardButton(text='learn new words'),
#         ],
#     ],
#     resize_keyboard=True
# )
#
#
# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
#
#
# async def send_to_admin(dp):
#     await bot.send_message(chat_id=environ.get('my_id'), text="Bot is active")
#
#
# @dp.message_handler(Command('menu'))
# async def show_menu(message: Message):
#     await message.answer("Here are your buttons", reply_markup=menu)
#
#
# @dp.message_handler(Text(equals=['learn new words', 'show learned words',
#                                  'show dictionary', 'delete dictionary',
#                                  'create new dictionary', 'update dictionary']))
# async def get_menu_choice(message: Message):
#     await message.answer(f'You chose dis: {message.text}',
#                          reply_markup=ReplyKeyboardRemove())
#
#
# @dp.message_handler()
# async def echo(message: Message):
#     await bot.send_message(chat_id=message.from_user.id,
#                            text=message.text)
#     await message.answer(text=message.text)  # Should do the same thing
#
# # --- app.py ---
#
# from aiogram import Bot, Dispatcher, executor
# import asyncio
# from dotenv import load_dotenv
# from os import environ
#
#
# load_dotenv()
#
# loop = asyncio.get_event_loop()
# bot = Bot(environ.get('BOT_TOKEN'), parse_mode='HTML')
# dp = Dispatcher(bot, loop=loop)
#
#
# if __name__ == '__main__':
#     from handlers import dp, send_to_admin
#     executor.start_polling(dp, on_startup=send_to_admin)
