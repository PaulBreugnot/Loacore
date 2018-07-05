import sqlite3 as sql
import ressources.pyfreeling as freeling

def load_lemmas_list(id_lemmas):
    lemmas = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for id_lemma in id_lemmas:
        c.execute("SELECT Lemma FROM Lemma WHERE ID_Lemma = '" + str(id_lemma) + "'")
        result = c.fetchone()
        if result is not None:
            lemmas.append(result[0])

    conn.close()
    return lemmas


def load_lemmas_in_words(words):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for word in words:
        if word.id_lemma is not None:
            c.execute("SELECT Lemma FROM Lemma WHERE ID_Lemma = '" + str(word.id_lemma) + "'")
            result = c.fetchone()
            word.set_lemma(result[0])

    conn.close()


def add_lemmas_to_sentences(sentences):
    """
    This function will perform a Freeling process to add Lemmas to words.
    However, the argument is actually a sentence to better fit Freeling usage.
    Our Sentence will be converted to a Freeling Sentence before processing.
    :param sentences: A list of src.database.classes.Sentence
    :return:
    """

    freeling_sentences = [sentence.freeling_sentence() for sentence in sentences]

    morfo = init_freeling()

    freeling_sentences = morfo.analyze(freeling_sentences)


def my_maco_options(lang,lpath) :

    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.DictionaryFile = lpath + "dicc.src"
    opt.PunctuationFile = lpath + "../common/punct.dat"
    return opt


def init_freeling():

    freeling.util_init_locale("default")

    lang = "es"
    ipath = "/usr/local"
    # path to language data
    lpath = ipath + "/share/freeling/" + lang + "/"

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
                             True,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             False)  # ProbabilityAssignment

    return morfo
