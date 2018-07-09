import os
import re
import sqlite3 as sql
from src.database.classes.classes import Review


def add_reviews_from_files(files):
    """
    Load files from file system, normalize and add reviews to database.
    :param files: list of files from which reviews must be added
    :return: added reviews
    """
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    added_reviews = []

    for file in files:

        # Load review as a string
        raw_text = file.load().read()

        # Normalization and review splitting
        reviews = normalize(raw_text)

        # Add reviews
        file_index = 0
        for review in reviews:
            sql_review = (file.id_file, file_index, review)

            c.execute("INSERT INTO Review (ID_File, File_Index, Review) "
                      "VALUES (?, ?, ?)", sql_review)

            # Get back id of last inserted review
            c.execute("SELECT last_insert_rowid()")
            id_review = c.fetchone()[0]

            # Keep trace of added reviews
            added_reviews.append(Review(id_review, file.id_file, file_index, review))

            file_index += 1

    conn.commit()
    conn.close()

    return added_reviews


def normalize(text):
    normalized_string = text.lower()
    reviews = re.findall(r'.+', normalized_string, re.MULTILINE)
    return reviews