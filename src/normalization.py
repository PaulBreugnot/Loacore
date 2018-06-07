from os import walk
from os import path
import re


def main():
    for dirpath, dirnames, filenames in walk('../data/raw/'):
        for name in filenames:
            raw_text = open(path.join(dirpath, name))
            normalized_string = raw_text.read().lower()
            alphanumeric_chars = re.findall(r'[\w\s]', normalized_string)
            dirname = re.findall(r'^\.\./data/raw/(.*)', dirpath)
            normalized_text = open(path.join('../data/normalized/', dirname[0], name), 'w')
            for char in alphanumeric_chars :
                normalized_text.write(char)


if __name__ == "__main__":
    main()

