
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


# commit_simple_polarity()
commit_optimistic_polarity()
