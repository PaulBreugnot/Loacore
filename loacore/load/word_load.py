import sqlite3 as sql
from loacore import DB_PATH
from loacore.classes.classes import Word


def load_words(id_words=[], load_lemmas=True, load_synsets=True):
    """

    Load :class:`Word` s from database.

    :param id_words: If specified, load only the words with corresponding ids. Otherwise, load all the words.
    :type id_words: :obj:`list` of :obj:`int`
    :param load_lemmas: Specify if Lemmas need to be loaded in :class:`Word` s.
    :type load_lemmas: boolean
    :param load_synsets: Specify if Synsets need to be loaded in :class:`Word` s.
    :type load_synsets: boolean
    :return: loaded words
    :rtype: :obj:`list` of :class:`Word`

    :Example:
        Load all words and their lemmas, synsets.

        >>> import loacore.load.word_load as word_load
        >>> words = word_load.load_words()
        >>> print([w.word for w in words[0:11]])
        ['teleferico', 'toboganvy', 'que', 'el', 'agua', 'huela', 'a', 'asufre', 'pista', 'de', 'baile']
        >>> print([w.lemma for w in words[0:11]])
        ['', '', 'que', 'el', 'agua', 'oler', 'a', '', 'pista', 'de', 'bailar']

    """
    words = []
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    if len(id_words) > 0:
        for id_word in id_words:
            c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag FROM Word "
                      "WHERE ID_Word = " + str(id_word) + " ORDER BY Sentence_Index")
            result = c.fetchone()
            if result is not None:
                words.append(Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
    else:
        c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag FROM Word")

        results = c.fetchall()
        for result in results:
            words.append(Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    if load_lemmas:
        import loacore.load.lemma_load as db_lemma_api
        db_lemma_api.load_lemmas_in_words(words)
    if load_synsets:
        import loacore.load.synset_load as db_synset_api
        db_synset_api.load_synsets_in_words(words)

    conn.close()
    return words


def load_words_in_sentences(sentences, load_lemmas=True, load_synsets=True):
    """

    Load :class:`Word` s into corresponding *sentences*, setting up their attribute :attr:`words`.\n
    Also return all the loaded words.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` or
        :func:`sentence_load.load_sentences()` when *load_words* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load sentences and words in one go.

    :param sentences: Sentences in which corresponding words should be loaded.
    :type sentences: :obj:`list` of :class:`Sentence`
    :param load_lemmas: Specify if Lemmas need to be loaded in :class:`Word` s.
    :type load_lemmas: boolean
    :param load_synsets: Specify if Synsets need to be loaded in :class:`Word` s.
    :type load_synsets: boolean
    :return: loaded words
    :rtype: :obj:`list` of :class:`Word`
    """

    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    words = []
    for sentence in sentences:
        sentence_words = []
        c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag "
                  "FROM Word "
                  "WHERE ID_Sentence = " + str(sentence.id_sentence) + " ORDER BY Sentence_Index")
        results = c.fetchall()
        for result in results:
            sentence_words.append(Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
        sentence.words = sentence_words
        words += sentence_words

    if load_lemmas:
        import loacore.load.lemma_load as db_lemma_api
        db_lemma_api.load_lemmas_in_words(words)
    if load_synsets:
        import loacore.load.synset_load as db_synset_api
        db_synset_api.load_synsets_in_words(words)

    conn.close()

    return words


def load_words_in_dep_trees(dep_trees, load_lemmas=True, load_synsets=True):
    """

    Load :class:`Word` s into corresponding *dep_trees*, setting up the attribute :attr:`word` of each node.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` when *load_deptrees* is set to
        :obj:`True`, or by :func:`dep_tree.load_deptrees()` when *load_words* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load dep_trees and words in one go.

    :param dep_trees: DepTrees in which corresponding words should be loaded.
    :type dep_trees: :obj:`list` of :class:`DepTree`
    :param load_lemmas: Specify if Lemmas need to be loaded in :class:`Word` s.
    :type load_lemmas: boolean
    :param load_synsets: Specify if Synsets need to be loaded in :class:`Word` s.
    :type load_synsets: boolean
    """

    def rec_children(c, node, words):
        c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag "
                  "FROM Word WHERE ID_Word = " + str(node.id_word))
        result = c.fetchone()
        node.word = Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        words.append(node.word)

        for node in node.children:
            rec_children(c, node, words)

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    words = []
    for dep_tree in dep_trees:
        rec_children(c, dep_tree.root, words)

    if load_lemmas:
        import loacore.load.lemma_load as db_lemma_api
        db_lemma_api.load_lemmas_in_words(words)
    if load_synsets:
        import loacore.load.synset_load as db_synset_api
        db_synset_api.load_synsets_in_words(words)

    conn.close()

