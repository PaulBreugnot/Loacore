import sqlite3 as sql
import os
from src.database.classes.classes import DepTree
from src.database.classes.classes import DepTreeNode


def load_dep_tree_in_sentences(sentences):

    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

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

    conn.close()


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
