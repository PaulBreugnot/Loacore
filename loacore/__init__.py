import os

RESULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'database', 'reviews.db'))
RESOURCES_PATHS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

FR_PATH = "/usr/local/share/"
lang = "es"
LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling", lang))


def set_lang(user_lang):
    """
    Set language used in Freeling.\n
    Possible values : 'as', 'ca', 'cy', 'de', 'en', 'es', 'fr', 'gl', 'hr', 'it', 'nb', 'pt', 'ru', 'sl'.
    :param user_lang: Freeling language
    :type user_lang: str
    """
    global lang
    global LANG_PATH
    lang = user_lang
    LANG_PATH = FR_PATH + "freeling/" + lang + "/"


def set_freeling_path(freeling_path):
    """
    Set Freeling path.
    :param freeling_path: Absolute path of the folder containing the *freeling* folder.
    :type freeling_path: :obj:`path-like object`
    """
    global FR_PATH
    global LANG_PATH
    FR_PATH = freeling_path
    LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling/", lang))
