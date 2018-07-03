import nltk
import re
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from prettytable import PrettyTable
from src.process.disambiguation import load_disambiguated_dict


class TextPolarity:

    def __init__(self, filename, indexed_lemmas, select='none'):
        self.filename = filename
        self.indexed_lemmas = indexed_lemmas
        self.pos_score, self.neg_score, self.obj_score = self.compute_scores(select)

    def compute_scores(self, select):
        word_polarities = []
        for indexed_lemma in self.indexed_lemmas:
            polarity = WordPolarity(self.filename, indexed_lemma, select=select)
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


class WordPolarity:

    loaded_disambiguated_dict = False
    disambiguated_dicts = dict()

    def __init__(self, filename, indexed_word, select='none'):
        self.filename = filename
        self.text_offset = re.findall(r'(\d+) .+', indexed_word)[0]
        self.word = re.findall(r'\d+ (.+)', indexed_word)[0]
        self.selected_synsets = self.select_synsets(self, wn.synsets(self.word, lang='spa'), select)
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
    def select_synsets(self, synsets, select):
        if select == 'common':
            return self.select_common_synsets(self, synsets)
        if select == 'optimistic':
            return self.select_optimistic_synsets(self, synsets)
        if select == 'pessimistic':
            return self.select_pessimistic_synsets(self, synsets)
        if select == 'disambiguated':
            return self.select_disambiguated_synset(self)
        if select == 'none':
            return synsets

    @staticmethod
    def select_optimistic_synsets(self, synsets):

        """
        :param synsets: the original lemma synsets
        :return: synsets with the most positive polarity, from SentiWordNet
        """

        most_positive_value = 0
        valid_synsets = []
        for synset in synsets:
            pos_value = swn.senti_synset(synset.name()).pos_score()
            if pos_value >= most_positive_value:
                if pos_value == most_positive_value:
                    valid_synsets.append(synset)
                else:
                    most_positive_value = pos_value
                    valid_synsets.clear()
                    valid_synsets.append(synset)
        return valid_synsets

    @staticmethod
    def select_pessimistic_synsets(self, synsets):

        """
        :param synsets: the original lemma synsets
        :return: synsets with the most negative polarity, from SentiWordNet
        """

        most_negative_value = 0
        valid_synsets = []
        for synset in synsets:
            neg_value = swn.senti_synset(synset.name()).neg_score()
            if neg_value >= most_negative_value:
                if neg_value == most_negative_value:
                    valid_synsets.append(synset)
                else:
                    most_negative_value = neg_value
                    valid_synsets.clear()
                    valid_synsets.append(synset)
        return valid_synsets

    @staticmethod
    def select_common_synsets(self, synsets):

        """
        :param synsets: the original lemma synsets
        :return: most common synsets senses. The common attribute is defined by the number in the WordNet synset
        representation.
        If there is a synset with number 01, all the synsets with number 01 will be selected.
        Else, all the synsets with the minimum number will be selected.

        Notice that each selected synset correspond to the most common sense for this particular synset name.

        For example, in the house synsets :
        [Synset('house.n.01'), Synset('firm.n.01'), Synset('house.n.03'), Synset('house.n.04'), Synset('house.n.05'),
        Synset('house.n.06'), Synset('house.n.07'), Synset('sign_of_the_zodiac.n.01'), Synset('house.n.09'),
        Synset('family.n.01'), Synset('theater.n.01'), Synset('house.n.12'), Synset('house.v.01'), Synset('house.v.02')]

        Will be selected : [Synset('house.n.01'), Synset('firm.n.01'), Synset('sign_of_the_zodiac.n.01'),
        Synset('family.n.01'), Synset('theater.n.01'), Synset('house.v.01')]

        But when we encounter the word "house" in a text, it is more probable that it is use for the sense
        Synset('house.n.03') rather that Synset('sign_of_the_zodiac.n.01')...
        """

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

    @staticmethod
    def select_disambiguated_synset(self):
        """
        :return: the synset corresponding to the disambiguated one corresponding to the word in its context,
        previously computed in disambiguated folder
        """

        if not self.loaded_disambiguated_dict:
            WordPolarity.load_dicts()
        disambiguated_dict = WordPolarity.disambiguated_dicts.get(self.filename)
        if disambiguated_dict.get(self.text_offset) is not None:
            return [wn.synset(disambiguated_dict.get(self.text_offset))]
        # print unkown words
        # print(self.word, " : ", wn.synsets(self.word))
        return []

    @staticmethod
    def load_dicts():
        for dirpath, dirnames, filenames in os.walk('../../data/disambiguated/'):
            for filename in filenames:
                WordPolarity.disambiguated_dicts.update([(filename, load_disambiguated_dict(filename))])
        WordPolarity.loaded_disambiguated_dict = True


