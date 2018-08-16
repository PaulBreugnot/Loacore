import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import Sentence


def load_sentences(id_sentences=[], load_words=False, load_deptrees=False):
    """
    Load sentences from database.

    :param id_sentences:
        If specified, load only the sentences with corresponding ids. Otherwise, load all the sentences.
    :type id_sentences: :obj:`list` of :obj:`int`
    :param load_words: Specify if Words need to be loaded in sentences.
    :type load_words: boolean
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in sentences.
    :type load_deptrees: boolean
    :return: Loaded sentences
    :rtype: :obj:`list` of |Sentence|

    :Example:
        Load sentences 1,2 and their words.

        >>> import loacore.load.sentence_load as sentence_load
        >>> sentences = sentence_load.load_sentences([1,2], load_words=True)
        >>> sentences[0].sentence_str(print_sentence=False)
        'teleferico'
        >>> sentences[1].sentence_str(print_sentence=False)
        'toboganvy que el agua huela a asufre'


    """
    from loacore.conf import DB_TIMEOUT
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    sentences = []
    if len(id_sentences) > 0:
        for id_sentence in id_sentences:
            c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                      "WHERE ID_Sentence = " + str(id_sentence) + " ORDER BY Review_Index")
            result = c.fetchone()
            if result is not None:
                sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    else:
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree "
                  "FROM Sentence ORDER BY ID_Review, Review_Index")
        results = c.fetchall()
        for result in results:
            sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    if load_words:
        import loacore.load.word_load as word_load
        word_load.load_words_in_sentences(sentences)

    if load_deptrees:
        import loacore.load.deptree_load as deptree_load
        deptree_load.load_dep_tree_in_sentences(sentences)

    conn.close()
    return sentences


def load_sentences_by_id_files(id_files, load_words=True, load_deptrees=True):
    """

    Ids of files from which sentences should be loaded.

    :param id_files: Ids of files from which reviews should be loaded.
    :type id_files: :obj:`list` of :obj:`int`
    :param load_words: Specify if Words need to be loaded in sentences.
    :type load_words: boolean
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in sentences.
    :type load_deptrees: boolean
    :return: Loaded sentences
    :rtype: :obj:`list` of |Sentence|

    :Example:
    Load all the sentences from file 1.

    >>> import loacore.load.sentence_load as sentence_load
    >>> sentences = sentence_load.load_sentences_by_id_files([1])
    >>> sentences[0].sentence_str(print_sentence=False)
    'teleferico'

    """
    from loacore.conf import DB_TIMEOUT
    sentences = []
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    for id_file in id_files:
        c.execute("SELECT ID_Sentence, Sentence.ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                  "JOIN Review ON Sentence.ID_Review = Review.ID_Review "
                  "WHERE ID_File = " + str(id_file) + " ORDER BY Review_Index")
        results = c.fetchall()
        for result in results:
            sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    conn.close()

    if load_words:
        import loacore.load.word_load as word_load
        word_load.load_words_in_sentences(sentences)

    if load_deptrees:
        import loacore.load.deptree_load as deptree_load
        deptree_load.load_dep_tree_in_sentences(sentences)

    return sentences


def load_sentences_in_reviews(reviews, load_words=False, load_deptrees=False):
    """

    Load sentences into corresponding *reviews*, setting up their attribute :attr:`sentences`.\n
    Also return all the loaded sentences.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` or :func:`review_load.load_reviews()`
        when *load_sentences* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load reviews and sentences in one go.

    :param reviews: Reviews in which corresponding sentences should be loaded.
    :type reviews: :obj:`list` of |Review|
    :param load_words: Specify if Words need to be loaded in sentences.
    :type load_words: boolean
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in sentences.
    :type load_deptrees: boolean
    :return: Loaded sentences
    :rtype: :obj:`list` of |Sentence|
    """
    from loacore.conf import DB_TIMEOUT
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    loaded_sentences = []

    for review in reviews:
        review_sentences = []
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                  "WHERE ID_Review = " + str(review.id_review) + " ORDER BY Review_Index")
        results = c.fetchall()
        for result in results:
            review_sentences.append(Sentence(result[0], result[1], result[2], result[3]))
        review.sentences = review_sentences
        loaded_sentences += review_sentences

    conn.close()

    if load_words:
        import loacore.load.word_load as word_load
        word_load.load_words_in_sentences(loaded_sentences)

    if load_deptrees:
        import loacore.load.deptree_load as deptree_load
        deptree_load.load_dep_tree_in_sentences(loaded_sentences)

    return loaded_sentences

