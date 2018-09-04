from loacore.load import file_load
from loacore.analysis.sentiment_analysis import compute_simple_files_polarity

files = file_load.load_database(id_files=(1,), load_in_temp_file=True, workers=4, load_deptrees=False)

for file in files:
    print(str(file.id_file) + " : " + str(len(file.reviews)))

polarities = compute_simple_files_polarity(files, commit_polarities=True)
