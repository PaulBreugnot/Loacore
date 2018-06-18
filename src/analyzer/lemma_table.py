import os
import nltk
import re
from prettytable import PrettyTable


def main():
    draw_table()


def get_folder(file_name):
    for dirpath, dirnames, filenames in os.walk('../../data/raw/'):
        for filename in filenames:
            if filename == file_name:
                dirname = re.findall(r'^\.\./\.\./data/raw/(.*)', dirpath)
                return dirname[0]


def get_words(file_name, lemmatized=True):
    if(lemmatized):
        for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
            for filename in filenames:
                if filename == file_name:
                    lemmas_file = open(os.path.join(dirpath, filename), encoding='utf-8')
                    lemmas = nltk.word_tokenize(lemmas_file.read())
                    return lemmas

    else:
        for dirpath, dirnames, filenames in os.walk('../../data/tokenized/processed'):
            for filename in filenames:
                if filename == file_name:
                    tokens_file = open(os.path.join(dirpath, filename), encoding='utf-8')
                    tokens = nltk.word_tokenize(tokens_file.read())
                    return tokens


def get_words_count(file_name, lemmatized=True):
    words = get_words(file_name, lemmatized)
    return len(words)


def get_reduction_rate(file_name):
    if get_words_count(file_name, lemmatized=False) > 0:
        return round(1 - get_words_count(file_name) / get_words_count(file_name, lemmatized=False), 2)
    return 0


def draw_table():
    table = PrettyTable(['Folder', 'File', 'Words count (tokens)', 'Words count (lemmas)', 'Reduction rate'])
    for dirpath, dirnames, filenames in os.walk('../../data/raw/'):
        for filename in filenames:
            folder = get_folder(filename)
            tokens_count = get_words_count(filename, lemmatized=False)
            lemmas_count = get_words_count(filename)
            reduction = get_reduction_rate(filename)
            table.add_row([folder, filename, tokens_count, lemmas_count, reduction])
    print(table)


if __name__ == "__main__":
    main()