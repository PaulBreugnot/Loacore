import src.database.db_review_api as review_api
import src.database.db_sentence_api as sentence_api
import src.database.db_synset_api as synset_api

#reviews = review_api.load_reviews('../../data/raw/TempAlta/Enero_2018/_ENCUESTA_ENERO_2018_.txt')
#sentence_api.add_sentences_from_reviews(reviews)

synset_api.load_synset(1)