def main():
    print([swn.senti_synset(synset.name()).pos_score() for synset in wn.synsets('servicio', lang='spa')])
    print([swn.senti_synset(synset.name()).neg_score() for synset in wn.synsets('servicio', lang='spa')])
    #print_polarity_table(select='disambiguated')
    #plot_polarity_pie_charts(select='disambiguated')
    #save_polarity_pie_charts()


def print_polarity_table(select='none'):
    table = PrettyTable(['Folder', 'File', 'Pos_Score', 'Neg_Score', 'Obj_Score'])
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            print(filename)
            folder = get_folder(filename)
            txt_polarity = get_text_polarity(filename, select=select)
            table.add_row([folder, filename, txt_polarity.pos_score, txt_polarity.neg_score, txt_polarity.obj_score])
    print(table)


def save_polarity_pie_charts():
    select_modes = ['none', 'optimistic', 'pessimistic', 'common', 'disambiguated']
    for select_mode in select_modes:
        plot_polarity_pie_charts(select=select_mode, show=False)
        plt.savefig('../../results/sentiment_analysis/mode_' + select_mode + '.png', dpi=200)
        plt.clf()


def plot_polarity_pie_charts(select='none', show=True):
    folders = []
    file_names = []
    pos_scores = []
    neg_scores = []
    obj_scores = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            folder = get_folder(filename)
            txt_polarity = get_text_polarity(filename, select)
            folders.append(folder)
            file_names.append(filename)
            pos_scores.append(txt_polarity.pos_score)
            neg_scores.append(txt_polarity.neg_score)
            obj_scores.append(txt_polarity.obj_score)

    pies_data = []
    pies_titles = []
    index = 0
    while index < len(folders):
        current_folder = folders[index]
        pie_pos_score = pos_scores[index]
        pie_neg_score = neg_scores[index]
        pie_obj_score = obj_scores[index]
        if not pie_pos_score is None:
            while index + 1 < len(folders) and folders[index + 1] == current_folder:
                if not pos_scores[index + 1] is None:
                    pie_pos_score = (pie_pos_score + pos_scores[index + 1]) / 2
                    pie_neg_score = (pie_neg_score + neg_scores[index + 1]) / 2
                    pie_obj_score = (pie_obj_score + obj_scores[index + 1]) / 2
                index += 1
            pies_data.append([pie_pos_score, pie_neg_score, pie_obj_score])
            pies_titles.append(folders[index])
            index += 1

    index = 0
    labels = ['Positive', 'Negative', 'Objective']
    colors = ['green', 'red', 'skyblue']
    fig, axes = plt.subplots(int(len(pies_titles) / 4), 4, constrained_layout=False)
    for x in axes.flatten():
        x.axis("off")
    fig.set_figheight(3.5 * int(len(pies_titles) / 4))
    fig.set_figwidth(14)
    while index < len(pies_titles):
        axe = fig.add_subplot(int(len(pies_titles) / 4), 4, index + 1)
        axe.pie(pies_data[index], colors=colors, autopct='%1.1f%%')
        axe.set_title(pies_titles[index])
        index += 1
    pos_patch = mpatches.Patch(color='green', label='Positive')
    neg_patch = mpatches.Patch(color='red', label='Negative')
    obj_patch = mpatches.Patch(color='skyblue', label='Objective')
    plt.figlegend(handles=[pos_patch, neg_patch, obj_patch])
    plt.suptitle("Select Mode : " + select)
    if show:
        plt.show()


def get_folder(file_name):
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            if filename == file_name:
                dirname = re.findall(r'^\.\./\.\./data/lemmatized/(.*)', dirpath)
                return dirname[0]


def get_text_polarity(file_name, select='none'):
    word_polarities = []
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized'):
        for filename in filenames:
            if filename == file_name:
                lemmas_file = open(os.path.join(dirpath, filename), encoding='utf-8')
                lemmas = re.findall(r'\d+ .+', lemmas_file.read(), re.MULTILINE)
                return TextPolarity(file_name, lemmas, select)


if __name__ == "__main__":
    main()