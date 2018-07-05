import os
import src.database.db_file_api as file_api


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

test_load_db()