import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import DepTree
from loacore.classes.classes import DepTreeNode


def load_dep_trees(id_dep_trees=(), load_words=True):
    """

    Load Dep Trees from database.

    :param id_dep_trees: If specified, load only the deptrees with corresponding ids. Otherwise, load all the deptrees.
    :type id_dep_trees: :obj:`sequence` of :obj:`int`
    :param load_words: Specify if Words need to be loaded in Dep Trees.
    :type load_words: boolean
    :return: loaded deptrees
    :rtype: :obj:`list` of |DepTree|

    :Example:
    Load all deptrees from database : can take a few moments.

    >>> import loacore.load.deptree_load as deptree_load
    >>> deptrees = deptree_load.load_dep_trees()
    >>> deptree_str = deptrees[500].dep_tree_str()
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
    from loacore.conf import DB_TIMEOUT

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

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
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
        import loacore.load.word_load as word_load
        word_load.load_words_in_dep_trees(dep_trees)

    conn.close()

    return dep_trees


def load_dep_tree_in_sentences(sentences, load_words=True):
    """

    Load Dep Trees into corresponding *sentences*, setting up their attribute :attr:`dep_tree`.\n
    Also return all the loaded deptrees.\n

    .. note::
        This function is automatically called by :func:`file_load.load_database()` or
        :func:`sentence_load.load_sentences()` when *load_deptrees* is set to :obj:`True`.
        In most of the cases, those functions should be used instead to load sentences and deptrees in one go.

    :param sentences: Sentences in which corresponding DepTrees should be loaded.
    :type sentences: :obj:`list` of |Sentence|
    :param load_words: Specify if Words need to be loaded in Dep Trees.
    :type load_words: boolean
    :return: loaded deptrees
    :rtype: :obj:`list` of |DepTree|
    """
    import os
    from loacore.conf import DB_TIMEOUT

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    sentences_dict = {s.id_sentence: s for s in sentences}

    # Load dep trees
    dep_trees = {}
    c.execute("SELECT ID_Dep_Tree, ID_Dep_Tree_Node, ID_Sentence FROM Dep_Tree "
              "WHERE ID_Sentence IN " + str(tuple([s.id_sentence for s in sentences])))
    for result in c.fetchall():
        dep_tree = DepTree(result[0], result[1], result[2])
        sentences_dict[result[2]].dep_tree = dep_tree
        dep_trees[result[0]] = dep_tree

    # Load roots
    current_nodes = {}
    c.execute("SELECT ID_Dep_Tree_Node, ID_Dep_Tree, ID_Word, Label, root FROM Dep_Tree_Node "
              "WHERE ID_Dep_Tree IN " + str(tuple(dep_trees.keys())) + " "
              "AND root = 1")
    for result in c.fetchall():
        node = DepTreeNode(result[0], result[1], result[2], result[3], 1)
        current_nodes[result[0]] = node
        dep_trees[result[1]].root = node

    depth = 0
    while len(current_nodes) > 0:
        print("[" + str(os.getpid()) + "] Loading depth " + str(depth))
        depth += 1
        if len(current_nodes) > 1:
            tuple_str = str(tuple(current_nodes.keys()))
        else:
            tuple_str = "(" + str(list(current_nodes.keys())[0]) + ")"

        c.execute("SELECT ID_Parent_Node, ID_Dep_Tree_Node, ID_Dep_Tree, ID_Word, Label, root "
                  "FROM Dep_Tree_Node JOIN Dep_Tree_Node_Children "
                  "ON Dep_Tree_Node.ID_Dep_Tree_Node = Dep_Tree_Node_Children.ID_Child_Node "
                  "WHERE ID_Parent_Node IN " + tuple_str)

        nodes_to_update = current_nodes.copy()
        current_nodes.clear()
        for result in c.fetchall():
            child_node = DepTreeNode(result[1], result[2], result[3], result[4], 0)
            nodes_to_update[result[0]].children.append(child_node)
            current_nodes[result[1]] = child_node

    if load_words:
        print("[" + str(os.getpid()) + "] Loading words in deptrees...")
        import loacore.load.word_load as word_load
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
