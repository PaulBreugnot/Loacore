from loacore.classes.classes import Polarity


def compute_simple_reviews_polarity(reviews, commit_polarities=False):
    """

    Perform the easiest sentiment analysis possible : a normalized sum of the positive/negative/objective polarities
    available in all synsets of each review, setting the polarity in the review.polarities dict, with the entry
    "simple".

    :param reviews: Files to process
    :type reviews: :obj:`list` of |Review|
    :param commit_polarities: If True, results will be committed to database.
    :type commit_polarities: bool
    :return: Reviews with polarity.
    :rtype: |ReviewIterator|

    :Example:

        Commit simple polarities of uci files to database.

        .. code-block:: Python

            import loacore.analysis.sentiment_analysis as sentiment_analysis
            import loacore.load.file_load as file_load
            import loacore.load.review_load as review_load

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            reviews = review_load.load_reviews_by_id_files(id_files=ids, load_sentences=True, load_words=True)
            sentiment_analysis.compute_simple_reviews_polarity(reviews, commit_polarities=True)

    .. warning::

        If *reviews* have been loaded in temporary files (with *load_in_temp_file=True* in
        :func:`~loacore.load.file_load.load_database()`), input *reviews* (that is an iterator) won't be modified
        dynamically. However, results can be committed to database normally, and results will be available in the
        returned ReviewIterator (i.e. new temp files).
    """

    def commit_subset():
        nonlocal modified_reviews
        nonlocal temp_files
        temp_files.append(save_to_temp_file(modified_reviews))
        if commit_polarities:
            import loacore.process.polarity_process as polarity_process
            polarity_process.commit_polarities(modified_reviews, "simple")
        modified_reviews.clear()

    from loacore.utils.data_stream import ReviewIterator, save_to_temp_file
    from loacore.utils.db import database_backup

    with database_backup():
        # Reviews are split to avoid RAM overload
        temp_files = []
        split_size = 500
        index = 0
        review_count = 0
        modified_reviews = []
        for review in reviews:
            index += 1
            review_count += 1
            print("\r" + str(review_count) + " reviews processed.", end="")
            review_pos_score = 0
            review_neg_score = 0
            review_obj_score = 0
            for sentence in review.sentences:
                for word in sentence.words:
                    if word.synset is not None:
                        review_pos_score += word.synset.pos_score
                        review_neg_score += word.synset.neg_score
                        review_obj_score += word.synset.obj_score
            total = review_pos_score + review_neg_score + review_obj_score
            if total > 0:
                review.polarities["simple"] =\
                    Polarity(None, "simple", review.id_review,
                             review_pos_score/total, review_neg_score/total, review_obj_score/total)
            else:
                review.polarities["simple"] = Polarity(None, "simple", review.id_review, 0, 0, 0)

            modified_reviews.append(review)

            if index == split_size:
                index = 0
                commit_subset()

        commit_subset()
    print("")

    return ReviewIterator(temp_file_list=temp_files)


