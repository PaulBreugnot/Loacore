
def lsi_model(reviews):
    """
    Train a Latent Semantic Indexing model from input *reviews*, with
    `gensim.models.LsiModel <https://radimrehurek.com/gensim/models/lsimodel.html>`_.\n
    During the process, a vocabulary and a dictionary mapping this vocabulary to unique integers
    (because `LsiModel <https://radimrehurek.com/gensim/models/lsimodel.html#gensim.models.lsimodel.LsiModel>`_
    use this representation of texts) is computed from input *reviews*, and this dictionary is also returned.\n
    To compute vocabulary, word lemmas are considered if defines, otherwise word forms are used.

    :param reviews: Input reviews.
    :type reviews: :obj:`list` of |Review|
    :return: A dictionary mapping vocabulary to integers, and the trained LSI model.
    :rtype:
        :obj:`dict` of :obj:`string` : :obj:`int`,
        `LsiModel <https://radimrehurek.com/gensim/models/lsimodel.html#gensim.models.lsimodel.LsiModel>`_
    """
    from gensim.test.utils import get_tmpfile
    from gensim.models import LsiModel

    word2int_dict = _word2int_dict(reviews)
    model = LsiModel(_reviews2int(reviews, word2int_dict))
    tmp_fname = get_tmpfile("lsi_model")
    model.save(tmp_fname)
    return word2int_dict, LsiModel.load(tmp_fname)


def _word2int_dict(reviews):
    word2int_dict = {}
    words = [w.lemma if w.lemma != "" else w.word for r in reviews for s in r.sentences for w in s.words]
    voc = set(words)
    index = 0
    for w in voc:
        word2int_dict[w] = index
        index += 1
    print("Computed dictionnary of " + str(len(word2int_dict.values())) + " words from " + str(len(words)) + " words.")
    return word2int_dict


def _reviews2int(reviews, word2int_dict):
    reviews_vectors = []
    for review in reviews:
        reviews_vectors.append(
            _review2int(review, word2int_dict))
    return reviews_vectors


def _review2int(review, word2int_dict):
    ids = [word2int_dict[w.lemma] if w.lemma in word2int_dict.keys() else word2int_dict[w.word]
           for s in review.sentences for w in s.words]
    bag_of_words = []
    for id_word in set(ids):
        bag_of_words.append((id_word, sum([1 if i == id_word else 0 for i in ids])))
    # print("Bag of word: " + str(bag_of_words))
    return bag_of_words


def reviews_2_vec(reviews, model, word2int_dict):
    """
    List of vector representations of *reviews*, as returned by :func:`review_2_vec()`.

    :param reviews: Input reviews.
    :type reviews: :obj:`list` of |Review|
    :param model: Trained LsiModel
    :type model: `LsiModel <https://radimrehurek.com/gensim/models/lsimodel.html#gensim.models.lsimodel.LsiModel>`_
    :param word2int_dict: A dictionary mapping vocabulary to integers.
    :type word2int_dict: :obj:`dict` of :obj:`string` : :obj:`int`
    :return: Vector representations of *reviews*.
    :rtype: :obj:`list` of `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
    """
    reviews_vectors = []
    for review in reviews:
        reviews_vectors.append(review_2_vec(review, model, word2int_dict))
    return reviews_vectors


def review_2_vec(review, model, word2int_dict):
    """
    Return a vector representation of *review* according to the given model.

    .. note::

        *word2int_dict* should be consistent with *model*, i.e. *word2int_dict* and *model* should be the results of
        the same call of :func:`lsi_model()`.

    :param review: Input review
    :param review: |Review|
    :param model: Trained LsiModel
    :type model: `LsiModel <https://radimrehurek.com/gensim/models/lsimodel.html#gensim.models.lsimodel.LsiModel>`_
    :param word2int_dict: A dictionary mapping vocabulary to integers.
    :type word2int_dict: :obj:`dict` of :obj:`string` : :obj:`int`
    :return: A vector representation of *review*, according to *model*.
    :rtype: `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
    """
    import numpy as np
    # print("---Review2Vec---")
    # print(type(model[_review2int(review, word2int_dict)]))
    # print(model[_review2int(review, word2int_dict)])
    # print("----------------")

    # TODO: need to check consistency of lsi model
    return np.array([t[1] for t in model[_review2int(review, word2int_dict)]])
