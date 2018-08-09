

def learn_model(reviews, reviews_vectors):
    """
    Learn and return a LinearSVC model from specified labelled reviews and Word2Vec dictionnary.

    :param reviews: Learning Dataset
    :type reviews: :obj:`list` of |Review|
    :param reviews_vectors: Vector representations of reviews
    :type reviews_vectors:
        :obj:`list` of `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
    :return: Learned model
    :rtype:
        `LinearSVC
        <http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC>`_
    """

    from sklearn.svm import LinearSVC

    labels = get_labels_vector(reviews)
    clf = LinearSVC()
    clf.fit(reviews_vectors, labels)

    return clf


def commit_analysis(clf, reviews, wv, analysis='svm', db_commit=False):
    """

    Predict polarity of each review in reviews and add the result to their *review.polarity* dictionary with the
    *analysis* label.

    :param clf: LinearSVC model
    :type clf:
        `LinearSVC
        <http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC>`_
    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :param wv: Word vectors dictionary
    :type wv:
        `KeyedVector
        <https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors>`_
    :param analysis: Analysis label
    :type analysis: string
    :param db_commit: If True, results are commit to the database.

    """
    import loacore.learning.word2vec as we
    from loacore.classes.classes import Polarity
    for review in reviews:
        score = clf.predict(we.review_2_vec(review, wv))
        if score == -1:
            review.polarities[analysis] = Polarity(None, analysis, review.id_review, 0, 1, 0)
        elif score == 1:
            review.polarities[analysis] = Polarity(None, analysis, review.id_review, 1, 0, 0)
        elif score == 0:
            review.polarities[analysis] = Polarity(None, analysis, review.id_review, 0, 0, 1)

    if db_commit:
        import loacore.process.polarity_process as polarity_process
        polarity_process.commit_polarities(reviews, analysis)


def get_labels_vector(reviews, ref='label'):
    """
    Return reviews classification based on specified ref analysis. Classes are represented as -1, 0, +1, according to
    the results of |Polarity| fucntions :

        - :func:`~loacore.classes.classes.Polarity.is_negative()`
        - :func:`~loacore.classes.classes.Polarity.is_objective()`
        - :func:`~loacore.classes.classes.Polarity.is_positive()`

    Especially used with reviews as the learning dataset, to return labels to give to the LinearSVC learning model.

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :param ref: Reference analysis
    :type ref: string
    :return: Reviews classification
    """
    labels = [-1 if review.polarities[ref].is_negative() else
              0 if review.polarities[ref].is_objective() else
              +1 if review.polarities[ref].is_positive() else None
              for review in reviews]

    return labels


def full_process(files, learn_test_split=0.7):
    import loacore.learning.word2vec as we
    print("Learning Word2Vec vocabulary...")
    reviews = [r for file in files for r in file.reviews]
    wv = we.word_2_vec(reviews)

    print(reviews)
    print(len(reviews))
    split_index = int(learn_test_split*len(reviews))
    learning_dataset = reviews[0:split_index]
    print("Learning dataset size : ", len(learning_dataset))
    testing_dataset = reviews[split_index:len(reviews)]
    print("Testing dataset size : ", len(testing_dataset))

    import loacore.learning.word2vec as we

    reviews_vectors = we.reviews_2_vec(learning_dataset, wv)
    print("Learning SVM model...")
    clf = learn_model(learning_dataset, reviews_vectors)
    print("Analyze testing set...")
    commit_analysis(clf, learning_dataset, reviews_vectors)

    import loacore.analysis.polarity_check as polarity_check
    polarity_check.check_polarity(files, analysis_to_check=['svm'])
