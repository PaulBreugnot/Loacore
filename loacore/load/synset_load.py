import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import Synset


def load_synsets(id_synsets=None):
    """
    Load |Synset| s from database.

    :param id_synsets: If specified, load only the synsets with corresponding ids. Otherwise, load all the synsets.
    :type id_synsets: :obj:`list` of |Word|
    :return: loaded synsets
    :rtype: :obj:`list` of |Synset|

    :Example:
    Load all synsets from database.

    >>> import loacore.load.synset_load as synset_load
    >>> synsets = synset_load.load_synsets()
    >>> print(synsets[0].synset_code)
    14845743-n
    >>> print(synsets[0].synset_name)
    water.n.01


    """
    from loacore.conf import DB_TIMEOUT

    synsets = []
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    if id_synsets is not None:
        for id_synset in id_synsets:
            c.execute("SELECT ID_Synset, ID_Word, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                      "FROM Synset WHERE ID_Synset = " + str(id_synset))
            result = c.fetchone()
            if result is not None:
                synsets.append(Synset(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
    else:
        c.execute("SELECT ID_Synset, ID_Word, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                  "FROM Synset")
        results = c.fetchall()
        for result in results:
            synsets.append(Synset(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    return synsets


def get_id_synsets_for_id_words(id_words):
    from loacore.conf import DB_TIMEOUT
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("SELECT Synset.ID_Synset "
              "FROM Synset "
              "JOIN Word ON Word.ID_Synset = Synset.ID_Synset "
              "WHERE Word.ID_Word IN " + str(tuple(id_words)))

    results = c.fetchall()
    id_synsets = []
    for result in results:
        id_synsets.append(result[0])

    return id_synsets


def load_synsets_in_words(words):
    """

    Load |Synset| s into corresponding *words*, setting up their attribute :attr:`synset`.\n
    Also return all the loaded synsets.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` when *load_words* is set to
        :obj:`True` or by :func:`word_load.load_words()` when *load_synsets* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load words and synsets in one go.

    :param words: Words in which corresponding synsets should be loaded.
    :type words: :obj:`list` of |Word|
    :return: loaded synsets
    :rtype: :obj:`list` of |Synset|
    """
    from loacore.conf import DB_TIMEOUT

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    synsets = []
    for word in words:
        if word.id_synset is not None:
            c.execute("SELECT ID_Synset, ID_Word, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                      "FROM Synset WHERE ID_Synset = " + str(word.id_synset))
            result = c.fetchone()
            word.synset = Synset(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
            synsets.append(word.synset)

    conn.close()

    return synsets


