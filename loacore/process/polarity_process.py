import sqlite3 as sql
from loacore import DB_PATH


def add_polarity_from_reviews(reviews):
    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    for review in reviews:
        # We assume that polarity values have already been extracted in add_reviews_from_files
        for polarity in review.polarities.values():
            c.execute("INSERT INTO Polarity (Analysis, ID_Review, Pos_Score, Neg_Score, Obj_Score) "
                      "VALUES (?, ?, ?, ?, ?)",
                      (polarity.analysis, review.id_review,
                       polarity.pos_score, polarity.neg_score, polarity.obj_score))

    conn.commit()
    conn.close()


def commit_polarities(reviews, label):

    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    for review in reviews:
        polarity = review.polarities[label]
        c.execute("INSERT INTO Polarity (Analysis, ID_Review, Pos_Score, Neg_Score, Obj_Score) "
                  "VALUES (?, ?, ?, ?, ?)",
                  (polarity.analysis, review.id_review,
                   polarity.pos_score, polarity.neg_score, polarity.obj_score))

    conn.commit()
    conn.close()