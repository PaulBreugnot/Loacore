import os
import re
import src.utils.file_writer as file_writer


def main():
    for dirpath, dirnames, filenames in os.walk('../../data/raw/'):
        for name in filenames:
            raw_text = open(os.path.join(dirpath, name), encoding='windows-1252')

            normalized_string = '\n'.join(normalize(raw_text.read()))
            write_normalized_text(normalized_string, dirpath, name)


def write_normalized_text(normalized_string, dirpath, filename):
    subname = re.findall(r'^\.\./\.\./data/raw/(.*)', dirpath)
    directory = os.path.join('../../data/normalized/', subname[0])
    file_writer.write(normalized_string, directory, filename)


def normalize(text):
    normalized_string = text.lower()
    reviews = re.findall(r'.+', normalized_string, re.MULTILINE)
    return reviews


if __name__ == "__main__":
    main()

