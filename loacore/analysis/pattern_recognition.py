"""

Patterns recognitions are realized on the dependency trees computed with Freeling. This means that *parent-child*
structures will be matched, what **don't necessarily correspond to adjacent words in the original sentence**.
"""


def pos_tag_patterns_recognition(sentences, pattern):
    """
    Recognize a PoS_tag pattern in the DepTrees associated to specified sentences.\n
    PoS_tags corresponding to each language can be found there :
    https://talp-upc.gitbooks.io/freeling-4-1-user-manual/content/tagsets.html

    :param sentences: Sentences to process
    :type sentences: :obj:`list` of |Sentence|
    :param pattern:
        A 2 dimensional list of strings representing patterns. The patterns list pattern[i] represents the PoS_tags that
        will match at position i. ex : *pattern = [['V'], ['A', 'NC']]* recognizes verbs followed by an adjective or a
        common noun.

        .. note::   Matches are performed with the beginning of the PoS_tag, according to the length of the specified
                    tags. For example, 'A' will match 'AQ0CS00', 'AQ0MS00'...

    :type pattern: :obj:`list` of :obj:`list` of :obj:`str`
    :return: Matching patterns in specified sentences, as node tuples.
    :rtype: :obj:`list` of :obj:`tuple` of |DepTreeNode|

    :Example:
        Find all Noun/Adjective patterns in file 28 (_PQRS.txt).

        >>> import loacore.load.sentence_load as sentence_load
        >>> sentences = sentence_load.load_sentences_by_id_files([28])
        >>> import loacore.analysis.pattern_recognition as pattern_recognition
        >>> patterns = pattern_recognition.pos_tag_patterns_recognition(sentences, [['N'], ['A']])
        >>> patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True)
        ( manera : NCFS000, grosera : AQ0FS00 )
        ( manera : NCFS000, igual : AQ0CS00 )
        ( señora : NCFS000, irrespetuosa : AQ0FS00 )
        ( zona : NCFS000, visible : AQ0CS00 )
        ( manera : NCFS000, grosera : AQ0FS00 )
        ( espacio : NCMS000, mejor : AQ0CS00 )
        ( atencion : NCFS000, mejor : AQ0CS00 )
        ...

    .. note::

        This function can also be used to recognize unigram patterns.

            **Example :** Find all verbs in file 28 (_PQRS.txt)

            >>> import loacore.load.sentence_load as sentence_load
            >>> sentences = sentence_load.load_sentences_by_id_files([28])
            >>> import loacore.analysis.pattern_recognition as pattern_recognition
            >>> patterns = pattern_recognition.pos_tag_patterns_recognition(sentences, [['V']])
            >>> patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True, label_display=True)
            ( parece : VMIP3S0 : sentence )
            ( promueven : VMIP3P0 : S )
            ( atiende : VMIP3S0 : S )
            ( atiendan : VMSP3P0 : S )
            ( atiende : VMIP3S0 : S )
            ( viniera : VMSI3S0 : S )
            ( orientar : VMN0000 : S )
            ( contratar : VMN0000 : S )
            ( era : VSII3S0 : sentence )
            ( argumentando : VMG0000 : gerundi )
            ( poner : VMN0000 : S )
            ...

    """

    def pos_tag_rec(results, current_matching_nodes, node, pattern, index):
        if node.word.PoS_tag is not None:
            if '*' in pattern[index]:
                current_matching_nodes.append(node)
                if index == len(pattern) - 1:
                    results.append(current_matching_nodes)
                else:
                    for child in node.children:
                        pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)
            else:
                for i in range(len(pattern[index])):
                    # Need to consider the length of each tag in pattern[index]
                    if node.word.PoS_tag[:len(pattern[index][i])] == pattern[index][i]:
                        current_matching_nodes.append(node)
                        if index == len(pattern) - 1:
                            results.append(current_matching_nodes)
                        else:
                            for child in node.children:
                                pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)
        elif pattern[index] == '*':
            # Allow to match a word withou PoS_tag
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                for child in node.children:
                    pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)

    def children_rec(results, node):
        pos_tag_rec(results, [], node, pattern, 0)
        for child in node.children:
            children_rec(results, child)
        return results

    matching_nodes = []
    for sentence in sentences:
        dep_tree = sentence.dep_tree

        matching_nodes += children_rec([], dep_tree.root)
    return matching_nodes


