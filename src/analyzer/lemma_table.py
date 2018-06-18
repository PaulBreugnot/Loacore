import os


def main():
    get_lemmas("_ENCUESTA_ENERO_2018_.txt")


def get_lemmas(file_name):
    for dirpath, dirnames, filenames in os.walk('../../data/lemmatized/'):
        for filename in filenames:
            if filename == file_name:
                print(dirpath)

if __name__ == "__main__":
    main()