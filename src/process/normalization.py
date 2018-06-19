import os
import re


def main():
    for dirpath, dirnames, filenames in os.walk('../../data/raw/'):
        for name in filenames:
            raw_text = open(os.path.join(dirpath, name), encoding='windows-1252')

            normalized_string = raw_text.read().lower()
            alphanumeric_chars = re.findall(r'[\w\s]', normalized_string)
            subname = re.findall(r'^\.\./\.\./data/raw/(.*)', dirpath)
            directory = os.path.join('../../data/normalized/', subname[0])
            if not os.path.exists(directory):
                os.makedirs(directory)

            normalized_text = open(os.path.join(directory, name), 'w', encoding='utf-8')
            for char in alphanumeric_chars:
                normalized_text.write(char)


if __name__ == "__main__":
    main()

