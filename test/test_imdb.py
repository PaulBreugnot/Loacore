
def add_train_imdb_neg():
    import loacore.process.file_process as file_process
    import loacore.load.file_load as file_load
    from loacore.conf import DATA_PATH
    import os

    # file_load.clean_db()
    file_process.add_files(
        [os.path.join(DATA_PATH, 'raw', 'imdb', 'train', 'train_imdb_labelled_neg.txt')],
        encoding='utf8',
        lang='en')


def add_all():
    import loacore.process.file_process as file_process
    import os
    from loacore.conf import DATA_PATH
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(os.path.join(DATA_PATH, "raw", "imdb"))):
            for name in filenames:
                file_paths.append(os.path.join(dirpath, name))

    file_process.add_files(file_paths, encoding="utf8", lang="en")

add_train_imdb_neg()
# add_all()