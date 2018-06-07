from os import walk
from os import path
import re


def main():
    for dirpath, dirnames, filenames in walk('../data/raw/'):
        for name in filenames:
            raw_text = open(path.join(dirpath, name))
            normalized_string = raw_text.read().lower()
            dirname = re.findall(r'^\.\./data/raw/(.*)', dirpath)
            normalized_text = open(path.join('../data/normalized/', dirname[0], name), 'w')
            normalized_text.write(normalized_string)


if __name__ == "__main__":
    main()