def compute_simple_files_polarity(files, commit_polarities=True):
    """
    Compute the simple polarity of all the reviews in each file, and then compute the normalized sum of polarities of
    all reviews of each file, and return them as a dictionary that map id_files to polarity tuples (pos_score,
    neg_score, obj_score).

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :param commit_polarities: If True, results will be committed to database.
    :type commit_polarities: bool
    :return: Polarity dict
    :rtype: :obj:`dict` of :obj:`int` : :obj:`tuple`

    :Example:
        Load uci files, compute basic polarities, and show results with :func:`utils.print_polarity_table`.

        >>> import loacore.load.file_load as file_load
        >>> import loacore.analysis.sentiment_analysis as sentiment_analysis
        >>> ids = file_load.get_id_files_by_file_path([r'.*/uci/.+'])
        >>> files = file_load.load_database(id_files=ids, load_deptrees=False)
        >>> polarities = sentiment_analysis.compute_simple_files_polarity(files)
        >>> from loacore.utils import plot_polarities
        >>> plot_polarities.print_polarity_table(polarities)
        +---------------------------+-----------+-----------+-----------+
        |            File           | Pos_Score | Neg_Score | Obj_Score |
        +---------------------------+-----------+-----------+-----------+
        |     imdb_labelled.txt     |   0.117   |   0.088   |   0.795   |
        |     yelp_labelled.txt     |   0.123   |   0.086   |   0.790   |
        | amazon_cells_labelled.txt |   0.118   |   0.090   |   0.792   |
        +---------------------------+-----------+-----------+-----------+

    """

    file_score_dict = {}
    for file in files:
        reviews_with_polarities = compute_simple_reviews_polarity(file.reviews, commit_polarities=commit_polarities)
        pos_score = sum([r.polarities["simple"].pos_score for r in reviews_with_polarities])
        neg_score = sum([r.polarities["simple"].neg_score for r in reviews_with_polarities])
        obj_score = sum([r.polarities["simple"].obj_score for r in reviews_with_polarities])
        total = pos_score + neg_score + obj_score
        file_score_dict[file.id_file] = (pos_score / total, neg_score / total, obj_score / total)

    return file_score_dict


