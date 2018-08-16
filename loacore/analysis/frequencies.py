from loacore.conf import DB_PATH
import sqlite3 as sql

##############################
# Dependency Label Frequencies
##############################

# ------
# Simple
# ------


def label_frequencies(files):
    """
    Compute simple dependency label frequencies if files.\n
    Results are returned in a dictionary that map file names to frequencies. \n
    Frequencies are represented has dictionaries that map dependency labels to frequencies. \n
    A list of dependency labels is also returns. \n

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :return: Dependency labels, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`str` , :obj:`dict` of :obj:`str` : :obj:`dict` of :obj:`str` : :obj:`float`

    :Example:

        Compute simple label frequencies of uci files.

        .. code-block: Python

            import loacore.load.file_load as file_load
            import loacore.analysis.frequencies as frequencies

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            files = file_load.load_database(id_files=ids, load_reviews=False)
            labels, frequencies = frequencies.label_frequencies(files)

    """
    from collections import OrderedDict
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    frequencies = {}
    labels = get_label_set(files, c)
    for file in files:
        freq = {}
        for label in labels:
            freq[label] = count_label(file, label, c)
        freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))
        total = sum(freq.values())
        freq = {k: freq[k]/total for k in freq.keys()}
        frequencies[file.get_filename()] = freq

    conn.close()
    return labels, frequencies


def get_label_set(files, c):
    """
    Returns all the existing dependency labels in files, through a SQL request.\n

    .. note ::

         For a more efficient call from :func:`label_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param files: Files to process. Notice that only the id_files are needed.
    :type files: :obj:`list` of |File|
    :param c: SQL cursor
    :return: Dependency labels
    :rtype: :obj:`list` of :obj:`str`
    """
    ids = tuple(f.id_file for f in files)
    c.execute("SELECT Label "
              "FROM Dep_Tree JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Review.ID_Review = Sentence.ID_Review "
              "JOIN Dep_Tree_Node ON Dep_Tree.ID_Dep_Tree = Dep_Tree_Node.ID_Dep_Tree "
              "WHERE Review.ID_File IN " + str(ids) + " GROUP BY Label")
    results = c.fetchall()
    return [result[0] for result in results]


def count_label(file, label, c):
    """
    Count the number of occurrence of *label* if all the dependency trees of *file*, through an SQL request.

    .. note ::

         For a more efficient call from :func:`label_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param file: File to process
    :type file: |File|
    :param label: Dependency label
    :type label: str
    :param c: SQL cursor
    :return: Number of label occurrences
    :rtype: int
    """
    c.execute("SELECT COUNT(*) FROM Dep_Tree "
              "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Review.ID_Review = Sentence.ID_Review "
              "JOIN Dep_Tree_Node ON Dep_Tree.ID_Dep_Tree = Dep_Tree_Node.ID_Dep_Tree "
              "WHERE Review.ID_File = " + str(file.id_file) + " AND Label = '" + label + "'")
    return int(c.fetchone()[0])

# ------
# Bigram
# ------


def bigram_label_frequencies(files):
    """
    Compute bigram dependency label frequencies if files.\n
    A "bigram label" is defined as a tuple constituted by the label of a parent node, and the label of one of its
    children.\n
    Results are returned in a dictionary that map file names to frequencies. \n
    Frequencies are represented has dictionaries that map dependency labels to frequencies. \n
    A list of dependency labels is also returns. \n

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :return: Dependency labels, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`str` , :obj:`dict` of :obj:`str` : :obj:`dict` of :obj:`str` : :obj:`float`

    :Example:

        Compute bigram label frequencies of uci files.

        .. code-block: Python

            import loacore.load.file_load as file_load
            import loacore.analysis.frequencies as frequencies

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            files = file_load.load_database(id_files=ids, load_reviews=False)
            labels, frequencies = frequencies.bigram_label_frequencies(files)

    """
    from collections import OrderedDict
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    frequencies = {}
    bigram_labels = get_bigram_label_set(files, c)
    for file in files:
        freq = {}
        for bigram_label in bigram_labels:
            freq[bigram_label] = count_bigram_label(file, bigram_label, c)
        freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))
        total = sum(freq.values())
        freq = {k: freq[k] / total for k in freq.keys()}
        frequencies[file.get_filename()] = freq
    return bigram_labels, frequencies


