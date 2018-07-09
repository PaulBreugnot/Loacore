import os
import sqlite3 as sql
from src.database.classes.classes import File


def load_files_by_id_files(id_files):
    files = []
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    for id_file in id_files:
        c.execute("SELECT ID_File, File_Path FROM File WHERE ID_File = " + str(id_file))
        result = c.fetchone()
        if result is not None:
            files.append(File(result[0], result[1]))

    conn.close()
    return files


def load_files():
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Path FROM File")

    files = []
    results = c.fetchall()
    for result in results:
        files.append(File(result[0], result[1]))

    conn.close()
    return files


def load_database(load_reviews=True, load_sentences=True, load_words=True, load_deptrees=True):

    # Load Files
    files = load_files()

    if load_reviews:
        # Load Reviews
        import src.database.load.review_load as review_load
        reviews = review_load.load_reviews_in_files(files)

        if load_sentences:
            # Load Sentences
            import src.database.load.sentence_load as sentence_load
            sentences = sentence_load.load_sentences_in_reviews(reviews)

            if load_words:
                # Load Words
                import src.database.load.word_load as word_load
                word_load.load_words_in_sentences(sentences)

                if load_deptrees:
                    # Load DepTrees
                    import src.database.load.deptree_load as deptree_load
                    deptree_load.load_dep_tree_in_sentences(sentences)

    return files


def remove_files(files):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = on")
    for file in files:
        c.execute("DELETE FROM File WHERE File_Path = '" + file.file_path + "'")

    conn.commit()
    conn.close()


def clean_db():

    """
    Thanks to implemented references, delete the content of File table will also delete in cascade all the
    dependencies : all the others tables.
    :return: nothing
    """
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    c.execute("DELETE FROM File")
    conn.commit()
    conn.close()


