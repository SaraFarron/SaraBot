import telegram
from os import environ


bot = telegram.Bot(token=environ.get('BOT_TOKEN'))
updates = bot.get_updates()
chat_id = updates[0].message.from_user.id
bot.send_message(text='hi', chat_id=chat_id)
