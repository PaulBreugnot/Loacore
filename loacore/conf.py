import os


def check_db():
    if not os.path.exists(DB_PATH):
        import loacore.utils.db as db
        print("No database available. A new database will be downloaded.")
        db.download_db(db_name="new", forced=True)


RESULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'results'))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
DB_PATH = os.path.abspath(os.path.join(DATA_PATH, 'database', 'reviews.db'))
check_db()
RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

MAX_DB_COMMIT_ATTEMPTS = 20
DB_TIMEOUT = 180
DB_ERROR_TIMEOUT = 10

lang = ""
FR_PATH = ""
LANG_PATH = ""
CURRENT_CONF_NAME = ""


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
    c.execute("UPDATE Configuration (lang, freeling_path) = (?, ?) WHERE config_name = '" + CURRENT_CONF_NAME + "'",
              (user_lang, FR_PATH))

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
        Absolute path of the folder containing the *freeling* folder.
    :type freeling_path: |path-like-object|
    """

    import sqlite3 as sql

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    print("Updating Configuration...")
    c.execute("DELETE FROM Configuration")
    c.execute("INSERT INTO Configuration SET (lang, freeling_path) VALUES (?, ?)", (lang, freeling_path))

    conn.commit()
    print("Done.")
    conn.close()

    _load_conf()


def check_freeling_path():
    """
    :return: Current *freeling_path*.
    """
    return FR_PATH


def set_result_path(result_path):
    """
    Set result path. A new folder will be created if it doesn't exist.
    Changes are permanent, until the next call to :func:`~loacore.conf.set_result_path`.\n

    :param result_path:
        Absolute path of the folder containing the *result* folder.
    :type result_path: |path-like-object|
    """
    import sqlite3 as sql

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    print("Updating Configuration...")
    c.execute("UPDATE Configuration SET result_path = ? WHERE config_name = '" + CURRENT_CONF_NAME + "'",
              (result_path, ))

    conn.commit()
    print("Done.")
    conn.close()

    _load_conf()


def check_result_path():
    """
    :return: Current *result_path*
    """
    return RESULT_PATH


def set_output_path(output_path):
    """
    Set output path. A new folder will be created if it doesn't exist.
    Changes are permanent, until the next call to :func:`~loacore.conf.set_output_path`.\n

    :param output_path:
        Absolute path of the folder containing the *result* folder.
    :type output_path: |path-like-object|
    """
    import sqlite3 as sql

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    print("Updating Configuration...")
    c.execute("UPDATE Configuration SET output_path = ? WHERE config_name = '" + CURRENT_CONF_NAME + "'",
              (output_path, ))

    conn.commit()
    print("Done.")
    conn.close()

    _load_conf()


def check_output_path():
    """
    :return: Current *output_path*
    """
    return OUTPUT_PATH


def set_data_path(data_path):
    """
    Set data path. A new folder will be created if it doesn't exist.
    Changes are permanent, until the next call to :func:`~loacore.conf.set_data_path`.\n

    :param data_path:
        Absolute path of the folder containing the *result* folder.
    :type data_path: |path-like-object|
    """
    # Tricky one, because the program will still need to read the default database at initialization.

    import sqlite3 as sql
    import shutil
    from loacore.utils.db import database_backup
    from loacore.load.file_load import clean_db

    if not os.path.exists(os.path.join(data_path, "database")):
        os.makedirs(os.path.join(data_path, "database"))

    with database_backup():
        conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
        c = conn.cursor()
        print("Updating Configuration...")
        c.execute("UPDATE Configuration SET data_path = ? WHERE config_name = '" + CURRENT_CONF_NAME + "'",
                  (data_path,))

        conn.commit()
        print("Done.")
        conn.close()

        new_db_path = os.path.abspath(os.path.join(data_path, 'database', 'reviews.db'))

        shutil.copyfile(DB_PATH, new_db_path)

        # Delete everything except Configuration in initialization database
        clean_db()

        # New data paths will be loaded
        _load_conf()


def check_data_path():
    """
    :return: Current *data_path*
    """
    return DATA_PATH


def set_external_conf(folder_path):
    """
    Set a path for all external data/output, creating *result*, *output* and *data* folders at the specified path.
    Configuration is updated calling :func:`~loacore.conf.set_result_path`, :func:`~loacore.conf.set_output_path` and
    :func:`~loacore.conf.set_data_path`.

    :param folder_path:
        Absolute path of the folder containing the *result*, *output* and *data* folders.
    :type data_path: |path-like-object|
    """
    set_result_path(os.path.join(folder_path, "result"))
    set_output_path(os.path.join(folder_path, "output"))
    set_data_path(os.path.join(folder_path, "data"))


def _load_conf(config_name=None):
    global CURRENT_CONF_NAME
    if config_name is None:
        import platform
        if platform.system() == "Windows":
            config_name = "windows_default"
        else:
            config_name = "linux_default"

    CURRENT_CONF_NAME = config_name
    _load_external_conf(config_name)
    _load_freeling_conf(config_name)

    print("Freeling path : " + check_freeling_path())
    print("Default language : " + check_lang())
    print("Data path : " + check_data_path())
    print("Result path : " + check_result_path())
    print("Output path : " + check_output_path())


def _load_freeling_conf(config_name):
    import sqlite3 as sql
    import platform
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("SELECT lang, freeling_path FROM Configuration WHERE config_name = '" + config_name + "'")
    result = c.fetchone()
    global FR_PATH
    FR_PATH = result[1]
    # if platform.system() == "Windows":
    #     # C:\ management (otherwise, we get C:foo)
    #     result[1][1] = "\\" + result[1][1]
    #     list_path = result[1].split('\\')
    #     FR_PATH = ""
    # else:
    #     list_path = result[1].split('/')
    #     FR_PATH = "/"
    # for path in list_path:
    #     FR_PATH = os.path.join(FR_PATH, path)

    global lang
    lang = result[0]
    global LANG_PATH
    LANG_PATH = os.path.join(FR_PATH, "freeling", lang)

    conn.close()


def _load_external_conf(config_name):

    # If external configuration information are found in the current database, global variable at the header of this
    # file are redefined.
    # Otherwise, default configuration defined in the header is used.

    import sqlite3 as sql
    # import platform
    global DB_PATH

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("SELECT result_path, data_path, output_path FROM Configuration WHERE config_name = '" + config_name + "'")
    result = c.fetchone()
    if result[0] is not None:
        global RESULT_PATH
        RESULT_PATH = result[0]

    if result[1] is not None:
        global DATA_PATH
        DATA_PATH = result[1]
        DB_PATH = os.path.join(DATA_PATH, 'database', 'reviews.db')

    if result[2] is not None:
        global OUTPUT_PATH
        OUTPUT_PATH = result[2]

    # if platform.system() == "Windows":
    #     split_char = "\\"
    #     # C:\ management (otherwise, we get C:foo)
    #     result[0][1] = "\\" + result[0][1]
    #     result[1][1] = "\\" + result[1][1]
    #     result[2][1] = "\\" + result[2][1]
    # else:
    #     split_char = "/"
    #
    # if result[0] is not None:
    #     global RESULT_PATH
    #     RESULT_PATH = ""
    #     for path in result[0].split(split_char):
    #         RESULT_PATH = os.path.join(RESULT_PATH, path)
    #
    # if result[1] is not None:
    #     global DATA_PATH
    #     DATA_PATH = ""
    #     for path in result[1].split(split_char):
    #         DATA_PATH = os.path.join(DATA_PATH, path)
    #         print("Loaded datapath : " + str(DATA_PATH))
    #
    #     DB_PATH = os.path.join(DATA_PATH, 'database', 'reviews.db')
    #     print("Resulting db path : " + str(DB_PATH))
    #
    # if result[2] is not None:
    #     global OUTPUT_PATH
    #     OUTPUT_PATH = ""
    #     for path in result[2].split(split_char):
    #         OUTPUT_PATH = os.path.join(OUTPUT_PATH, path)


def _set_temp_lang(temp_lang):
    global lang
    lang = temp_lang
    global LANG_PATH
    LANG_PATH = os.path.abspath(os.path.join(FR_PATH, "freeling", lang))

