import os


def write(text, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file = open(os.path.join(directory, filename), 'w', encoding='utf-8')
    file.write(text)