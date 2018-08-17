import os
import sqlite3 as sql
from loacore.conf import DB_PATH
from nltk.corpus import wordnet as wn
from loacore.classes.classes import Synset
from loacore.utils.status import ProcessState

import importlib
from loacore.conf import FREELING_API
freeling = importlib.import_module("freeling."I + FREELING_API+".pyfreeling")

def add_synsets_to_sentences(sentences, print_synsets=False,
                             _state_queue=None, _id_process=None, freeling_modules=None):
    """
    Performs a Freeling process to disambiguate words of the sentences according to their context
    (UKB algorithm) linking them to a unique synset (if possible).\n
    Our sentences are converted to Freeling Sentences before processing.\n
    Notice that even if we may have already computed the Lemmas for example, Freeling Sentences generated from our
    sentences are "raw sentences", without any analysis linked to their Words. So we make all the Freeling
    process from scratch every time, except *tokenization* and *sentence splitting*, to avoid any confusion.

    .. note:: This function should be used only inside the file_process.add_files() function.

    :param sentences: Sentences to process
    :type sentences: :obj:`list` of |Sentence|
    :param print_synsets: If True, print disambiguation results
    :type print_synsets: boolean
    """

    from loacore.conf import DB_TIMEOUT
    from loacore.utils.db import safe_commit, safe_execute

    freeling_sentences = [sentence.compute_freeling_sentence() for sentence in sentences]

    if freeling_modules is None:
        if _state_queue is not None:
            _state_queue.put(
                ProcessState(_id_process, os.getpid(), "Loading Freeling...", " - "))
        morfo, tagger, sen, wsd = init_freeling()
    else:
        morfo, tagger, sen, wsd = freeling_modules

    _disambiguation_state(_state_queue, _id_process)
    # perform morphosyntactic analysis and disambiguation
    processed_sentences = morfo.analyze(freeling_sentences)
    processed_sentences = tagger.analyze(processed_sentences)
    # annotate and disambiguate senses
    processed_sentences = sen.analyze(processed_sentences)
    processed_sentences = wsd.analyze(processed_sentences)

    # Copy freeling results into our Words
    for s in range(len(sentences)):
        sentence = sentences[s]

        if not len(sentence.words) == len(processed_sentences[s]):
            print("/!\\ Warning, sentence offset error in synset_process /!\\")
            print(sentence.sentence_str())
            print([w.get_form() for w in processed_sentences[s]])

        for w in range(len(sentence.words)):
            word = sentence.words[w]
            rank = processed_sentences[s][w].get_senses()
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

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    sentence_count = 0
    total_sentence = len(sentences)
    for sentence in sentences:
        # Print state
        sentence_count += 1
        _commit_state(_state_queue, _id_process, sentence_count, total_sentence)

        for word in sentence.words:
            synset = word.synset

            if synset is not None:
                # Add synset

                safe_execute(c,
                             "INSERT INTO Synset (ID_Word, Synset_Code, Synset_Name) "
                             "VALUES (?, ?, ?)",
                             0,
                             _state_queue,
                             _id_process,
                             mark_args=(word.id_word, synset.synset_code, synset.synset_name)
                             )

                # Get back id of last inserted review
                safe_execute(c,
                             "SELECT last_insert_rowid()",
                             0,
                             _state_queue,
                             _id_process)
                id_synset = c.fetchone()[0]

                # Update Word table
                safe_execute(c,
                             "UPDATE Word SET ID_Synset = " + str(id_synset) + " WHERE ID_Word = " + str(word.id_word),
                             0,
                             _state_queue,
                             _id_process)

    safe_commit(conn, 0, _state_queue, _id_process)

    conn.close()


def add_polarity_to_synsets(id_words, _state_queue=None, _id_process=None):
    """
    Adds the positive/negative/objective polarities of all the synsets currently in the table
    Synset, from the SentiWordNet corpus.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    """

    from nltk.corpus import sentiwordnet as swn
    from loacore.load import synset_load
    from loacore.utils.db import safe_commit, safe_execute
    from loacore.conf import DB_TIMEOUT

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    synsets = synset_load.load_synsets(id_synsets=synset_load.get_id_synsets_for_id_words(id_words))

    synset_count = 0
    total_synset = len(synsets)
    for synset in synsets:
        # Print state
        synset_count += 1
        _commit_polarity_state(_state_queue, _id_process, synset_count, total_synset)
        synset.pos_score = swn.senti_synset(synset.synset_name).pos_score()
        if synset.pos_score is not None:
            # There is an entry in the SentiWordNet database for our synset
            synset.neg_score = swn.senti_synset(synset.synset_name).neg_score()
            synset.obj_score = 1 - (synset.pos_score + synset.neg_score)

            safe_execute(c,
                         "UPDATE Synset SET (Pos_Score, Neg_Score, Obj_Score) "
                         "= (" + str(synset.pos_score) + ", " + str(synset.neg_score) + ", " + str(
                             synset.obj_score) + ") "
                         "WHERE Id_Synset = " + str(synset.id_synset),
                         0,
                         _state_queue,
                         _id_process
                         )

    if _state_queue is None:
        print("")
    safe_commit(conn, 0, _state_queue, _id_process)

    conn.close()


# ********************************************* Freeling Options****************************************************** #

def my_maco_options(lang, lpath):

    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.ProbabilityFile = os.path.join(lpath, "probabilitats.dat")
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
                             False,  # RetokContractions,
                             False,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             True)  # ProbabilityAssignment

    # create tagger
    tagger = freeling.hmm_tagger(os.path.join(lpath, "tagger.dat"), False, 2)

    # create sense annotator
    sen = freeling.senses(os.path.join(lpath, "senses.dat"))
    # create sense disambiguator
    wsd = freeling.ukb(os.path.join(lpath, "ukb.dat"))

    return morfo, tagger, sen, wsd


def _disambiguation_state(state_queue, id_process):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(), "Disambiguation", "-"))
    else:
        print("Disambiguation", end="\n")


def _commit_state(state_queue, id_process, sentence_count, total_sentence):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(), "Synset DB commit...", str(sentence_count) + " / " + str(total_sentence)))
    else:
        print("\r" + str(sentence_count) + " / " + str(total_sentence) + " sentences added.", end="")


def _commit_polarity_state(state_queue, id_process, sentence_count, total_sentence):
    if state_queue is not None:
        state_queue.put(
            ProcessState(id_process, os.getpid(),
                         "Add polarity to synset", str(sentence_count) + " / " + str(total_sentence)))
    else:
        print("\r" + str(sentence_count) + " / " + str(total_sentence) + " polarities added.", end="")