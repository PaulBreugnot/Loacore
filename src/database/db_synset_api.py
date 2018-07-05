import sqlite3 as sql
import ressources.pyfreeling as freeling
from nltk.corpus import wordnet as wn
from src.database.classes import Synset


def load_synsets_list(id_synsets):
    synsets = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for id_synset in id_synsets:
        c.execute("SELECT ID_Synset, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                  "FROM Synset WHERE ID_Synset = " + str(id_synset))
        result = c.fetchone()
        if result is not None:
            synsets.append(Synset(result[0], result[1], result[2], result[4], result[5]))

    return synsets


def load_synsets_in_words(words):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for word in words:
        if word.id_synset is not None:
            c.execute("SELECT ID_Synset, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                      "FROM Synset WHERE ID_Synset = " + str(word.id_synset))
            result = c.fetchone()
            word.set_synset(Synset(result[0], result[1], result[2], result[4], result[5]))

    conn.close()

def add_synsets_to_sentences(sentences):
    """
    Disambiguation.
    This function will perform a Freeling process to disambiguate words of the sentences according to their context
    (UKB algorithm) linking them to a unique synset (if possible).
    Our Sentence will be converted to a Freeling Sentence before processing.
    Notice that even if we may have computed the Lemma for example, Freeling Sentences generated from our sentences are
    "raw sentences", without any analysis linked to their Words. So we make all the freeling process since the
    beginning every time (except tokenization and sentence splitting) to avoid any confusion.
    :param sentences: A list of src.database.classes.Sentence
    :return:
    """

    freeling_sentences = [sentence.compute_freeling_sentence() for sentence in sentences]

    morfo, tagger, sen, wsd = init_freeling()

    print(len(freeling_sentences))
    # perform morphosyntactic analysis and disambiguation
    freeling_sentences = morfo.analyze(freeling_sentences)
    freeling_sentences = tagger.analyze(freeling_sentences)
    # annotate and disambiguate senses
    freeling_sentences = sen.analyze(freeling_sentences)
    freeling_sentences = wsd.analyze(freeling_sentences)
    print(len(freeling_sentences))

    # Copy freeling results into our Words
    for s in range(len(sentences)):
        sentence = sentences[s]
        for w in range(len(sentence.words)):
            word = sentence.words[w]
            rank = freeling_sentences[s][w].get_senses()
            if len(rank) > 0:
                print("Word : " + word.word)
                print("Synset code : " + rank[0][0])
                print("Synset name : " + wn.of2ss(rank[0][0]).name())


def my_maco_options(lang,lpath) :

    # create options holder
    opt = freeling.maco_options(lang);

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = "";
    opt.ProbabilityFile = lpath + "probabilitats.dat";
    opt.DictionaryFile = lpath + "dicc.src";
    opt.PunctuationFile = lpath + "../common/punct.dat";
    return opt;


def init_freeling():

    freeling.util_init_locale("default")

    lang = "es"
    ipath = "/usr/local"
    # path to language data
    lpath = ipath + "/share/freeling/" + lang + "/"

    # create the analyzer with the required set of maco_options
    morfo = freeling.maco(my_maco_options(lang, lpath))

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
                             True);  # ProbabilityAssignment

    # create tagger
    tagger = freeling.hmm_tagger(lpath + "tagger.dat", False, 2)

    # create sense annotator
    sen = freeling.senses(lpath + "senses.dat")
    # create sense disambiguator
    wsd = freeling.ukb(lpath + "ukb.dat")

    return morfo, tagger, sen, wsd