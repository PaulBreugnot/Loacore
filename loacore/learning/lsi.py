
def lsi_model(reviews):
    from gensim.test.utils import get_tmpfile
    from gensim.models import LsiModel

    model = LsiModel(reviews2int(reviews, voc_dict(reviews)))
    tmp_fname = get_tmpfile("lsi_model")
    model.save(tmp_fname)
    return LsiModel.load(tmp_fname)


def voc_dict(reviews):
    word_dict = {}
    words = set([w.lemma if w.lemma != "" else w.word for r in reviews for s in r.sentences for w in s.words])
    index = 0
    for w in words:
        word_dict[w] = index
        index += 1
    print("Computed dictionnary of " + str(len(word_dict.values())) + " words from " + str(len(words)) + "words.")
    return word_dict


def reviews2int(reviews, word_dict):
    reviews_vectors = []
    for review in reviews:
        reviews_vectors.append(
            review2int(review, word_dict))
    return reviews_vectors


def review2int(review, word_dict):
    return [word_dict[w.lemma] if w.lemma in word_dict.keys() else word_dict[w.word] for w in review.words]


def reviews_2_vec(reviews, model, word_dict):
    reviews_vectors = []
    for review in reviews:
        reviews_vectors.append(review_2_vec(review, model, word_dict))
    return reviews_vectors


def review_2_vec(review, model, word_dict):
    return model[review2int(review, word_dict)]