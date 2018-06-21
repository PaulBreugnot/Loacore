import os
import re
import nltk
import src.utils.file_writer as file_writer


def main():

    stop_words = init_stopwords()
    for dirpath, dirnames, filenames in os.walk('../../data/normalized/'):
        for filename in filenames:
            normalized_text = open(os.path.join(dirpath, filename), encoding='utf-8')

            tokens = init_tokens(normalized_text.read(), sort=True)

            write_raw_tokens(tokens, dirpath, filename)

            process_tokens(tokens, stop_words)

            write_processed_tokens(tokens, dirpath, filename)


def write_raw_tokens(tokens, dirpath, filename):
    print(len(tokens))
    raw_tokens_string = '\n'.join(tokens)
    dirname = re.findall(r'^\.\./\.\./data/normalized/(.*)', dirpath)
    directory = os.path.join('../../data/tokenized/raw/', dirname[0])
    file_writer.write(raw_tokens_string, directory, filename)


def write_processed_tokens(tokens, dirpath, filename):

    processed_tokens_string = '\n'.join(tokens)
    dirname = re.findall(r'^\.\./\.\./data/normalized/(.*)', dirpath)
    directory = os.path.join('../../data/tokenized/processed/', dirname[0])
    file_writer.write(processed_tokens_string, directory, filename)


def init_stopwords():
    stop_words_file = open('../../ressources/stopwords.txt')
    stop_words_string = stop_words_file.read()
    stop_words = re.findall(r'^(\w+)\s*(?:\|.*\s*)?', stop_words_string, re.MULTILINE)
    return stop_words


def init_tokens(text, sort=False):
    tokens = nltk.word_tokenize(text)
    if sort:
        tokens = sorted(tokens)
    return tokens


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
