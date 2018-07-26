
def test_label_frequencies():
    import loacore.load.file_load as file_load
    import loacore.analysis.frequencies as frequencies

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_reviews=False)
    labels, frequencies = frequencies.label_frequencies(files)
    frequencies.plot_frequencies(labels, frequencies)


def test_label_bigram_frequencies():
    import loacore.load.file_load as file_load
    import loacore.analysis.frequencies as frequencies
    import loacore.utils.plot_frequencies as plot_frequencies
    import os
    from loacore import RESULT_PATH

    ids = file_load.get_id_files_by_file_paths([r'.*/uci/.+'])
    files = file_load.load_database(id_files=ids, load_reviews=False)
    labels, freq = frequencies.bigram_label_frequencies(files)

    plot_frequencies.frequencies_bar_chart(
        freq,
        plot=False,
        save=True,
        file_path=os.path.join(RESULT_PATH, 'frequencies', 'label_frequencies', 'uci'),
        file_name="uci_label_bigrams_frequencies.pdf",
        val_number=60)


test_label_bigram_frequencies()