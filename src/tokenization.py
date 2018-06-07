import os
import re
import nltk
import matplotlib.pyplot as plt
from nltk.probability import FreqDist



def main():
    for dirpath, dirnames, filenames in os.walk('../data/normalized/'):
        for name in filenames:
            normalized_text = open(os.path.join(dirpath, name))
            tokens = nltk.word_tokenize(normalized_text.read())
            fdist = FreqDist(tokens)
            fdist.plot(50)


if __name__ == "__main__":
    main()