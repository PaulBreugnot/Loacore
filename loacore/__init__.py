import os

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', 'data', 'database', 'reviews.db'))

FR_PATH = "/usr/local/share/"
lang = "es"
LANG_PATH = FR_PATH + "freeling/" + lang + "/"