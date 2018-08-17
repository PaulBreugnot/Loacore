import os
import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import Sentence
from loacore.utils.status import ProcessState

import importlib
from loacore.conf import FREELING_API
freeling = importlib.import_module("freeling" + FREELING_API+".pyfreeling")


def add_sentences_from_reviews(reviews, _state_queue=None, _id_process=None, freeling_modules=None):
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
    from loacore.classes.classes import Word
    from loacore.utils.db import safe_commit, safe_execute
    from loacore.conf import DB_TIMEOUT

    if freeling_modules is None:
        if _state_queue is not None:
            _state_queue.put(
                ProcessState(_id_process, os.getpid(), "Loading Freeling...", " - "))
        morfo, tk, sp = init_freeling()
    else:
        morfo, tk, sp = freeling_modules

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    added_sentences = []
    review_count = 0
    total_review = len(reviews)
    for review in reviews:

        # Print state
        review_count += 1
        _tokenization_state(_state_queue, _id_process, review_count, total_review)

        raw_review = review.review
        tokens = tk.tokenize(raw_review)
        sentences = sp.split(tokens)
        sentences = morfo.analyze(sentences)

        review_index = 0

        for sentence in sentences:

            if len(sentence) <= 50:
                review_sentence = Sentence(None, review.id_review, review_index, None)

                review_index += 1

                # Add words
                sentence_index = 0
                for word in sentence:
                    review_sentence.words.append(Word(None, None, sentence_index, word.get_form(), None, None, None))
                    sentence_index += 1

                review.sentences.append(review_sentence)

    sentence_count = 0
    total_sentence = len([s for r in reviews for s in r.sentences])
    for r in reviews:
        for s in r.sentences:

            # Print state
            sentence_count += 1
            _commit_state(_state_queue, _id_process, sentence_count, total_sentence)

            # Add sentence
            safe_execute(c,
                         "INSERT INTO Sentence (ID_Review, Review_Index) "
                         "VALUES (?, ?)",
                         0,
                         _state_queue,
                         _id_process,
                         mark_args=(s.id_review, s.review_index)
                         )

            # Get back id of last inserted sentence
            safe_execute(c,
                         "SELECT last_insert_rowid()",
                         0,
                         _state_queue,
                         _id_process)
            id_sentence = c.fetchone()[0]
            s.id_sentence = id_sentence

            sql_words = []
            for w in s.words:
                w.id_sentence = id_sentence
                sql_words.append((id_sentence, w.sentence_index, w.word))
                safe_execute(c,
                             "INSERT INTO Word (ID_Sentence, Sentence_Index, word) VALUES (?, ?, ?)",
                             0,
                             _state_queue,
                             _id_process,
                             mark_args=sql_words,
                             execute_many=True)
            added_sentences.append(s)

    if _state_queue is None:
        print("")

    safe_commit(conn, 0, _state_queue, _id_process)

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


def _tokenization_state(state_queue, id_process, review_count, total_review):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(), "Tokenization", str(review_count) + " / " + str(total_review)))
    else:
        print("\r" + str(review_count) + " / " + str(total_review) + " reviews processed.", end="")


def _commit_state(state_queue, id_process, sentence_count, total_sentence):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(), "Token DB commit...", str(sentence_count) + " / " + str(total_sentence)))
    else:
        print("\r" + str(sentence_count) + " / " + str(total_sentence) + " sentences added.", end="")
