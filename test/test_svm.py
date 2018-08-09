
def test_tokens():
    import loacore.load.file_load as file_load
    import loacore.learning.word2vec as we
    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_deptrees=False)

    print(we.get_tokens_list(files))


def test_vectors():
    import loacore.load.file_load as file_load
    import loacore.learning.word2vec as we
    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_deptrees=False)

    vectors = we.word_2_vec(files)
    print(vectors['movie'])
    print(len(vectors['movie']))


def test_review_vectors():
    import loacore.load.file_load as file_load
    import loacore.learning.word2vec as we
    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_deptrees=False)

    word_vectors = we.word_2_vec(files)

    reviews = [r for review in [f.reviews for f in files] for r in review]

    review_vectors = we.reviews_2_vec(reviews, word_vectors)
    for i in range(3):
        print(reviews[i].review)
        print(review_vectors[i])


def test_full_process():
    import loacore.learning.svm as svm
    import loacore.load.file_load as file_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/yelp_labelled.txt'])
    files = file_load.load_database(id_files=ids, load_deptrees=False)
    svm.full_process(files)


# test_tokens()
# test_vectors()
# test_review_vectors()
test_full_process()
