from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from dotenv import load_dotenv
from sqlite3 import connect
from sqlite3 import OperationalError
from word import Word
import logging

load_dotenv()
logger = logging.getLogger(__name__)

MENU, LEARN, LEARNED_WORDS, \
NEW_DICTIONARY, UPDATE_DICTIONARY, DEL_DICTIONARY, \
GET_DICTIONARY, ADD_WORDS = range(8)


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


def start(update, _):
    reply_keyboard = [
        [
            'learn new words',
            'show learned words',
            'create new dictionary',
            'update dictionary',
            'delete dictionary',
            'show dictionary',
        ]
    ]

    markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
    update.message.reply_text(
        'Hello! I am helping people to improve their vocabulary in english.'
        '/cancel <- command to undo current conversation. Works anytime!',
        reply_markup=markup_key)

    return MENU


def start_buttons(update, _):
    pass


def learn(update, _):
    pass


def learned_words(update, _):
    with dbopen('words.db') as c:
        c.execute("SELECT * FROM learned_words")
        update.message.reply_text(c.fetchall())

    return MENU


def get_dictionary_name(update, _):
    update.message.reply_text('Enter dictionary name')
    return NEW_DICTIONARY


def new_dictionary(update, _):
    name = update.message.text
    with dbopen('words.db') as c:
        try:
            c.execute("""CREATE TABLE :name (
                russian text,
                english text
            )""", {'name': name})
        except OperationalError:
            update.message.reply_text('Dictionary names must be unique')
            return MENU

    update.message.reply_text('Done!')
    return ADD_WORDS


def add_words(update, context):  # TODO fix
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


def update_dictionary(update, _):
    pass


def delete_dictionary(update, _):  # TODO add confirmation
    name = update.message.text
    with dbopen('words.db') as c:
        c.execute("DROP TABLE :name", {'name': name})
        update.message.reply_text('Done!')

    return MENU


def get_dictionary(update, _):
    name = update.message.text
    with dbopen('words.db') as c:
        c.execute("SELECT * FROM :name", {'name': name})
        update.message.reply_text(c.fetchall())

    return MENU


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# def delete_word(update, context):
#     with dbopen('words.db') as c:
#         c.execute("DELETE FROM words WHERE english = :pattern OR russian = :pattern",
#                   {'pattern': context.args[0]})
#             # update.message.reply_text("No such word")
#     update.message.reply_text("Deleted")
#
#
# def edit_word(update, context):  # TODO create conversation instead of command
#     with dbopen('words.db') as c:
#         c.execute("""UPDATE words SET russian=:russian
#                     WHERE english=:english""",
#                   {'russian': context.args[0], 'english': context.args[1]})
#             # update.message.reply_text("No such word")
#     update.message.reply_text("Updated")
#
#
# def show_db(update, context):
#     with dbopen('words.db') as c:
#         c.execute("SELECT * FROM words")
#         update.message.reply_text(c.fetchall())
#
#
# def get_word(update, context):
#     with dbopen('words.db') as c:
#         c.execute("SELECT * FROM words WHERE english=:pattern OR russian=:pattern",
#                   {'pattern': context.args[0]})
#         update.message.reply_text(c.fetchall())
#
#
# def echo(update, context):
#     update.message.reply_text(update.message.text)
#
#
