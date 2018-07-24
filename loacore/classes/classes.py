class File:
    """
    :ivar id_file: ID_File used in File table
    :vartype id_file: int
    :ivar file_path: Path used to load file from file system.
    :vartype file_path: path-like object
    :ivar reviews: File reviews
    :vartype reviews: :obj:`list` of :class:`Review`

    """

    def __init__(self, id_file, file_path):
        self.id_file = id_file
        self.file_path = file_path
        self.reviews = []

    def sentence_list(self):
        """
        Convenient way to get all the sentences of the file, avoiding Reviews.

        :return: List of file sentences
        :rtype: :obj:`list` of :class:`Sentence`
        """
        sentences = []
        for review in self.reviews:
            sentences += review.sentences
        return sentences

    def get_directory_name(self):
        import re
        return re.findall(r'.*/(.+)/.+\.txt', self.file_path)[0]

    def get_filename(self):

        import re
        return re.findall(r'.+/(.+\.txt)', self.file_path)[0]

    @staticmethod
    def sentence_list_from_files(files):
        """
        Convenient way to get all the sentences of the specified files, avoiding Reviews.

        :param files: Files
        :type files: :obj:`list` of :class:`File`
        :return: List of file sentences
        :rtype: :obj:`list` of :class:`Sentence`
        """
        sentences = []
        for file in files:
            sentences += file.sentence_list()
        return sentences

    def load(self, encoding='windows-1252'):
        """
        Load file from file system using :attr:`file_path` and specified encoding.

        :param encoding:
            Source file encoding. Default is set to *windows-1252*, the encoding obtained from .txt conversion in Excel.
        :return: file object
        """
        return open(self.file_path, encoding=encoding)


class Review:
    """
    :ivar id_review: ID_Review used id Review table
    :vartype id_review: int
    :ivar id_file: SQL reference to the corresponding File
    :vartype id_file: int
    :ivar file_index: Index of the Review in referenced File
    :vartype file_index: int
    :ivar review: Review represented as a string
    :vartype review: string
    :ivar polarity: review polarity: 0 or 1
    :vartype polarity: int
    :ivar sentences: Review Sentences
    :vartype sentences: :obj:`list` of :class:`Sentence`
    """

    def __init__(self, id_review, id_file, file_index, review, polarity=None):
        self.id_review = id_review
        self.id_file = id_file
        self.file_index = file_index
        self.review = review
        self.polarity = polarity
        self.sentences = []


class Sentence:

    """
    :ivar id_sentence: ID_Sentence used in Sentence table
    :vartype id_sentence: int
    :ivar id_review: SQL reference to the corresponding Review
    :vartype id_review: int
    :ivar review_index: Index of the Sentence in referenced Review
    :vartype review_index: int
    :ivar id_dep_tree: SQL reference to a possibly associated DepTree
    :vartype id_dep_tree: int
    :ivar words: Sentence Words
    :vartype words: :obj:`list` of :class:`Word`
    :ivar dep_tree: Possibly associated DepTree
    :vartype dep_tree: :class:`DepTree`
    :ivar freeling_sentence: result of :meth:`compute_freeling_sentence()` when called
    :vartype freeling_sentence: :class:`pyfreeling.sentence`

    """

    def __init__(self, id_sentence, id_review, review_index, id_dep_tree):
        self.id_sentence = id_sentence
        self.id_review = id_review
        self.review_index = review_index
        self.id_dep_tree = id_dep_tree
        self.words = []
        self.dep_tree = None
        self.freeling_sentence = None

    def print_sentence(self, print_sentence=True):
        """

        Convenient way of printing sentences from their word list attribute.

        :param print_sentence:
            Can be set to False to compute and return the string corresponding to the sentence, without
            printing it.
        :return: String representation of the sentence
        :rtype: string
        """
        sentence_str =' '.join([w.word for w in self.words])
        if print_sentence:
            print(sentence_str)
        return sentence_str

    def compute_freeling_sentence(self):
        """
        Generates a basic :class:`pyfreeling.sentence` instance, converting :attr:`words` as :class:`pyfreeling.word` .
        \nThis function is used to process :class:`Sentence` with Freeling.

        :Example:
            Load :class:`Sentence` s from database and convert them into Freeling Sentences.

            >>> import loacore.load.sentence_load as sentence_load
            >>> sentences = sentence_load.load_sentences()
            >>> freeling_sentences = [s.compute_freeling_sentence() for s in sentences]

        :return: generated Freeling Sentence instance
        :rtype: :class:`pyfreeling.sentence`
        """

        from ressources.pyfreeling import sentence as freeling_sentence_class
        fr_words = [word.compute_freeling_word() for word in self.words]
        fr_sentence = freeling_sentence_class(fr_words)
        self.freeling_sentence = fr_sentence
        return self.freeling_sentence