def get_bigram_label_set(files, c):
    """
    Returns all the existing bigram dependency labels in files, through a SQL request.\n
    A "bigram label" is defined as a tuple constituted by the label of a parent node, and the label of one of its
    children.

    .. note ::

         For a more efficient call from :func:`bigram_label_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param files: Files to process. Notice that only the id_files are needed.
    :type files: :obj:`list` of |File|
    :param c: SQL cursor
    :return: Bigram labels as string tuples.
    :rtype: :obj:`list` of :obj:`tuple` of :obj:`str`

    """
    ids = tuple(f.id_file for f in files)
    c.execute("SELECT Parent.Label, Child.Label "
              "FROM Dep_Tree_Node_Children "
              "JOIN Dep_Tree_Node Child ON Dep_Tree_Node_Children.ID_Child_Node = Child.ID_Dep_Tree_Node "
              "JOIN Dep_Tree_Node Parent ON Dep_Tree_Node_Children.ID_Parent_Node = Parent.ID_Dep_Tree_Node "
              "JOIN Dep_Tree ON Parent.ID_Dep_Tree = Dep_Tree.ID_Dep_Tree "
              "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Sentence.ID_Review = Review.ID_Review "
              "WHERE Review.ID_File IN " + str(ids) + " "
              "GROUP BY Parent.Label, Child.Label")

    return c.fetchall()


def count_bigram_label(file, bigram_label, c):
    """
    Count the number of occurrence of *bigram_label* if all the dependency trees of *file*, through an SQL request.

    .. note ::

         For a more efficient call from :func:`bigram_label_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param file: File to process
    :type file: |File|
    :param bigram_label: Tuple of two dependency labels.
    :type bigram_label: :obj:`tuple` of :obj:`str`
    :param c: SQL cursor
    :return: Number of bigram_label occurrences
    :rtype: int
    """
    c.execute("SELECT COUNT(*) "
              "FROM Dep_Tree_Node_Children "
              "JOIN Dep_Tree_Node Child ON Dep_Tree_Node_Children.ID_Child_Node = Child.ID_Dep_Tree_Node "
              "JOIN Dep_Tree_Node Parent ON Dep_Tree_Node_Children.ID_Parent_Node = Parent.ID_Dep_Tree_Node "
              "JOIN Dep_Tree ON Parent.ID_Dep_Tree = Dep_Tree.ID_Dep_Tree "
              "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Sentence.ID_Review = Review.ID_Review "
              "WHERE Review.ID_File = " + str(file.id_file) + " "
              "AND (Parent.Label, Child.Label) = " + str(bigram_label))
    return int(c.fetchone()[0])

#####################
# PoS_tag Frequencies
#####################

# ------
# Simple
# ------


def pos_tag_frequencies(files, tag_len=2):
    """
    Same idea as :func:`label_frequencies', but with Part Of Speech tags.\n
    The number of characters of the PoS_tags to consider can be specified with tag_len.

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :param tag_len: Number of letters kept in each PoS_tag
    :param tag_len: int
    :return: PoS_tags, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`str` , :obj:`dict` of :obj:`str` : :obj:`dict` of :obj:`str` : :obj:`float`

    :Example:

        Compute simple PoS_tags frequencies of uci files.

        .. code-block: Python

            import loacore.load.file_load as file_load
            import loacore.analysis.frequencies as frequencies

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            files = file_load.load_database(id_files=ids, load_reviews=False)
            labels, frequencies = frequencies.pos_tag_frequencies(files)

    """
    from collections import OrderedDict
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    frequencies = {}
    pos_tags = get_pos_tag_set(files, c, tag_len)
    for file in files:
        freq = {}
        for pos_tag in pos_tags:
            freq[pos_tag] = count_pos_tag(file, pos_tag, c)
        freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))
        total = sum(freq.values())
        freq = {k: freq[k]/total for k in freq.keys()}
        frequencies[file.get_filename()] = freq

    conn.close()
    return pos_tags, frequencies


def get_pos_tag_set(files, c, tag_len):
    """
    Returns all the existing pos_tags in files, through a SQL request.\n
    Only the first *tag_len* characters of the tags are considered.

    .. note ::

         For a more efficient call from :func:`pos_tag_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param files: Files to process. Notice that only the id_files are needed.
    :type files: :obj:`list` of |File|
    :param c: SQL cursor
    :param tag_len: Number of letters kept in each PoS_tag
    :param tag_len: int
    :return: PoS_tags
    :rtype: :obj:`list` of :obj:`str`
    """
    ids = tuple(f.id_file for f in files)
    c.execute("SELECT PoS_tag "
              "FROM Dep_Tree JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Review.ID_Review = Sentence.ID_Review "
              "JOIN Dep_Tree_Node ON Dep_Tree.ID_Dep_Tree = Dep_Tree_Node.ID_Dep_Tree "
              "JOIN Word ON Dep_Tree_Node.ID_Word = Word.ID_Word "
              "WHERE Review.ID_File IN " + str(ids) + " GROUP BY PoS_tag")
    results = c.fetchall()
    tags = []
    for result in results:
        if result[0] is not None:
            tags.append(result[0][0:tag_len])
        else:
            tags.append(None)
    return list(set(tags))


