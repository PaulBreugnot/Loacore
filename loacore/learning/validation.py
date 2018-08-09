def k_fold_validation(reviews, wv, k):
    from sklearn.model_selection import cross_val_score
    import loacore.svm as svm
    import loacore.learning.word2vec as we
    from sklearn.svm import LinearSVC

    reviews_vectors = we.reviews_2_vec(reviews, wv)
    labels = svm.get_labels_vector(reviews)
    clf = LinearSVC()

    print(cross_val_score(clf, reviews_vectors, labels, cv=k))


def leave_p_out_validation(reviews, wv, p):
    from sklearn.model_selection import cross_val_score
    import loacore.svm as svm
    import loacore.learning.word2vec as we
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import LeavePOut

    lpo = LeavePOut(p=p)
    reviews_vectors = we.reviews_2_vec(reviews, wv)
    labels = svm.get_labels_vector(reviews)
    clf = LinearSVC()

    print(cross_val_score(clf, reviews_vectors, labels, cv=lpo))
