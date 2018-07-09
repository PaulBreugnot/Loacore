import os
import sqlite3 as sql
from src.database.classes.classes import Synset


def load_synsets_list(id_synsets):
    synsets = []
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    for id_synset in id_synsets:
        c.execute("SELECT ID_Synset, ID_Word, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                  "FROM Synset WHERE ID_Synset = " + str(id_synset))
        result = c.fetchone()
        if result is not None:
            synsets.append(Synset(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    return synsets


def load_synsets_in_words(words):
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()
    for word in words:
        if word.id_synset is not None:
            c.execute("SELECT ID_Synset, ID_Word, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score "
                      "FROM Synset WHERE ID_Synset = " + str(word.id_synset))
            result = c.fetchone()
            word.synset = Synset(result[0], result[1], result[2], result[3], result[4], result[5], result[6])

    conn.close()


def load_synsets():
    conn = sql.connect(os.path.join('..', '..', 'data', 'database', 'reviews.db'))
    c = conn.cursor()

    synsets = []
    c.execute("SELECT ID_Synset, ID_Word, Synset_Code, Synset_Name, Neg_Score, Pos_Score, Obj_Score FROM Synset")
    results = c.fetchall()
    for result in results:
        synsets.append(Synset(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    conn.close()
    return synsets

