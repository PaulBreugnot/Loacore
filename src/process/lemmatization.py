import os
import re
import ressources.pyfreeling as freeling
import src.utils.file_writer as file_writer


def main():

    sp, morfo = init_analyzers()

    for dirpath, dirnames, filenames in os.walk('../../data/tokenized/processed/'):
        for filename in filenames:
            tokenized_text = open(os.path.join(dirpath, filename), encoding='utf-8')
            indexed_tokens = re.findall(r'\d+ \w*', tokenized_text.read(), re.MULTILINE)
            lemmas_dict = search_lemmas(unindexed_tokens(indexed_tokens), sp, morfo)
            lemmatize_indexed_tokens = lemmatize(indexed_tokens, lemmas_dict)
            write_lemmas(lemmatize_indexed_tokens, dirpath, filename)


def init_analyzers():
    lang = "es"
    ipath = "/usr/local"
    # path to language data
    lpath = ipath + "/share/freeling/" + lang + "/"

    freeling.util_init_locale("default")

    # create the analyzer with the required set of maco_options
    morfo = freeling.maco(maco_options(lang, lpath))
    #  then, (de)activate required modules
    morfo.set_active_options(False,  # UserMap
                             False,  # NumbersDetection,
                             False,  # PunctuationDetection,
                             False,  # DatesDetection,
                             True,  # DictionarySearch,
                             False,  # AffixAnalysis,
                             False,  # CompoundAnalysis,
                             False,  # RetokContractions,
                             False,  # MultiwordsDetection,
                             False,  # NERecognition,
                             False,  # QuantitiesDetection,
                             False)  # ProbabilityAssignment

    # create analyzers
    sp = freeling.splitter(lpath + "splitter.dat");

    return sp, morfo


def maco_options(lang,lpath) :
    # For more options : https://talp-upc.gitbooks.io/freeling-tutorial/content/code/example01.py.html
    # create options holder
    opt = freeling.maco_options(lang);

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.DictionaryFile = lpath + "dicc.src"
    return opt


def unindexed_tokens(tokens):
    unindexed_tokens_list = []
    for token in tokens:
        unindexed_tokens_list.append(freeling.word(re.findall(r'\d+ (.+)', token)[0]))

    #Lot of useless operations, but freeling format requires it...
    return unindexed_tokens_list


def search_lemmas(tokens, sp, morfo):

    lemmas_dict = dict()
    sentences_list = sp.split(tokens)

    # perform morphosyntactic analysis (here : dictionary search)
    sentences_list = morfo.analyze(sentences_list)

    for sentence in sentences_list:
        for word in sentence:
            lemma = word.get_lemma()
            if (len(lemma)) > 0:
                #print(word, ' : ', lemma)
                lemmas_dict.update([(word.get_form(), lemma)])
    return lemmas_dict


def lemmatize(indexed_tokens, lemmas_dict, sort=True):
    lemmatize_indexed_tokens = []
    for indexed_token in indexed_tokens:
        index = re.findall(r'(\d+ ).+', indexed_token)[0]
        word = re.findall(r'\d+ (.+)', indexed_token)[0]
        lemma = lemmas_dict.get(word)
        if lemma is not None:
            lemmatize_indexed_tokens.append(index + lemma)
    if sort:
        lemmatize_indexed_tokens = sorted(lemmatize_indexed_tokens, key=lambda token: re.findall(r'\d+ (.*)', token)[0])
    return lemmatize_indexed_tokens


def write_lemmas(lemmas, dirpath, filename):

    lemmas_string = '\n'.join(lemmas)
    dirname = re.findall(r'^\.\./\.\./data/tokenized/processed/(.*)', dirpath)
    directory = os.path.join('../../data/lemmatized/', dirname[0])
    file_writer.write(lemmas_string, directory, filename)


if __name__ == "__main__":
    main()
