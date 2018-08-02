

def word_2_vec(files):
    from gensim.test.utils import get_tmpfile
    from gensim.models import Word2Vec, KeyedVectors

    path = get_tmpfile("wordvectors.kv")

    tokens = get_tokens_list(files)

    model = Word2Vec(tokens, size=100, window=5, min_count=1, workers=4)
    model.wv.save(path)
    wv = KeyedVectors.load(path, mmap='r')
    return wv


def reviews_2_vec(reviews, wv):
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
    import numpy as np
    review_vector = [wv[w.word_2_vec_key] for s in review.sentences for w in s.words if w.word_2_vec_key is not None]
    return np.array([np.mean(review_vector, axis=0)])


def get_tokens_list(files):
    import re
    tokens = []
    for file in files:
        for review in file.reviews:
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


