

class File:

    def __init__(self, id_file, file_path):
        self.id_file = id_file
        self.file_path = file_path
        self.reviews = []

    def load_reviews(self):
        """
        This method should only be used to load the sentences of an isolated Review.
        Otherwise, please use method src.database.db_review_api.load_reviews_in_files()
        :return: loaded reviews
        """
        import src.database.db_review_api as review_api
        self.reviews = review_api.load_reviews_by_id_file(self.id_file)
        return self.get_reviews()

    def load(self):
        return open(self.file_path, encoding='windows-1252')


class Review:

    def __init__(self, id_review, id_file, file_index, review):
        self.id_review = id_review
        self.id_file = id_file
        self.file_index = file_index
        self.review = review
        self.sentences = []

    def load_sentences(self):
        """
        This method should only be used to load the sentences of an isolated Review.
        Otherwise, please use method src.database.db_sentence_api.load_sentences_in_reviews()
        :return: loaded sentences
        """
        import src.database.db_sentence_api as sentence_api
        self.sentences = sentence_api.load_sentences_list_by_id_review(self.id_review)
        return self.get_sentences()


class Sentence:

    def __init__(self, id_sentence, id_review, review_index, id_dep_tree):
        self.id_sentence = id_sentence
        self.id_review = id_review
        self.review_index = review_index
        self.id_dep_tree = id_dep_tree
        self.words = []
        self.freeling_sentence = None

    def load_words(self):
        """
        This method should only be used to load the words of an isolated Sentence.
        Otherwise, please use method src.database.db_word_api.load_words_in_sentences()
        :return: loaded words
        """
        import src.database.db_word_api as db_word_api
        self.words = db_word_api.load_words_list_by_id_sentence(self.id_sentence)
        return self.get_words()

    def compute_freeling_sentence(self):
        from ressources.pyfreeling import sentence as freeling_sentence_class
        fr_words = [word.compute_freeling_word() for word in self.words]
        fr_sentence = freeling_sentence_class(fr_words)
        self.freeling_sentence = fr_sentence
        return self.freeling_sentence


class Word:

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

    def load_lemma(self):
        """
        This method should only be used to load the lemma of an isolated Word.
        Otherwise, please use method src.database.db_lemma_api.load_lemmas_in_words()
        :return: loaded Lemma
        """
        import src.database.db_lemma_api as db_lemma_api
        self.lemma = db_lemma_api.load_lemmas_list([self.id_lemma])[0]
        return self.get_lemma()

    def load_synset(self):
        """
        This method should only be used to load the synset of an isolated Word.
        Otherwise, please use method src.database.db_synset_api.load_synsets_in_words()
        :return: loaded Synset
        """
        import src.database.db_synset_api as db_synset_api
        self.synset = db_synset_api.load_synsets([self.id_synset])[0]
        return self.get_synset()

    def compute_freeling_word(self):
        # TODO : consistent initialization according to the use of freeling modules
        from ressources.pyfreeling import word as freeling_word_class
        from ressources.pyfreeling import analysis as freeling_analysis
        fr_word = freeling_word_class()
        fr_word.set_form(self.word)

        """
        if self.lemma is not None:
            fr_analysis = freeling_analysis()
            fr_analysis.set_lemma(self.lemma)
            fr_word.set_analysis(fr_analysis)
        """

        self.freeling_word = fr_word
        return fr_word


class Synset:

    def __init__(self, id_synset, id_word, synset_code, synset_name, pos_score, neg_score, obj_score):
        self.id_synset = id_synset
        self.id_word = id_word
        self.synset_code = synset_code
        self.synset_name = synset_name
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = obj_score