class Word:
    """
    :ivar id_word: ID_Word used in Word table
    :vartype id_word: int
    :ivar id_sentence: SQL reference to the corresponding Sentence
    :vartype id_sentence: int
    :ivar sentence_index: Index of the Word in referenced Sentence
    :vartype sentence_index: int
    :ivar word: Word form
    :vartype word: string
    :ivar id_lemma: SQL references to the corresponding Lemma (Table Lemma)
    :vartype id_lemma: int
    :ivar lemma: Possibly associated Lemma
    :vartype lemma: string
    :ivar id_synset: SQL references to corresponding Synset
    :vartype id_synset: int
    :ivar synset: Possibly associated Synset
    :vartype synset: :class:`Synset`
    :ivar PoS_tag: Possibly associated Part-of-Speech tag
    :vartype PoS_tag: string
    :ivar freeling_word: result of :meth:`compute_freeling_word()` when called
    :vartype freeling_word: :class:`pyfreeling.word`
    """

    def __init__(self, id_word, id_sentence, sentence_index, word, id_lemma, id_synset, PoS_tag):
        self.id_word = id_word
        self.id_sentence = id_sentence
        self.sentence_index = sentence_index
        self.word = word
        self.id_lemma = id_lemma
        self.lemma = None
        self.id_synset = id_synset
        self.synset = None
        self.PoS_tag = PoS_tag
        self.freeling_word = None

    def compute_freeling_word(self):
        """
        Generates a basic :class:`pyfreeling.word` instance, generated by only the word form, even if some analysis
        could have already been realized.\n
        Moreover, only :func:`loacore.classes.classes.File.load_sentence()` (that itself uses this function) should be used,
        because all Freeling analysis work with :class:`pyfreeling.sentence` instances.
        """

        from ressources.pyfreeling import word as freeling_word_class
        fr_word = freeling_word_class()
        fr_word.set_form(self.word)

        self.freeling_word = fr_word
        return fr_word


class Synset:
    """
    :ivar id_synset: ID_Synset used in Synset table
    :vartype id_synset: int
    :ivar id_word: SQL reference to the corresponding Word
    :vartype id_word: int
    :ivar synset_code: Synset as represented in Freeling (ex : 01123148-a)
    :vartype synset_code: string
    :ivar synset_name: Synset as represent in WordNet and SentiWordNet (ex : good.a.01)
    :vartype synset_name: string
    :ivar neg_score: Negative polarity from SentiWordNet.
    :vartype neg_score: float
    :ivar pos_score: Positive polarity from SentiWordNet.
    :vartype pos_score: float
    :ivar obj_score: Objective polarity from SentiWordNet.
    :vartype obj_score: float

    .. note:: neg_score + pos_score + obj_score = 1

    """

    def __init__(self, id_synset, id_word, synset_code, synset_name, neg_score, pos_score, obj_score):
        self.id_synset = id_synset
        self.id_word = id_word
        self.synset_code = synset_code
        self.synset_name = synset_name
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = obj_score


class DepTree:
    """
    :ivar id_dep_tree: Id_Dep_Tree used in DepTree table
    :vartype id_dep_tree: int
    :ivar id_dep_tree_node: SQL reference to root node (Dep_Tree_Node table)
    :vartype id_dep_tree_node: int
    :ivar id_sentence: SQL reference to the corresponding Sentence
    :vartype id_sentence: int
    :ivar root: Root node
    :vartype root: :class:`DepTreeNode`
    """

    def __init__(self, id_dep_tree, id_dep_tree_node, id_sentence):
        self.id_dep_tree = id_dep_tree
        self.id_dep_tree_node = id_dep_tree_node
        self.id_sentence = id_sentence
        self.root = None

    def print_dep_tree(self, root=None, print_dep_tree=True):
        """
        :param root: If set, node from which to start to print the tree. self.root otherwise.
        :type root: :class:`DepTreeNode`
        :param print_dep_tree:
            Can be set to False to compute and return the string corresponding to the tree, without
            printing it.
        :type print_dep_tree: boolean
        :return: String representation of DepTree instance
        :rtype: string
        """
        dep_tree_str = []
        if root is None:
            root = self.root
        self.print_node(dep_tree_str, root, "")
        dep_tree_str = '\n'.join(dep_tree_str)
        if print_dep_tree:
            print(dep_tree_str)
        return dep_tree_str

    def print_node(self, dep_tree_str, node, offset):
        if node.word is None:
            dep_tree_str.append(offset + "ID_Word : " + str(node.id_word) + "Label : " + str(node.label))
        else:
            dep_tree_str.append(offset + node.word.word + ' (' + str(node.label) + ', ' + str(node.word.PoS_tag) + ', '
                + node.word.lemma + ')')
        for child in node.children:
            self.print_node(dep_tree_str, child, offset + '    ')


class DepTreeNode:
    """
    :ivar id_dep_tree_node: ID_Dep_Tree_Node used in Dep_Tree_Node table
    :vartype id_dep_tree_node: int
    :ivar id_dep_tree: SQL reference to the corresponding DepTree
    :vartype id_dep_tree: int
    :ivar id_word: SQL reference to corresponding id_word
    :vartype id_word: int
    :ivar word: Possibly loaded associated word
    :vartype word: :class:`Word`
    :ivar label: Node dependency label. See annex for details.
    :vartype label: string
    :ivar root: True if and only if this is the root of the corresponding DepTree
    :vartype root: boolean
    :ivar children: Node children
    :vartype children: :obj:`list` of :class:`DepTreeNode`
    """
    def __init__(self, id_dep_tree_node, id_dep_tree, id_word, label, root):
        self.id_dep_tree_node = id_dep_tree_node
        self.id_dep_tree = id_dep_tree
        self.id_word = id_word
        self.word = None
        self.label = label
        self.root = root
        self.children = []
