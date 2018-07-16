import os
import loacore.database.process.file_process as file_process
import loacore.database.load.file_load as file_load
import loacore.database.load.sentence_load as sentence_api
import loacore.database.load.lemma_load as lemma_api
import loacore.database.load.synset_load as synset_api
import loacore.database.load.deptree_load as deptree_api
import loacore.database.load.word_load as word_api


def add_files_to_database():
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(os.path.join('..', '..', 'data', 'raw')):
        for name in filenames:
            file_paths.append(os.path.join(dirpath, name))

    file_process.add_files(file_paths)


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


def test_lemmas():
    sentences = sentence_api.load_sentences()
    lemma_api.add_lemmas_to_sentences(sentences)


def test_synsets():
    sentences = sentence_api.load_sentences()
    synset_api.add_synsets_to_sentences(sentences)


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


def test_analysis():
    import loacore.database.analysis.sentiment_analysis as sentiment_analysis
    files = file_load.load_database(load_deptrees=False)
    sentiment_analysis.print_polarity_table(sentiment_analysis.compute_files_polarity(files))


def test_adj_pattern():
    import loacore.database.analysis.pattern_recognition as pattern_recognition
    #files = file_load.load_database(id_files=[31, 33])
    files = file_load.load_database()
    sentences = []
    for file in files:
        for review in file.reviews:
            sentences += review.sentences

    patterns = pattern_recognition.adj_noun_pattern_recognition(sentences)
    pattern_recognition.opposite_recognition(patterns)


def test_verb_pattern():
    import loacore.database.analysis.pattern_recognition as pattern_recognition
    files = file_load.load_database(id_files=[31, 33])
    #files = file_load.load_database()
    sentences = []
    for file in files:
        for review in file.reviews:
            sentences += review.sentences

    patterns = pattern_recognition.verb_object_recognition(sentences)


def test_label_pattern():
    import loacore.database.analysis.pattern_recognition as pattern_recognition
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
    import loacore.database.analysis.pattern_recognition as pattern_recognition
    files = file_load.load_database(id_files=[31, 33])
    # files = file_load.load_database()
    sentences = []
    for file in files:
        for review in file.reviews:
            sentences += review.sentences

    patterns = pattern_recognition.pos_tag_patterns_recognition(sentences, ['RN'])
    pattern_recognition.print_patterns(patterns)


def test_general_pattern():
    import loacore.database.analysis.pattern_recognition as pattern_recognition
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

#file_load.clean_db()
#add_files_to_database()
#test_lemmas()
#test_synsets()
#test_load_db()
test_dep_tree()
#test_analysis()
#test_verb_pattern()
#test_label_pattern()
#test_pos_tag_pattern()
#test_general_pattern()
