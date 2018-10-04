from loacore.process.file_process import add_files
from loacore.conf import DATA_PATH
import os

print(DATA_PATH)
print(os.path.join(DATA_PATH, "raw/imdb/test/test_imdb_labelled_neg.txt"))
add_files([os.path.join(DATA_PATH, "raw/imdb/test/test_imdb_labelled_neg.txt")], workers=2)