def label_patterns_recognition(sentences, pattern):
    """
    Recognize a dependency label pattern in the DepTrees associated to specified sentences.\n
    Labels used for Spanish can be found there :\n
        - http://clic.ub.edu/corpus/webfm_send/20
        - http://clic.ub.edu/corpus/webfm_send/18
        - http://clic.ub.edu/corpus/webfm_send/49

    :param sentences: Sentences to process
    :type sentences: :obj:`list` of |Sentence|
    :param pattern:
        A 2 dimensional list of strings representing patterns. The patterns list pattern[i] represents the label that
        will match at position i. ex : *pattern = [['sentence', 'v'], ['*']]* could be used to find all the dependency
        functions that could follow *sentence* of *v* function.

    :type pattern: :obj:`list` of :obj:`list` of :obj:`str`
    :return: Matching patterns in specified sentences, as node tuples.
    :rtype: :obj:`list` of :obj:`tuple` of |DepTreeNode|

    :Example:
        Find all node to which a verbal modifier is applied in file 28 (_PQRS.txt).\n
        (classically, a negation that applies to the parent verb)

        >>> import loacore.load.sentence_load as sentence_load
        >>> sentences = sentence_load.load_sentences_by_id_files([28])
        >>> import loacore.analysis.pattern_recognition as pattern_recognition
        >>> patterns = pattern_recognition.label_patterns_recognition(sentences, [['*'], ['mod']])
        >>> patterns_str = pattern_recognition.print_patterns(patterns, label_display=True)
        ( bajar : ao, ya : mod )
        ( bajar : ao, no : mod )
        ( podia : S, tampoco : mod )
        ( quiere : ao, no : mod )
        ( dejan : S, no : mod )
        ...

    .. note::

        This function can also be used to recognize unigram patterns.

            **Example :** Find all the nodes with dependency label 'suj' in file 28 (_PQRS.txt)

            >>> import loacore.load.sentence_load as sentence_load
            >>> sentences = sentence_load.load_sentences_by_id_files([28])
            >>> import loacore.analysis.pattern_recognition as pattern_recognition
            >>> patterns = pattern_recognition.label_patterns_recognition(sentences, [['suj']])
            >>> patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True, label_display=True)
            ( colmo : NCMS000 : suj )
            ( que : None : suj )
            ( que : None : suj )
            ( tencion : None : suj )
            ( señora : NCFS000 : suj )
            ( que : None : suj )
            ( turista : NCCS000 : suj )
            ( ella : None : suj )
            ( que : None : suj )
            ...

    """

    def label_rec(results, current_matching_nodes, node, pattern, index):
        if '*' in pattern[index] or node.label in pattern[index]:
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                for child in node.children:
                    label_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)

    def children_rec(results, node):
        label_rec(results, [], node, pattern, 0)

        for child in node.children:
            children_rec(results, child)

        return results

    matching_nodes = []
    for sentence in sentences:
        dep_tree = sentence.dep_tree

        matching_nodes += children_rec([], dep_tree.root)
    return matching_nodes