def compute_extreme_reviews_polarity(reviews, commit_polarities=False, pessimistic=False, freeling_lang="es"):
    """

    Performs *extreme* reviews polarity computation : only the most pessimistic or optimistic sense
    (according to pessimistic argument) is considered. Those values tend to show how the disambiguation process is
    important, due to the huge difference between pessimistic and optimistic scores.\n
    Also notice that this function is an interesting example of how other processes could be applied to data already
    computed in database. Here, the disambiguated synsets are not used, and all senses re-computed with Freeling are
    used.\n
    Check source code for more detailed explanations about this example.\n
    \n
    Polarities are then stored in reviews, with the analysis label 'optimistic' or 'pessimistic' according to
    *pessimistic* parameter, and eventually committed to database if *commit_polarities* is set to True.

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :param commit_polarities: If True, results will be committed to database.
    :type commit_polarities: bool
    :param pessimistic: Specify if pessimistic computing should be used. Optimistic is used if set to False.
    :type pessimistic: boolean
    :param freeling_lang:
        Specify language used by Freeling. Default : 'es'.\n
        Possible values : 'as', 'ca', 'cs', 'cy', 'de', 'en', 'es', 'fr', 'gl', 'hr', 'it', 'nb', 'pt', 'ru', 'sl')\n
        See https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/basics.html for more details.
    :type freeling_lang: String
    :return: Reviews with polarity.
    :rtype: :obj:`list` of |Review|

    :Example:

        Commit pessimistic polarities of uci files to database.

        .. code-block:: Python

            import loacore.analysis.sentiment_analysis as sentiment_analysis
            import loacore.load.file_load as file_load
            import loacore.load.review_load as review_load

            ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
            reviews = review_load.load_reviews_by_id_files(id_files=ids, load_sentences=True, load_words=True)
            sentiment_analysis.compute_extreme_reviews_polarity(reviews, commit_polarities=True, pessimistic=True,
                                                                freeling_lang='en')

    .. warning::

        If *reviews* have been loaded in temporary files (with *load_in_temp_file=True* in
        :func:`~loacore.load.file_load.load_database()`), input *reviews* (that is an iterator) won't be modified
        dynamically. However, results can be committed to database normally, and results will be available in the
        returned ReviewIterator (i.e. new temp files).
    """

    from loacore.conf import set_lang
    set_lang(freeling_lang)

    from pyFreelingApi import freeling_api as freeling
    from nltk.corpus import wordnet as wn
    from nltk.corpus import sentiwordnet as swn

    def my_maco_options(lang, lpath):
        # create options holder
        opt = freeling.maco_options(lang)

        # Provide files for morphological submodules. Note that it is not
        # necessary to set file for modules that will not be used.
        opt.DictionaryFile = lpath + "dicc.src"
        opt.ProbabilityFile = lpath + "probabilitats.dat"
        opt.PunctuationFile = lpath + "../common/punct.dat"
        return opt

    def init_freeling():

        freeling.util_init_locale("default")

        from loacore.conf import lang
        from loacore.conf import LANG_PATH as lpath

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
                                 True)  # ProbabilityAssignment

        # create tagger
        tagger = freeling.hmm_tagger(lpath + "tagger.dat", False, 2)

        # create sense annotator
        sen = freeling.senses(lpath + "senses.dat")

        return morfo, tagger, sen

    def pessimistic_score(synsets):
        selected_synset = None
        max_score = 0
        for synset in synsets:
            if not synset[0][0] == '8':
                # ignore synsets offsets 8.......-.
                # they are odd synsets that WordNet can't find...
                synset_name = wn.of2ss(synset[0]).name()
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
            if not synset[0][0] == '8':
                # ignore synsets offsets 8.......-.
                # they are odd synsets that WordNet can't find...
                synset_name = wn.of2ss(synset[0]).name()
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

    morfo, tagger, sen = init_freeling()

    if pessimistic:
        analysis_label = 'pessimistic'
    else:
        analysis_label = 'optimistic'

    modified_reviews = []
    for review in reviews:
        review_pos_score = 0
        review_neg_score = 0
        review_obj_score = 0

        # Convert Sentences in Freeling Sentences
        freeling_sentences = [s.compute_freeling_sentence() for s in review.sentences]

        # Freeling analysis : lemmatization
        freeling_sentences = morfo.analyze(freeling_sentences)
        freeling_sentences = tagger.analyze(freeling_sentences)
        # add senses
        freeling_sentences = sen.analyze(freeling_sentences)

        # Score computation
        for s in freeling_sentences:
            for w in s:
                if not w.get_lemma() == '':
                    # Possible synsets are computed using nltk and WordNet
                    if pessimistic:
                        score = pessimistic_score(w.get_senses())
                    else:
                        score = optimistic_score(w.get_senses())

                    review_pos_score += score[0]
                    review_neg_score += score[1]
                    review_obj_score += score[2]

        total = review_pos_score + review_neg_score + review_obj_score

        if total > 0:
            review.polarities[analysis_label] =\
                Polarity(None, analysis_label, review.id_review,
                         review_pos_score/total, review_neg_score/total, review_obj_score/total)
        else:
            review.polarities[analysis_label] = \
                Polarity(None, analysis_label, review.id_review, 0, 0, 0)
        modified_reviews.append(review)

    if commit_polarities:
        import loacore.process.polarity_process as polarity_process
        polarity_process.commit_polarities(modified_reviews, analysis_label)

    return modified_reviews


