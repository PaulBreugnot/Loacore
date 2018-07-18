import os
import re


def uci_preprocess(source, destination, ignore=[]):
    from loacore.utils import file_writer

    for dirpath, dirnames, filenames in os.walk(source):
        for name in filenames:
            if not name in ignore:
                print(name)
                uci_file = open(os.path.join(dirpath, name), encoding="utf8")
                file_str = uci_file.read()
                sentences = re.findall(r'(.+)\t\d', file_str, re.MULTILINE)
                sentences = '\n'.join(sentences)
                file_writer.write(sentences, destination, name)