def count_pos_tag(file, pos_tag, c):
    """
    Count the number of occurrence of *pos_tag* if all the words of *file*, through an SQL request.

    .. note ::

         For a more efficient call from :func:`pos_tag_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param file: File to process
    :type file: |File|
    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :param c: SQL cursor
    :return: Number of pos_tag occurrences
    :rtype: int
    """

    if pos_tag is not None:
        c.execute("SELECT COUNT(*) FROM Dep_Tree "
                  "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
                  "JOIN Review ON Review.ID_Review = Sentence.ID_Review "
                  "JOIN Dep_Tree_Node ON Dep_Tree.ID_Dep_Tree = Dep_Tree_Node.ID_Dep_Tree "
                  "JOIN Word ON Dep_Tree_Node.ID_Word = Word.ID_Word "
                  "WHERE Review.ID_File = " + str(file.id_file) + " AND PoS_tag LIKE '" + str(pos_tag) + "%'")
    else:
        c.execute("SELECT COUNT(*) FROM Dep_Tree "
                  "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
                  "JOIN Review ON Review.ID_Review = Sentence.ID_Review "
                  "JOIN Dep_Tree_Node ON Dep_Tree.ID_Dep_Tree = Dep_Tree_Node.ID_Dep_Tree "
                  "JOIN Word ON Dep_Tree_Node.ID_Word = Word.ID_Word "
                  "WHERE Review.ID_File = " + str(file.id_file) + " AND PoS_tag IS null")
    return int(c.fetchone()[0])

# ------
# Bigram
# ------


def bigram_pos_tag_frequencies(files, tag_len=2):
    """
    Same idea as :func:`label_frequencies', but with Part Of Speech tags.\n
    The number of characters of the PoS_tags to consider can be specified with tag_len.

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :param tag_len: Number of letters kept in each PoS_tag
    :param tag_len: int
    :return: PoS_tags, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`str` , :obj:`dict` of :obj:`str` : :obj:`dict` of :obj:`str` : :obj:`float`

    :Example:

        Compute bigram PoS_tags frequencies of uci files.

        .. code-block: Python

            import loacore.load.file_load as file_load
            import loacore.analysis.frequencies as frequencies

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            files = file_load.load_database(id_files=ids, load_reviews=False)
            labels, frequencies = frequencies.bigram_pos_tags_frequencies(files)

    """
    from collections import OrderedDict
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    frequencies = {}
    bigram_pos_tags = get_bigram_pos_tag_set(files, c, tag_len)
    for file in files:
        freq = {}
        for bigram_pos_tag in bigram_pos_tags:
            freq[bigram_pos_tag] = count_bigram_pos_tag(file, bigram_pos_tag, c)
        freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))
        total = sum(freq.values())
        freq = {k: freq[k] / total for k in freq.keys()}
        frequencies[file.get_filename()] = freq
    return bigram_pos_tags, frequencies


def get_bigram_pos_tag_set(files, c, tag_len):
    """
    Returns all the existing bigram PoS_tag in files, through a SQL request.\n
    A "bigram PoS_tag" is defined as a tuple constituted by the PoS_tag of a parent node, and the PoS_tag of one of its
    children.

    .. note ::

         For a more efficient call from :func:`bigram_pos_tag_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param files: Files to process. Notice that only the id_files are needed.
    :type files: :obj:`list` of |File|
    :param c: SQL cursor
    :return: Bigram PoS_tags as string tuples.
    :rtype: :obj:`list` of :obj:`tuple` of :obj:`str`

    """
    ids = tuple(f.id_file for f in files)
    c.execute("SELECT Word_Parent.PoS_tag, Word_Child.PoS_tag "
              "FROM Dep_Tree_Node_Children "
              "JOIN Dep_Tree_Node Node_Child "
              "ON Dep_Tree_Node_Children.ID_Child_Node = Node_Child.ID_Dep_Tree_Node "
              "JOIN Word Word_Child "
              "ON Node_Child.ID_Word = Word_Child.ID_Word "
              "JOIN Dep_Tree_Node Node_Parent "
              "ON Dep_Tree_Node_Children.ID_Parent_Node = Node_Parent.ID_Dep_Tree_Node "
              "JOIN Word Word_Parent "
              "ON Node_Parent.ID_Word = Word_Parent.ID_Word "
              "JOIN Dep_Tree ON Node_Parent.ID_Dep_Tree = Dep_Tree.ID_Dep_Tree "
              "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Sentence.ID_Review = Review.ID_Review "
              "WHERE Review.ID_File IN " + str(ids) + " "
              "GROUP BY Word_Parent.PoS_tag, Word_Child.PoS_tag")

    results = c.fetchall()
    bigram_tags = []
    for result in results:
        if result[0] is not None:
            tag_parent = result[0][0:tag_len]
        else:
            tag_parent = None

        if result[1] is not None:
            tag_child = result[1][0:tag_len]
        else:
            tag_child = None

        tag = (tag_parent, tag_child)
        bigram_tags.append(tag)

    return list(set(bigram_tags))


