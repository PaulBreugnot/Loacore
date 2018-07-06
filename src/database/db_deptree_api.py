import sqlite3 as sql
import ressources.pyfreeling as freeling
from src.database.classes import DepTree
from src.database.classes import DepTreeNode


def load_dep_tree_in_sentences(sentences):

    conn = sql.connect('../../data/database/reviews.db')
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


def add_dep_tree_from_sentences(sentences, print_result=False):

    print("Loading Freeling Modules...")
    morfo, tagger, sen, wsd, parser = init_freeling()

    freeling_sentences = [sentence.compute_freeling_sentence() for sentence in sentences]

    print("Morphosyntactic analysis and tagging...")
    # perform morphosyntactic analysis and disambiguation
    freeling_sentences = morfo.analyze(freeling_sentences)
    freeling_sentences = tagger.analyze(freeling_sentences)

    print("Disambiguation...")
    # annotate and disambiguate senses
    freeling_sentences = sen.analyze(freeling_sentences)
    freeling_sentences = wsd.analyze(freeling_sentences)

    print("Dependency tree parsing...")
    # parse sentences
    freeling_sentences = parser.analyze(freeling_sentences)

    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()

    progress = 0
    end = len(sentences)
    for s in range(len(sentences)):
        progress += 1
        if progress == end:
            print(str(progress) + " / " + str(end) + " sentences added.")
        else:
            print(str(progress) + " / " + str(end) + " sentences added.", end='\r')
        sentence = sentences[s]

        # Add dep_tree to database
        dt = freeling_sentences[s].get_dep_tree()
        dep_tree = DepTree(None, None, sentence.id_sentence)

        c.execute("INSERT INTO Dep_Tree (ID_Sentence) VALUES (" + str(dep_tree.id_sentence) + ")")

        # Get back id_dep_tree
        c.execute("SELECT last_insert_rowid()")
        id_dep_tree = c.fetchone()[0]
        dep_tree.id_dep_tree = id_dep_tree

        # Database process
        root = None
        if len(sentence.words) != len(freeling_sentences[s]):
            print("ERROR!!!!!")
            return
        for w in range(len(sentence.words)):
            word = sentence.words[w]
            rank = freeling_sentences[s][w].get_senses()
            if len(rank) > 0:
                word.PoS_tag = freeling_sentences[s][w].get_tag()
                if print_result:
                    print("Word : " + word.word)
                    print(freeling_sentences[s][w].get_tag())
                    print(dt.get_node_by_pos(w).get_word().get_form())
                    print(dt.get_node_by_pos(w).get_label())

            # We use the get_node_by_pos function to map the tree to our sentence
            node = dt.get_node_by_pos(w)

            dep_tree_node = DepTreeNode(None, id_dep_tree, word.id_word, node.get_label(), 0)
            if node == dt.begin():
                dep_tree_node.root = 1
                root = dep_tree_node

            # Add DepTreeNode to database
            c.execute("INSERT INTO Dep_Tree_Node (ID_Dep_Tree, ID_Word, Label, root) "
                      "VALUES ("
                      "" + str(dep_tree_node.id_dep_tree) + ", "
                      "" + str(dep_tree_node.id_word) + ", "
                      "'" + dep_tree_node.label + "', "
                      "" + str(dep_tree_node.root) + ")")

            # Get back id_dep_tree_node
            c.execute("SELECT last_insert_rowid()")
            id_dep_tree_node = c.fetchone()[0]

            dep_tree_node.id_dep_tree_node = id_dep_tree_node

            # Use the freeling set_node_id function to store our db node id in the freeling node
            node.set_node_id(str(id_dep_tree_node))

            # Add PoS_tag to Word
            if word.PoS_tag is not None:
                c.execute("UPDATE Word SET PoS_tag = '" + word.PoS_tag +
                          "' WHERE ID_Word = " + str(word.id_word))

        # Add dep_tree root to database
        dep_tree.root = root
        c.execute("UPDATE Dep_Tree SET ID_Dep_Tree_Node = " + str(root.id_dep_tree_node) + " "
                  "WHERE ID_Dep_Tree = " + str(id_dep_tree))

        # Add children relations
        root_node = dt.begin()
        rec_children(c, root_node)

    conn.commit()
    print("Commit end.")
    conn.close()


def rec_children(c, node):
    for ch in range(0, node.num_children()):
        child = node.nth_child(ch)
        c.execute("INSERT INTO Dep_Tree_Node_Children (ID_Parent_Node, ID_Child_Node) "
                  "VALUES (" + str(node.get_node_id()) + ", "
                  + str(child.get_node_id()) + ")")
        rec_children(c, child)


def my_maco_options(lang,lpath) :

    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = ""
    opt.ProbabilityFile = lpath + "probabilitats.dat"
    opt.DictionaryFile = lpath + "dicc.src"
    opt.PunctuationFile = lpath + "../common/punct.dat"
    return opt


def init_freeling():

    freeling.util_init_locale("default")

    lang = "es"
    ipath = "/usr/local"
    # path to language data
    lpath = ipath + "/share/freeling/" + lang + "/"

    # create the analyzer with the required set of maco_options
    morfo = freeling.maco(my_maco_options(lang, lpath))

    morfo.set_active_options(False,  # UserMap
                             False,  # NumbersDetection,
                             True,  # PunctuationDetection,
                             False,  # DatesDetection,
                             True,  # DictionarySearch,
                             False,  # AffixAnalysis,
                             False,  # CompoundAnalysis,
                             False,  # RetokContractions,
                             False,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             True)  # ProbabilityAssignment

    # create tagger
    tagger = freeling.hmm_tagger(lpath + "tagger.dat", False, 2)

    # create sense annotator
    sen = freeling.senses(lpath + "senses.dat")
    # create sense disambiguator
    wsd = freeling.ukb(lpath + "ukb.dat")
    # create dependency parser
    parser = freeling.dep_treeler(lpath + "dep_treeler/dependences.dat")

    return morfo, tagger, sen, wsd, parser