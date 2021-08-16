import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
from dotenv import load_dotenv
from sqlite3 import connect
from sqlite3 import OperationalError

from word import Word


load_dotenv()  # take environment variables from .env.

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class dbopen(object):
    """
    Simple Context Manager for sqlite3 databases. Commits everything at exit.
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.conn = connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


def upload_file(update, context):
    pass


def add_word(update, context):
    russian = context.args[0]
    english = context.args[1]
    with dbopen('words.db') as c:
        c.execute("SELECT * FROM words WHERE russian=? AND english=?", (russian, english))
        if c.fetchone():
            update.message.reply_text('This word has been already added')
        else:
            word = Word(russian=russian, english=english)
            c.execute("INSERT INTO words VALUES (?, ?)", (word.russian, word.english))
            update.message.reply_text('Done!')


def learn(update, context):
    pass


def delete_word(update, context):
    with dbopen('words.db') as c:
        c.execute("DELETE FROM words WHERE english = :pattern OR russian = :pattern",
                  {'pattern': context.args[0]})
            # update.message.reply_text("No such word")
    update.message.reply_text("Deleted")


def edit_word(update, context):  # TODO create conversation instead of command
    with dbopen('words.db') as c:
        c.execute("""UPDATE words SET russian=:russian
                    WHERE english=:english""",
                  {'russian': context.args[0], 'english': context.args[1]})
            # update.message.reply_text("No such word")
    update.message.reply_text("Updated")


def show_db(update, context):
    with dbopen('words.db') as c:
        c.execute("SELECT * FROM words")
        update.message.reply_text(c.fetchall())


def start(update, context):
    with dbopen('words.db') as c:
        try:
            c.execute("""CREATE TABLE words (
                russian text,
                english text
            )""")
        except OperationalError:
            pass
        c.execute("INSERT INTO words VALUES ('идти', 'go')")
    update.message.reply_text('Done!')


def get_word(update, context):
    with dbopen('words.db') as c:
        c.execute("SELECT * FROM words WHERE english=:pattern OR russian=:pattern",
                  {'pattern': context.args[0]})
        update.message.reply_text(c.fetchall())


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


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
