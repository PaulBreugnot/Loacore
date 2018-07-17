import os
import re
import sqlite3 as sql
from loacore.classes.classes import Review


def add_reviews_from_files(files, encoding):
    """

    Load argument files from file system and normalize their content.\n
    Compute Reviews objects and add them to the database.

    .. note:: This function should be used only inside the :func:`file_process.add_files()` function.

    :param files: :class:`File` s to process
    :type files: :obj:`list` of :class:`File`
    :param encoding: Encoding used to load files.
    :type encoding: String
    :return: added :class:`Review` s
    :rtype: :obj:`list` of :class:`Review`

    """
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    added_reviews = []

    for file in files:

        # Load review as a string
        raw_text = file.load(encoding=encoding).read()

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
    """

    Performs raw text normalization.

    - Convertion to lower case
    - Review splitting using python regular expressions : each new line correspond to a new review

    :param text: text to process
    :type text: string
    :return: reviews
    :rtype: :obj:`list` of :obj:`string`
    """
    normalized_string = text.lower()
    reviews = re.findall(r'.+', normalized_string, re.MULTILINE)
    return reviews