def general_pattern_recognition(sentences, pattern, types):
    """
        Recognize a general pattern, compound of PoS_tags and dependency labels, in the DepTrees associated to specified
        sentences.\n


        :param sentences: Sentences to process
        :type sentences: :obj:`list` of |Sentence|
        :param pattern:
            A 2 dimensional list of strings representing patterns. The patterns list pattern[i] represents the label
            that will match at position i. ex : *pattern = [['V'], ['cc', 'ci', 'cd']]* will match all the
            *Verb/complement* structures.
        :type pattern: :obj:`list` of :obj:`list` of :obj:`str`
        :param types:
            Specify what type of match to use, such that *types[i]* specifies if elements of *pattern[i]* have to be
            condidered as PoS_tag or label. Notice that types is unidimensional, whereas pattern can be 2 dimensional :
            this means that for consistency reason, we assume that all the tags that can match in a position *i* are of
            the same nature.
        :type types:
            :obj:`list` of :obj:`str`. Allowed value are 'PoS_tag' and 'label'. Otherwise, nothing will
            match.
        :return: Matching patterns in specified sentences, as node tuples.
        :rtype: :obj:`list` of :obj:`tuple` of |DepTreeNode|

        :Example:
            Find all the Verb(PoS_tag)/complement(label) patterns in file 28(_PQRS.txt).\n
            (classically, a negation that applies to the parent verb)

            >>> import loacore.load.sentence_load as sentence_load
            >>> sentences = sentence_load.load_sentences_by_id_files([28])
            >>> import loacore.analysis.pattern_recognition as pattern_recognition
            >>> patterns = pattern_recognition.general_pattern_recognition(sentences, [['V'], ['cc', 'ci', 'cc']], ['PoS_tag', 'label'])
            >>> patterns_str = pattern_recognition.print_patterns(patterns, PoS_tag_display=True, label_display=True)
            ( parece : VMIP3S0 : sentence, me : None : ci )
            ( promueven : VMIP3P0 : S, en : None : cc )
            ( atiende : VMIP3S0 : S, de : None : cc )
            ( atiende : VMIP3S0 : S, como : None : cc )
            ( atiendan : VMSP3P0 : S, de : None : cc )
            ( atiende : VMIP3S0 : S, en : None : cc )
            ( viniera : VMSI3S0 : S, con : None : cc )
            ( orientar : VMN0000 : S, en : None : cc )
            ( orientar : VMN0000 : S, al : None : cc )
            ( poner : VMN0000 : S, le : None : ci )
            ( poner : VMN0000 : S, a : None : ci )
            ( establecer : VMN0000 : S, uun : None : cc )
            ...

        """

    def pos_tag_rec(results, current_matching_nodes, node, pattern, types, index):
        if node.word.PoS_tag is not None:
            if '*' in pattern[index]:
                current_matching_nodes.append(node)
                if index == len(pattern) - 1:
                    results.append(current_matching_nodes)
                else:
                    for child in node.children:
                        if types[index + 1] == 'pos_tag':
                            pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
                        else:
                            label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
            else:
                for i in range(len(pattern[index])):
                    # Need to consider the length of each tag in pattern[index]
                    if node.word.PoS_tag[:len(pattern[index][i])] == pattern[index][i]:
                        current_matching_nodes.append(node)
                        if index == len(pattern) - 1:
                            results.append(current_matching_nodes)
                        else:
                            for child in node.children:
                                if types[index + 1] == 'pos_tag':
                                    pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types,
                                                index + 1)
                                else:
                                    label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)

        elif '*' in pattern[index]:
            # Allow to match a word withou PoS_tag
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                if types[index + 1] == 'pos_tag':
                    for child in node.children:
                        pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
                else:
                    for child in node.children:
                        label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)

    def label_rec(results, current_matching_nodes, node, pattern, types, index):
        if '*' in pattern[index] or node.label in pattern[index]:
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                if types[index+1] == 'label':
                    for child in node.children:
                        label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
                else:
                    for child in node.children:
                        pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)

    def children_rec(results, node):
        if types[0] == 'label':
            label_rec(results, [], node, pattern, types, 0)
        else:
            pos_tag_rec(results, [], node, pattern, types, 0)

        for child in node.children:
            children_rec(results, child)

        return results

    matching_nodes = []
    for sentence in sentences:
        dep_tree = sentence.dep_tree

        matching_nodes += children_rec([], dep_tree.root)
    return matching_nodes


def opposite_recognition(patterns):
    for pattern in patterns:
        node_synset = pattern[0].word.synset
        child_synset = pattern[1].word.synset
        if node_synset is not None and child_synset is not None:
            if (node_synset.pos_score > node_synset.neg_score
                    and child_synset.neg_score > child_synset.pos_score
                    or node_synset.pos_score < node_synset.neg_score
                    and child_synset.neg_score < child_synset.pos_score):
                print(pattern[0].word.word + ' ' + pattern[1].word.word)
                print(str(node_synset.pos_score) + "    " + str(child_synset.pos_score))
                print(str(node_synset.neg_score) + "    " + str(child_synset.neg_score))