def compute_extreme_files_polarity(files, pessimistic=False, commit_polarities=True, freeling_lang='en'):
    """
    Compute the extreme polarity of all the reviews in each file, and then compute the normalized sum of polarities of
    all reviews of each file, and return them as a dictionary that map id_files to polarity tuples (pos_score,
    neg_score, obj_score).

    :param files: Files to process
    :type files: :obj:`list` of |File|
    :param pessimistic: Specify if pessimistic computing should be used. Optimistic is used if set to False.
    :type pessimistic: boolean
    :param commit_polarities: If True, results will be committed to database.
    :type commit_polarities: bool
    :param freeling_lang: Freeling language to use.
    :return: Score dictionary
    :rtype: :obj:`dict` of :obj:`int` : :obj:`tuple`

    :Example:
        Compute optimistic and pessimistic polarities of uci files.

        >>> import loacore.load.file_load as file_load
        >>> import loacore.analysis.sentiment_analysis as sentiment_analysis
        >>> from loacore.utils import plot_polarities
        >>> ids = file_load.get_id_files_by_file_path(r'.*/uci/.+')
        >>> files = file_load.load_database(id_files=ids, load_deptrees=False)
        >>> polarities = sentiment_analysis.compute_extreme_files_polarity(files, freeling_lang='en')
        >>> plot_polarities.print_polarity_table(polarities)
        +---------------------------+-----------+-----------+-----------+
        |            File           | Pos_Score | Neg_Score | Obj_Score |
        +---------------------------+-----------+-----------+-----------+
        |     imdb_labelled.txt     |   0.467   |   0.066   |   0.467   |
        |     yelp_labelled.txt     |   0.465   |   0.069   |   0.465   |
        | amazon_cells_labelled.txt |   0.462   |   0.076   |   0.462   |
        +---------------------------+-----------+-----------+-----------+
        >>> polarities = sentiment_analysis.compute_extreme_files_polarity(files, pessimistic=True, freeling_lang='en')
        >>> plot_polarities.print_polarity_table(polarities)
        +---------------------------+-----------+-----------+-----------+
        |            File           | Pos_Score | Neg_Score | Obj_Score |
        +---------------------------+-----------+-----------+-----------+
        |     imdb_labelled.txt     |   0.091   |   0.819   |   0.091   |
        |     yelp_labelled.txt     |   0.056   |   0.887   |   0.056   |
        | amazon_cells_labelled.txt |   0.049   |   0.901   |   0.049   |
        +---------------------------+-----------+-----------+-----------+

    """

    file_score_dict = {}
    if pessimistic:
        analysis_label = 'pessimistic'
    else:
        analysis_label = 'optimistic'

    for file in files:
        compute_extreme_reviews_polarity(file.reviews,
                                         pessimistic=pessimistic,
                                         freeling_lang=freeling_lang,
                                         commit_polarities=commit_polarities)
        pos_score = sum([r.polarities[analysis_label].pos_score for r in file.reviews])
        neg_score = sum([r.polarities[analysis_label].neg_score for r in file.reviews])
        obj_score = sum([r.polarities[analysis_label].obj_score for r in file.reviews])
        total = pos_score + neg_score + obj_score
        file_score_dict[file.id_file] = (pos_score / total, neg_score / total, obj_score / total)

    return file_score_dict


