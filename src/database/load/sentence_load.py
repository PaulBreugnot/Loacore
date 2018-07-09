import os
import sqlite3 as sql
from src.database.classes.classes import Sentence


def load_sentences_list_by_ids(id_sentences):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    for id_sentence in id_sentences:
        sentences = []
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                  "WHERE ID_Sentence = " + str(id_sentence) + " ORDER BY Review_Index")
        result = c.fetchone()
        if result is not None:
            sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    conn.close()
    return sentences


def load_sentences_list_by_id_review(id_review):
    sentences = []
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
              "WHERE ID_Review = " + str(id_review) + " ORDER BY Review_Index")
    results = c.fetchall()
    for result in results:
        sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    conn.close()
    return sentences


def load_sentences_in_reviews(reviews):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    loaded_sentences = []

    for review in reviews:
        review_sentences = []
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                  "WHERE ID_Review = " + str(review.id_review) + " ORDER BY Review_Index")
        results = c.fetchall()
        for result in results:
            review_sentences.append(Sentence(result[0], result[1], result[2], result[3]))
        review.sentences = review_sentences
        loaded_sentences += review_sentences

    conn.close()
    return loaded_sentences


def load_sentences():
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    loaded_sentences = []

    c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree "
              "FROM Sentence ORDER BY ID_Review, Review_Index")
    results = c.fetchall()
    for result in results:
        loaded_sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    # Load Words
    import src.database.load.word_load as word_api
    word_api.load_words_in_sentences(loaded_sentences)

    conn.close()
    return loaded_sentences
