import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import Polarity


def load_polarities_in_reviews(reviews):

    conn = sql.connect(DB_PATH)
    c = conn.cursor()
    for review in reviews:
        c.execute("SELECT ID_Polarity, Analysis, ID_Review, Pos_Score, Neg_Score, Obj_Score "
                  "FROM Polarity "
                  "WHERE ID_Review = " + str(review.id_review))
        results = c.fetchall()
        for result in results:
            review.polarities[result[1]] = Polarity(result[0], result[1], result[2], result[3], result[4], result[5])