
def add_train_imdb_neg():
    import loacore.process.file_process as file_process
    from loacore import DATA_PATH
    import os

    file_process.add_files(
        [os.path.join(DATA_PATH, 'raw', 'imdb', 'train', 'train_imdb_labelled_neg.txt')],
        encoding='utf8',
        lang='en')


add_train_imdb_neg()