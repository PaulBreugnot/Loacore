
def compute_simple_files_polarity(files):
    """

    Perform the easiest sentiment analysis possible : a normalized sum of the positive/negative/objective polarities
    available in all synsets of each file.\n
    Return a dictionnary that map id_files to a polarity tuple. A polarity tuple is a tuple of length 3, with this
    form : (positive_score, negative_score, objective_score)

    :param files: Files to process
    :type files: :obj:`list` of :class:`File`
    :return: IdFile/Scores dictionary
    :rtype: :obj:`dict` of :obj:`int` : :obj:`tuple`
    :Example:
        Load all files, compute basic polarities, and show results with :func:`utils.print_polarity_table`.

        >>> import loacore.load.file_load as file_load
        >>> import loacore.analysis.sentiment_analysis as sentiment_analysis
        >>> files = file_load.load_database(load_deptrees=False)
        >>> polarities = sentiment_analysis.compute_simple_files_polarity(files)
        >>> from loacore.utils import plot_polarities
        >>> plot_polarities.print_polarity_table(polarities)
        +-----------------------------------------------------+-----------+-----------+-----------+
        |                         File                        | Pos_Score | Neg_Score | Obj_Score |
        +-----------------------------------------------------+-----------+-----------+-----------+
        |     EncuestaTemporadaBajafinalbalneario2_EO.txt     |   0.000   |   0.000   |   1.000   |
        |     EncuestaTemporadaBajafinalbalneario2_CC.txt     |   0.069   |   0.016   |   0.915   |
        |     EncuestaTemporadaBajafinalbalneario2_GR.txt     |   0.000   |   0.000   |   1.000   |
        |     EncuestaTemporadaBajafinalbalneario2_JA.txt     |   0.060   |   0.065   |   0.875   |
        |     EncuestaTemporadaBajafinalbalneario2_CD.txt     |   0.080   |   0.057   |   0.863   |
        |     EncuestaTemporadaBajafinalbalneario3_JA.txt     |   0.055   |   0.023   |   0.922   |
        |     EncuestaTemporadaBajafinalbalneario3_CD.txt     |   0.019   |   0.022   |   0.958   |
        |     EncuestaTemporadaBajafinalbalneario3_CC.txt     |   0.044   |   0.003   |   0.953   |
        |     EncuestaTemporadaBajafinalbalneario3_GR.txt     |   0.036   |   0.000   |   0.964   |
        ...

    """

    file_score_dict = {}
    for file in files:
        file_pos_score = 0
        file_neg_score = 0
        file_obj_score = 0
        for review in file.reviews:
            for sentence in review.sentences:
                for word in sentence.words:
                    if word.synset is not None:
                        file_pos_score += word.synset.pos_score
                        file_neg_score += word.synset.neg_score
                        file_obj_score += word.synset.obj_score
        total = file_pos_score + file_neg_score + file_obj_score
        if total > 0:
            file_score_dict[file.id_file] = \
                (file_pos_score / total, file_neg_score / total, file_obj_score / total)

    return file_score_dict


