
def test_count():
    import loacore.load.file_load as file_load
    import loacore.analysis.vocabularies as voc
    from prettytable import PrettyTable

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+', r'.*/corrected/.+'])
    files = file_load.load_database(id_files=ids, load_deptrees=False)

    word_count = {}
    for file in files:
        word_count[file.id_file] = voc.word_count(file)

    lemma_count = {}
    for file in files:
        lemma_count[file.id_file] = voc.lemma_count(file)

    synset_count = {}
    for file in files:
        synset_count[file.id_file] = voc.synset_count(file)

    print("Sizes of vocabularies")
    table = PrettyTable(['File', 'Word Count', 'Lemma Count', 'Synset Count'])
    for file in files:
        table.add_row([file.get_filename(),
                       word_count[file.id_file],
                       lemma_count[file.id_file],
                       synset_count[file.id_file]])

    print(table)


test_count()