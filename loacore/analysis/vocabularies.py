from loacore import DB_PATH
import sqlite3 as sql


def word_count(file):
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT count(*) FROM "
              "(SELECT DISTINCT word "
              "FROM Word "
              "JOIN Sentence ON Word.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Review.ID_Review = Sentence.ID_Sentence "
              "WHERE Review.ID_File = " + str(file.id_file) + ")")

    return int(c.fetchone()[0])


def lemma_count(file):
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT count(*) FROM "
              "(SELECT DISTINCT Lemma "
              "FROM Word "
              "JOIN Lemma ON Word.ID_Lemma = Lemma.ID_Lemma "
              "JOIN Sentence ON Word.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Review.ID_Review = Sentence.ID_Sentence "
              "WHERE Review.ID_File = " + str(file.id_file) + ")")

    return int(c.fetchone()[0])


def synset_count(file):
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT count(*) FROM "
              "(SELECT DISTINCT Synset_Name "
              "FROM Word "
              "JOIN Synset ON Word.ID_Synset = Synset.ID_Synset "
              "JOIN Sentence ON Word.ID_Sentence = Sentence.ID_Sentence "
              "JOIN Review ON Review.ID_Review = Sentence.ID_Sentence "
              "WHERE Review.ID_File = " + str(file.id_file) + ")")

    return int(c.fetchone()[0])