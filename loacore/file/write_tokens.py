import re
import os


def write():
    import loacore.load.file_load as file_load
    import loacore.utils.file_writer as file_writer

    files = file_load.load_database(load_deptrees=False)

    for file in files:
        directory = re.findall(r'../../data/raw/(.+)', file.file_path)
        filename = re.findall(r'.+/(.+\.txt)', file.file_path)
        words = []
        for reviews in file.reviews:
            for sentence in reviews.sentences:
                for word in sentence.words:
                    words.append(word)
        words = sorted(words, key=lambda w: w.word)
        text = 'ID_Word\ttoken'
        for word in words:
            text += (str(word.id_word) + '\t' + word.word + '\n')

        file_writer.write(text, os.path.join('../../data/tokenized/', directory[0]), filename[0])
