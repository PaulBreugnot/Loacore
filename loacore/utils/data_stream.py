
class ReviewIterator(object):
    """
    An iterator used to stream reviews from
    `TemporaryFiles <https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile>`_
    This class is mainly used in :func:`~loacore.load.file_load.load_database()` when *load_in_temp_file* is
    :obj:`True`, to replace |File| attribute *reviews*.
    """

    def __init__(self, temp_file_list=[]):
        self.temp_file_list = temp_file_list

    def __iter__(self):
        import pickle
        for file in self.temp_file_list:
            unpickler = pickle.Unpickler(file)
            file.seek(0)
            for review in unpickler.load():
                yield review


def save_to_temp_file(reviews):
    """

    :param reviews:
        File to save in a `TemporaryFile <https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile>`_,
        using `pickle.Pickler <https://docs.python.org/3/library/pickle.html#pickle.Pickler>`_.\n
        Reviews list can then be normally reload using
        `pickle.Unpickler <https://docs.python.org/3/library/pickle.html#pickle.Unpickler>`_
    :type reviews: :obj:`list` of |Review|
    :return: Opened temporary file.
    :rtype: `TemporaryFile <https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile>`_
    """
    import tempfile
    import pickle

    reviews_temp_file = tempfile.TemporaryFile()

    pickler = pickle.Pickler(reviews_temp_file)
    pickler.dump(reviews)

    return reviews_temp_file
