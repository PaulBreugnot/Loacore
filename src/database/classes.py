

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

    def __init__(self, id_review, id_file, file_index, review):
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