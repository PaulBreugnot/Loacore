import os
import sqlite3 as sql
from loacore import DB_PATH
import resources.pyfreeling as freeling


def add_lemmas_to_sentences(sentences, print_lemmas=False):
    """

    Performs a Freeling process to add lemmas to :class:`Word` s.\n
    However, the argument is actually a sentence to better fit Freeling usage.\n
    Our :class:`Sentence` s will be converted to a Freeling Sentences before processing.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    :param sentences: :class:`Sentence` s to process
    :type sentences: :obj:`list` of :class:`Sentence`
    :param print_lemmas: If True, print lemmatization results
    :type print_lemmas: boolean
    """

    freeling_sentences = [sentence.compute_freeling_sentence() for sentence in sentences]

    morfo = init_freeling()

    freeling_sentences = morfo.analyze(freeling_sentences)

    # Copy freeling results into our Words
    for s in range(len(sentences)):
        sentence = sentences[s]
        for w in range(len(sentence.words)):
            word = sentence.words[w]
            word.lemma = freeling_sentences[s][w].get_lemma()
            if print_lemmas:
                print(word.word + " : " + word.lemma)

    # Add lemmas to database
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    for sentence in sentences:
        for word in sentence.words:
            # Add Lemma to Lemma Table
            c.execute("INSERT INTO Lemma (Lemma, ID_Word) VALUES (?, ?)", (word.lemma, word.id_word))

            # Get back id of last inserted lemma
            c.execute("SELECT last_insert_rowid()")
            id_lemma = c.fetchone()[0]

            # Update Word table
            c.execute("UPDATE Word SET ID_Lemma = " + str(id_lemma) + " WHERE ID_Word = " + str(word.id_word))

    conn.commit()
    conn.close()


# ********************************************* Freeling Options****************************************************** #

def my_maco_options(lang, lpath):

    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.DictionaryFile = lpath + "dicc.src"
    opt.PunctuationFile = lpath + "../common/punct.dat"
    return opt


def init_freeling():

    freeling.util_init_locale("default")

    import loacore
    lang = loacore.lang
    # path to language data
    lpath = loacore.LANG_PATH

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
