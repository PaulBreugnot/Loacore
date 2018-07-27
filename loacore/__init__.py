import os

RESULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'database', 'reviews.db'))

FR_PATH = "/usr/local/share/"
lang = "es"
LANG_PATH = FR_PATH + "freeling/" + lang + "/"


def set_lang(user_lang):
    global lang
    global LANG_PATH
    lang = user_lang
    LANG_PATH = FR_PATH + "freeling/" + lang + "/"
