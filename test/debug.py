from loacore.load import file_load
from loacore.analysis.sentiment_analysis import compute_simple_reviews_polarity

files = file_load.load_database(load_in_temp_file=False)

compute_simple_reviews_polarity(files[0].reviews, commit_polarities=True)
for r in files[0].reviews:
    print(r.review)
