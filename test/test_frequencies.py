
def test_label_frequencies():
    import loacore.load.file_load as file_load
    import loacore.analysis.frequencies as frequencies
    import loacore.utils.plot_frequencies as plot_frequencies
    import os
    from loacore import RESULT_PATH

    ids = file_load.get_id_files_by_file_paths([r'.*/corrected/.+'])
    files = file_load.load_database(id_files=ids, load_reviews=False)
    labels, freq = frequencies.label_frequencies(files)
    plot_frequencies.write_frequencies(
        freq,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'simple_label_frequencies', 'table', 'corrected'))
    plot_frequencies.frequencies_bar_chart(
        freq,
        plot=False,
        save=True,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'simple_label_frequencies', 'charts', 'corrected'),
        file_name="corrected_simple_label_frequencies.pdf",
        val_number=60)


def test_label_bigram_frequencies():
    import loacore.load.file_load as file_load
    import loacore.analysis.frequencies as frequencies
    import loacore.utils.plot_frequencies as plot_frequencies
    import os
    from loacore import RESULT_PATH

    ids = file_load.get_id_files_by_file_paths([r'.*/corrected/.+'])
    files = file_load.load_database(id_files=ids, load_reviews=False)
    labels, freq = frequencies.bigram_label_frequencies(files)

    plot_frequencies.write_frequencies(
        freq,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'bigram_label_frequencies', 'table', 'corrected'))
    plot_frequencies.frequencies_bar_chart(
        freq,
        plot=False,
        save=True,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'bigram_label_frequencies', 'charts', 'corrected'),
        file_name="corrected_bigram_labels_frequencies.pdf",
        val_number=60)


def test_pos_tag_frequencies():
    import loacore.load.file_load as file_load
    import loacore.analysis.frequencies as frequencies
    import loacore.utils.plot_frequencies as plot_frequencies
    import os
    from loacore import RESULT_PATH

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_reviews=False)
    labels, freq = frequencies.pos_tag_frequencies(files)
    plot_frequencies.write_frequencies(
        freq,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'simple_pos_tag_frequencies', 'table', 'corrected'))
    plot_frequencies.frequencies_bar_chart(
        freq,
        plot=False,
        save=True,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'simple_pos_tag_frequencies', 'charts', 'corrected'),
        file_name="corrected_simple_pos_tag_frequencies.pdf",
        val_number=60)


def test_pos_tag_bigram_frequencies():
    import loacore.load.file_load as file_load
    import loacore.analysis.frequencies as frequencies
    import loacore.utils.plot_frequencies as plot_frequencies
    import os
    from loacore import RESULT_PATH

    ids = file_load.get_id_files_by_file_paths([r'.*/corrected/.+'])
    files = file_load.load_database(id_files=ids, load_reviews=False)
    labels, freq = frequencies.bigram_pos_tag_frequencies(files)

    plot_frequencies.write_frequencies(
        freq,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'bigram_pos_tag_frequencies', 'table', 'corrected'))
    plot_frequencies.frequencies_bar_chart(
        freq,
        plot=False,
        save=True,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'bigram_pos_tag_frequencies', 'charts', 'corrected'),
        file_name="corrected_bigram_pos_tags_frequencies.pdf",
        val_number=60)


test_label_frequencies()
test_label_bigram_frequencies()
test_pos_tag_frequencies()
test_pos_tag_bigram_frequencies()
