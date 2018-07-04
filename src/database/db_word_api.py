import sqlite3 as sql
import src.database.classes.Word as Word


def load_words_list_by_ids(id_words, load_lemmas=True, load_synsets=True):
    words = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for id_word in id_words:
        c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag FROM Word "
                  "WHERE ID_Word = " + str(id_word))
        result = c.fetchone()
        if result is not None:
            words.append(Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    if load_lemmas:
        import src.database.db_lemma_api as db_lemma_api
        db_lemma_api.load_lemmas_in_words(words)
    if load_synsets:
        import src.database.db_synset_api as db_synset_api
        db_synset_api.load_synsets_in_words(words)

    conn.close()
    return words


def load_words_list_by_id_sentence(id_sentence, load_lemmas=True, load_synsets=True):
    words = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag FROM Word "
              "WHERE ID_Sentence = " + str(id_sentence))
    results = c.fetchall()
    for result in results:
        words.append(Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    if load_lemmas:
        import src.database.db_lemma_api as db_lemma_api
        db_lemma_api.load_lemmas_in_words(words)
    if load_synsets:
        import src.database.db_synset_api as db_synset_api
        db_synset_api.load_synsets_in_words(words)

    conn.close()
    return words


def load_words_in_sentences(sentences, load_lemmas=True, load_synsets=True):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    words = []
    for sentence in sentences:
        sentence_words = []
        c.execute("SELECT ID_Word, ID_Sentence, Sentence_Index, word, ID_Lemma, ID_Synset, PoS_tag "
                  "FROM Word"
                  "WHERE ID_Sentence = " + str(sentence.get_id_sentence()))
        results = c.fetchall()
        for result in results:
            sentence_words.append(Word(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
        sentence.set_words(sentence_words)
        words.append(sentence_words)

    if load_lemmas:
        import src.database.db_lemma_api as db_lemma_api
        db_lemma_api.load_lemmas_in_words(words)
    if load_synsets:
        import src.database.db_synset_api as db_synset_api
        db_synset_api.load_synsets_in_words(words)

    conn.close()
