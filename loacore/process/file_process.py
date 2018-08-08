import sqlite3 as sql
from loacore import DB_PATH
from loacore.classes.classes import File


def add_files(file_paths, encoding='windows-1252', lang="es"):
    """
    This function performs the full process on all the file_paths specified, and add the results to the corresponding
    tables.

    :param file_paths: Paths used to load files
    :type file_paths: :obj:`list` of :obj:`path-like object`
    :param encoding: Files encoding.
    :param lang:
        Specify language used by Freeling. Default : 'es'.\n
        Possible values : 'as', 'ca', 'cs', 'cy', 'de', 'en', 'es', 'fr', 'gl', 'hr', 'it', 'nb', 'pt', 'ru', 'sl')\n
        See https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/basics.html for more details.
    :type lang: String
    :type encoding: String

    :Example:

    Process and load file from the relative directory *data/raw/*

    .. code-block:: python

       file_paths = []
       for dirpath, dirnames, filenames in os.walk(os.path.join('data', 'raw')):
           for name in filenames:
               file_paths.append(os.path.join(dirpath, name))

       file_process.add_files(file_paths)

    """
    from loacore import set_lang
    set_lang(lang)

    conn = sql.connect(DB_PATH)
    c = conn.cursor()

    # Add files
    files = []
    for file_path in file_paths:
        c.execute("INSERT INTO File (File_Path) VALUES (?)", [file_path])

        # Get back id of last inserted file
        c.execute("SELECT last_insert_rowid()")
        id_file = c.fetchone()[0]

        # Keep trace of added Files
        files.append(File(id_file, file_path))

    conn.commit()
    conn.close()

    # ********************************************* RAW DATA ********************************************************* #

    # Add all reviews from all files
    print("==> Normalization")
    import loacore.process.review_process as review_process
    reviews = review_process.add_reviews_from_files(files, encoding=encoding)

    # ****************************************** POLARITY LABEL ****************************************************** #
    print("==> Adding polarities to DB")
    import loacore.process.polarity_process as polarity_process
    polarity_process.add_polarity_from_reviews(reviews)

    # ********************************************* FREELING ********************************************************* #

    splitted_reviews = split_reviews(reviews)
    review_count = 1
    for reviews in splitted_reviews:
        print("\nProcessing review " + str(review_count) + "/" + str(len(splitted_reviews)))
        print("==> Tokenization")
        # Tokenization + Add all sentences and all words from all reviews
        import loacore.process.sentence_process as sentence_process
        added_sentences = sentence_process.add_sentences_from_reviews(reviews)
        print("Added sentences : " + str(len(added_sentences)))

        # Reload sentences with words
        import loacore.load.sentence_load as sentence_load
        sentences = sentence_load.load_sentences(id_sentences=[s.id_sentence for s in added_sentences], load_words=True)

        # Lemmatization
        print("==> Lemmatization")
        import loacore.process.lemma_process as lemma_process
        lemma_process.add_lemmas_to_sentences(sentences)

        # Disambiguation
        print("==> Disambiguation")

        import loacore.process.synset_process as synset_process
        synset_process.add_synsets_to_sentences(sentences)

        # Synset polarities
        print("Adding synset polarities...")
        synset_process.add_polarity_to_synsets()

        # Dep tree
        print("Dependency tree processing...")
        import loacore.process.deptree_process as deptree_process
        deptree_process.add_dep_tree_from_sentences(sentences)


def split_reviews(reviews):
    split_reviews_list=[]
    n = int(len(reviews)/1000)
    split_number = 0
    for i in range(n):
        split_number += len(reviews[i*1000:(i+1)*1000])
        split_reviews_list.append(reviews[i*1000:(i+1)*1000])

    if n*1000 < len(reviews):
        split_number += len(reviews[n*1000:len(reviews)])
        split_reviews_list.append(reviews[n*1000:len(reviews)])

    print("Reviews number : " + str(len(reviews)))
    print("Split into : " + str(len(split_reviews_list)) + "(total : " + str(split_number) + ")")

    return split_reviews_list
