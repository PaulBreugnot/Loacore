import sqlite3 as sql
from loacore import DB_PATH
from loacore.classes.classes import Review


def load_reviews(id_reviews=[], load_sentences=False, load_words=False, load_deptrees=False):
    """

    Load :class:`Review` s from database.

    :param id_reviews: If specified, load only the reviews with corresponding ids. Otherwise, load all the reviews.
    :type id_reviews: :obj:`list` of :obj:`int`
    :param load_sentences: Specify if Sentences need to be loaded in :class:`Review` s.
    :type load_sentences: boolean
    :param load_words: If Sentences have been loaded, specify if Words need to be loaded in :class:`Sentence` s.
    :type load_words: boolean
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in :class:`Sentence` s.
    :type load_deptrees: boolean
    :return: Loaded reviews
    :rtype: :obj:`list` of :class:`Review` s

    :Example:
        Load all reviews with sentences and words

        >>> import loacore.load.review_load as review_load
        >>> reviews = review_load.load_reviews(load_sentences=True, load_words=True)
        >>> reviews[0].sentences[0].print_sentence(print_sentence=False)
        'teleferico'

    """
    reviews = []
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    if len(id_reviews) > 0:
        for id_review in id_reviews:
            c.execute("SELECT ID_Review, Review.ID_File, File_Index, Review "
                      "FROM Review WHERE ID_Review = " + str(id_review) + " ORDER BY File_Index")
            result = c.fetchone()
            if result is not None:
                reviews.append(Review(result[0], result[1], result[2], result[3]))
    else:
        c.execute("SELECT ID_Review, Review.ID_File, File_Index, Review FROM Review")
        results = c.fetchall()
        for result in results:
            reviews.append(Review(result[0], result[1], result[2], result[3]))

    conn.close()

    if load_sentences:
        # Load Sentences
        import loacore.database.load.sentence_load as sentence_load
        sentence_load.load_sentences_in_reviews(reviews, load_words=load_words, load_deptrees=load_deptrees)

    return reviews


def load_reviews_by_id_files(id_files, load_sentences=False, load_words=False, load_deptrees=False):
    """

    Load :class:`Review` s of files specified by their ids.

    :param id_files: Ids of files from which reviews should be loaded.
    :type id_files: :obj:`list` of :obj:`int`
    :param load_sentences: Specify if Sentences need to be loaded in :class:`Review` s.
    :type load_sentences: boolean
    :param load_words: If Sentences have been loaded, specify if Words need to be loaded in :class:`Sentence` s.
    :type load_words: boolean
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in :class:`Sentence` s.
    :type load_deptrees: boolean
    :return: Loaded reviews
    :rtype: :obj:`list` of :class:`Review` s

    :Example:

        Load reviews from the first file as "raw" reviews, without :class:`Sentence` s.

        >>> import loacore.load.review_load as review_load
        >>> reviews = review_load.load_reviews_by_id_files([1])
        >>> print(reviews[0].review)
        teleferico

    """
    reviews = []
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    for id_file in id_files:
        c.execute("SELECT ID_Review, ID_File, File_Index, Review "
                  "FROM Review WHERE ID_File = " + str(id_file) + " ORDER BY File_Index")
        results = c.fetchall()
        for result in results:
            reviews.append(Review(result[0], result[1], result[2], result[3]))

    conn.close()

    if load_sentences:
        # Load Sentences
        import loacore.load.sentence_load as sentence_load
        sentence_load.load_sentences_in_reviews(reviews, load_words=load_words, load_deptrees=load_deptrees)

    return reviews


def load_reviews_in_files(files, load_sentences=False, load_words=False, load_deptrees=False):
    """

    Load :class:`Review` s into corresponding *files*, setting up their attribute :attr:`reviews`.\n
    Also return all the loaded reviews.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` when *load_reviews* is set to
        :obj:`True`. In most of the cases, this function should be used to load files and reviews in one go.

    :param files: Files in which corresponding reviews will be loaded.
    :type files: :obj:`list` of :class:`File`
    :param load_sentences: Specify if Sentences need to be loaded in :class:`Review` s.
    :type load_sentences: boolean
    :param load_words: If Sentences have been loaded, specify if Words need to be loaded in :class:`Sentence` s.
    :type load_words: boolean
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in :class:`Sentence` s.
    :type load_deptrees: boolean
    :return: Loaded reviews
    :rtype: :obj:`list` of :class:`Review` s
    """
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    reviews = []

    for file in files:
        file_reviews = []
        c.execute("SELECT ID_Review, ID_File, File_Index, Review "
                  "FROM Review WHERE ID_File = " + str(file.id_file) + " ORDER BY File_Index")
        results = c.fetchall()
        for result in results:
            file_reviews.append(Review(result[0], result[1], result[2], result[3]))
        file.reviews = file_reviews
        reviews += file_reviews

    conn.close()

    if load_sentences:
        # Load Sentences
        import loacore.database.load.sentence_load as sentence_load
        sentence_load.load_sentences_in_reviews(reviews, load_words=load_words, load_deptrees=load_deptrees)

    return reviews


def count_reviews(file_path):
    from loacore import DB_PATH
    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count(ID_Review) FROM Review JOIN File ON Review.ID_File = File.ID_File "
              "WHERE File_Path = '" + file_path + "'")

    conn.close()
    return c.fetchone()[0]


