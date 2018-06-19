import nltk
import os
import re


def main():

    for dirpath, dirnames, filenames in os.walk('../../data/tokenized/processed/'):
        for filename in filenames:
            normalized_text = open(os.path.join(dirpath, filename), encoding='utf-8')
            tokens = sorted(list(set(nltk.word_tokenize(normalized_text.read()))))

            processed_tokens = stem(tokens)

            write_processed_tokens(processed_tokens, dirpath, filename)


def write_processed_tokens(tokens, dirpath, filename):
    dirname = re.findall(r'^\.\./\.\./data/tokenized/processed/(.*)', dirpath)
    directory = os.path.join('../../data/stemmed/', dirname[0])
    if not os.path.exists(directory):
        os.makedirs(directory)

    tokens_file = open(os.path.join(directory, filename), 'w', encoding='utf-8')
    for token in tokens:
        tokens_file.write(token)
        tokens_file.write('\n')


def stem(tokens):
    stemmer = nltk.stem.snowball.SpanishStemmer()
    processed_tokens = sorted(list(set([stemmer.stem(t) for t in tokens])))
    for t in tokens:
        stem = stemmer.stem(t)
        if stem != t:
            # Check
            print("word : ", t, "    stem :", stem)
    return processed_tokens


if __name__ == "__main__":
    main()