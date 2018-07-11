import re
import os


def write():
    import src.database.load.file_load as file_load
    import src.utils.file_writer as file_writer

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
        text = 'ID_Word\tID_Lemma\tLemma\n'
        for word in words:
            text += (str(word.id_word) + '\t' + str(word.id_lemma) + '\t' + word.lemma + '\n')

        file_writer.write(text, os.path.join('../../data/lemmatized/', directory[0]), filename[0])