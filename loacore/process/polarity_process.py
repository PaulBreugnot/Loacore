import sqlite3 as sql
from loacore.conf import DB_PATH


def add_polarity_from_reviews(reviews):
    conn = sql.connect(DB_PATH, timeout=60)
    c = conn.cursor()

    polarity_count = 0
    total_polarity = len([p for r in reviews for p in r.polarities.values()])
    for review in reviews:
        # We assume that polarity values have already been extracted in add_reviews_from_files
        for polarity in review.polarities.values():
            polarity_count += 1
            print("\r" + str(polarity_count) + " / " + str(total_polarity) + " polarities added.", end="")
            c.execute("INSERT INTO Polarity (Analysis, ID_Review, Pos_Score, Neg_Score, Obj_Score) "
                      "VALUES (?, ?, ?, ?, ?)",
                      (polarity.analysis, review.id_review,
                       polarity.pos_score, polarity.neg_score, polarity.obj_score))
    print("")
    conn.commit()

    conn.close()


def commit_polarities(reviews, label):

    conn = sql.connect(DB_PATH, timeout=60)
    c = conn.cursor()
    for review in reviews:
        polarity = review.polarities[label]
        c.execute("INSERT INTO Polarity (Analysis, ID_Review, Pos_Score, Neg_Score, Obj_Score) "
                  "VALUES (?, ?, ?, ?, ?)",
                  (polarity.analysis, review.id_review,
                   polarity.pos_score, polarity.neg_score, polarity.obj_score))
        conn.commit()

    conn.close()
