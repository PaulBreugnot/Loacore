import sqlite3 as sql
import ressources.pyfreeling as freeling
from src.database.classes import Sentence


def load_sentences(id_reviews):
    for id_review in id_reviews:
        sentences = []
        conn = sql.connect('../../data/database/reviews.db')
        c = conn.cursor()
        c.execute("SELECT ID_Sentence, ID_Review, Review_Index, ID_Dep_Tree, Sentence FROM Sentence "
                  "WHERE ID_Sentence = " + str(id_review))
        results = c.fetchall()
        for result in results:
            sentences.append(Sentence(result[0], result[1], result[2], result[3]))

    conn.close()
    return sentences


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