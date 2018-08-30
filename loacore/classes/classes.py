class File:
    """
    :ivar id_file: ID_File used in File table
    :vartype id_file: int
    :ivar file_path: Path used to load file from file system.
    :vartype file_path: path-like object
    :ivar reviews: File reviews
    :vartype reviews: :obj:`list` of |Review|

    """

    def __init__(self, id_file, file_name):
        self.id_file = id_file
        self.file_name = file_name
        self.reviews = []

    def sentence_list(self):
        """
        Convenient way to get all the sentences of the file, avoiding Reviews.

        :return: List of file sentences
        :rtype: :obj:`list` of |Sentence|
        """
        sentences = []
        for review in self.reviews:
            sentences += review.sentences
        return sentences

    def get_directory_name(self):
        import re
        return re.findall(r'.*/(.+)/.+\.txt', self.file_name)[0]

    def get_filename(self):

        import re
        return re.findall(r'.+/(.+\.txt)', self.file_name)[0]

    @staticmethod
    def sentence_list_from_files(files):
        """
        Convenient way to get all the sentences of the specified files, avoiding Reviews.

        :param files: Files
        :type files: :obj:`list` of |File|
        :return: List of file sentences
        :rtype: :obj:`list` of |Sentence|
        """
        sentences = []
        for file in files:
            sentences += file.sentence_list()
        return sentences

    def load(self, encoding='utf8'):
        """
        Load file from file system using :attr:`file_path` and specified encoding.

        :param encoding:
            Source file encoding. Default : *utf8*.
        :return: file object
        """
        return open(self.file_name, encoding=encoding)


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
    :ivar sentences: Review Sentences
    :vartype sentences: :obj:`list` of |Sentence|
    :ivar polarities:
        Polarities associated to the review, that can come from directly from the source file for polarity label
        datasets, or from the result of different analysis. Each polarity can be identified with its analysis attribute.
    :vartype polarity: :obj:`list` of |Polarity|
    """

    def __init__(self, id_review, id_file, file_index, review):
        self.id_review = id_review
        self.id_file = id_file
        self.file_index = file_index
        self.review = review
        self.sentences = []
        self.polarities = dict()

    def review_str(self, colored_polarity=True, analysis=[]):
        """

        :param colored_polarity:
            If True, polarities are colored printed.
            (red = Negative, green = Positive, yellow = Objective, black = No Synset)
        :type colored_polarity: boolean
        :param analysis: The polarities computed with the specified analysis will be added at the end of each review.
        :type analysis: :obj:`list` of :obj:`str`
        :return: Review string representation
        :rtype: string
        """
        review_str = ' '.join([s.sentence_str(colored_polarity=colored_polarity) for s in self.sentences])
        for a in analysis:
            if a not in self.polarities.keys():
                print("Missing analysis : '" + a + "'. Available : " + str(list(self.polarities.keys())))
            else:
                if colored_polarity:
                    review_str += "\t" + a + "=["\
                       + "\033[32m" + str(self.polarities[a].pos_score) + "\033[30m, "\
                       + "\033[31m" + str(self.polarities[a].neg_score) + "\033[30m, "\
                       + "\033[33m" + str(self.polarities[a].obj_score) + "\033[30m]"
                else:
                    review_str += "\t" + a + "=["\
                       + str(self.polarities[a].pos_score) + ", "\
                       + str(self.polarities[a].neg_score) + ", "\
                       + str(self.polarities[a].obj_score) + "]"

        return review_str


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
    :vartype words: :obj:`list` of |Word|
    :ivar dep_tree: Possibly associated DepTree
    :vartype dep_tree: |DepTree|
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

    def sentence_str(self, colored_polarity=False):
        """

        Convenient way of printing sentences from their word list attribute.

        :param colored_polarity:
            If True, polarities are colored printed.
            (red = Negative, green = Positive, yellow = Objective, black = No Synset)
        :type colored_polarity: boolean
        :return: String representation of the sentence
        :rtype: string
        """

        if colored_polarity:
            sentence_str = ' '.join([w.colored_word() for w in self.words])
            sentence_str += '\033[0m'
        else:
            sentence_str = ' '.join([w.word for w in self.words])

        return sentence_str

    def compute_freeling_sentence(self):
        """
        Generates a basic :class:`pyfreeling.sentence` instance, converting :attr:`words` as :class:`pyfreeling.word` .
        \nThis function is used to process |Sentence| with Freeling.

        :Example:
            Load sentences from database and convert them into Freeling Sentences.

            >>> import loacore.load.sentence_load as sentence_load
            >>> sentences = sentence_load.load_sentences()
            >>> freeling_sentences = [s.compute_freeling_sentence() for s in sentences]

        :return: generated Freeling Sentence instance
        :rtype: :class:`pyfreeling.sentence`
        """

        from pyFreelingApi import freeling_api as freeling
        freeling_sentence_class = freeling.sentence

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
    :vartype synset: |Synset|
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
        self.word_2_vec_key = None

    def compute_freeling_word(self):
        """
        Generates a basic :class:`pyfreeling.word` instance, generated by only the word form, even if some analysis
        could have already been realized.\n
        Moreover, only :func:`loacore.classes.classes.File.load_sentence()` (that itself uses this function) should be used,
        because all Freeling analysis work with :class:`pyfreeling.sentence` instances.
        """

        from pyFreelingApi import freeling_api as freeling
        freeling_word_class = freeling.word

        fr_word = freeling_word_class()
        fr_word.set_form(self.word)

        self.freeling_word = fr_word
        return fr_word

    def colored_word(self):
        """
        Colored representation of word. If a Synset is associated, colored are assigned as follow :

            - pos_score > neg_score => red
            - neg_score > pos_score => green
            - neg_score = pos_score => yellow

        :return: Colored word
        :rtype: string
        """
        if self.synset is not None:
            if self.synset.pos_score > self.synset.neg_score:
                return '\033[32m' + self.word + '\033[0m'
            if self.synset.pos_score < self.synset.neg_score:
                return '\033[31m' + self.word + '\033[0m'
            return '\033[33m' + self.word + '\033[0m'
        return '\033[0m' + self.word + '\033[0m'


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
    :vartype root: |DepTreeNode|
    """

    def __init__(self, id_dep_tree, id_dep_tree_node, id_sentence):
        self.id_dep_tree = id_dep_tree
        self.id_dep_tree_node = id_dep_tree_node
        self.id_sentence = id_sentence
        self.root = None

    def dep_tree_str(self, root=None, colored_polarity=False):
        """
        :param root: If set, node from which to start to print the tree. self.root otherwise.
        :type root: |DepTreeNode|
        :param colored_polarity:
            If True, polarities are colored printed.
            (red = Negative, green = Positive, yellow = Objective, black = No Synset)
        :type colored_polarity: boolean
        :return: String representation of DepTree instance
        :rtype: string
        """
        dep_tree_str = []
        if root is None:
            root = self.root
        self.node_str(dep_tree_str, root, "", colored_polarity)
        dep_tree_str = '\n'.join(dep_tree_str)

        return dep_tree_str

    def node_str(self, dep_tree_str, node, offset, colored_polarity):
        if node.word is None:
            dep_tree_str.append(offset + "ID_Word : " + str(node.id_word) + "Label : " + str(node.label))
        else:
            if colored_polarity:
                word = node.word.colored_word() + '\033[30m'
            else:
                word = node.word.word
            dep_tree_str.append(offset + word + ' (' + str(node.label) + ', ' + str(node.word.PoS_tag) + ', '
                                + node.word.lemma + ')')
        for child in node.children:
            self.node_str(dep_tree_str, child, offset + '    ', colored_polarity)