def count_bigram_pos_tag(file, bigram_pos_tag, c):
    """
    Count the number of occurrence of *bigram_pos_tag* if all the dependency trees of *file*, through an SQL request.

    .. note ::

         For a more efficient call from :func:`bigram_pos_tag_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore.conf import DB_PATH
            conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
            c = conn.cursor()

    :param file: File to process
    :type file: |File|
    :param bigram_pos_tag: Tuple of two pos_tags.
    :type bigram_pos_tag: :obj:`tuple` of :obj:`str`
    :param c: SQL cursor
    :return: Number of bigram_pos_tag occurrences
    :rtype: int
    """

    prepared_statement = \
        "SELECT COUNT(*) " \
        "FROM Dep_Tree_Node_Children " \
        "JOIN Dep_Tree_Node Node_Child " \
        "ON Dep_Tree_Node_Children.ID_Child_Node = Node_Child.ID_Dep_Tree_Node " \
        "JOIN Word Word_Child " \
        "ON Node_Child.ID_Word = Word_Child.ID_Word " \
        "JOIN Dep_Tree_Node Node_Parent " \
        "ON Dep_Tree_Node_Children.ID_Parent_Node = Node_Parent.ID_Dep_Tree_Node " \
        "JOIN Word Word_Parent " \
        "ON Node_Parent.ID_Word = Word_Parent.ID_Word " \
        "JOIN Dep_Tree ON Node_Parent.ID_Dep_Tree = Dep_Tree.ID_Dep_Tree " \
        "JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence " \
        "JOIN Review ON Sentence.ID_Review = Review.ID_Review " \
        "WHERE Review.ID_File = " + str(file.id_file) + " "

    if bigram_pos_tag[0] is not None and bigram_pos_tag[1] is not None:
        c.execute(prepared_statement +
                  "AND Word_Parent.PoS_tag LIKE '" + bigram_pos_tag[0] + "%' "
                  "AND Word_Child.PoS_tag LIKE '" + bigram_pos_tag[1] + "%'")

    elif bigram_pos_tag[0] is None and bigram_pos_tag[1] is None:
        c.execute(prepared_statement +
                  "AND Word_Parent.PoS_tag IS null "
                  "AND Word_Child.PoS_tag IS null")
    elif bigram_pos_tag[0] is None:
        c.execute(prepared_statement +
                  "AND Word_Parent.PoS_tag IS null "
                  "AND Word_Child.PoS_tag LIKE '" + bigram_pos_tag[1] + "%'")
    elif bigram_pos_tag[1] is None:
        c.execute(prepared_statement +
                  "AND Word_Parent.PoS_tag LIKE '" + bigram_pos_tag[0] + "%' "
                  "AND Word_Child.PoS_tag IS null")

    return int(c.fetchone()[0])


###################
# Polarity Pos Tags
###################

def polarity_word_pos_tag_frequencies(files, polarity, tag_len=2):
    """
    Compute PoS_tag frequencies only for words with the specified polarity.

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :param polarity: Word polarity to consider.
    :type polarity: :obj:`str` : {'positive', 'negative'}
    :param tag_len: Number of letters kept in each PoS_tag
    :param tag_len: int
    :return: PoS_tags, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`str` , :obj:`dict` of :obj:`str` : :obj:`dict` of :obj:`str` : :obj:`float`

    :Example:

        Compute pos_tag (first 2 characters) frequencies for positive words in uci files.

        .. code-block:: Python

            import loacore.load.file_load as file_load
            import loacore.analysis.frequencies as frequencies

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            files = file_load.load_database(id_files=ids, load_reviews=False)
            labels, freq = frequencies.polarity_word_pos_tag_frequencies(files, 'positive')

    """
    from collections import OrderedDict
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    frequencies = {}
    pos_tags = get_polarity_pos_tag_set(files, c, tag_len, polarity)
    for file in files:
        freq = {}
        for pos_tag in pos_tags:
            freq[pos_tag] = count_pos_tag(file, pos_tag, c)
        freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))
        total = sum(freq.values())
        freq = {k: freq[k] / total for k in freq.keys()}
        frequencies[file.get_filename()] = freq
    return pos_tags, frequencies


