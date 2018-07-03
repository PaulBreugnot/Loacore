import sqlite3 as sql


def main():
    list_files()


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
    print(c.fetchall())

    conn.close()


def process(file_path):
    '''

    :param file_path: file to process and store in db
    :return: nothing
    This function will made all the possible processes applicable to the file, feeding the complete database.
    '''


if __name__ == "__main__":
    main()