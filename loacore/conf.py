import os

RESULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'database', 'reviews.db'))
RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

MAX_DB_COMMIT_ATTEMPTS = 20
DB_TIMEOUT = 180
DB_ERROR_TIMEOUT = 10

lang = ""
FR_PATH = ""
LANG_PATH = ""


def set_lang(user_lang):
    """
    Set default language used in Freeling.\n
    Changes are permanent, until the next call to :func:`~loacore.conf.set_lang`.\n
    Possible values : 'as', 'ca', 'cy', 'de', 'en', 'es', 'fr', 'gl', 'hr', 'it', 'nb', 'pt', 'ru', 'sl'.

    :param user_lang: Freeling language
    :type user_lang: str
    """
    import sqlite3 as sql

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    print("Updating Configuration...")
    c.execute("DELETE FROM Configuration")
    c.execute("INSERT INTO Configuration (lang, freeling_path) VALUES (?, ?)", (user_lang, FR_PATH))

    conn.commit()
    print("Done.")
    conn.close()

    _load_conf()


def check_lang():
    """
    Return current *lang*.
    """
    return lang


def set_freeling_path(freeling_path):
    """
    Set Freeling path.
    Changes are permanent, until the next call to :func:`~loacore.conf.set_freeling_path`.\n

    :param freeling_path:
        Absolute path of the folder containing the *freeling* folder.\n
        :example:
            .. code-block:: console

                /usr/local/share/

        The path must always be specified in the following format : */path/to/freeling* .
        Python will then automatically format it according to the current OS.
    :type freeling_path: |path-like-object|
    """

    import sqlite3 as sql

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    print("Updating Configuration...")
    c.execute("DELETE FROM Configuration")
    c.execute("INSERT INTO Configuration (lang, freeling_path) VALUES (?, ?)", (lang, freeling_path))

    conn.commit()
    print("Done.")
    conn.close()

    _load_conf()


def check_freeling_path():
    """
    Return current *freeling_path*.
    """
    return FR_PATH


def _load_conf(config_name=None):
    if config_name is None:
        import platform
        if platform.system() == "Windows":
            config_name = "windows_default"
        else:
            config_name = "linux_default"

    _load_external_conf(config_name)
    _load_freeling_conf(config_name)


def _load_freeling_conf(config_name):
    import sqlite3 as sql
    import platform
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("SELECT lang, freeling_path FROM Configuration WHERE config_name = '" + config_name + "'")
    result = c.fetchone()
    global FR_PATH
    if platform.system() == "Windows":
        list_path = result[1].split('\\')
        FR_PATH = ""
    else:
        list_path = result[1].split('/')
        FR_PATH = "/"
    for path in list_path:
        FR_PATH = os.path.abspath(os.path.join(FR_PATH, path))

    global lang
    lang = result[0]
    global LANG_PATH
    LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling", lang))

    conn.close()


def _load_external_conf(config_name):

    # If external configuration information are found in the current database, global variable at the header of this
    # file are redefined.
    # Otherwise, default configuration defined in the header is used.

    import sqlite3 as sql
    import platform
    global DB_PATH

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("SELECT result_path, data_path, output_path FROM Configuration WHERE config_name = '" + config_name + "'")
    result = c.fetchone()
    if result[0] is not None:
        global RESULT_PATH
        if platform.system() == "Windows":
            RESULT_PATH = os.path.join(result[0].split("\\"))
        else:
            RESULT_PATH = os.path.join(result[0].split("/"))

    if result[1] is not None:
        global DATA_PATH
        if platform.system() == "Windows":
            DATA_PATH = os.path.join(result[1].split("\\"))
        else:
            DATA_PATH = os.path.join(result[1].split("/"))

        DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'database', 'reviews.db'))

    if result[2] is not None:
        global OUTPUT_PATH
        if platform.system() == "Windows":
            OUTPUT_PATH = os.path.join(result[2].split("\\"))
        else:
            OUTPUT_PATH = os.path.join(result[2].split("/"))


def _set_temp_lang(temp_lang):
    global lang
    lang = temp_lang
    global LANG_PATH
    LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling", lang))

