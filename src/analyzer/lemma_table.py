import os
import nltk
import re


def main():
    get_words("_ENCUESTA_ENERO_2018_.txt")
    get_words("_ENCUESTA_ENERO_2018_.txt", lemmatized=False)
    get_words_count("_ENCUESTA_ENERO_2018_.txt")
    get_words_count("_ENCUESTA_ENERO_2018_.txt", lemmatized=False)
    print(get_reduction_rate("_ENCUESTA_ENERO_2018_.txt"))
    print(get_folder("_ENCUESTA_ENERO_2018_.txt"))


def get_folder(file_name):
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            if filename == file_name:
                dirname = re.findall(r'^\.\./\.\./data/lemmatized/(.*)', dirpath)
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
    return round(1 - get_words_count(file_name) / get_words_count(file_name, lemmatized=False), 2)


if __name__ == "__main__":
    main()