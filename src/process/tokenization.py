import os
import re
import nltk
from nltk.probability import FreqDist


def main():

    stop_words = init_stopwords()
    for dirpath, dirnames, filenames in os.walk('../../data/normalized/'):
        for filename in filenames:
            normalized_text = open(os.path.join(dirpath, filename), encoding='utf-8')
            tokens = sorted(nltk.word_tokenize(normalized_text.read()))

            write_raw_tokens(tokens, dirpath, filename)

            process_tokens(tokens, stop_words)

            write_processed_tokens(tokens, dirpath, filename)


def write_raw_tokens(tokens, dirpath, filename):
    dirname = re.findall(r'^\.\./\.\./data/normalized/(.*)', dirpath)
    directory = os.path.join('../../data/tokenized/raw/', dirname[0])
    if not os.path.exists(directory):
        os.makedirs(directory)

    tokens_file = open(os.path.join(directory, filename), 'w', encoding='utf-8')
    for token in tokens:
        tokens_file.write(token)
        tokens_file.write('\n')


def write_processed_tokens(tokens, dirpath, filename):
    dirname = re.findall(r'^\.\./\.\./data/normalized/(.*)', dirpath)
    directory = os.path.join('../../data/tokenized/processed/', dirname[0])
    if not os.path.exists(directory):
        os.makedirs(directory)

    tokens_file = open(os.path.join(directory, filename), 'w', encoding='utf-8')
    for token in tokens:
        tokens_file.write(token)
        tokens_file.write('\n')


def init_stopwords():
    stop_words_file = open('../../ressources/stopwords.txt')
    stop_words_string = stop_words_file.read()
    stop_words = re.findall(r'^(\w+)\s*(?:\|.*\s*)?', stop_words_string, re.MULTILINE)
    return stop_words


def process_tokens(tokens, stop_words):
    # Remove stop words
    for stop_word in stop_words:
        while stop_word in tokens:
            tokens.remove(stop_word)
    # Remove decimal characters

    decimals_to_remove = []
    for token in tokens:
        decimal = (len(re.findall(r'\d+', token)) > 0)
        if decimal:
            decimals_to_remove.append(token)

    for word in decimals_to_remove:
        while word in tokens:
            tokens.remove(word)

if __name__ == "__main__":
    main()