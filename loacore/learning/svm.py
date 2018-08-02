

def learn_model(reviews, wv):
    import loacore.learning.word_embeddings as we
    from sklearn.svm import LinearSVC

    reviews_vectors = we.reviews_2_vec(reviews, wv)
    labels = get_labels_vector(reviews)
    clf = LinearSVC()
    clf.fit(reviews_vectors, labels)

    return clf


def commit_analysis(clf, reviews, wv, analysis='svm', db_commit=False):
    import loacore.learning.word_embeddings as we
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
    labels = [-1 if review.polarities[ref].is_negative() else
              0 if review.polarities[ref].is_objective() else
              +1 if review.polarities[ref].is_positive() else None
              for review in reviews]

    return labels


def full_process(files, learn_test_split=0.7):
    import loacore.learning.word_embeddings as we
    print("Learning Word2Vec vocabulary...")
    wv = we.word_2_vec(files)

    reviews = [r for file in files for r in file.reviews]
    print(reviews)
    print(len(reviews))
    split_index = int(learn_test_split*len(reviews))
    learning_dataset = reviews[0:split_index]
    print("Learning dataset size : ", len(learning_dataset))
    testing_dataset = reviews[split_index:len(reviews)]
    print("Testing dataset size : ", len(testing_dataset))

    print("Learning SVM model...")
    clf = learn_model(learning_dataset, wv)
    print("Analyze testing set...")
    commit_analysis(clf, learning_dataset, wv)

    import loacore.analysis.polarity_check as polarity_check
    polarity_check.check_polarity(files, analysis_to_check=['svm'])
