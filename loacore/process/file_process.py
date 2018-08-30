import sqlite3 as sql
from loacore.conf import DB_PATH
from loacore.classes.classes import File

from pyFreelingApi import freeling_api as freeling


def add_files(file_paths, encoding='utf8', lang="", workers=1):
    """
    This function performs the full process on all the file_paths specified, and add the results to the corresponding
    tables. While file a processing and adding to the database, the :class:`~loacore.utils.db.database_backup` is used
    so that if an error occurs during the full process (including a user interruption) the database is restored as it
    was before the call of this function.

    :param file_paths: Paths used to load files
    :type file_paths: :obj:`list` of |path-like-object|
    :param encoding: Files encoding.
    :param lang:
        If specify, *lang* will be used as Freeling language.
        Otherwise, default language is used (See :mod:`loacore`) \n
        Possible values : 'as', 'ca', 'cs', 'cy', 'de', 'en', 'es', 'fr', 'gl', 'hr', 'it', 'nb', 'pt', 'ru', 'sl')\n
        See https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/basics.html for more details.
    :type lang: str
    :type encoding: str
    :param workers:
        Number of workers used to perform Freeling processes.\n
        If *workers* <= 0, Multiprocessing is not used and all the programm is run in a unique process.\n
        if *workers* > 0, *workers* processes are created in addition of the main process. This is useful to take
        advantage of multi-core architectures to greatly speed up the process.

        .. note::

            To control the state of each process when *workers* > 0, a Python curses app is opened. Notice that
            seems to work badly in PyCharm terminal.

    :type workers: int

    :Example:

    Process and load file from the relative directory *data/raw/*

    .. code-block:: python

       file_paths = []
       for dirpath, dirnames, filenames in os.walk(os.path.join('data', 'raw')):
           for name in filenames:
               file_paths.append(os.path.join(dirpath, name))

       file_process.add_files(file_paths)

    """
    from loacore.conf import DB_TIMEOUT
    from loacore.utils.db import database_backup

    if not lang == "":
        from loacore.conf import _set_temp_lang
        _set_temp_lang(lang)

    conn = sql.connect(DB_PATH, timeout=DB_TIMEOUT)
    c = conn.cursor()

    with database_backup():
        # Add files
        files = []
        for file_path in file_paths:
            c.execute("INSERT INTO File (File_Name) VALUES (?)", [file_path])
            conn.commit()

            # Get back id of last inserted file
            c.execute("SELECT last_insert_rowid()")
            id_file = c.fetchone()[0]

            # Keep trace of added Files
            files.append(File(id_file, file_path))

        conn.close()

        # ********************************************* RAW DATA ******************************************************#

        # Add all reviews from all files
        print("==> Normalization")
        import loacore.process.review_process as review_process
        reviews = review_process.add_reviews_from_files(files, encoding=encoding)

        # ****************************************** POLARITY LABEL ***************************************************#
        print("==> Adding polarities to DB")
        import loacore.process.polarity_process as polarity_process
        polarity_process.add_polarity_from_reviews(reviews)

        # ********************************************* FREELING ********************************************************* #

        split_reviews = _split_reviews(reviews, 500)
        # reviews.clear()

        freeling_modules = load_all_freeling_modules()

        if workers <= 0:
            review_count = 0
            total_reviews = len(split_reviews)
            for reviews in split_reviews[0:1]:
                print("\nProcess review " + str(review_count) + " / " + str(total_reviews))
                _split_reviews_process(reviews, freeling_modules)

        else:
            from multiprocessing import Process, Queue
            import queue
            process_queue = queue.Queue()

            index = 0

            state_queue = Queue(maxsize=100)

            for reviews in split_reviews:
                index += 1
                process_queue.put(
                    Process(
                        target=_split_reviews_process,
                        args=(reviews, freeling_modules),
                        kwargs={'_state_queue': state_queue, '_id_process': index}))

            running_processes = []

            import os
            import sys
            from loacore.conf import OUTPUT_PATH
            with open(os.path.join(OUTPUT_PATH, "log.out"), "w") as log_file,\
                    open(os.path.join(OUTPUT_PATH, "error_log.out"), "w") as error_log_file:
                sys.stdout = log_file
                sys.stderr = error_log_file

                printer = Process(target=_print_states_process, args=(index, state_queue))
                printer.start()

                while not process_queue.empty():
                        if len(running_processes) < workers:
                            p = process_queue.get()
                            p.start()
                            running_processes.append(p)
                        terminated_processes = []
                        for p in running_processes:
                            if not p.is_alive():
                                terminated_processes.append(p)
                        for p in terminated_processes:
                            running_processes.remove(p)
                for p in running_processes:
                    p.join()

                running_processes.clear()
                printer.join()

        if not lang == "":
            from loacore.conf import _load_conf
            _load_conf()


