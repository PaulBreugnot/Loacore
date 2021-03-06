
def add_train_imdb_pos(workers):
    import loacore.process.file_process as file_process
    import loacore.load.file_load as file_load
    from loacore.conf import DATA_PATH
    import os

    # file_load.clean_db()
    file_process.add_files(
        [os.path.join(DATA_PATH, 'raw', 'imdb', 'train', 'train_imdb_labelled_pos.txt')],
        encoding='utf8',
        lang='en',
        workers=workers)


def add_train_imdb_neg(workers):
    import loacore.process.file_process as file_process
    import loacore.load.file_load as file_load
    from loacore.conf import DATA_PATH
    import os

    # file_load.clean_db()
    file_process.add_files(
        [os.path.join(DATA_PATH, 'raw', 'imdb', 'train', 'train_imdb_labelled_neg.txt')],
        encoding='utf8',
        lang='en',
        workers=workers)


def add_test_imdb_neg(workers):
    import loacore.process.file_process as file_process
    import loacore.load.file_load as file_load
    from loacore.conf import DATA_PATH
    import os

    # file_load.clean_db()
    file_process.add_files(
        [os.path.join(DATA_PATH, 'raw', 'imdb', 'test', 'test_imdb_labelled_neg.txt')],
        encoding='utf8',
        lang='en',
        workers=workers)


def add_test_imdb_pos(workers):
    import loacore.process.file_process as file_process
    import loacore.load.file_load as file_load
    from loacore.conf import DATA_PATH
    import os

    # file_load.clean_db()
    file_process.add_files(
        [os.path.join(DATA_PATH, 'raw', 'imdb', 'test', 'test_imdb_labelled_pos.txt')],
        encoding='utf8',
        lang='en',
        workers=workers)


def add_all():
    import loacore.process.file_process as file_process
    import os
    from loacore.conf import DATA_PATH
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(os.path.join(DATA_PATH, "raw", "imdb"))):
            for name in filenames:
                file_paths.append(os.path.join(dirpath, name))

    file_process.add_files(file_paths, encoding="utf8", lang="en")


def main(workers=0):
    # add_train_imdb_neg()
    add_test_imdb_pos(workers)
    # add_all()


if __name__ == "__main__":
    main()
