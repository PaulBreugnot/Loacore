import sqlite3 as sql


def main():
    #add_file('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt')
    print(list_files())
    #load_file(7)


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


def list_files():
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute('SELECT * FROM File')
    result = c.fetchall()
    conn.close()

    return result


def load_file(id_file):
    conn = sql.connect('../../data/database/reviews.db')
    c = conn.cursor()
    c.execute("SELECT File_Path FROM File WHERE ID_File = " + str(id_file))
    path = c.fetchone()[0]
    conn.close()

    return open(path, encoding='windows-1252')


def process(file_path):
    '''

    :param file_path: file to process and store in db
    :return: nothing
    This function will made all the possible processes applicable to the file, feeding the complete database.
    '''


if __name__ == "__main__":
    main()