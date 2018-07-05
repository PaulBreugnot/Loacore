import os
import src.database.db_file_api as file_api
import src.database.db_sentence_api as sentence_api
import src.database.db_lemma_api as lemma_api


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
                    print("        " + word.word + " ")


def test_lemmas():
    sentences = sentence_api.load_sentences()
    lemma_api.add_lemmas_to_sentences(sentences)


test_lemmas()
#test_load_db()