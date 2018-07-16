import re
import os


def write():
    import loacore.load.file_load as file_load
    import loacore.utils.file_writer as file_writer

    files = file_load.load_database(load_deptrees=False)

    for file in files:
        directory = re.findall(r'../../data/raw/(.+)', file.file_path)
        filename = re.findall(r'.+/(.+\.txt)', file.file_path)
        text = ''
        for review in file.reviews:
            text += (str(review.file_index) + '\t')
            text += review.review
            text += "\n"
        file_writer.write(text, os.path.join('../../data/normalized/', directory[0]), filename[0])