class DepTreeNode:
    """
    :ivar id_dep_tree_node: ID_Dep_Tree_Node used in Dep_Tree_Node table
    :vartype id_dep_tree_node: int
    :ivar id_dep_tree: SQL reference to the corresponding DepTree
    :vartype id_dep_tree: int
    :ivar id_word: SQL reference to corresponding id_word
    :vartype id_word: int
    :ivar word: Possibly loaded associated word
    :vartype word: |Word|
    :ivar label: Node dependency label. See annex for details.
    :vartype label: string
    :ivar root: True if and only if this is the root of the corresponding DepTree
    :vartype root: boolean
    :ivar children: Node children
    :vartype children: :obj:`list` of |DepTreeNode|
    """
    def __init__(self, id_dep_tree_node, id_dep_tree, id_word, label, root):
        self.id_dep_tree_node = id_dep_tree_node
        self.id_dep_tree = id_dep_tree
        self.id_word = id_word
        self.word = None
        self.label = label
        self.root = root
        self.children = []


class Polarity:
    """
    Object used to store possible polarities of a review.

    :ivar id_polarity: ID_Polarity used in Polarity table.
    :vartype id_polarity: int
    :ivar analysis: An analysis identifier, from which the polarity come from.
    :vartype analysis: string
    :ivar id_review: SQL reference to the corresponding Review
    :vartype id_review: int
    :ivar pos_score: Positive polarity
    :vartype pos_score: float
    :ivar neg_score: Negative polarity
    :vartype neg_score: float
    :ivar obj_score: Objective polarity
    :vartype obj_score: float
    """

    def __init__(self, id_polarity, analysis, id_review, pos_score, neg_score, obj_score):
        self.id_polarity = id_polarity
        self.analysis = analysis
        self.id_review = id_review
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = obj_score

    def is_positive(self):
        """
        :return: True if pos_score > neg_score
        :rtype: boolean
        """
        if self.pos_score > self.neg_score:
            return True
        return False

    def is_negative(self):
        """
        :return: True if pos_score > neg_score
        :rtype: boolean
        """
        if self.pos_score < self.neg_score:
            return True
        return False

    def is_objective(self):
        """
        :return: True if pos_score > neg_score
        :rtype: boolean
        """
        if self.pos_score == self.neg_score:
            return True
        return False
