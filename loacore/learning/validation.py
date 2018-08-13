def k_fold_validation(reviews, reviews_vectors, k):
    """
    Performs a K-Fold validation from *reviews* and their associated vector representation using sklearn function
    `cross_val_score
    <http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score>`_.

    :param reviews: Reviews to check.
    :type reviews: :obj:`list` of |Review|
    :param reviews_vectors: Vectors representations associated to reviews.
    :type reviews_vectors:
        :obj:`list` of `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
    :param k: K-Fold model parameter
    :type k: int
    :return: Cross validation results.
    :rtype:
        array-like object, as returned by `cross_val_score
        <http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score>`_.
    """
    from sklearn.model_selection import cross_val_score
    import loacore.learning.svm as svm
    from sklearn.svm import LinearSVC

    labels = svm.get_labels_vector(reviews)
    clf = LinearSVC()

    return cross_val_score(clf, reviews_vectors, labels, cv=k)


def leave_p_out_validation(reviews, reviews_vectors, p):
    """
    Performs a Leave-P-out validation from *reviews* and their associated vector representation using sklearn function
    `cross_val_score
    <http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score>`_.

    :param reviews: Reviews to check.
    :type reviews: :obj:`list` of |Review|
    :param reviews_vectors: Vectors representations associated to reviews.
    :type reviews_vectors:
        :obj:`list` of `numpy.array <https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.array.html>`_
    :param p: Leave-P-out model parameter
    :type p: int
    :return: Cross validation results.
    :rtype:
        array-like object, as returned by `cross_val_score
        <http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score>`_.
        """
    from sklearn.model_selection import cross_val_score
    import loacore.learning.svm as svm
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import LeavePOut

    lpo = LeavePOut(p=p)
    labels = svm.get_labels_vector(reviews)
    clf = LinearSVC()

    print(cross_val_score(clf, reviews_vectors, labels, cv=lpo))

