import loacore.load.file_load as file_load
files = file_load.load_database()

# import loacore.analysis.sentiment_analysis as sentiment_analysis
# sentiment_analysis.compute_pattern_files_polarity(files)


import loacore.analysis.pattern_recognition as pattern_recognition
for file in files:
    for review in file.reviews:
        for sentence in review.sentences:
            patterns = pattern_recognition.pos_tag_patterns_recognition([sentence], [['*'], ['A']])
            dt = sentence.dep_tree
            for pattern in patterns:
                sentence.print_sentence()
                dt.print_dep_tree(root=pattern[0])
                print('')

