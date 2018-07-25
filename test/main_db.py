import os
import loacore.process.file_process as file_process
import loacore.load.file_load as file_load
import loacore.load.sentence_load as sentence_api
import loacore.load.deptree_load as deptree_api
import loacore.load.word_load as word_api


def add_files_to_database():
    from loacore import DATA_PATH
    file_paths = []

    # for dirpath, dirnames, filenames in os.walk(os.path.join(DATA_PATH, 'raw', 'TempAlta')):
    #     for name in filenames:
    #         print(name)
    #         file_paths.append(os.path.join(dirpath, name))
    #
    # for dirpath, dirnames, filenames in os.walk(os.path.join(DATA_PATH, 'raw', 'TempBaja')):
    #     for name in filenames:
    #         print(name)
    #         file_paths.append(os.path.join(dirpath, name))
    #
    # file_process.add_files(file_paths, lang='es')
    # file_paths.clear()

    for dirpath, dirnames, filenames in os.walk(os.path.abspath(os.path.join(DATA_PATH, 'raw', 'uci'))):
        for name in filenames:
            print(name)
            file_paths.append(os.path.join(dirpath, name))

    file_process.add_files(file_paths, encoding='utf8', lang='en')
    file_paths.clear()

    for dirpath, dirnames, filenames in os.walk(os.path.abspath(os.path.join(DATA_PATH, 'raw', 'corrected'))):
        for name in filenames:
            print(name)
            file_paths.append(os.path.join(dirpath, name))

    file_process.add_files(file_paths, encoding='UTF-16LE', lang='es')
    file_paths.clear()


def test_load_db():
    files = file_load.load_database()

    for file in files:
        for review in file.reviews:
            print("Review : ")
            print(str(review.id_review) + " : " + review.review)
            for sentence in review.sentences:
                print("    Sentence : ")
                for word in sentence.words:
                    print("        Word : " + word.word + " : " + word.lemma)
                    print("            Lemma : " + word.lemma)
                    if word.synset is not None:
                        print("            Synset : " + word.synset.synset_name)
                    else:
                        print("            Synset : None")


def test_dep_tree():
    selected_sentences = []
    sentences = sentence_api.load_sentences_by_id_files(id_files=[1])
    for sentence in sentences:
        # for word in sentence.words:
        #    if word.word == "no":
        selected_sentences.append(sentence)
    '''
    deptree_api.add_dep_tree_from_sentences([sentences[172]], print_result=False)
    deptree_api.load_dep_tree_in_sentences(sentences)
    word_api.load_words_in_dep_trees([sentences[172].dep_tree])
    '''
    deptree_api.load_dep_tree_in_sentences(selected_sentences)

    dep_trees = [sentence.dep_tree for sentence in selected_sentences]
    word_api.load_words_in_dep_trees(dep_trees)
    for dep_tree in dep_trees:
        dep_tree.print_dep_tree()


def test_label_pattern():
    import loacore.analysis.pattern_recognition as pattern_recognition
    files = file_load.load_database(id_files=[31, 33])
    # files = file_load.load_database()
    sentences = []
    for file in files:
        for review in file.reviews:
            sentences += review.sentences

    patterns = pattern_recognition.label_patterns_recognition(sentences, ['neg'])
    for pattern in patterns:
        for node in pattern:
            print(node.word.word + " : " + node.label)


def test_pos_tag_pattern():
    import loacore.analysis.pattern_recognition as pattern_recognition
    files = file_load.load_database(id_files=[31, 33])
    # files = file_load.load_database()
    sentences = []
    for file in files:
        for review in file.reviews:
            sentences += review.sentences

    patterns = pattern_recognition.pos_tag_patterns_recognition(sentences, ['RN'])
    pattern_recognition.print_patterns(patterns)


def test_general_pattern():
    import loacore.analysis.pattern_recognition as pattern_recognition
    files = file_load.load_database(id_files=[31, 33])
    # files = file_load.load_database()
    sentences = []
    for file in files:
        for review in file.reviews:
            sentences += review.sentences

    patterns = pattern_recognition.general_pattern_recognition(
        sentences, [['V'], ['cc', 'cd', 'ci']], ['pos_tag', 'label'])
    for pattern in patterns:
        print("( ", end='')
        for node in pattern[:-1]:
            print(node.word.word, " : ", node.word.PoS_tag, " : ", node.label, end=", ")
        print(pattern[-1].word.word, " : ", pattern[-1].word.PoS_tag, " : ", pattern[-1].label, " )")


def test_load_polarities():
    import loacore.load.file_load as file_load
    import itertools

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_sentences=False)
    reviews = itertools.chain.from_iterable([f.reviews for f in files])
    for review in reviews:
        print(review.review, " : ", review.polarities["label"].pos_score, ", ",
              review.polarities["label"].neg_score, ", ",
              review.polarities["label"].obj_score)


#file_load.clean_db()
#add_files_to_database()
#test_load_db()
#test_dep_tree()
#test_pos_tag_pattern()
#test_general_pattern()
test_load_polarities()
