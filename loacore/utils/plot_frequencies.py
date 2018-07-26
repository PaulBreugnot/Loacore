from loacore import RESULT_PATH
import os


def frequencies_bar_chart(files_frequencies, plot=False, save=True,
                          gui=False,
                          file_path=os.path.join(RESULT_PATH, 'frequencies'),
                          file_name='frequencies_bar_chart.pdf',
                          val_number=0):
    """
    This function allows to plot or save results of :mod:`loacore.analysis.frequencies`.\n
    If plot is set to True, results will be presented in a matplotlib figure, but *save* will be set to False.
    (matplotlib restriction)\n
    Notice that all the results are arbitrarily re-ordered in the order of the first file of files_frequencies. This
    means for example that the right-most label of the graph corresponds to the most common of the first file, but that
    is not necessarily true for the others. This could also be useful to consider when *val_number* is used to show only
    "interesting" labels. Those labels actually correspond to the *val_number* most common labels of the first file.

    :param files_frequencies: Dictionary that maps file names to frequencies.
    :type files_frequencies: :obj:`dict` of :obj:`string` : :obj:`dict` of label : :obj:`float` .
    :param plot: If True, plot results as a figure.
    :type plot: boolean
    :param save: If not *plot*, save figure as a PDF.
    :type save: boolean
    :param gui: Specify if a GUI should be used to set directory.
    :type gui: boolean
    :param file_path:
        Path of the directory used.\n
        Default : 'RESULT_PATH/frequencies/'
    :type file_path: :obj:`path-like object`
    :param file_name: File name
    :type file_name: string
    :param val_number: Number of labels to show. Only the most commons in the first file will be kept.

    :Example:

        Save the 60 most commons bigram labels frequencies of uci files in a PDF.

        .. code-block:: Python

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

    """
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import cm

    if plot:
        save = False

    if val_number > 0:
        labels, files_frequencies = _truncate(files_frequencies, val_number)

    labels, files_frequencies = _resort(files_frequencies)
    n_labels = len(labels)

    fig, ax = plt.subplots()

    index = np.arange(n_labels)
    margin = 0.1
    bar_width = (1. - 2. * margin) / len(files_frequencies)

    color = iter(cm.rainbow(np.linspace(0, 1, len(files_frequencies))))

    for num, vals in enumerate(files_frequencies.keys()):
        print(files_frequencies[vals])
        ax.bar(index + margin + num * bar_width, files_frequencies[vals].values(), bar_width, color=next(color),
               label=vals)

    ax.set_xlabel('Label')
    ax.set_ylabel('Frequencies')
    ax.set_title('Label Frequencies')
    ax.set_xticks(index + 1 / len(files_frequencies))
    ax.set_xticklabels(labels)
    ax.legend()
    plt.xticks(rotation='vertical')

    # Plot
    if plot:
        plt.show()

    # Save PDF
    if save:
        fig.set_figwidth(n_labels)
        fig.set_figheight(15)
        from matplotlib.backends.backend_pdf import PdfPages
        if gui:
            from tkinter import filedialog
            from tkinter import Tk

            root = Tk()
            root.withdraw()
            root.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                         filetypes=[("PDF", "*.pdf")])
            pp = PdfPages(root.filename)
        else:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            pp = PdfPages(os.path.join(file_path, file_name))
        pp.savefig()
        pp.close()


def _resort(files_frequencies):
    # Re-order all the frequencies in the same order as the first frequencies of files_frequencies
    from collections import OrderedDict
    reference_freq = files_frequencies[list(files_frequencies.keys())[0]]  # Arbitrary
    new_frequencies = {}
    for k_freq in files_frequencies.keys():
        new_freq = OrderedDict()
        for k_ref in reference_freq:
            new_freq[k_ref] = files_frequencies[k_freq][k_ref]
        new_frequencies[k_freq] = new_freq

    return list(reference_freq.keys()), new_frequencies


def _truncate(files_frequencies, val_number):
    reference_freq = files_frequencies[list(files_frequencies.keys())[0]]  # Arbitrary
    labels_kept = list(reference_freq.keys())[-val_number:len(reference_freq)]

    truncated_frequencies = {}
    for freq_k in files_frequencies.keys():
        truncated_freq = {}
        for k in files_frequencies[freq_k].keys():
            if k in labels_kept:
                truncated_freq[k] = files_frequencies[freq_k][k]
        truncated_frequencies[freq_k] = truncated_freq

    return labels_kept, truncated_frequencies
