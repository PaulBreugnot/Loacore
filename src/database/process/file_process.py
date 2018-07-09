import os
import sqlite3 as sql
from src.database.classes.classes import File


def add_files(file_paths):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    # Add files
    files = []
    for file_path in file_paths:
        c.execute("INSERT INTO File (File_Path) VALUES ('" + file_path + "');")

        # Get back id of last inserted file
        c.execute("SELECT last_insert_rowid()")
        id_file = c.fetchone()[0]

        # Keep trace of added Files
        files.append(File(id_file, file_path))

    conn.commit()
    conn.close()

    # ********************************************* RAW DATA ********************************************************* #

    # Add all reviews from all files
    import src.database.process.review_process as review_process
    reviews = review_process.add_reviews_from_files(files)

    # ********************************************* FREELING ********************************************************* #

    # Tokenization + Add all sentences and all words from all reviews
    import src.database.process.sentence_process as sentence_process
    sentence_process.add_sentences_from_reviews(reviews)

    # Reload sentences with words
    import src.database.load.sentence_load as sentence_load
    sentences = sentence_load.load_sentences()

    # Lemmatization
    import src.database.process.lemma_process as lemma_process
    lemma_process.add_lemmas_to_sentences(sentences)

    # Disambiguation
    import src.database.process.synset_process as synset_process
    synset_process.add_synsets_to_sentences(sentences)

    # Synset polarities
    synset_process.add_polarity_to_synsets()

    # Dep tree
    import src.database.process.deptree_process as deptree_process
    deptree_process.add_dep_tree_from_sentences(sentences)