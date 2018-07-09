

def compute_files_polarity(files):

    for file in files:
        file_pos_score = 0
        file_neg_score = 0
        file_obk_score = 0
        for review in file.reviews:
            for sentence in review.sentences:
                for word in sentence.words:
                    file_pos_score += word.synset.pos_score
                    