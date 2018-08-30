import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import File


def _load_files_by_id_files(id_files):

    # Load files with specified ids, only initialized with id_file and file_path

    from loacore.conf import DB_TIMEOUT
    files = []
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    for id_file in id_files:
        c.execute("SELECT ID_File, File_Name FROM File WHERE ID_File = " + str(id_file))
        result = c.fetchone()
        if result is not None:
            files.append(File(result[0], result[1]))

    conn.close()
    return files


def _load_files():

    from loacore.conf import DB_TIMEOUT
    # Load all the files of the database, only initialized with id_file and file_path

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("SELECT ID_File, File_Name FROM File")

    files = []
    results = c.fetchall()
    for result in results:
        files.append(File(result[0], result[1]))

    conn.close()
    return files


def load_database(id_files=(),
                  load_reviews=True, load_polarities=True, load_sentences=True, load_words=True, load_deptrees=True,
                  load_in_temp_file=False,
                  workers=1):
    """
    Load the complete database as a :obj:`list` of |File| , with all the dependencies specified in parameters
    loaded in them.

    :param id_files: If specified, load only the files with the corresponding ids. Otherwise, load all the files.
    :type id_files: :obj:`list` of :obj:`int`
    :param load_reviews: Specify if Reviews need to be loaded if files.
    :type load_reviews: bool
    :param load_polarities: If Reviews have been loaded, specify if Polarities need to be loaded in reviews.
    :type load_polarities: bool
    :param load_sentences: If Reviews have been loaded, specify if Sentences need to be loaded in reviews.
    :type load_sentences: bool
    :param load_words: If Sentences have been loaded, specify if Words need to be loaded in sentences.
    :type load_words: bool
    :param load_deptrees: If Words have been loaded, specify if DepTrees need to be loaded in sentences.
    :type load_deptrees: bool
    :param workers:
        Number of workers used to load database.\n
        If *workers* <= 0, Multiprocessing is not used and all the program is run in a unique process.\n
        if *workers* > 0, *workers* processes are created in addition of the main process. This is useful to take
        advantage of multi-core architectures to greatly speed up the process.
    :type workers: int
    :param load_in_temp_file:
        If True, loaded reviews are stored in temporary file and |File| reviews attribute becomes
        a :class:`~loacore.utils.data_stream.ReviewIterator`. This option is useful, and even necessary, when huge files
        are loaded to manage RAM usage.
    :type load_in_temp_file: bool
    :return: loaded files
    :rtype: :obj:`list` of |File|

    .. note::
        Among the dependencies, only the load_deptrees should be set to False to significantly reduce processing
        time if they are not needed. Loading other structures is quite fast.

    :Example:
        Load files 1,2,3 with only their :attr:`id_file` and :attr:`id_path`.

        >>> import loacore.load.file_load as file_load
        >>> files = file_load.load_database(id_files=[1, 2, 3], load_reviews=False)
        >>> print([f.file_name for f in files])
        ['../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_EO.txt',
        '../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_CC.txt',
        '../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_GR.txt']

    :Example:
        Load the first 10 files without Dep Trees.

        >>> import loacore.load.file_load as file_load
        >>> files = load_database(id_files=range(1, 11), load_deptrees=False)
        >>> print(files[3].reviews[8].review)
        que sea mas grande el parqueadero

    :Example:
        Load the complete database.

        >>> import loacore.load.file_load as file_load
        >>> files = load_database()
        >>> print(len(files))
        33

    """

    # Load Files
    if len(id_files) == 0:
        files = _load_files()
    else:
        files = _load_files_by_id_files(id_files)

    if load_reviews:
        # Load Reviews
        import loacore.load.review_load as review_load
        from loacore.process.file_process import _split_reviews
        from loacore.utils.data_stream import ReviewIterator
        from loacore.utils.data_stream import save_to_temp_file

        review_load.load_reviews_in_files(files)
        split_size = 500

        # Maps id_files to review subsets
        split_reviews = {}
        for file in files:
            # Ensure that each subset come from a unique file
            split_reviews[file.id_file] = _split_reviews(file.reviews, split_size)

        if workers <= 0:
            for file in files:
                if load_in_temp_file:
                    file.reviews = ReviewIterator()
                for review_sublist in split_reviews[file.id_file]:
                    _load_reviews_process(load_polarities, load_sentences, load_words, load_deptrees,
                                          review_sublist)
                    if load_in_temp_file:
                        file.reviews.temp_file_list.append(save_to_temp_file(review_sublist))

        else:
            from multiprocessing import Process, Queue
            import queue

            process_queue = queue.Queue()
            result_queue = Queue()

            id_file_map = {f.id_file: f for f in files}
            for file in files:
                if load_in_temp_file:
                    file.reviews = ReviewIterator()
                else:
                    file.reviews = []
                for review_sublist in split_reviews[file.id_file]:
                    process_queue.put(Process(
                        target=_load_reviews_process,
                        args=(load_polarities, load_sentences, load_words, load_deptrees, review_sublist),
                        kwargs={"_result_queue": result_queue, "_id_file": file.id_file}))

            # Main launcher
            running_processes = []
            while not process_queue.empty():

                    # Launch processes
                    if len(running_processes) < workers:
                        p = process_queue.get()
                        p.start()
                        running_processes.append(p)
                    terminated_processes = []

                    # Check terminated processes
                    for p in running_processes:
                        if not p.is_alive():
                            terminated_processes.append(p)
                    for p in terminated_processes:
                        running_processes.remove(p)

                    # Check results
                    while not result_queue.empty():
                        result = result_queue.get()
                        if load_in_temp_file:
                            id_file_map[result[0]].reviews.temp_file_list.append(save_to_temp_file(result[1]))
                        else:
                            id_file_map[result[0]].reviews += result[1]

            # Wait for the end of last processes
            while len(running_processes) > 0:
                # Check terminated processes
                terminated_processes = []
                for p in running_processes:
                    if not p.is_alive():
                        terminated_processes.append(p)
                for p in terminated_processes:
                    running_processes.remove(p)

                # Check results
                while not result_queue.empty():
                    result = result_queue.get()
                    if load_in_temp_file:
                        id_file_map[result[0]].reviews.temp_file_list.append(save_to_temp_file(result[1]))
                    else:
                        id_file_map[result[0]].reviews += result[1]

    return files


