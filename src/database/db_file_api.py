import sqlite3 as sql
from src.database.classes import File


def load_files_by_id_files(id_files):
    files = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for id_file in id_files:
        c.execute("SELECT ID_File, File_Path FROM File WHERE ID_File = " + str(id_file))
        result = c.fetchone()
        if result is not None:
            files.append(File(result[0], result[1]))

    conn.close()
    return files


def load_files():
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Path FROM File")

    files = []
    results = c.fetchall()
    for result in results:
        files.append(File(result[0], result[1]))

    conn.close()
    return files


def load_database():

    # Load Files
    files = load_files()

    # Load Reviews
    import src.database.db_review_api as review_api
    reviews = review_api.load_reviews_in_files(files)

    # Load Sentences
    import src.database.db_sentence_api as sentence_api
    sentences = sentence_api.load_sentences_in_reviews(reviews)

    # Load Words
    import src.database.db_word_api as word_api
    word_api.load_words_in_sentences(sentences)

    return files


def add_files(file_paths):
    conn = sql.connect('../../data/database/reviews.db')
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
    import src.database.db_review_api as review_api
    reviews = review_api.add_reviews_from_files(files)

    # ********************************************* FREELING ********************************************************* #

    # Tokenization + Add all sentences and all words from all reviews
    import src.database.db_sentence_api as sentence_api
    sentence_api.add_sentences_from_reviews(reviews)

    # Lemmatization
    import src.database.db_lemma_api as lemma_api
    import src.database.db_sentence_api as sentence_api
    sentences = sentence_api.load_sentences()
    lemma_api.add_lemmas_to_sentences(sentences)


def remove_file(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("DELETE FROM File WHERE File_Path = '" + file_path + "';")

    conn.commit()
    conn.close()



