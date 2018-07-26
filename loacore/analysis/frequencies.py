from loacore import DB_PATH
import sqlite3 as sql


def label_frequencies(files):
    """
    Compute simple dependency label frequencies if files.\n
    Results are returned in a dictionary that map file names to frequencies. \n
    Frequencies are represented has dictionaries that map dependency labels to frequencies. \n
    A list of dependency labels is also returns. \n

    :param files: Files to process
    :type files: :obj:`list` of :class:`File`
    :return: Dependency labels, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`string` , :obj:`dict` of :obj:`string` : :obj:`dict` of :obj:`string` : :obj:`float`

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
    conn = sql.connect(DB_PATH)
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


def bigram_label_frequencies(files):
    """
    Compute bigram dependency label frequencies if files.\n
    A "bigram label" is defined as a tuple constituted by the label of a parent node, and the label of one of its
    children.\n
    Results are returned in a dictionary that map file names to frequencies. \n
    Frequencies are represented has dictionaries that map dependency labels to frequencies. \n
    A list of dependency labels is also returns. \n

    :param files: Files to process
    :type files: :obj:`list` of :class:`File`
    :return: Dependency labels, and a dictionary that maps file names to frequencies
    :rtype: :obj:`list` of :obj:`string` , :obj:`dict` of :obj:`string` : :obj:`dict` of :obj:`string` : :obj:`float`

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
    conn = sql.connect(DB_PATH)
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


def get_label_set(files, c):
    """
    Returns all the existing bigram dependency labels in files, through a SQL request.\n

    .. note ::

         For a more efficient call from :func:`label_frequencies`, this function takes an already initialized SQL
         cursor as an argument.
         If you want to use it, you can initialize *c* with the following code :

         .. code-block:: Python

            import sqlite3 as sql
            from loacore import DB_PATH
            conn = sql.connect(DB_PATH)
            c = conn.cursor()

    :param files: Files to process. Notice that only the id_files are needed.
    :type files: :obj:`list` of :class:`File`
    :param c: SQL cursor
    :return: Dependency labels
    :rtype: :obj:`list` of :obj:`string`
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
            from loacore import DB_PATH
            conn = sql.connect(DB_PATH)
            c = conn.cursor()

    :param file: File to process
    :type file: :class:`File`
    :param label: Dependency label
    :type label: string
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
            from loacore import DB_PATH
            conn = sql.connect(DB_PATH)
            c = conn.cursor()

    :param files: Files to process. Notice that only the id_files are needed.
    :type files: :obj:`list` of :class:`File`
    :param c: SQL cursor
    :return: Bigram labels as string tuples.
    :rtype: :obj:`list` of :obj:`tuple` of :obj:`string`

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
            from loacore import DB_PATH
            conn = sql.connect(DB_PATH)
            c = conn.cursor()

    :param file: File to process
    :type file: :class:`File`
    :param bigram_label: Tuple of two dependency labels.
    :type bigram_label: :obj:`tuple` of :obj:`string`
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



