import sqlite3 as sql
from loacore.conf import DB_PATH


def load_lemmas(id_lemmas=()):
    """

    Load lemmas from database.

    :param id_lemmas: If specified, load only the lemmas with corresponding ids. Otherwise, load all the lemmas.
    :type id_lemmas: :obj:`sequence` of :obj:`int`
    :return: loaded lemmas
    :rtype: :obj:`list` of :obj:`str`

    :Example:

    Load all lemmas from database.

    >>> import loacore.load.lemma_load as lemma_load
    >>> lemmas = lemma_load.load_lemmas()
    >>> print(len(lemmas))
    103827
    >>> print(lemmas[10])
    bailar

    """
    from loacore.conf import DB_TIMEOUT

    lemmas = []
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    if len(id_lemmas) > 0:
        for id_lemma in id_lemmas:
            c.execute("SELECT Lemma FROM Lemma WHERE ID_Lemma = '" + str(id_lemma) + "'")
            result = c.fetchone()
            if result is not None:
                lemmas.append(result[0])

    else:
        c.execute("SELECT Lemma FROM Lemma")
        results = c.fetchall()
        for result in results:
            lemmas.append(result[0])

    conn.close()
    return lemmas


def load_lemmas_in_words(words):
    """

    Load lemmas into corresponding *words*, setting up their attribute :attr:`lemma`.\n
    Also return all the loaded lemmas.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` when *load_words* is set to
        :obj:`True` or by :func:`word_load.load_words()` when *load_synsets* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load words and synsets in one go.

    :param words: Words in which corresponding synsets should be loaded.
    :type words: :obj:`list` of |Word|
    :return: loaded lemmas
    :rtype: :obj:`list` of :obj:`str`
    """
    from loacore.conf import DB_TIMEOUT

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    lemmas = []
    for word in words:
        if word.id_lemma is not None:
            c.execute("SELECT Lemma FROM Lemma WHERE ID_Lemma = '" + str(word.id_lemma) + "'")
            result = c.fetchone()
            word.lemma = result[0]
            lemmas.append(word.lemma)

    conn.close()

    return lemmas
