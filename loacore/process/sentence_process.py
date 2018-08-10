import os
import sys
import sqlite3 as sql
from loacore.conf import DB_PATH
import resources.pyfreeling as freeling
from loacore.classes.classes import Sentence


def add_sentences_from_reviews(reviews):
    """

    Performs the first Freeling process applied to each normalized review.\n
    Each review is tokenized, and then splitted into sentences, thanks to corresponding Freeling modules.\n
    A representation of the Sentences and their Words (tokens) are then added to corresponding tables.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :return: added sentences
    :rtype: :obj:`list` of |Sentence|
    """

    morfo, tk, sp = init_freeling()

    conn = sql.connect(DB_PATH, timeout=120)
    c = conn.cursor()

    added_sentences = []
    review_count = 0
    total_review = len(reviews)
    for review in reviews:
        review_count += 1
        print("\r" + str(review_count) + " / " + str(total_review) + " sentences added.", end="\n")
        sys.stdout.flush()
        raw_review = review.review
        tokens = tk.tokenize(raw_review)
        sentences = sp.split(tokens)
        sentences = morfo.analyze(sentences)

        review_index = 0
        for sentence in sentences:
            # Add sentence
            c.execute("INSERT INTO Sentence (ID_Review, Review_Index) "
                      "VALUES (?, ?)", (review.id_review, review_index))
            conn.commit()

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

def my_maco_options(lang, lpath):

    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.DictionaryFile = os.path.join(lpath, "dicc.src")
    opt.PunctuationFile = os.path.join(lpath, "..", "common", "punct.dat")
    return opt


def init_freeling():
    freeling.util_init_locale("default")

    from loacore.conf import lang
    from loacore.conf import LANG_PATH as lpath

    # create the analyzer with the required set of maco_options
    morfo = freeling.maco(my_maco_options(lang, lpath))

    morfo.set_active_options(False,  # UserMap
                             False,  # NumbersDetection,
                             True,  # PunctuationDetection,
                             False,  # DatesDetection,
                             True,  # DictionarySearch,
                             False,  # AffixAnalysis,
                             False,  # CompoundAnalysis,
                             True,  # RetokContractions,
                             False,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             False)  # ProbabilityAssignment

    tk = freeling.tokenizer(os.path.join(lpath, "tokenizer.dat"))
    sp = freeling.splitter(os.path.join(lpath, "splitter.dat"))

    return morfo, tk, sp