def get_polarity_pos_tag_set(files, c, tag_len, polarity):
    """
    Select possible Part of Speech tags for words in files with the specified polarity, thanks to an SQL request.

    :param files: File to process
    :type files: |File|
    :param tag_len: Number of letters kept in each PoS_tag
    :param tag_len: int
    :param c: SQL cursor
    :param polarity: Word polarity to consider.
    :type polarity: :obj:`str` : {'positive', 'negative'}
    :return: PoS tags
    :rtype: :obj:`list` of :obj:`str`
    """
    ids = tuple(f.id_file for f in files)
    prepared_statement = \
        "SELECT PoS_tag " \
        "FROM Word " \
        "JOIN Synset ON Word.ID_Word = Synset.ID_Word " \
        "JOIN Sentence ON Word.ID_Sentence = Sentence.ID_Sentence " \
        "JOIN Review ON Sentence.ID_Review = Review.ID_Review " \
        "WHERE Review.ID_File IN " + str(ids) + " AND "
    if polarity == 'positive':
        c.execute(prepared_statement +
                  "Pos_Score > Neg_Score "
                  "GROUP BY PoS_tag"
                  )

    elif polarity == 'negative':
        c.execute(prepared_statement +
                  "Pos_Score < Neg_Score "
                  "GROUP BY PoS_tag"
                  )

    results = c.fetchall()
    tags = []
    print(tag_len)
    for result in results:
        if result[0] is not None:
            tags.append(result[0][0:tag_len])
    return list(set(tags))

#################
# Polarity Labels
#################


def polarity_word_label_frequencies(files, polarity):
    """
    Compute label frequencies for words with the specified polarity.

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :param polarity: Word polarity to consider.
    :type polarity: :obj:`str` : {'positive', 'negative'}
    :return: Labels, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`str` , :obj:`dict` of :obj:`str` : :obj:`dict` of :obj:`str` : :obj:`float`

    :Example:

        .. code-block:: Python

            import loacore.load.file_load as file_load
            import loacore.analysis.frequencies as frequencies

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            files = file_load.load_database(id_files=ids, load_reviews=False)
            labels, freq = frequencies.polarity_word_label_frequencies(files, 'positive')

    """
    from collections import OrderedDict
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    frequencies = {}
    labels = get_polarity_label_set(files, c, polarity)
    for file in files:
        freq = {}
        for label in labels:
            freq[label] = count_label(file, label, c)
        freq = OrderedDict(sorted(freq.items(), key=lambda t: t[1]))
        total = sum(freq.values())
        freq = {k: freq[k] / total for k in freq.keys()}
        frequencies[file.get_filename()] = freq
    return labels, frequencies


def get_polarity_label_set(files, c, polarity):
    """
    Select all the possible dependency labels for words in files with the specified polarity, thanks to an SQL request.

    :param files: File to process
    :type files: |File|
    :param c: SQL cursor
    :param polarity: Word polarity to consider.
    :type polarity: :obj:`str` : {'positive', 'negative'}
    :return: Dependency labels
    :rtype: :obj:`list` of :obj:`str`
    """
    ids = tuple(f.id_file for f in files)
    prepared_statement = \
        "SELECT Label " \
        "FROM Dep_Tree JOIN Sentence ON Dep_Tree.ID_Sentence = Sentence.ID_Sentence " \
        "JOIN Review ON Review.ID_Review = Sentence.ID_Review " \
        "JOIN Dep_Tree_Node ON Dep_Tree.ID_Dep_Tree = Dep_Tree_Node.ID_Dep_Tree " \
        "JOIN Word ON Dep_Tree_Node.ID_Word = Word.ID_Word " \
        "JOIN Synset ON Word.ID_Synset = Synset.ID_Synset " \
        "WHERE Review.ID_File IN " + str(ids) + " AND "

    if polarity == 'positive':
        c.execute(prepared_statement +
                  "Pos_Score > Neg_Score "
                  "GROUP BY Label")

    elif polarity == 'negative':
        c.execute(prepared_statement +
                  "Pos_Score < Neg_Score "
                  "GROUP BY Label")

    results = c.fetchall()
    return [result[0] for result in results]
