import os
import sqlite3 as sql
import ressources.pyfreeling as freeling
from src.database.classes.classes import Sentence


def add_sentences_from_reviews(reviews):
    """

    Performs the first Freeling process applied to each normalized review.\n
    Each review is tokenized, and then splitted into sentences, thanks to corresponding Freeling modules.\n
    A representation of the Sentences and their Words (tokens) are then added to corresponding tables.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    :param reviews: :class:`Review` s to process
    :type reviews: :obj:`list` of :class:`Review`
    :return: added :class:`Sentence` s
    :rtype: :obj:`list` of :class:`Sentence`
    """

    tk, sp = init_freeling()

    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    added_sentences = []
    for review in reviews:
        raw_review = review.review
        tokens = tk.tokenize(raw_review)
        sentences = sp.split(tokens)

        review_index = 0
        for sentence in sentences:

            # Add sentence
            c.execute("INSERT INTO Sentence (ID_Review, Review_Index) "
                      "VALUES (?, ?)", (review.id_review, str(review_index)))

            # Get back id of last inserted sentence
            c.execute("SELECT last_insert_rowid()")
            id_sentence = c.fetchone()[0]

            # Keep trace of added sentences
            added_sentence = Sentence(id_sentence, review.id_review, review_index, None)
            added_sentences.append(added_sentence)

            review_index += 1

            # Add words
            sql_words = []
            sentence_index = 0
            for word in sentence:
                sql_words.append((id_sentence, sentence_index, word.get_form()))
                sentence_index += 1
            c.executemany("INSERT INTO Word (ID_Sentence, Sentence_Index, word) VALUES (?, ?, ?)", sql_words)

    conn.commit()
    conn.close()

    return added_sentences


# ********************************************* Freeling Options****************************************************** #

def init_freeling():
    freeling.util_init_locale("default");

    lang = "es"
    ipath = "/usr/local"
    # path to language data
    lpath = ipath + "/share/freeling/" + lang + "/"

    tk = freeling.tokenizer(lpath + "tokenizer.dat");
    sp = freeling.splitter(lpath + "splitter.dat");

    return tk, sp
