import os
import src.database.file.write_tokens as write_tokens
import src.database.file.write_lemmas as write_lemmas
import src.database.file.write_synsets as write_synsets
import src.database.file.write_reviews as write_reviews
import src.database.file.write_dep_trees as write_dep_trees

os.chdir('..')
#write_tokens.write()
#write_lemmas.write()
#write_synsets.write()
write_reviews.write()
#write_dep_trees.write()
