

def word_2_vec(reviews):
    """
    Learn a Word2Vec dictionary from the tokens of specified reviews (tokens obtained with :func:`get_tokens_list()` .

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :return: Word2Vec dictionary
    :rtype:
        `KeyedVector
        <https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors>`_
    """
    from gensim.test.utils import get_tmpfile
    from gensim.models import Word2Vec, KeyedVectors

    path = get_tmpfile("wordvectors.kv")

    tokens = get_tokens_list(reviews)

    model = Word2Vec(tokens, size=100, window=5, min_count=1, workers=4)
    model.wv.save(path)
    wv = KeyedVectors.load(path, mmap='r')
    return wv


def reviews_2_vec(reviews, wv):
    """
    Returns a list of vector representations of the reviews, according to the specified Word2Vec dictionary.\n
    (Currently : mean of the Word2Vec vectors of words)

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :param wv: Word2Vec dictionary
    :type wv:
        `KeyedVector
        <https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors>`_
    :return: Vector list
    :rtype:
        :obj:`list` of `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
    """
    import numpy as np
    review_vectors = []
    for review in reviews:
        review_vectors.append(
            [wv[w.word_2_vec_key] for s in review.sentences for w in s.words if w.word_2_vec_key is not None])
    vectors = [np.array(
        np.mean(review_vector, axis=0))
        for review_vector in review_vectors if len(review_vector) > 0]

    return vectors


def review_2_vec(review, wv):
    """
        Returns a vector representations review, according to the specified Word2Vec dictionary.\n
        (Currently : mean of the Word2Vec vectors of words)

        :param review: Reviews to process
        :type review: :obj:`list` of |Review|
        :param wv: Word2Vec dictionary
        :type wv:
            `KeyedVector
            <https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors>`_
        :return: Vector list
        :rtype:
            :obj:`list` of `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
        """
    import numpy as np
    review_vector = [wv[w.word_2_vec_key] for s in review.sentences for w in s.words if w.word_2_vec_key is not None]
    return np.array([np.mean(review_vector, axis=0)])


def get_tokens_list(reviews):
    """
    Returns a list of all tokens in specified reviews. For each word, if a lemma is found, lemma is used. Otherwise,
    word form is used.

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :return: List of tokens
    :rtype: :obj:`list` of :obj:`str`
    """
    import re
    tokens = []
    for review in reviews:
        for sentence in review.sentences:
            sentence_tokens = []
            for word in sentence.words:
                if re.fullmatch(r'\w+', word.word):
                    if word.lemma != '':
                        word.word_2_vec_key = word.lemma
                    else:
                        word.word_2_vec_key = word.word
                    sentence_tokens.append(word.word_2_vec_key)
            tokens.append(sentence_tokens)
    return tokens


