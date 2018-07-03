import ressources.pyfreeling as freeling


def main():

    # Awesome freeling tools
    tk, sp, morfo, sen, wsd, tagger, parser = init_analyzers()

    #sample_sentence = "Me sentí super bien, muchisimas gracias fue una experiencia buena."
    #sample_sentence = "mucho ruido por parte de los trabajadores que realizan la remodelacion"
    sample_sentence = "muy mal servicio muy mala atension preocuparse más por el bienestar de las personas"
    # tokenize input line into a list of words
    lw = tk.tokenize(sample_sentence)
    # split list of words in sentences, return list of sentences
    ls = sp.split(lw)

    # perform morphosyntactic analysis and disambiguation
    ls = morfo.analyze(ls)
    ls = tagger.analyze(ls)
    # annotate and disambiguate senses
    ls = sen.analyze(ls)
    ls = wsd.analyze(ls)
    # parse sentences
    ls = parser.analyze(ls)

    # for each sentence in list
    for s in ls:

        # for each node in dependency tree
        dt = s.get_dep_tree()
        print_tree(dt)
        node = dt.begin()
        while node != dt.end():
            ssubj = ""
            lsubj = ""
            sdobj = ""
            ldobj = ""
            # if it is a verb, check dependants
            if node.get_word().get_tag()[0] == 'V':
                for ch in range(0, node.num_children()):
                    child = node.nth_child(ch)
                    if child.get_label() == "SBJ":
                        (lsubj, ssubj) = extract_lemma_and_sense(child.get_word())
                    #if child.get_label() == "OBJ":
                    #    (ldobj, sdobj) = extract_lemma_and_sense(child.get_word())

                #if lsubj != "" and ldobj != "":
                if lsubj != "":
                    (lpred, spred) = extract_lemma_and_sense(node.get_word())
                    print("SVO : (pred:   ", lpred, "[" + spred + "]")
                    print("       subject:", lsubj, "[" + ssubj + "]")
                    #print("       dobject:", ldobj, "[" + sdobj + "]")
                    print("      )")

            node.incr()


def print_tree(dt):
    print_node(dt.begin(), '')


def print_node(node, offset):
    print(offset, node.get_word().get_form(), ' (', node.get_label(), ', ', node.get_word().get_tag(), ', ', node.get_word().get_lemma(), ')')
    for ch in range(0, node.num_children()):
        child = node.nth_child(ch)
        print_node(child, offset + '    ')


def extract_lemma_and_sense(w) :
    lem = w.get_lemma()
    sens=""
    if len(w.get_senses()) > 0:
        sens = w.get_senses()[0][0]
    return lem, sens


def maco_options(lang, lpath):
    # For more options : https://talp-upc.gitbooks.io/freeling-tutorial/content/code/example01.py.html
    # create options holder
    opt = freeling.maco_options(lang)

    # Provide files for morphological submodules. Note that it is not
    # necessary to set file for modules that will not be used.
    opt.DictionaryFile = lpath + "dicc.src"
    opt.ProbabilityFile = lpath + "probabilitats.dat"
    opt.PunctuationFile = lpath + "../common/punct.dat"
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
                             True,  # PunctuationDetection,
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

    parser = freeling.dep_treeler(lpath + "dep_treeler/dependences.dat")

    return tk, sp, morfo, sen, wsd, tagger, parser


if __name__ == "__main__":
    main()
