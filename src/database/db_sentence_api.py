import sqlite3 as sql
import ressources.pyfreeling as freeling
from src.database.classes import Sentence


def load_sentences_list_by_ids(id_sentences):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for id_sentence in id_sentences:
        sentences = []
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                  "WHERE ID_Sentence = " + str(id_sentence))
        result = c.fetchone()
        if result is not None:
            sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    conn.close()
    return sentences


def load_sentences_list_by_id_review(id_review):
    sentences = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
              "WHERE ID_Review = " + str(id_review))
    results = c.fetchall()
    for result in results:
        sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    conn.close()
    return sentences


def load_sentences_in_reviews(reviews):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for review in reviews:
        review_sentences = []
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree FROM Sentence "
                  "WHERE ID_Review = " + str(review.id_review))
        results = c.fetchall()
        for result in results:
            review_sentences.append(Sentence(result[0], result[1], result[2], result[3]))
        review.set_sentences(review_sentences)


def add_sentences_from_reviews(reviews):
    tk, sp = init_freeling()

    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()

    for review in reviews:
        raw_review = review.get_review()
        tokens = tk.tokenize(raw_review)
        sentences = sp.split(tokens)

        review_index = 0
        sql_sentences = []
        for sentence in sentences:
            sql_sentences.append((review.get_id_review(), str(review_index)))
            c.execute("INSERT INTO Sentence (ID_Review, Review_Index) "
                  "VALUES (?, ?)", (review.get_id_review(), str(review_index)))
            review_index += 1
            c.execute("SELECT last_insert_rowid()")
            id_sentence = c.fetchone()[0]
            sql_words = []
            sentence_index = 0
            for word in sentence:
                sql_words.append((id_sentence, sentence_index, word.get_form()))
                sentence_index += 1
            c.executemany("INSERT INTO Word (ID_Sentence, Sentence_Index, word) VALUES (?, ?, ?)", sql_words)

    conn.commit()
    conn.close()


def init_freeling():
    freeling.util_init_locale("default");

    lang = "es"
    ipath = "/usr/local"
    # path to language data
    lpath = ipath + "/share/freeling/" + lang + "/"
    tk = freeling.tokenizer(lpath + "tokenizer.dat");
    sp = freeling.splitter(lpath + "splitter.dat");

    return tk, sp