import logging
from telegram.ext import (
    Updater, CommandHandler,
    MessageHandler, Filters,
    ConversationHandler, RegexHandler)
from os import environ
from dotenv import load_dotenv
from logic import (
    start, start_buttons,
    learn, learned_words,
    new_dictionary, update_dictionary,
    delete_dictionary, get_dictionary,
    get_dictionary_name,
    error)

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MENU, LEARN, LEARNED_WORDS, \
NEW_DICTIONARY, UPDATE_DICTIONARY, DEL_DICTIONARY, \
GET_DICTIONARY, ADD_WORDS = range(8)


def main():
    updater = Updater(environ.get('BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[ConversationHandler('start', start)],
        states={
            MENU: [RegexHandler(
                '^(learn new words)$',
                learn,
                pass_user_data=True),
                RegexHandler(
                    '^(show learned words)$',
                    learned_words,
                    pass_user_data=True),
                RegexHandler(
                    '^(create new dictionary)$',
                    get_dictionary_name,
                    pass_user_data=True),
                RegexHandler(
                    '^(update dictionary)$',
                    update_dictionary,
                    pass_user_data=True),
                RegexHandler(
                    '^(delete dictionary)$',
                    delete_dictionary,
                    pass_user_data=True),
                RegexHandler(
                    '^(show dictionary)$',
                    get_dictionary,
                    pass_user_data=True),
            ],
            LEARN: [],
            NEW_DICTIONARY: [MessageHandler(Filters.text,
                                            new_dictionary,
                                            pass_user_data=True)
                             ],
            UPDATE_DICTIONARY: [ConversationHandler()
                                ],
            DEL_DICTIONARY: [MessageHandler(Filters.text,
                                            delete_dictionary,
                                            pass_user_data=True)
                             ],
            GET_DICTIONARY: [MessageHandler(Filters.text,
                                            get_dictionary,
                                            pass_user_data=True)
                             ],
            ADD_WORDS: [],

        }
    )

    dp.add_handler(conv_handler)

    # dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
