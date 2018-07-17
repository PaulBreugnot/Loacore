import sqlite3 as sql
from loacore import DB_PATH
from loacore.classes.classes import DepTree
from loacore.classes.classes import DepTreeNode


def load_dep_trees(id_dep_trees=[], load_words=True):
    """

    Load :class:`DepTree` s from database.

    :param id_dep_trees: If specified, load only the deptrees with corresponding ids. Otherwise, load all the deptrees.
    :type id_dep_trees: :obj:`list` of :obj:`int`
    :param load_words: Specify if Words need to be loaded in :class:`DepTree` s.
    :type load_words: boolean
    :return: loaded deptrees
    :rtype: :obj:`list` of :class:`DepTree`

    :Example:
    Load all deptrees from database : can take a few moments.

    >>> import loacore.load.deptree_load as deptree_load
    >>> deptrees = deptree_load.load_dep_trees()
    >>> deptree_str = deptrees[500].print_dep_tree()
    instalaciones (sentence, NCFP000, instalación)
        las (spec, None, el)
        agua (sn, NCCS000, agua)
            el (spec, None, el)
            fria (s.a, None, )
                y (coord, None, y)
                caliente (grup.a, AQ0CS00, calentar)
            caminata (sn, NCFS000, caminata)
                la (spec, None, el)
            tranquilidad (sn, NCFS000, tranquilidad)
                la (spec, None, el)
            servicio (sn, NCMS000, servicio)
                el (spec, None, el)

    """

    def load_dep_tree_from_result(result, c):
        dep_tree = DepTree(result[0], result[1], result[2])

        # Select root
        c.execute("SELECT ID_Dep_Tree_Node, ID_Dep_Tree, ID_Word, Label, root FROM Dep_Tree_Node "
                  "WHERE ID_Dep_Tree = " + str(dep_tree.id_dep_tree) + " "
                                                                       "AND root = 1")

        result = c.fetchone()
        if result is not None:
            # Set root
            dep_tree.root = DepTreeNode(result[0], result[1], result[2], result[3], 1)

            # Load children
            rec_children_select(c, dep_tree.root)
        return dep_tree

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    dep_trees = []

    if len(id_dep_trees) > 0:
        for id_dep_tree in id_dep_trees:

            c.execute("SELECT ID_Dep_Tree, ID_Dep_Tree_Node, ID_Sentence FROM Dep_Tree "
                      "WHERE ID_Dep_Tree = " + id_dep_tree)

            result = c.fetchone()
            if result is not None:
                dep_tree = load_dep_tree_from_result(result, c)
                dep_trees.append(dep_tree)

    else:
        c.execute("SELECT ID_Dep_Tree, ID_Dep_Tree_Node, ID_Sentence FROM Dep_Tree")

        results = c.fetchall()
        for result in results:
            dep_tree = load_dep_tree_from_result(result, c)
            dep_trees.append(dep_tree)

    if load_words:
        import loacore.database.load.word_load as word_load
        word_load.load_words_in_dep_trees(dep_trees)

    conn.close()

    return dep_trees


def load_dep_tree_in_sentences(sentences, load_words=True):
    """

    Load :class:`DepTree` s into corresponding *sentences*, setting up their attribute :attr:`dep_tree`.\n
    Also return all the loaded deptrees.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` or
        :func:`sentence_load.load_sentences()` when *load_deptrees* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load sentences and deptrees in one go.

    :param sentences: Sentences in which corresponding DepTrees should be loaded.
    :type sentences: :obj:`list` of :class:`Sentence`
    :param load_words: Specify if Words need to be loaded in :class:`DepTree` s.
    :type load_words: boolean
    :return: loaded deptrees
    :rtype: :obj:`list` of :class:`DepTree`
    """

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    dep_trees = []
    for sentence in sentences:

        c.execute("SELECT ID_Dep_Tree, ID_Dep_Tree_Node, ID_Sentence FROM Dep_Tree "
                  "WHERE ID_Sentence = " + str(sentence.id_sentence))

        result = c.fetchone()
        if result is not None:
            dep_tree = DepTree(result[0], result[1], result[2])

            # Select root
            c.execute("SELECT ID_Dep_Tree_Node, ID_Dep_Tree, ID_Word, Label, root FROM Dep_Tree_Node "
                      "WHERE ID_Dep_Tree = " + str(dep_tree.id_dep_tree) + " "
                      "AND root = 1")

            result = c.fetchone()
            if result is not None:
                # Set root
                dep_tree.root = DepTreeNode(result[0], result[1], result[2], result[3], 1)

                # Load children
                rec_children_select(c, dep_tree.root)

            sentence.dep_tree = dep_tree
            dep_trees.append(dep_tree)

    if load_words:
        import loacore.database.load.word_load as word_load
        word_load.load_words_in_dep_trees([sentence.dep_tree for sentence in sentences])

    conn.close()

    return dep_trees


def rec_children_select(cursor, node):

    cursor.execute("SELECT ID_Dep_Tree_Node, ID_Dep_Tree, ID_Word, Label, root "
                   "FROM Dep_Tree_Node JOIN Dep_Tree_Node_Children "
                   "ON Dep_Tree_Node.ID_Dep_Tree_Node = Dep_Tree_Node_Children.ID_Child_Node "
                   "WHERE ID_Parent_Node = " + str(node.id_dep_tree_node))

    results = cursor.fetchall()
    children = []
    for result in results:
        child = DepTreeNode(result[0], result[1], result[2], result[3], 0)
        children.append(child)
        rec_children_select(cursor, child)
    node.children = children