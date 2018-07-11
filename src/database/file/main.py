import os
import src.database.file.write_tokens as write_tokens
import src.database.file.write_lemmas as write_lemmas
import src.database.file.write_synsets as write_synsets

os.chdir('..')
write_tokens.write()
write_lemmas.write()
write_synsets.write()
