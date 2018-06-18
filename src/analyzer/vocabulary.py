import os
import nltk

def main():
    print(compute_vocab())
    print(compute_vocab())


def compute_vocab(file_name):
    vocabulary = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            if filename == file_name:
                file = open(os.path.join(dirpath, filename), encoding='utf-8')
                for word in nltk.word_tokenize(file.read()):
                    vocabulary.append(word)
    return sorted(list(set(vocabulary)))


def compute_vocab():
    vocabulary = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            file = open(os.path.join(dirpath, filename), encoding='utf-8')
            for word in nltk.word_tokenize(file.read()):
                vocabulary.append(word)
    return sorted(list(set(vocabulary)))


if __name__ == "__main__":
    main()