import os

import loacore.preprocess.uci_preprocess as uci
import loacore


def preprocess():
    uci.uci_preprocess(os.path.abspath(
        "/home/paulbreugnot/Documents/NLP/sentiment labelled sentences/sentiment labelled sentences"),
        os.path.abspath(os.path.join(loacore.DATA_PATH, "raw", "uci")),
        ignore=["readme.txt", ".DS_Store"])


def process():
    import loacore.process.file_process as file_process
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(os.path.join(loacore.DATA_PATH, "raw", "uci"))):
            for name in filenames:
                if name == "yelp_labelled.txt":
                    file_paths.append(os.path.join(dirpath, name))

    file_process.add_files(file_paths, encoding="utf8", lang="en")


def load_uci():
    import loacore.load.file_load as file_load
    return file_load.load_database(id_files=[2])


def show_dep_trees(files):
    for file in files:
        for review in file.reviews:
            for sentence in review.sentences:
                print(len(sentence.dep_tree.root.children))
                sentence.dep_tree.print_dep_tree()


def pattern_test():
    import loacore.load.file_load as file_load
    files = file_load.load_database(id_files=[1, 2, 3])

    import loacore.analysis.sentiment_analysis as sentiment_analysis
    sentiment_analysis.compute_pattern_files_polarity(files)


def show_adj_patterns(files):
    import loacore.analysis.pattern_recognition as pattern_recognition
    for file in files:
        for review in file.reviews:
            for sentence in review.sentences:
                patterns = pattern_recognition.pos_tag_patterns_recognition([sentence], [['*'], ['JJ']])
                dt = sentence.dep_tree
                for pattern in patterns:
                    sentence.print_sentence()
                    dt.print_dep_tree(root=pattern[0])
                    print('')


def show_verb_patterns(files):
    import loacore.analysis.pattern_recognition as pattern_recognition
    for file in files:
        for review in file.reviews:
            for sentence in review.sentences:
                patterns = pattern_recognition.pos_tag_patterns_recognition([sentence], [['V', 'MD'], ['*']])
                dt = sentence.dep_tree
                for pattern in patterns:
                    sentence.print_sentence()
                    dt.print_dep_tree(root=pattern[0])
                    print('')


def test_verb_table():
    import loacore.load.sentence_load as sentence_load
    sentences = sentence_load.load_sentences(load_words=True)

    import loacore.analysis.pattern_recognition as pattern_recognition
    pattern_recognition.verb_context_table(sentences)


process()
# show_dep_trees(load_uci())
# pattern_test()
# show_adj_patterns(load_uci())
# show_verb_patterns(load_uci())
# test_verb_table()
