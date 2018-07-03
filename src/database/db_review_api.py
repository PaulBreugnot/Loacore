import sqlite3 as sql
import src.database.db_file_api as file_api
import src.process.normalization as norm


def main():
    add_reviews_from_file('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt')
    print(list_reviews('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt'))


def add_review(id_file, file_index, review):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("INSERT INTO Review (ID_File, File_Index, Review) "
              "VALUES (" + str(id_file) + ", " + str(file_index) + ", '" + review + "');")
    conn.commit()
    conn.close()


def list_reviews(file_path):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Review")
    #c.execute("SELECT * FROM Review JOIN File WHERE File_Path = '" + file_path + "'")
    result = c.fetchall()
    conn.close()

    return result


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

    raw_text = file_api.load_file(id_file).read()
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


if __name__ == "__main__":
    main()