def _load_reviews_process(load_polarities, load_sentences, load_words, load_deptrees, reviews,
                          _id_file=None, _result_queue=None):
    import os
    print("[" + str(os.getpid()) + "] Process initialized.")
    if load_polarities:
        # Load Polarities
        print("[" + str(os.getpid()) + "] Loading polarities...")
        import loacore.load.polarity_load as polarity_load
        polarity_load.load_polarities_in_reviews(reviews)

    if load_sentences:
        # Load Sentences
        print("[" + str(os.getpid()) + "] Loading sentences...")
        import loacore.load.sentence_load as sentence_load
        sentences = sentence_load.load_sentences_in_reviews(reviews)

        if load_words:
            # Load Words
            print("[" + str(os.getpid()) + "] Loading words...")
            import loacore.load.word_load as word_load
            word_load.load_words_in_sentences(sentences)
            if load_deptrees:
                # Load DepTrees
                print("[" + str(os.getpid()) + "] Loading dep trees...")
                import loacore.load.deptree_load as deptree_load
                deptree_load.load_dep_tree_in_sentences(sentences)
    if _result_queue is not None:
        # Multiprocess return
        _result_queue.put((_id_file, reviews))
    else:
        # Normal return
        return reviews


def get_id_files_by_file_path(file_path_re):
    """
    This function can be used to retrieve file ids in database from their path.\n
    For more information about how Python regular expressions work, see https://docs.python.org/3/library/re.html .

    :param file_path_re: Regular expression to check
    :type file_path_re: :obj:`str`
    :return: Ids of matching files.
    :rtype: :obj:`list` of :obj:`int`

    :Example:
    Find if files of files in an uci folder.

        >>> import loacore.load.file_load as file_load
        >>> ids = file_load.get_id_files_by_file_path(r'.*/uci/.+')
        >>> print(ids)
        [1, 2, 3]

    .. note::

        The full path of a file (as saved in the database) can be used as a regular expression.

    """
    import re

    id_files = []
    files = load_database(load_reviews=False, load_sentences=False, load_words=False, load_deptrees=False)
    for file in files:
        regexp = file_path_re
        if re.fullmatch(regexp, file.file_name) is not None:
            id_files.append(file.id_file)

    return list(set(id_files))


def remove_files(files):
    """
    Remove specified files from database. Implemented references will also engender the deletion of all files
    dependencies in database.

    :param files: :obj:`list` of |File|
    """
    from loacore.conf import DB_TIMEOUT
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = on")
    for file in files:
        c.execute("DELETE FROM File WHERE File_Path = '" + file.file_name + "'")

    conn.commit()
    conn.close()


def clean_db():
    """
    Remove all files from database. Implemented references will also engender the deletion of all files
    dependencies in database : all the tables will be emptied.
    """
    from loacore.conf import DB_TIMEOUT
    print("Cleaning all database...")
    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    c.execute("DELETE FROM File")
    c.execute("DELETE FROM Review")
    c.execute("DELETE FROM Sentence")
    c.execute("DELETE FROM Word")
    c.execute("DELETE FROM Synset")
    c.execute("DELETE FROM Lemma")
    c.execute("DELETE FROM Dep_Tree")
    c.execute("DELETE FROM Dep_Tree_Node")
    c.execute("DELETE FROM Dep_Tree_Node_Children")
    c.execute("DELETE FROM Polarity")
    conn.commit()
    conn.close()


