import os
import sqlite3 as sql
from src.database.classes.classes import Review


def load_reviews_list_by_ids(id_reviews):
    reviews = []
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    for id_review in id_reviews:
        c.execute("SELECT ID_Review, Review.ID_File, File_Index, Review "
                  "FROM Review WHERE ID_Review = " + str(id_review) + " ORDER BY File_Index")
        result = c.fetchone()
        if result is not None:
            reviews.append(Review(result[0], result[1], result[2], result[3]))

    conn.close()
    return reviews


def load_reviews_by_id_file(id_file):
    reviews = []
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    c.execute("SELECT ID_Review, ID_File, File_Index, Review "
              "FROM Review WHERE ID_File = " + str(id_file) + " ORDER BY File_Index")
    results = c.fetchall()
    for result in results:
        reviews.append(Review(result[0], result[1], result[2], result[3]))

    conn.close()
    return reviews


def load_reviews_in_files(files):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    loaded_reviews = []

    for file in files:
        file_reviews = []
        c.execute("SELECT ID_Review, ID_File, File_Index, Review "
                  "FROM Review WHERE ID_File = " + str(file.id_file) + " ORDER BY File_Index")
        results = c.fetchall()
        for result in results:
            file_reviews.append(Review(result[0], result[1], result[2], result[3]))
        file.reviews = file_reviews
        loaded_reviews += file_reviews

    conn.close()
    return loaded_reviews


def count_reviews(file_path):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    c.execute("SELECT count(ID_Review) FROM Review JOIN File ON Review.ID_File = File.ID_File "
              "WHERE File_Path = '" + file_path + "'")

    conn.close()
    return c.fetchone()[0]


