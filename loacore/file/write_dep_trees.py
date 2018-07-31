import os
import re


def write():
    import loacore.load.file_load as file_load
    import loacore.utils.file_writer as file_writer

    files = file_load.load_database()

    for file in files:
        directory = re.findall(r'../../data/raw/(.+)', file.file_path)
        filename = re.findall(r'.+/(.+\.txt)', file.file_path)
        text = ''
        for review in file.reviews:
            for sentence in review.sentences:
                text += "+-------------------------------------------------------------------------------------------\n"
                text += "| File Index : " + str(review.file_index) + "\n"
                text += "| Sentence : " + " ".join([w.word for w in sentence.words]) + "\n"
                text += "+-------------------------------------------------------------------------------------------\n"
                text += sentence.dep_tree.dep_tree_str(print_dep_tree=False)
                text += "\n\n"
        file_writer.write(text, os.path.join('../../data/dep_trees/', directory[0]), filename[0])