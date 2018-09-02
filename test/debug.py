from loacore.load import file_load
from loacore.analysis.sentiment_analysis import compute_simple_files_polarity

files = file_load.load_database(load_in_temp_file=True, workers=4, load_deptrees=False)

polarities = compute_simple_files_polarity(files, commit_polarities=True)
