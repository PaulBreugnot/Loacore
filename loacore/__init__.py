import os

# FR_PATH = "/usr/local/share/"
# lang = "es"
# LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling", lang))

RESULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'database', 'reviews.db'))
RESOURCES_PATHS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

lang = ""
FR_PATH = ""
LANG_PATH = ""


def _load_conf():
    import sqlite3 as sql
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT lang, freeling_path FROM Configuration")
    result = c.fetchone()
    global FR_PATH
    FR_PATH = os.path.join(result[1].split('/'))
    global lang
    lang = result[0]
    global LANG_PATH
    LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling", lang))

    conn.close()


def set_lang(user_lang):
    """
    Set language used in Freeling.\n
    Possible values : 'as', 'ca', 'cy', 'de', 'en', 'es', 'fr', 'gl', 'hr', 'it', 'nb', 'pt', 'ru', 'sl'.
    :param user_lang: Freeling language
    :type user_lang: str
    """
    import sqlite3 as sql

    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM Configuration")
    c.execute("INSERT INTO Configuration (lang, freeling_path) VALUES (?, ?)", (user_lang, FR_PATH))

    conn.close()

    _load_conf()


def set_freeling_path(freeling_path):
    """
    Set Freeling path.
    :param freeling_path:
        Absolute path of the folder containing the *freeling* folder.\n
        The path must always be specified in the following format : */path/to/freeling* .
        Python will then automatically format it according to the current OS.
    :type freeling_path: :obj:`path-like object`
    """

    import sqlite3 as sql

    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM Configuration")
    c.execute("INSERT INTO Configuration (lang, freeling_path) VALUES (?, ?)", (lang, freeling_path))

    conn.close()

    _load_conf()


_load_conf()
