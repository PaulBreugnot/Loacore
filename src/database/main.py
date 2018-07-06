import os
import src.database.db_file_api as file_api
import src.database.db_sentence_api as sentence_api
import src.database.db_lemma_api as lemma_api
import src.database.db_synset_api as synset_api
import src.database.db_deptree_api as deptree_api
import src.database.db_word_api as word_api


def add_files_to_database():
    file_paths = []
    for dirpath, dirnames, filenames in os.walk('../../data/raw/'):
        for name in filenames:
            file_paths.append(os.path.join(dirpath, name))

    file_api.add_files(file_paths)


def test_load_db():
    files = file_api.load_database()

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
    sentences = sentence_api.load_sentences()
    '''
    deptree_api.add_dep_tree_from_sentences([sentences[172]], print_result=False)
    deptree_api.load_dep_tree_in_sentences(sentences)
    word_api.load_words_in_dep_trees([sentences[172].dep_tree])
    '''
    deptree_api.add_dep_tree_from_sentences(sentences, print_result=False)
    deptree_api.load_dep_tree_in_sentences(sentences)
    word_api.load_words_in_dep_trees([sentences[172].dep_tree])
    sentences[172].dep_tree.print_dep_tree()

#add_files_to_database()
#test_lemmas()
#test_synsets()
#test_load_db()
test_dep_tree()