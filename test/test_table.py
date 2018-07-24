

def verb_patterns_tables():
    import os
    from loacore import RESULT_PATH
    import loacore.utils.file_writer as file_writer
    import loacore.load.file_load as file_load
    import loacore.analysis.pattern_recognition as pattern_recognition

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+', r'.*/corrected/.+'])
    files = file_load.load_database(id_files=ids, load_deptrees=False)
    for file in files:
        table = pattern_recognition.verb_context_table(file.sentence_list())
        directory = os.path.join(RESULT_PATH, 'context_tables', 'verbs', file.get_directory_name())
        file_writer.write(table, directory, file.get_filename())


def adj_patterns_table():
    import os
    from loacore import RESULT_PATH
    import loacore.utils.file_writer as file_writer
    import loacore.load.file_load as file_load
    import loacore.analysis.pattern_recognition as pattern_recognition

    # English files
    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids)
    for file in files:
        table = pattern_recognition.adj_pattern_table(file.sentence_list())
        directory = os.path.join(RESULT_PATH, 'context_tables', 'adj', file.get_directory_name())
        file_writer.write(table, directory, file.get_filename())

    # Spanish files
    ids = file_load.get_id_files_by_file_paths([r'.*/corrected/.+'])
    files = file_load.load_database(id_files=ids)
    for file in files:
        table = pattern_recognition.adj_pattern_table(file.sentence_list(), lang='es')
        directory = os.path.join(RESULT_PATH, 'context_tables', 'adj', file.get_directory_name())
        file_writer.write(table, directory, file.get_filename())


# adj_patterns_table()
