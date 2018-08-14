
def check_db():
    """
    Performs a basic database check, printing some information about the amount of data currently in the database.
    """
    import sqlite3 as sql
    from loacore.conf import DB_PATH

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    # File check
    c.execute("SELECT count(*) FROM File")
    files_num = c.fetchone()[0]

    # Files without reviews?
    c.execute("SELECT count(*) FROM File "
              "WHERE ID_File NOT IN "
              "(SELECT ID_File FROM Review GROUP BY ID_File)")
    files_without_reviews = c.fetchone()[0]

    # Review check
    c.execute("SELECT count(*) FROM Review")
    reviews_num = c.fetchone()[0]

    # Reviews without sentences?
    c.execute("SELECT count(*) FROM Review "
              "WHERE ID_Review NOT IN "
              "(SELECT ID_Review FROM Sentence GROUP BY ID_Review)")
    reviews_without_sentence = c.fetchone()[0]

    # Sentence check
    c.execute("SELECT count(*) FROM Sentence")
    sentence_num = c.fetchone()[0]

    # Sentences without words?
    c.execute("SELECT count(*) FROM Sentence "
              "WHERE ID_Sentence NOT IN "
              "(SELECT ID_Sentence FROM Word GROUP BY ID_Sentence)")
    sentences_without_word = c.fetchone()[0]

    # Word check
    c.execute("SELECT count(*) FROM Word")
    word_num = c.fetchone()[0]
    c.execute("SELECT count(*) FROM Lemma")
    word_lemma_number = c.fetchone()[0]
    c.execute("SELECT count(*) FROM Synset")
    word_synset_count = c.fetchone()[0]
    c.execute("SELECT count(*) FROM Word WHERE PoS_tag != ''")
    tagged_words = c.fetchone()[0]
    c.execute("SELECT count(*) FROM Word WHERE ID_Word NOT IN "
              "(SELECT ID_Word FROM Dep_Tree_Node GROUP BY ID_WORD)")
    unlabelled_words = c.fetchone()[0]

    # Dep trees check
    # We consider dep trees as consistent if each node that is not a root has exactly one parent.
    c.execute("SELECT count(*) FROM "
              "(SELECT count(*) AS num_parent "
              "FROM ("
              "SELECT ID_Parent_Node, ID_Child_Node "
              "FROM Dep_Tree_Node_Children "
              "WHERE ID_Child_Node "
              "IN (SELECT ID_Dep_Tree_Node FROM Dep_Tree_Node WHERE root = 0)) "
              "GROUP BY ID_Child_Node ) "
              "WHERE num_parent != 1")
    dep_trees_consistency = (c.fetchone()[0] == 0)

    print("Files\n=====")
    print("Files : " + str(files_num))
    print("Files without review : " + str(files_without_reviews))
    print("\nReviews\n=======")
    print("Reviews : " + str(reviews_num))
    print("Reviews without sentence : " + str(reviews_without_sentence))
    print("Note : "
          "Those reviews are usually only composed of too long sentences, that's why their sentences are not parsed.")
    print("\nSentences\n=========")
    print("Sentences : " + str(sentence_num))
    print("Sentences without words : " + str(sentences_without_word))
    print("\nWords\n=====")
    print("Words : " + str(word_num))
    print("Lemmatized words : " + str(word_lemma_number))
    print("Words with synsets : " + str(word_synset_count))
    print("Tagged words : " + str(tagged_words))
    print("Unlabelled words : " + str(unlabelled_words))
    print("\nDependency trees\n=================")
    print("Consistency : ", end="")
    if dep_trees_consistency:
        print("\u001b[32mOK\u001b[0m")
    else:
        print("\u001b[31mSome nodes are without parents.\u001b[0m")


def main():
    check_db()


if __name__ == "__main__":
    main()