def compute_pattern_reviews_polarity(reviews, commit_polarities=False, adj_pattern=True, cc_pattern=True,
                                     print_polarity_commutations=False):
    """
    Compute reviews polarity considering adjective and/or complement polarity commutation.

    :param reviews: Reviews to process
    :type reviews: :obj:`list` of |Review|
    :param commit_polarities: If True, results will be committed to database.
    :type commit_polarities: bool
    :param adj_pattern: If True, adjective commutation are considered.
    :type adj_pattern: bool
    :param cc_pattern: If True, complement commutation are considered.
    :type cc_pattern: bool
    :param print_polarity_commutations: If True, prints elements where a commutation occured.
    :type print_polarity_commutations: bool
    :return: Reviews with polarity.
    :rtype: :obj:`list` of |Review|

    .. warning::

        If *reviews* have been loaded in temporary files (with *load_in_temp_file=True* in
        :func:`~loacore.load.file_load.load_database()`), input *reviews* (that is an iterator) won't be modified
        dynamically. However, results can be committed to database normally, and results will be available in the
        returned ReviewIterator (i.e. new temp files).
    """

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
            if child.word.PoS_tag is not None and child.word.PoS_tag[:2] == 'JJ':
                    # An adjective is applied to parent_node
                    if resolve_adj_rule(node, child):
                        if print_polarity_commutations:
                            print("ADJ : ", node.word.word, " : ", child.word.word)
                        # if at least one negative adjective is applied to a positive node, its polarity is inverted
                        return neg_score, pos_score
        # Nothing is changed
        return pos_score, neg_score

    def resolve_cc_rule(parent_node, child_pos_score, child_neg_score):
        # child is the adj applied to parent_node
        # returns true if we need to invert parent_node polarity
        if parent_node.word.synset is not None:
            if (parent_node.word.synset.pos_score < parent_node.word.synset.neg_score
                    and child_pos_score > child_neg_score):
                # VerbN + ComplementP
                # Complement needs to be considered negative
                return True
            return False
        return False

    def check_cc_pattern(node, child, child_score, CC_to_print):
        child_pos_score = child_score[0]
        child_neg_score = child_score[1]
        child_obj_score = child_score[2]
        if child.label == 'OBJ':
                # An complement is applied to parent_node
                if resolve_cc_rule(node, child_pos_score, child_neg_score):
                    # print(node.word.word)
                    CC_to_print.append(node)
                    return child_neg_score, child_pos_score, child_obj_score
        # Nothing is changed
        return child_pos_score, child_neg_score, child_obj_score

    def children_rec(parent_node, CC_to_print):
        if parent_node.word.synset is not None:
            node_pos_score = parent_node.word.synset.pos_score
            node_neg_score = parent_node.word.synset.neg_score
            node_obj_score = parent_node.word.synset.obj_score
        else:
            node_pos_score = 0
            node_neg_score = 0
            node_obj_score = 0

        if adj_pattern:
            # Here, we potentially need to invert the Noun parent polarity
            if parent_node.word.PoS_tag is not None and parent_node.word.PoS_tag[0] == 'N':
                node_pos_score, node_neg_score = check_adj_pattern(parent_node, node_pos_score, node_neg_score)

        # print(parent_node.word.word)
        # print(" ", [n.word.word for n in parent_node.children])

        for child in parent_node.children:
            child_score = children_rec(child, CC_to_print)
            if cc_pattern:
                # Here, we potentially need to invert the Complement child tree polarity
                if parent_node.word.PoS_tag is not None and parent_node.word.PoS_tag[0] == 'V':
                    child_score = check_cc_pattern(parent_node, child, child_score, CC_to_print)
            node_pos_score += child_score[0]
            node_neg_score += child_score[1]
            node_obj_score += child_score[2]

        return node_pos_score, node_neg_score, node_obj_score

    analysis_label = "pattern"
    if adj_pattern:
        analysis_label += "_adj"
    if cc_pattern:
        analysis_label += "_cc"

    print(analysis_label)
    print(check_cc_pattern)

    modified_reviews = []
    for review in reviews:
        review_pos_score = 0
        review_neg_score = 0
        review_obj_score = 0
        for sentence in review.sentences:
            dep_tree = sentence.dep_tree
            test_score = 0
            for word in sentence.words:
                if word.synset is not None:
                    test_score += word.synset.pos_score

            CC_to_print = []

            pos_score, neg_score, obj_score = children_rec(dep_tree.root, CC_to_print)

            total = pos_score + neg_score + obj_score
            if total > 0:
                pos_score = pos_score / total
                neg_score = neg_score / total
                obj_score = obj_score / total

                review_pos_score += pos_score
                review_neg_score += neg_score
                review_obj_score += obj_score

            if print_polarity_commutations:
                for node in CC_to_print:
                    sentence.sentence_str()
                    print("ROOT NODE : ", node.word.word)
                    dep_tree.dep_tree_str(root=node)

                if not pos_score == test_score:
                    sentence.sentence_str()
                    print(pos_score, " : ", test_score)
                    print('')

        total = review_pos_score + review_neg_score + review_obj_score

        if total > 0:
            review.polarities[analysis_label] = Polarity(None, analysis_label, review.id_review,
                                                         review_pos_score/total,
                                                         review_neg_score/total,
                                                         review_obj_score/total)
        else:
            review.polarities[analysis_label] = Polarity(None, analysis_label, review.id_review, 0, 0, 0)

        modified_reviews.append(review)

    if commit_polarities:
        import loacore.process.polarity_process as polarity_process
        polarity_process.commit_polarities(modified_reviews, analysis_label)

    return modified_reviews
