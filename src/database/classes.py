

class File:

    def __init__(self, id_file, file_path, load_reviews=False):
        self.id_file = id_file
        self.file_path = file_path
        self.reviews = []
        if load_reviews:
            self.load_reviews()

    def get_id_file(self):
        return self.id_file

    def get_file_path(self):
        return self.file_path

    def get_reviews(self):
        return self.reviews

    def set_reviews(self, reviews):
        self.reviews = reviews

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

    def __init__(self, id_review, id_file, file_index, review, load_sentences=False):
        self.id_review = id_review
        self.id_file = id_file
        self.file_index = file_index
        self.review = review
        self.sentences = []
        if load_sentences:
            self.load_sentences()

    def get_id_review(self):
        return self.id_review

    def get_id_file(self):
        return self.id_file

    def get_file_index(self):
        return self.file_index

    def get_review(self):
        return self.review

    def get_sentences(self):
        return self.sentences

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

    def __init__(self, id_sentence, id_review, review_index, id_dep_tree, sentence):
        self.id_sentence = id_sentence
        self.id_review = id_review
        self.review_index = review_index
        self.id_dep_tree = id_dep_tree
        self.sentence = sentence
        self.words = []

    def get_id_sentence(self):
        return self.id_sentence

    def get_id_review(self):
        return self.id_review

    def get_review_index(self):
        return self.review_index

    def get_id_dep_tree(self):
        return self.id_dep_tree

    def get_sentence(self):
        return self.sentence

    def set_words(self, words):
        self.words = words

    def get_words(self):
        return self.words

    def load_words(self):
        """
        This method should only be used to load the words of an isolated Sentence.
        Otherwise, please use method src.database.db_word_api.load_words_in_sentences()
        :return: loaded words
        """
        import src.database.db_word_api as db_word_api
        self.words = db_word_api.load_words_list_by_id_sentence(self.id_sentence)
        return self.get_words()


class Word:

    def __init__(self, id_word, id_sentence, sentence_index, word, id_lemma, id_synset, PoS_tag):
        self.id_word = id_word
        self.id_sentence = id_sentence
        self.sentence_index = sentence_index
        self.word = word
        self.id_lemma = id_lemma
        self.lemma = ''
        self.id_synset = id_synset
        self.synset = None
        self.PoS_tag = PoS_tag

    def set_id_lemma(self, id_lemma):
        self.id_lemma = id_lemma

    def set_lemma(self, lemma):
        self.lemma = lemma

    def set_id_synset(self, id_synset):
        self.id_synset = id_synset

    def set_synset(self, synset):
        self.synset = synset

    def set_PoS_tag(self, PoS_tag):
        self.PoS_tag = PoS_tag

    def get_id_word(self):
        return self.id_word

    def get_id_sentence(self):
        return self.id_sentence

    def get_sentence_index(self):
        return self.sentence_index

    def get_word(self):
        return self.word

    def get_id_lemma(self):
        return self.id_lemma

    def get_lemma(self):
        return self.lemma

    def get_id_synset(self):
        return self.id_synset

    def get_synset(self):
        return self.synset

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

    def freeling_word(self):
        # TODO : consistent initialization according to the use of freeling modules
        from ressources.pyfreeling import word
        return word(self.word)


class Synset:

    def __init__(self, id_synset, synset_code, synset_name, pos_score, neg_score, obj_score):
        self.id_synset = id_synset
        self.synset_code = synset_code
        self.synset_name = synset_name
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = obj_score

    def get_id_synset(self):
        return self.id_synset

    def get_synset_code(self):
        """
        :return:  synset as represented in Freeling
        """
        return self.synset_code

    def get_synset_name(self):
        """
        :return: synset as represented in NLTK, WordNet and SentiWordNet
        """
        return self.synset_name

    """
    Scores coming from SentiWordNet
    """
    def get_pos_score(self):
        return self.pos_score

    def get_neg_score(self):
        return self.neg_score

    def get_obj_score(self):
        return self.obj_score