def compute_extreme_files_polarity(files, pessimistic=False):
    """

    Performs *extreme* file polarity computation : only the most pessimistic or optimistic sense
    (according to pessimistic argument) is considered. Those values tend to show how the disambiguation process is
    important, due to the huge difference between pessimistic and optimistic scores.\n
    Also notice that this function is an interesting example of how other processes could be applied to data already
    computed in database. Here, the computed scores of disambiguated synsets are not used, and their are computed from
    the re-computed possible senses thanks to freeling.\n
    Check source code for more detailed explanations about this example.\n
    \n
    Return a dictionnary that map id_files to a polarity tuple. A polarity tuple is a tuple of length 3, with this
    form : (positive_score, negative_score, objective_score)

    :param files: Files to process
    :type files: :obj:`list` of :obj:`files`
    :param pessimistic: Specify if pessimistic computing should be used. Optimistic is used if set to False.
    :type pessimistic: boolean
    :return: IdFile/Scores dictionary
    :rtype: :obj:`dict` of :obj:`int` : :obj:`tuple`

    :Example:
        Compute optimistic and pessimistic polarities and save them as .pdf files using the GUI.

        >>> import loacore.load.file_load as file_load
        >>> import loacore.analysis.sentiment_analysis as sentiment_analysis
        >>> from loacore.utils import plot_polarities
        >>> files = file_load.load_database(load_deptrees=False)
        >>> polarities = sentiment_analysis.compute_extreme_files_polarity(files)
        >>> plot_polarities.save_polarity_pie_charts(polarities)
        >>> polarities = sentiment_analysis.compute_extreme_files_polarity(files, pessimistic=True)
        >>> plot_polarities.save_polarity_pie_charts(polarities)

    """

    import ressources.pyfreeling as freeling
    from nltk.corpus import wordnet as wn
    from nltk.corpus import sentiwordnet as swn

    def my_maco_options(lang, lpath):
        # create options holder
        opt = freeling.maco_options(lang)

        # Provide files for morphological submodules. Note that it is not
        # necessary to set file for modules that will not be used.
        opt.DictionaryFile = lpath + "dicc.src"
        opt.PunctuationFile = lpath + "../common/punct.dat"
        return opt

    def init_freeling():

        freeling.util_init_locale("default")

        import loacore
        lang = loacore.lang
        # path to language data
        lpath = loacore.LANG_PATH

        # create the analyzer with the required set of maco_options
        morfo = freeling.maco(my_maco_options(lang, lpath))
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
                                 False)  # ProbabilityAssignment

        return morfo

    def pessimistic_score(synsets):
        selected_synset = None
        max_score = 0
        for synset in synsets:
            # Convert freeling sense to a synset name
            synset_name = synset.name()
            # Get score from SentiWordNet
            neg_score = swn.senti_synset(synset_name).neg_score()
            if neg_score > max_score:
                max_score = neg_score
                selected_synset = synset_name
        if selected_synset is not None:
            return (swn.senti_synset(selected_synset).pos_score(),
                    swn.senti_synset(selected_synset).neg_score(),
                    swn.senti_synset(selected_synset).pos_score())
        else:
            return 0, 0, 0

    def optimistic_score(synsets):
        selected_synset = None
        max_score = 0
        for synset in synsets:
            # Convert freeling sense to a synset name
            synset_name = synset.name()
            # Get score from SentiWordNet
            pos_score = swn.senti_synset(synset_name).pos_score()
            if pos_score > max_score:
                max_score = pos_score
                selected_synset = synset_name
        if selected_synset is not None:
            return (swn.senti_synset(selected_synset).pos_score(),
                    swn.senti_synset(selected_synset).neg_score(),
                    swn.senti_synset(selected_synset).pos_score())
        else:
            return 0, 0, 0

    morfo = init_freeling()

    file_score_dict = {}
    for file in files:
        file_pos_score = 0
        file_neg_score = 0
        file_obj_score = 0

        # Convert Sentences in Freeling Sentences
        freeling_sentences = []
        for review in file.reviews:
            freeling_sentences += [s.compute_freeling_sentence() for s in review.sentences]

        # Freeling analysis : lemmatization
        freeling_sentences = morfo.analyze(freeling_sentences)

        # Score computation
        for s in freeling_sentences:
            for w in s:
                if not w.get_lemma() == '':
                    # Possible synsets are computed using nltk and WordNet
                    if pessimistic:
                        score = pessimistic_score(wn.synsets(w.get_lemma(), lang='spa'))
                    else:
                        score = optimistic_score(wn.synsets(w.get_lemma(), lang='spa'))

                    file_pos_score += score[0]
                    file_neg_score += score[1]
                    file_obj_score += score[2]

        total = file_pos_score + file_neg_score + file_obj_score
        if total > 0:
            file_score_dict[file.id_file] = \
                (file_pos_score / total, file_neg_score / total, file_obj_score / total)

    return file_score_dict


def compute_pattern_files_polarity(files, check_adj_pattern=True):

    def verb_pattern_rec(node, score):
        # node is a verb
        return score

    def resolve_adj_rule(parent_node, child):
        # child is the adj applied to parent_node
        # returns true if we need to invert parent_node polarity
        if parent_node.word.synset is not None and child.word.synset is not None:
            if (parent_node.word.synset.pos_score > parent_node.word.synset.neg_score
                    and child.word.synset.pos_score < child.word.synset.neg_score):
                # AdjN + NounP
                # Noun needs to be considered negative
                return True
            return False
        return False

    def check_adj_pattern(node, pos_score, neg_score):
        for child in node.children:
            if child.word.PoS_tag is not None:
                if child.word.PoS_tag[0] == 'A':
                    # An adjective is applied to parent_node
                    if resolve_adj_rule(node, child):
                        print(node.word.word, " : ", child.word.word)
                        # if at least one negative adjective is applied to a positive node, its polarity is inverted
                        return neg_score, pos_score
        # Nothing is changed
        return pos_score, neg_score

    def children_rec(parent_node):
        if parent_node.word.synset is not None:
            node_pos_score = parent_node.word.synset.pos_score
            node_neg_score = parent_node.word.synset.neg_score
        else:
            node_pos_score = 0
            node_neg_score = 0

        if check_adj_pattern:
            node_pos_score, node_neg_score = check_adj_pattern(parent_node, node_pos_score, node_neg_score)

        for child in parent_node.children:
            child_score = children_rec(child)
            node_pos_score += child_score[0]
            node_neg_score += child_score[1]

        return node_pos_score, node_neg_score

    for file in files:
        for review in file.reviews:
            for sentence in review.sentences:
                dep_tree = sentence.dep_tree
                test_score = 0
                for word in sentence.words:
                    if word.synset is not None:
                        test_score += word.synset.pos_score
                print(children_rec(dep_tree.root)[0], " : ", test_score)