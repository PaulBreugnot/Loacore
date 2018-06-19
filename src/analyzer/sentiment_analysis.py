import nltk
import re
import os
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from prettytable import PrettyTable


class text_polarity:

    def __init__(self, lemmas):
        self.lemmas = lemmas
        self.pos_score, self.neg_score, self.obj_score = self.compute_scores()

    def compute_scores(self):
        word_polarities = []
        for lemma in self.lemmas:
            polarity = word_polarity(lemma)
            if len(polarity.selected_synsets) > 0:
                word_polarities.append(polarity)
        if len(word_polarities) > 0:
            pos_score = 0
            neg_score = 0
            for polarity in word_polarities:
                pos_score += polarity.pos_score
                neg_score += polarity.neg_score
            pos_score = round(pos_score / len(word_polarities), 2)
            neg_score = round(neg_score / len(word_polarities), 2)
            obj_score = round(1 - (pos_score + neg_score), 2)
            return pos_score, neg_score, obj_score
        else:
            #Empty file...
            return None, None, None


class word_polarity:

    def __init__(self, word):
        self.word = word
        self.selected_synsets = self.select_synsets(self, wn.synsets(self.word, lang='spa'))
        self.pos_score, self.neg_score, self.obj_score = self.compute_scores()

    def compute_scores(self):
        if len(self.selected_synsets) > 0:
            pos_score = 0
            neg_score = 0
            for synset in self.selected_synsets:
                pos_score += swn.senti_synset(synset.name()).pos_score()
                neg_score += swn.senti_synset(synset.name()).neg_score()

            pos_score = pos_score / len(self.selected_synsets)
            neg_score = neg_score / len(self.selected_synsets)
            obj_score = 1 - (pos_score + neg_score)
            return pos_score, neg_score, obj_score
        else:
            return None, None, None

    @staticmethod
    def select_synsets(self, synsets):
        most_common_number = float("inf")
        valid_synsets = []
        for synset in synsets:
            number = int(re.findall(r'.+\..+\.(.+)', synset.name())[0])
            if number <= most_common_number:
                if number == most_common_number:
                    valid_synsets.append(synset)
                else:
                    most_common_number = number
                    valid_synsets.clear()
                    valid_synsets.append(synset)
        return valid_synsets


def main():
    polarity = get_text_polarity('__ENCUESTA_SATISFACCION_HOSPEDAJE_ALOJAMIENTO_N.txt')
    print(polarity.pos_score)
    print(polarity.neg_score)
    print(polarity.obj_score)
    print_polarity_table()


def print_polarity_table():
    table = PrettyTable(['Folder', 'File', 'Pos_Score', 'Neg_Score', 'Obj_Score'])
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            folder = get_folder(filename)
            txt_polarity = get_text_polarity(filename)
            table.add_row([folder, filename, txt_polarity.pos_score, txt_polarity.neg_score, txt_polarity.obj_score])
    print(table)


def get_folder(file_name):
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            if filename == file_name:
                dirname = re.findall(r'^\.\./\.\./data/lemmatized/(.*)', dirpath)
                return dirname[0]


def get_text_polarity(file_name):
    word_polarities = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized'):
        for filename in filenames:
            if filename == file_name:
                lemmas_file = open(os.path.join(dirpath, filename), encoding='utf-8')
                lemmas = nltk.word_tokenize(lemmas_file.read())
                return text_polarity(lemmas)


if __name__ == "__main__":
    main()