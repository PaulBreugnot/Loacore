import nltk
import os
import re


def main():

    for dirpath, dirnames, filenames in os.walk('../data/tokenized/processed/'):
        for filename in filenames:
            normalized_text = open(os.path.join(dirpath, filename), encoding='utf-8')
            tokens = sorted(list(set(nltk.word_tokenize(normalized_text.read()))))

            processed_tokens = lemmatize(tokens)

            write_processed_tokens(processed_tokens, dirpath, filename)


def write_processed_tokens(tokens, dirpath, filename):
    dirname = re.findall(r'^\.\./data/tokenized/processed/(.*)', dirpath)
    directory = os.path.join('../data/lemmatized/', dirname[0])
    if not os.path.exists(directory):
        os.makedirs(directory)

    tokens_file = open(os.path.join(directory, filename), 'w', encoding='utf-8')
    for token in tokens:
        tokens_file.write(token)
        tokens_file.write('\n')


def lemmatize(tokens):
    lemmatizer = nltk.WordNetLemmatizer()
    processed_tokens = sorted(list(set([lemmatizer.lemmatize(t) for t in tokens])))
    for t in tokens:
        lemma = lemmatizer.lemmatize(t)
        if lemma != t:
            # Check
            print("word : ", t, "    lemma :", lemma)
    return processed_tokens


if __name__ == "__main__":
    main()