import os
import sqlite3 as sql
import ressources.pyfreeling as freeling
from nltk.corpus import wordnet as wn
from src.database.classes.classes import Synset


def add_synsets_to_sentences(sentences, print_synsets = False):
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

    # perform morphosyntactic analysis and disambiguation
    freeling_sentences = morfo.analyze(freeling_sentences)
    freeling_sentences = tagger.analyze(freeling_sentences)
    # annotate and disambiguate senses
    freeling_sentences = sen.analyze(freeling_sentences)
    freeling_sentences = wsd.analyze(freeling_sentences)

    # Copy freeling results into our Words
    for s in range(len(sentences)):
        sentence = sentences[s]
        for w in range(len(sentence.words)):
            word = sentence.words[w]
            rank = freeling_sentences[s][w].get_senses()
            if len(rank) > 0:
                word.synset = Synset(None, word.id_word, rank[0][0], wn.of2ss(rank[0][0]).name(), None, None, None)
                if print_synsets:
                    print("Word : " + word.word)
                    print("Synset code : " + rank[0][0])
                    print("Synset name : " + wn.of2ss(rank[0][0]).name())

    # Add synsets to database

    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    for sentence in sentences:
        for word in sentence.words:
            synset = word.synset

            if synset is not None:
                # Add synset
                c.execute("INSERT INTO Synset (ID_Word, Synset_Code, Synset_Name) "
                          "VALUES (" + str(word.id_word) + ", '" + synset.synset_code + "', '" + synset.synset_name + "')")

                # Get back id of last inserted review
                c.execute("SELECT last_insert_rowid()")
                id_synset = c.fetchone()[0]

                # Update Word table
                c.execute("UPDATE Word SET ID_Synset = " + str(id_synset) + " WHERE ID_Word = " + str(word.id_word))

    conn.commit()
    conn.close()


def add_polarity_to_synsets():
    from nltk.corpus import sentiwordnet as swn
    from src.database.load import synset_load
    """
    This no argument fonction add the positive/negative/objective polarity of all the synsets currently in the table
    Synset, from the SentiWordNet corpus.
    :return:
    """
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    synsets = synset_load.load_synsets()

    for synset in synsets:
        synset.pos_score = swn.senti_synset(synset.synset_name).pos_score()
        if synset.pos_score is not None:
            # There is an entry in the SentiWordNet database for our synset
            synset.neg_score = swn.senti_synset(synset.synset_name).neg_score()
            synset.obj_score = 1 - (synset.pos_score + synset.neg_score)

            c.execute("UPDATE Synset SET (Pos_Score, Neg_Score, Obj_Score) "
                      "= (" + str(synset.pos_score) + ", " + str(synset.neg_score) + ", " + str(synset.obj_score) + ") "
                      "WHERE Id_Synset = " + str(synset.id_synset))

    conn.commit()
    conn.close()


# ********************************************* Freeling Options****************************************************** #

def my_maco_options(lang, lpath):

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