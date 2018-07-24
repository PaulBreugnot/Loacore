import sqlite3 as sql
from loacore import DB_PATH
from loacore.classes.classes import File


def _load_files_by_id_files(id_files):

    # Load files with specified ids, only initialized with id_file and file_path

    files = []
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    for id_file in id_files:
        c.execute("SELECT ID_File, File_Path FROM File WHERE ID_File = " + str(id_file))
        result = c.fetchone()
        if result is not None:
            files.append(File(result[0], result[1]))

    conn.close()
    return files


def _load_files():

    # Load all the files of the database, only initialized with id_file and file_path

    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Path FROM File")

    files = []
    results = c.fetchall()
    for result in results:
        files.append(File(result[0], result[1]))

    conn.close()
    return files


def load_database(id_files=[], load_reviews=True, load_sentences=True, load_words=True, load_deptrees=True):
    """
    Load the complete database as a :obj:`list` of :class:`File` , with all the dependencies specified in parameters
    loaded in them.

    :param id_files: If specified, load only the files with the corresponding ids. Otherwise, load all the files.
    :param load_reviews: Specify if Reviews need to be loaded if :class:`File` s.
    :param load_sentences: If Reviews have been loaded, specify if Sentences need to be loaded in :class:`Review` s.
    :param load_words: If Sentences have been loaded, specify if Words need to be loaded in :class:`Sentence` s.
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in :class:`Sentence` s.
    :return: loaded files
    :rtype: :obj:`list` of :class:`File`

    .. note::
        Among the dependencies, only the load_deptrees should be set to False to significantly reduce processing
        time if they are not needed. Loading other structures is quite fast.

    :Example:
        Load files 1,2,3 with only their :attr:`id_file` and :attr:`id_path`.

        >>> import loacore.load.file_load as file_load
        >>> files = file_load.load_database(id_files=[1, 2, 3], load_reviews=False)
        >>> print([f.file_path for f in files])
        ['../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_EO.txt',
        '../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_CC.txt',
        '../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_GR.txt']

    :Example:
        Load the first 10 files without :class:`DepTree` s.

        >>> import loacore.load.file_load as file_load
        >>> files = load_database(id_files=range(1, 11), load_deptrees=False)
        >>> print(files[3].reviews[8].review)
        que sea mas grande el parqueadero

    :Example:
        Load the complete database.

        >>> import loacore.load.file_load as file_load
        >>> files = load_database()
        >>> print(len(files))
        33

    """

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    # Load Files
    if len(id_files) == 0:
        files = _load_files()
    else:
        files = _load_files_by_id_files(id_files)

    if load_reviews:
        # Load Reviews
        import loacore.load.review_load as review_load
        reviews = review_load.load_reviews_in_files(files)

        if load_sentences:
            # Load Sentences
            import loacore.load.sentence_load as sentence_load
            sentences = sentence_load.load_sentences_in_reviews(reviews)

            if load_words:
                # Load Words
                import loacore.load.word_load as word_load
                word_load.load_words_in_sentences(sentences)

                if load_deptrees:
                    # Load DepTrees
                    import loacore.load.deptree_load as deptree_load
                    deptree_load.load_dep_tree_in_sentences(sentences)

    return files


def get_id_files_by_file_paths(file_paths_re):
    """
    This function can be used to retrieve file ids in database from their path.\n
    All the regular expression in the ** argument list** will be checked.\n
    For more information about how Python regular expressions work, see https://docs.python.org/3/library/re.html .

    :param file_paths_re: Regular expressions to check
    :type file_paths_re: :obj:`list` of :obj:`string`
    :return: Ids of matching files.
    :rtype: :obj:`list` of :obj:`int`

    :Example:
    Find if files of files in an uci folder.

        >>> import loacore.load.file_load as file_load
        >>> ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
        >>> print(ids)
        [1, 2, 3]

    .. note::

        The full path of a file (as saved in the database) can be used as a regular expression.

    """
    import re

    id_files = []
    files = load_database(load_reviews=False, load_sentences=False, load_words=False, load_deptrees=False)
    for file_path_re in file_paths_re:
        for file in files:
            regexp = file_path_re
            if re.fullmatch(regexp, file.file_path) is not None:
                id_files.append(file.id_file)

    return list(set(id_files))


def remove_files(files):
    """
    Remove specified files from database. Implemented references will also engender the deletion of all files
    dependencies in database.

    :param files: :obj:`list` of :class:`File`
    """
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = on")
    for file in files:
        c.execute("DELETE FROM File WHERE File_Path = '" + file.file_path + "'")

    conn.commit()
    conn.close()


def clean_db():
    """
    Remove all files from database. Implemented references will also engender the deletion of all files
    dependencies in database : all the tables will be emptied.
    """
    print("Cleaning all database...")
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM File")
    c.execute("DELETE FROM Review")
    c.execute("DELETE FROM Sentence")
    c.execute("DELETE FROM Word")
    c.execute("DELETE FROM Synset")
    c.execute("DELETE FROM Lemma")
    c.execute("DELETE FROM Dep_Tree")
    c.execute("DELETE FROM Dep_Tree_Node")
    c.execute("DELETE FROM Dep_Tree_Node_Children")
    conn.commit()
    conn.close()


