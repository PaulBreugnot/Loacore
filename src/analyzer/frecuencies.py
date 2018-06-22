from nltk.probability import FreqDist
import nltk
import os
import re


def main():
    vocab = init_vocabulary()
    print(vocab)
    for dirpath, dirnames, filenames in os.walk('../../data/disambiguated/'):
        for filename in filenames:
            lemmas_file = open(os.path.join(dirpath, filename), encoding='utf-8')
            fdist = compute_lemmas_frecuencies(lemmas_file, vocab, show=True)


def plot_freq_dist(file_name, vocab):
    for dirpath, dirnames, filenames in os.walk('../../data/disambiguated/'):
        for filename in filenames:
            if filename == file_name:
                lemmas_file = open(os.path.join(dirpath, filename), encoding='utf-8')
                compute_lemmas_frecuencies(lemmas_file, vocab, show=True)
                return


def init_vocabulary():
    global_voc = open('../../results/vocabularies/global/global_vocab.txt', encoding='utf-8')
    return re.findall(r'(.*)\s', global_voc.read(), re.MULTILINE)


def compute_lemmas_frecuencies(loaded_file, vocab, show=False):
    lemmas = re.findall(r'.*# (.*)', loaded_file.read(), re.MULTILINE)
    print(lemmas)
    fdist = FreqDist()
    for token in lemmas:
        if token in vocab:
                fdist[token] += 1
    if show:
        fdist.plot()
    return fdist


if __name__ == "__main__":
    main()