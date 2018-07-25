import sqlite3 as sql
from loacore import DB_PATH
import ressources.pyfreeling as freeling
from nltk.corpus import wordnet as wn
from loacore.classes.classes import Synset


def add_synsets_to_sentences(sentences, print_synsets=False):
    """
    Performs a Freeling process to disambiguate words of the sentences according to their context
    (UKB algorithm) linking them to a unique synset (if possible).\n
    Our :class:`Sentence` s are converted to Freeling Sentences before processing.\n
    Notice that even if we may have already computed the Lemmas for example, Freeling Sentences generated from our
    :class:`Sentence` s are "raw sentences", without any analysis linked to their Words. So we make all the Freeling
    process from scratch every time, except *tokenization* and *sentence splitting*, to avoid any confusion.

    .. note:: This function should be used only inside the file_process.add_files() function.

    :param sentences: :class:`Sentence` s to process
    :type sentences: :obj:`list` of :class:`Sentence`
    :param print_synsets: If True, print disambiguation results
    :type print_synsets: boolean
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
                if not rank[0][0][0] == '8':
                    # ignore synsets offsets 8.......-.
                    # they are odd synsets that WordNet can't find...
                    word.synset = Synset(None, word.id_word, rank[0][0], wn.of2ss(rank[0][0]).name(), None, None, None)
                if print_synsets:
                    print("Word : " + word.word)
                    print("Synset code : " + rank[0][0])
                    print("Synset name : " + wn.of2ss(rank[0][0]).name())

    # Add synsets to database

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    for sentence in sentences:
        for word in sentence.words:
            synset = word.synset

            if synset is not None:
                # Add synset
                c.execute("INSERT INTO Synset (ID_Word, Synset_Code, Synset_Name) "
                          "VALUES (?, ?, ?)", (word.id_word, synset.synset_code, synset.synset_name))

                # Get back id of last inserted review
                c.execute("SELECT last_insert_rowid()")
                id_synset = c.fetchone()[0]

                # Update Word table
                c.execute("UPDATE Word SET ID_Synset = " + str(id_synset) + " WHERE ID_Word = " + str(word.id_word))

    conn.commit()
    conn.close()


def add_polarity_to_synsets():
    """
    Adds the positive/negative/objective polarities of all the synsets currently in the table
    Synset, from the SentiWordNet corpus.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    """

    from nltk.corpus import sentiwordnet as swn
    from loacore.load import synset_load

    conn = sql.connect(DB_PATH)
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
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = ""
    opt.ProbabilityFile = lpath + "probabilitats.dat"
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
                             True)  # ProbabilityAssignment

    # create tagger
    tagger = freeling.hmm_tagger(lpath + "tagger.dat", False, 2)

    # create sense annotator
    sen = freeling.senses(lpath + "senses.dat")
    # create sense disambiguator
    wsd = freeling.ukb(lpath + "ukb.dat")

    return morfo, tagger, sen, wsd
