import sqlite3 as sql
import src.database.db_file_api as file_api
import src.process.normalization as norm
from src.database.classes import Review


#def main():
    #add_reviews_from_file('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt')
    #print(list_reviews('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt'))
    #load_reviews('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt')
    #print(count_reviews('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt'))


def load_reviews(file_path):
    reviews = []
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_Review, Review.ID_File, File_Index, Review "
              "FROM Review JOIN File ON Review.ID_File = File.ID_File WHERE File_Path = '" + file_path + "'")
    results = c.fetchall()
    for result in results:
        reviews.append(Review(result[0], result[1], result[2], result[3]))
    return reviews


def count_reviews(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT count(ID_Review) FROM Review JOIN File ON Review.ID_File = File.ID_File WHERE File_Path = '" + file_path + "'")
    return c.fetchone()[0]


def add_reviews_from_file(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT ID_File FROM File WHERE File_Path = '" + file_path + "'")
    try:
        result = c.fetchone()
        if result is not None:
            id_file = result[0]
        else:
            raise ValueError("File " + file_path + " does not belong to database.")
    except ValueError as e:
        print('\n')
        print(e)
        return

    print(id_file)
    raw_text = file_api.load_file(id_file).load().read()
    reviews = norm.normalize(raw_text)

    sql_reviews = []
    file_index = 0
    for review in reviews:
        sql_reviews.append((id_file, file_index, review))
        file_index += 1

    c.executemany("INSERT INTO Review (ID_File, File_Index, Review) "
                  "VALUES (?, ?, ?)", sql_reviews)
    conn.commit()
    conn.close()

