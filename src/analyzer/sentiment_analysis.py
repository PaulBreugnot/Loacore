import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn


def main():
    print(wn.lemmas('baños', lang='spa'))
    get_polarity('agua')


def get_polarity(word):
    english_synset = wn.synsets(word, lang='spa')
    print('English synsets : ', english_synset)

    for synset in english_synset:
        print(swn.senti_synset(synset.name()).obj_score())


if __name__ == "__main__":
    main()