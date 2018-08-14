import os
import sqlite3 as sql
from loacore.conf import DB_PATH
import resources.pyfreeling as freeling
from loacore.utils.status import ProcessState


def add_lemmas_to_sentences(sentences, print_lemmas=False, _state_queue=None, _id_process=None, freeling_modules=None):
    """

    Performs a Freeling process to add lemmas to words.\n
    However, the argument is actually a sentence to better fit Freeling usage.\n
    Our sentences will be converted to a Freeling Sentences before processing.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    :param sentences: Sentences to process
    :type sentences: :obj:`list` of |Sentence|
    :param print_lemmas: If True, print lemmatization results
    :type print_lemmas: boolean
    """
    from loacore.utils.db import safe_commit

    freeling_sentences = [sentence.compute_freeling_sentence() for sentence in sentences]

    if freeling_modules is None:
        if _state_queue is not None:
            _state_queue.put(
                ProcessState(_id_process, os.getpid(), "Loading Freeling...", " - "))
        morfo = init_freeling()
    else:
        morfo = freeling_modules


    # Print sentence
    _lemmatization_state(_state_queue, _id_process)

    processed_sentences = morfo.analyze(freeling_sentences)

    # Copy freeling results into our Words
    for s in range(len(sentences)):
        sentence = sentences[s]

        if not len(sentence.words) == len(processed_sentences[s]):
            print("/!\\ Warning, sentence offset error in lemma_process /!\\")
            print(sentence.sentence_str())
            print([w.get_form() for w in processed_sentences[s]])

        for w in range(len(sentence.words)):
            word = sentence.words[w]
            word.lemma = processed_sentences[s][w].get_lemma()
            if print_lemmas:
                print(word.word + " : " + word.lemma)

    # Add lemmas to database
    conn = sql.connect(DB_PATH, timeout=1800)
    c = conn.cursor()

    sentence_count = 0
    total_sentence = len(sentences)
    _commit_state(_state_queue, _id_process, " - ", " - ")
    for sentence in sentences:
        # Print state
        sentence_count += 1
        _commit_state(_state_queue, _id_process, sentence_count, total_sentence)

        for word in sentence.words:
            # Add Lemma to Lemma Table
            c.execute("INSERT INTO Lemma (Lemma, ID_Word) VALUES (?, ?)", (word.lemma, word.id_word))

            # Get back id of last inserted lemma
            c.execute("SELECT last_insert_rowid()")
            id_lemma = c.fetchone()[0]

            # Update Word table
            c.execute("UPDATE Word SET ID_Lemma = " + str(id_lemma) + " WHERE ID_Word = " + str(word.id_word))

    print("")
    safe_commit(conn, 0, _state_queue, _id_process)

    conn.close()


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
    #  then, (de)activate required modules
    morfo.set_active_options(False,  # UserMap
                             False,  # NumbersDetection,
                             True,  # PunctuationDetection,
                             False,  # DatesDetection,
                             True,  # DictionarySearch,
                             False,  # AffixAnalysis,
                             False,  # CompoundAnalysis,
                             False,  # RetokContractions,
                             False,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             False)  # ProbabilityAssignment

    return morfo


def _lemmatization_state(state_queue, id_process):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(), "Lemmatization", "-"))
    else:
        print("Lemmatization", end="\n")


def _commit_state(state_queue, id_process, sentence_count, total_sentence):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(), "Lemma DB commit...", str(sentence_count) + " / " + str(total_sentence)))
    else:
        print("\r" + str(sentence_count) + " / " + str(total_sentence) + " sentences added.", end="")
