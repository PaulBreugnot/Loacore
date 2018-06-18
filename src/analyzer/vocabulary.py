import os
import nltk


def main():
    print(compute_global_vocab())
    print(len(compute_global_vocab()))
    write_global_vocab(compute_global_vocab())


def compute_vocab(file_name):
    vocabulary = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            if filename == file_name:
                file = open(os.path.join(dirpath, filename), encoding='utf-8')
                for word in nltk.word_tokenize(file.read()):
                    vocabulary.append(word)
    return sorted(list(set(vocabulary)))


def compute_global_vocab():
    vocabulary = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            file = open(os.path.join(dirpath, filename), encoding='utf-8')
            for word in nltk.word_tokenize(file.read()):
                vocabulary.append(word)
    return sorted(list(set(vocabulary)))


def write_global_vocab(vocabulary):
    write_vocab(vocabulary, 'global_vocab.txt', '../../results/vocabularies/global/')


def write_vocab(vocabulary, filename, path):
    file = open(os.path.join(path, filename), 'w', encoding='utf-8')
    for word in vocabulary:
        file.write(word)
        file.write('\n')

if __name__ == "__main__":
    main()