def verb_context_table(sentences, context_length=2):
    """
    Return a string table with the following fields :

        - Verb : a word with a verb PoS_tag
        - Context : the context of the words. *context_length* defines the number of words to display before and after
          the verb.
        - synset : name of the synset associated to the verb
        - polarity + : positive polarity
        - polarity - : negative polarity
        - polarity = : objective polarity

    :param sentences: Sentences to process
    :type sentences: :obj:`list` of |Sentence|
    :param context_length: Number of words to display before and after the verb.
    :type context_length: int
    :return: Table as a :obj:`str`
    :rtype: string

    :Example:
        Load files from uci and corrected folders (after they have been added to database) and print their verb context
        tables.

        >>> import loacore.load.file_load as file_load
        >>> import loacore.analysis.pattern_recognition as pattern_recognition
        >>> ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+', r'.*/corrected/.+'])
        >>> files = file_load.load_database(id_files=ids, load_deptrees=False)
        >>> for file in files:
        ...     print(pattern_recognition.verb_context_table(file.sentence_list()))
        ...
    """
    from prettytable import PrettyTable
    table = PrettyTable(["Verb", "context", "synset", "Polarity +", "Polarity -", "Polarity ="])
    for sentence in sentences:
        for word in sentence.words:
            if word.PoS_tag is not None and word.PoS_tag[0] == 'V':
                str_list = []
                i = word.sentence_index
                while i > 0 and word.sentence_index - i <= context_length:
                    str_list.insert(0, sentence.words[i].word)
                    i -= 1
                if i > 0:
                    str_list.insert(0, "...")

                i = word.sentence_index + 1
                while i < len(sentence.words) and i - word.sentence_index <= context_length:
                    str_list.append(sentence.words[i].word)
                    i += 1
                if i < len(sentence.words):
                    str_list.append("...")

                if word.synset is not None:
                    table.add_row([word.lemma, ' '.join(str_list), word.synset.synset_name,
                                   str(word.synset.pos_score), str(word.synset.neg_score), str(word.synset.obj_score)])
    return table.get_string()


def adj_pattern_table(sentences, polarity_commuter_only=True, lang='en'):
    """
    Return a string table with the following fiels :

        - Noun : word with a Noun PoS_tag, with an associated adjective
        - N_Polarity + : noun positive polarity
        - N_Polatity - : noun negative polarity
        - Adj : word with an Adjective PoS_tag, associated to the Noun according to the sentence dependency tree
        - A_Polarity + : adjective positive polarity
        - A_Polarity - : adjective negative polarity

    Only the words associated to a synset are considered.

    :param sentences: Sentences to process
    :type sentences: :obj:`list` of |Sentence|
    :param polarity_commuter_only:
        If True, only the patterns that are subject to a polarity commutation are displayed, i.e. those constituted by a
        positive noun associated to a negative adjective.
    :type polarity_commuter_only: boolean
    :param lang:
        Language used. (PoS_tags and dependency labels to match are chosen accordingly) Possible values : 'en', 'es'
    :type lang: string
    :return: Table as a :obj:`str`
    :rtype: string

    :Example:
        Load Spanish files from corrected folder (previously added to database) and print their adj pattern table, with
        polarity commutation only.

        >>> import loacore.load.file_load as file_load
        >>> import loacore.analysis.pattern_recognition as pattern_recognition
        >>> ids = file_load.get_id_files_by_file_paths([r'.*/corrected/.+'])
        >>> files = file_load.load_database(id_files=ids)
        >>> for file in files:
        ...     print(pattern_recognition.adj_pattern_table(file.sentence_list(), lang='es'))
        ...

    """
    from prettytable import PrettyTable
    table = PrettyTable(
        ["Noun", "N_Polarity +", "N_Polarity -", "Adj", "A_Polarity +", "A_Polarity -"])
    if lang == 'en':
        patterns = pos_tag_patterns_recognition(sentences, [['N'], ['JJ']])
    elif lang == 'es':
        patterns = pos_tag_patterns_recognition(sentences, [['N'], ['A']])

    for pattern in patterns:
        if polarity_commuter_only:
            if pattern[0].word.synset is not None and pattern[1].word.synset is not None:
                if (pattern[0].word.synset.pos_score > pattern[0].word.synset.neg_score
                        and pattern[1].word.synset.pos_score < pattern[1].word.synset.neg_score):
                    table.add_row([pattern[0].word.word,
                                   pattern[0].word.synset.pos_score,
                                   pattern[0].word.synset.neg_score,
                                   pattern[1].word.word,
                                   pattern[1].word.synset.pos_score,
                                   pattern[1].word.synset.neg_score])
        else:
            if pattern[0].word.synset is not None and pattern[1].word.synset is not None:
                table.add_row([pattern[0].word.word,
                               pattern[0].word.synset.pos_score,
                               pattern[0].word.synset.neg_score,
                               pattern[1].word.word,
                               pattern[1].word.synset.pos_score,
                               pattern[1].word.synset.neg_score])

    return table.get_string()
