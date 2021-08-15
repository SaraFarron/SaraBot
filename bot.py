import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
from dotenv import load_dotenv
import sqlite3


load_dotenv()  # take environment variables from .env.

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def upload_file(update, context):
    pass


def add_word(update, context):
    pass


def learn(update, context):
    pass


def delete_word(update, context):
    pass


def edit_word(update, context):
    pass


def start(update, context):
    conn = sqlite3.connect('word.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE words (
        russian text,
        english text
    )""")  # TODO if sqlite3.OperationalError then dont create
    c.execute("INSERT INTO words VALUES ('go', 'идти')")

    conn.commit()
    conn.close()


    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(environ.get('BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
