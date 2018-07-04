

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

    def load_reviews(self):
        import src.database.db_review_api as review_api
        self.reviews = review_api.load_reviews(self.file_path)

    def load(self):
        return open(self.file_path, encoding='windows-1252')


class Review:

    def __init__(self, id_review, id_file, file_index, review, load_sentences=False):
        self.id_review = id_review
        self.id_file = id_file
        self.file_index = file_index
        self.review = review

    def get_id_review(self):
        return self.id_review

    def get_id_file(self):
        return self.id_file

    def get_file_index(self):
        return self.file_index

    def get_review(self):
        return self.review

    def load_sentences(self):
        '''

        :return: nothing
        Load review's sentences from database
        '''


class Sentence:

    def __init__(self, id_sentence, id_review, review_index, id_dep_tree, sentence):
        self.id_sentence = id_sentence
        self.id_review = id_review
        self.review_index = review_index
        self.id_dep_tree = id_dep_tree
        self.sentence = sentence

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
