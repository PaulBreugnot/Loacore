import sqlite3 as sql
from src.database.classes import File




'''
def main():
    #add_file('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt')
    files = load_files(load_reviews=True)
    for file in files:
        print(file.get_id_file())
        print(file.get_file_path())
        for review in file.get_reviews():
            print(file.get_file_path())
            print(review.get_review())
    #load_file(7)
'''


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

