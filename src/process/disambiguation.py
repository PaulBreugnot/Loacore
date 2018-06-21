import os
import re
import ressources.pyfreeling as freeling
import src.utils.file_writer as file_writer
from nltk.corpus import wordnet as wn


def main():

    # Awesome freeling tools
    tk, sp, morfo, sen, wsd, tagger = init_analyzers()

    for dirpath, dirnames, filenames in os.walk('../../data/tokenized/processed/'):
        for filename in filenames:
            tokens = open(os.path.join(dirpath, filename), encoding='utf-8').read()
            disambiguated_tokens = disambiguate_tokens(tokens, tk, sp, morfo, sen, wsd, tagger)
            write_disambiguated_tokens(disambiguated_tokens, dirpath, filename)


def disambiguate_tokens(tokens, tk, sp, morfo, sen, wsd, tagger):

    disambiguated_tokens = []
    # The file contains not ordered tokens, in the same order as in the original file
    # The tk.tokenize() function just convert them to the appropriate freeling format
    lw = tk.tokenize(tokens)
    # split list of words in sentences, return list of sentences
    # Actually, one sentence here
    ls = sp.split(lw)

    # perform morphosyntactic analysis and disambiguation
    ls = morfo.analyze(ls)
    ls = tagger.analyze(ls)
    # annotate and disambiguate senses
    ls = sen.analyze(ls)
    ls = wsd.analyze(ls)
    if len(ls) > 0:
        for index in range(len(ls[0])):
            rank = ls[0][index].get_senses()
            if len(rank) > 0:
                disambiguated_tokens.append(wn.of2ss(rank[0][0]).name() + "# " + lw[index].get_form())
            else:
                disambiguated_tokens.append("# " + lw[index].get_form())
    return disambiguated_tokens


def write_disambiguated_tokens(tokens, dirpath, filename):
    tokens_string = '\n'.join(tokens)
    dirname = re.findall(r'^\.\./\.\./data/tokenized/processed/(.*)', dirpath)
    directory = os.path.join('../../data/disambiguated/', dirname[0])
    file_writer.write(tokens_string, directory, filename)


def maco_options(lang,lpath) :
    # For more options : https://talp-upc.gitbooks.io/freeling-tutorial/content/code/example01.py.html
    # create options holder
    opt = freeling.maco_options(lang);

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.DictionaryFile = lpath + "dicc.src"
    opt.ProbabilityFile = lpath + "probabilitats.dat"
    return opt


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
                             True)  # ProbabilityAssignment

    # create analyzers
    tk = freeling.tokenizer(lpath + "tokenizer.dat")
    sp = freeling.splitter(lpath + "splitter.dat");
    # create sense annotator
    sen = freeling.senses(lpath + "senses.dat")
    # create sense disambiguator
    wsd = freeling.ukb(lpath + "ukb.dat")

    tagger = freeling.hmm_tagger(lpath + "tagger.dat", True, 2)

    return tk, sp, morfo, sen, wsd, tagger


if __name__ == "__main__":
    main()
