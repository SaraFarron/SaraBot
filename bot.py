import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
from dotenv import load_dotenv
from logic import (
    start, show_db, add_word,
    delete_word, edit_word,
    get_word, echo, error
                   )


load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SEARCH_FOR_WORD, GET_NEW_WORD = range(2)


def main():
    updater = Updater(environ.get('BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showdb", show_db))
    dp.add_handler(CommandHandler("add", add_word))
    dp.add_handler(CommandHandler("delete", delete_word))
    dp.add_handler(CommandHandler("update", edit_word))
    dp.add_handler(CommandHandler("get", get_word))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
