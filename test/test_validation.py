
def test_k_fold():
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load
    import loacore.learning.word2vec as w2v
    import loacore.learning.validation as val

    ids = file_load.get_id_files_by_file_path(r'.*/uci/yelp_labelled.txt')
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True,
                                                   load_sentences=True,
                                                   load_words=True,
                                                   workers=0)
    wv = w2v.word_2_vec(reviews)
    reviews_vectors = w2v.reviews_2_vec(reviews, wv)
    val.k_fold_validation(reviews, reviews_vectors, 3)


def test_leave_p_out():
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load
    import loacore.learning.word2vec as w2v
    import loacore.learning.validation as val

    ids = file_load.get_id_files_by_file_path(r'.*/uci/yelp_labelled.txt')
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True,
                                                   load_sentences=True,
                                                   load_words=True)
    wv = w2v.word_2_vec(reviews)
    reviews_vectors = w2v.reviews_2_vec(reviews, wv)
    print(val.leave_p_out_validation(reviews, reviews_vectors, 1))


def test_lsi_k_fold():
    import loacore.learning.lsi as lsi
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load
    import loacore.learning.validation as val

    ids = file_load.get_id_files_by_file_path(r'.*/uci/yelp_labelled.txt')
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True,
                                                   load_sentences=True,
                                                   load_words=True)[:100]
    word2int_dict, model = lsi.lsi_model(reviews)
    reviews_vectors = lsi.reviews_2_vec(reviews, model, word2int_dict)
    # print(type(reviews_vectors))
    # print(len(reviews_vectors))
    # print(reviews_vectors)
    # TODO: need to check consistency of lsi model
    print(val.k_fold_validation(reviews, reviews_vectors, 3))


def test_lsi_leave_p_out():
    import loacore.learning.lsi as lsi
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load
    import loacore.learning.validation as val

    ids = file_load.get_id_files_by_file_path(r'.*/uci/yelp_labelled.txt')
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True,
                                                   load_sentences=True,
                                                   load_words=True)
    word2int_dict, model = lsi.lsi_model(reviews)
    reviews_vectors = lsi.reviews_2_vec(reviews, model, word2int_dict)
    print(val.leave_p_out_validation(reviews, reviews_vectors, 1))


def main():
    # test_k_fold()
    # test_leave_p_out()
    test_lsi_k_fold()


if __name__ == "__main__":
    main()
