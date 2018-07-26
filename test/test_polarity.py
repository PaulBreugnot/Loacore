
def commit_simple_polarity():
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load
    import loacore.load.polarity_load as polarity_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids, load_sentences=True, load_words=True)
    sentiment_analysis.compute_simple_reviews_polarity(reviews, commit_polarities=True)

    polarity_load.load_polarities_in_reviews(reviews)
    for review in reviews:
        print(review.review, " : ", review.polarities["simple"].pos_score, ", ",
              review.polarities["simple"].neg_score, ", ",
              review.polarities["simple"].obj_score)


def commit_optimistic_polarity():
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids, load_sentences=True, load_words=True)
    sentiment_analysis.compute_extreme_reviews_polarity(reviews,
                                                        commit_polarities=True, freeling_lang='en')

    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True, load_sentences=True, load_words=True)
    for review in reviews:
        print(review.review, " : ", review.polarities["optimistic"].pos_score, ", ",
              review.polarities["optimistic"].neg_score, ", ",
              review.polarities["optimistic"].obj_score)


def commit_pessimistic_polarity():
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids, load_sentences=True, load_words=True)
    sentiment_analysis.compute_extreme_reviews_polarity(reviews,
                                                        commit_polarities=True, pessimistic=True, freeling_lang='en')

    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True, load_sentences=True, load_words=True)
    for review in reviews:
        print(review.review, " : ", review.polarities["pessimistic"].pos_score, ", ",
              review.polarities["pessimistic"].neg_score, ", ",
              review.polarities["pessimistic"].obj_score)


def commit_pattern_adj_cc_polarity():
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_sentences=True, load_words=True, load_deptrees=True)
    sentiment_analysis.compute_pattern_reviews_polarity(reviews, commit_polarities=True)

    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True, load_sentences=True, load_words=True)
    for review in reviews:
        print(review.review, " : ", review.polarities["pattern_adj_cc"].pos_score, ", ",
              review.polarities["pattern_adj_cc"].neg_score, ", ",
              review.polarities["pattern_adj_cc"].obj_score)


def commit_pattern_adj_polarity():
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_sentences=True, load_words=True, load_deptrees=True)
    sentiment_analysis.compute_pattern_reviews_polarity(reviews, commit_polarities=True, cc_pattern=False)

    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True, load_sentences=True, load_words=True)
    for review in reviews:
        print(review.review, " : ", review.polarities["pattern_adj"].pos_score, ", ",
              review.polarities["pattern_adj"].neg_score, ", ",
              review.polarities["pattern_adj"].obj_score)


def commit_pattern_cc_polarity():
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_sentences=True, load_words=True, load_deptrees=True)
    sentiment_analysis.compute_pattern_reviews_polarity(reviews, commit_polarities=True, adj_pattern=False)

    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_polarities=True, load_sentences=True, load_words=True)
    for review in reviews:
        print(review.review, " : ", review.polarities["pattern_cc"].pos_score, ", ",
              review.polarities["pattern_cc"].neg_score, ", ",
              review.polarities["pattern_cc"].obj_score)


def test_polarity_pie_charts():
    import loacore.load.file_load as file_load
    import loacore.analysis.sentiment_analysis as sentiment_analysis
    import loacore.utils.plot_polarities as plot_polarities
    import os
    from loacore import RESULT_PATH

    ids = file_load.get_id_files_by_file_paths([r'./uci/.+'])
    files = file_load.load_database(id_files=ids)
    polarities = sentiment_analysis.compute_simple_files_polarity(files)
    plot_polarities.save_polarity_pie_charts(polarities,
                                             file_path=os.path.join(RESULT_PATH, 'sentiment_analysis', 'simple', 'uci'),
                                             file_name='uci_polarity_pie_charts.pdf')


def test_check_polarities():
    import loacore.load.file_load as file_load
    import loacore.analysis.polarity_check as polarity_check

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_sentences=False)
    polarity_check.check_polarity(files)


def test_pattern_polarity():

    import loacore.load.file_load as file_load
    import loacore.load.review_load as review_load
    import loacore.analysis.sentiment_analysis as sentiment_analysis

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/yelp_labelled.txt'])
    reviews = review_load.load_reviews_by_id_files(id_files=ids,
                                                   load_sentences=True, load_words=True, load_deptrees=True)
    sentiment_analysis.compute_pattern_reviews_polarity(reviews)

    for review in reviews:
        print(review.review, " : ", review.polarities["pattern_adj_cc"].pos_score, ", ",
              review.polarities["pattern_adj_cc"].neg_score, ", ",
              review.polarities["pattern_adj_cc"].obj_score)


# commit_simple_polarity()
# commit_optimistic_polarity()
# commit_pessimistic_polarity()
# test_pattern_polarity()
# test_check_polarities()
# commit_pattern_adj_cc_polarity()
# commit_pattern_adj_polarity()
# commit_pattern_cc_polarity()
# test_check_polarities()
test_polarity_pie_charts()
