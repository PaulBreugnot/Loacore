import sqlite3 as sql
from src.database.classes import File


def load_files_by_id_files(id_files, load_reviews=False):
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


def load_files(load_reviews=False):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Path FROM File")

    files = []
    results = c.fetchall()
    for result in results:
        files.append(File(result[0], result[1], load_reviews))
    conn.close()
    return files


def add_file(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("INSERT INTO File (File_Path) VALUES ('" + file_path + "');")

    conn.commit()
    conn.close()


def remove_file(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("DELETE FROM File WHERE File_Path = '" + file_path + "';")

    conn.commit()
    conn.close()


def load_file(id_file, load_reviews=False):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Path FROM File WHERE ID_File = " + str(id_file))
    result = c.fetchone()
    conn.close()

    return File(result[0], result[1], load_reviews)


def load_files(load_reviews=False):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Path FROM File")

    files = []
    results = c.fetchall()
    for result in results:
        files.append(File(result[0], result[1], load_reviews))
    conn.close()
    return files


def process(file_path):
    '''

    :param file_path: file to process and store in db
    :return: nothing
    This function will made all the possible processes applicable to the file, feeding the complete database.
    '''

