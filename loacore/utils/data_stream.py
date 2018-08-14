
class ReviewIterator(object):

    def __init__(self):
        self.temp_file_list = []

    def __iter__(self):
        import pickle
        for file in self.temp_file_list:
            unpickler = pickle.Unpickler(file)
            file.seek(0)
            for review in unpickler.load():
                yield review


def save_to_temp_file(reviews):
    import tempfile
    import pickle
    reviews_temp_file = tempfile.TemporaryFile()
    # print(bytearray("This is a test", encoding='utf8'))
    # reviews_temp_file.write(bytearray("This is a test", encoding='utf8'))
    # print(reviews_temp_file.read())

    pickler = pickle.Pickler(reviews_temp_file)
    pickler.dump(reviews)

    return reviews_temp_file