def _split_reviews(reviews, split_size):
    import loacore.utils.data_stream as data_stream
    split_reviews_list = []
    n = int(len(reviews)/split_size)
    split_number = 0
    for i in range(n):
        split_number += len(reviews[i*split_size:(i+1)*split_size])
        # split reviews are stored as temporary file to limit RAM usage
        # split_reviews_list.append(
        #     data_stream.ReviewIterator(
        #         temp_file_list=data_stream.save_to_temp_file(reviews[i*split_size:(i+1)*split_size])))
        split_reviews_list.append(reviews[i*split_size:(i+1)*split_size])

    if n*split_size < len(reviews):
        split_number += len(reviews[n*split_size:len(reviews)])
        split_reviews_list.append(reviews[n*split_size:len(reviews)])

    print("Reviews number : " + str(len(reviews)))
    print("Split into : " + str(len(split_reviews_list)) + "(total : " + str(split_number) + ")")

    return split_reviews_list


def _split_reviews_process(reviews, freeling_modules, _state_queue=None, _id_process=None):
    import os
    from loacore.utils.status import ProcessState

    # Tokenization + Add all sentences and all words from all reviews
    import loacore.process.sentence_process as sentence_process
    added_sentences = sentence_process.add_sentences_from_reviews(
        reviews,
        _state_queue=_state_queue,
        _id_process=_id_process,
        freeling_modules=(freeling_modules["morfo"], freeling_modules["tk"], freeling_modules["sp"]))
    print(len(added_sentences))

    # added_sentences = sentence_process.add_sentences_from_reviews(
    #     reviews,
    #     _state_queue=state_queue,
    #     _id_process=id_process)

    # Reload sentences with words
    import loacore.load.sentence_load as sentence_load
    if _state_queue is not None:
        _state_queue.put(ProcessState(_id_process, os.getpid(), "Reload Sentences", "-"))
    else:
        print("Reload Sentences...")

    sentences = sentence_load.load_sentences(id_sentences=[s.id_sentence for s in added_sentences], load_words=True)

    # Some test outputs ############################################
    from loacore.conf import OUTPUT_PATH
    f = open(os.path.join(OUTPUT_PATH, "test_sentence.txt"), 'w')
    f.write(str(len(sentences)) + "\n")
    for s in sentences:
        f.write(str(len(s.words)) + "\t" + s.sentence_str() + "\n")
    f.close()
    #################################################################

    # Lemmatization
    import loacore.process.lemma_process as lemma_process
    lemma_process.add_lemmas_to_sentences(
        sentences,
        _state_queue=_state_queue,
        _id_process=_id_process,
        freeling_modules=freeling_modules["morfo"])

    # lemma_process.add_lemmas_to_sentences(
    #     sentences,
    #     _state_queue=state_queue,
    #     _id_process=id_process)

    # Disambiguation
    import loacore.process.synset_process as synset_process
    synset_process.add_synsets_to_sentences(
        sentences,
        _state_queue=_state_queue,
        _id_process=_id_process,
        freeling_modules=(freeling_modules["morfo"],
                          freeling_modules["tagger"],
                          freeling_modules["sen"],
                          freeling_modules["wsd"]))

    # synset_process.add_synsets_to_sentences(
    #     sentences,
    #     _state_queue=state_queue,
    #     _id_process=id_process)

    # Synset polarities
    id_words = [w.id_word for s in sentences for w in s.words]
    synset_process.add_polarity_to_synsets(
        id_words,
        _state_queue=_state_queue,
        _id_process=_id_process)

    # Dep tree
    import loacore.process.deptree_process as deptree_process
    deptree_process.add_dep_tree_from_sentences(
        sentences,
        _state_queue=_state_queue,
        _id_process=_id_process,
        freeling_modules=(freeling_modules["morfo"],
                          freeling_modules["tagger"],
                          freeling_modules["sen"],
                          freeling_modules["wsd"],
                          freeling_modules["parser"]))

    # deptree_process.add_dep_tree_from_sentences(
    #     sentences,
    #     _state_queue=state_queue,
    #     _id_process=id_process)

    if _state_queue is not None:
        _state_queue.put(ProcessState(_id_process, os.getpid(), "Terminated", " - "))


