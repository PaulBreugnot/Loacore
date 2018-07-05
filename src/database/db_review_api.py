import sqlite3 as sql
import src.database.db_file_api as file_api
import src.process.normalization as norm
from src.database.classes import Review


def load_reviews_list_by_ids(id_reviews):
    reviews = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for id_review in id_reviews:
        c.execute("SELECT ID_Review, Review.ID_File, File_Index, Review "
                  "FROM Review WHERE ID_Review = " + str(id_review))
        result = c.fetchone()
        if result is not None:
            reviews.append(Review(result[0], result[1], result[2], result[3]))

    return reviews


def load_reviews_by_id_file(id_file):
    reviews = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_Review, ID_File, File_Index, Review "
              "FROM Review WHERE ID_File = " + str(id_file))
    results = c.fetchall()
    for result in results:
        reviews.append(Review(result[0], result[1], result[2], result[3]))
    return reviews


def load_reviews_in_files(files):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    for file in files:
        file_reviews = []
        c.execute("SELECT ID_Review, ID_File, File_Index, Review "
                  "FROM Review WHERE ID_File = " + str(file.get_id_file()))
        results = c.fetchall()
        for result in results:
            file_reviews.append(Review(result[0], result[1], result[2], result[3]))
        file.set_reviews(file_reviews)

    conn.close()


def count_reviews(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT count(ID_Review) FROM Review JOIN File ON Review.ID_File = File.ID_File "
              "WHERE File_Path = '" + file_path + "'")
    return c.fetchone()[0]


def add_reviews_from_files(files):
    """
    Load files from file system, normalize and add reviews to database.
    :param files: list of files from which reviews must be added
    :return: added reviews
    """
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    sql_reviews = []
    for file in files:
        c.execute("SELECT ID_File FROM File WHERE ID_File = " + file.get_id_file())

        raw_text = file_api.load_file(file.get_id_file()).load().read()

        # Normalization
        reviews = norm.normalize(raw_text)

        file_index = 0
        for review in reviews:
            sql_reviews.append((file.get_id_file(), file_index, review))
            file_index += 1

    c.executemany("INSERT INTO Review (ID_File, File_Index, Review) "
                  "VALUES (?, ?, ?)", sql_reviews)
    conn.commit()
    conn.close()

    return sql_reviews

