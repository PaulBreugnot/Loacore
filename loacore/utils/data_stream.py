import pickle


class ReviewIterator(object):
    """
    An iterator used to stream reviews from
    `TemporaryFiles <https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryFile>`_
    This class is mainly used in :func:`~loacore.load.file_load.load_database()` when *load_in_temp_file* is
    :obj:`True`, to replace |File| attribute *reviews*.
    """

    def __init__(self, temp_file_list=None, iterator_length=-1):
        if temp_file_list is not None:
            self.temp_file_list = temp_file_list
        else:
            self.temp_file_list = []
        self.iterator_length = iterator_length

    def __iter__(self):
        for file in self.temp_file_list:
            file.seek(0)
            unpickler = pickle.Unpickler(file)
            for review in unpickler.load():
                yield review

    def __len__(self):
        return self.iterator_length


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


def split_reviews(reviews, split_size):
    split_reviews_list = []
    n = int(len(reviews)/split_size)
    split_number = 0
    for i in range(n):
        split_number += len(reviews[i*split_size:(i+1)*split_size])
        # split reviews are stored as temporary file to limit RAM usage
        # split_reviews_list.append(
        #     data_stream.ReviewIterator(
        #         temp_file_list=data_stream.save_to_temp_file(reviews[i*split_size:(i+1)*split_size])))
        split_reviews_list.append(reviews[i*split_size:(i+1)*split_size])

    if n*split_size < len(reviews):
        split_number += len(reviews[n*split_size:len(reviews)])
        split_reviews_list.append(reviews[n*split_size:len(reviews)])

    print("Reviews number : " + str(len(reviews)))
    print("Split into : " + str(len(split_reviews_list)) + "(total : " + str(split_number) + ")")

    return split_reviews_list