def _print_states_process(num_process, q):
    import curses
    from loacore.utils.status import ProcessState

    curses.update_lines_cols()

    def printer(stdscr):
        refresh_count = 0

        def plot_window():
            nonlocal refresh_count
            refresh_count += 1
            if refresh_count >= 1000:
                refresh_count = 0
                stdscr.clear()
            stdscr.move(0, 0)
            stdscr.addstr(0, 0, "Process")
            stdscr.addstr(0, 14, "PID")
            stdscr.addstr(0, 21, "Activity")
            stdscr.addstr(0, 45, "Progress")
            stdscr.move(0, 0)
            stdscr.chgat(curses.A_REVERSE)

            for i in range(min(curses.LINES - 1, num_process)):
                items = processes[i + 1].state_str()
                stdscr.move(i + 1, 0)
                stdscr.clrtoeol()
                stdscr.addstr(i + 1, 0, items[0])
                stdscr.addstr(i + 1, 14, items[1])
                stdscr.addstr(i + 1, 21, items[2])
                stdscr.addstr(i + 1, 45, items[3])
            if num_process + 1 <= curses.LINES:
                stdscr.move(num_process + 1, 0)
            stdscr.refresh()

        print("Printer initialized")
        for n in unterminated_processes:
            processes[n] = ProcessState(n, "-", "Waiting", "-")
        old_lines = curses.LINES
        while len(unterminated_processes) > 0:
            curses.update_lines_cols()
            if curses.LINES != old_lines:
                plot_window()
                old_lines = curses.LINES
            while not q.empty():
                state = q.get()
                processes[state.id_process] = state
                if state.activity == "Terminated" or state.activity == "DB error":
                    unterminated_processes.remove(state.id_process)
                plot_window()

        import os
        from loacore.conf import OUTPUT_PATH
        f = open(os.path.join(OUTPUT_PATH, "result.log"), "w")
        for i in processes.keys():
            items = processes[i].state_str()
            f.write(items[0] + '\t' + items[1] + '\t' + items[2] + '\t' + items[3] + '\t\n')
        f.close()

    unterminated_processes = [n + 1 for n in range(num_process)]
    processes = {}

    curses.wrapper(printer)


def my_maco_options(lang, lpath):
    import os

    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = ""
    opt.ProbabilityFile = os.path.join(lpath, "probabilitats.dat")
    opt.DictionaryFile = os.path.join(lpath, "dicc.src")
    opt.PunctuationFile = os.path.join(lpath, "..", "common", "punct.dat")
    return opt


def load_all_freeling_modules():

    print("Loading Freeling Modules...")

    import os

    freeling.util_init_locale("default")

    from loacore.conf import lang
    from loacore.conf import LANG_PATH


    # create the analyzer with the required set of maco_options
    morfo = freeling.maco(my_maco_options(lang, LANG_PATH))

    morfo.set_active_options(False,  # UserMap
                             False,  # NumbersDetection,
                             True,  # PunctuationDetection,
                             False,  # DatesDetection,
                             True,  # DictionarySearch,
                             False,  # AffixAnalysis,
                             False,  # CompoundAnalysis,
                             True,  # RetokContractions,
                             False,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             True)  # ProbabilityAssignment

    tk = freeling.tokenizer(os.path.join(LANG_PATH, "tokenizer.dat"))
    sp = freeling.splitter(os.path.join(LANG_PATH, "splitter.dat"))

    # create tagger
    tagger = freeling.hmm_tagger(os.path.join(LANG_PATH, "tagger.dat"), False, 2)

    # create sense annotator
    sen = freeling.senses(os.path.join(LANG_PATH, "senses.dat"))
    # create sense disambiguator
    wsd = freeling.ukb(os.path.join(LANG_PATH, "ukb.dat"))
    # create dependency parser
    parser = freeling.dep_treeler(os.path.join(LANG_PATH, "dep_treeler", "dependences.dat"))
    print("Done.")

    return {"tk": tk, "sp": sp, "morfo": morfo, "tagger": tagger, "sen": sen, "wsd": wsd, "parser": parser}



