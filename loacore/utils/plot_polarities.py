import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from loacore.conf import RESULT_PATH


def save_polarity_pie_charts(file_score_dict, gui=False,
                             file_path=os.path.join(RESULT_PATH, 'sentiment_analysis'),
                             file_name='polarity_pie_charts.pdf'):
    """
    Plot polarity pie charts using Matplotlib, and save them into a .pdf file.

    :param file_score_dict:
        Data to plot and save. The :obj:`dict` maps ID_Files to a polarity tuple (pos_score, neg_score, obj_score).
    :type file_score_dict: :obj:`dict` of :obj:`int` : :obj:`tuple`
    :param gui: Specify if a gui should be used to save file.
    :type gui: boolean
    :param file_path:
        If gui is not called : path of the directory in which plots will be saved.
        If directory doesn't exist, will be created.
        Default is set to *RESULT_PATH/sentiment_analysis/*
    :type file_path: |path-like-object|
    :param file_name: Name of the saved file.
    :type file_name: string
    """
    pies_data = [t for t in file_score_dict.values()]

    import loacore.load.file_load as file_load
    files = file_load.load_database(id_files=file_score_dict.keys(), load_reviews=False, load_sentences=False,
                                    load_words=False, load_deptrees=False)
    pies_titles = [re.findall(r'.+/(.+\.txt)', f.file_name)[0] for f in files]

    index = 0
    colors = ['green', 'red', 'skyblue']
    num_row = 1 + int(len(pies_titles) / 4)
    if num_row <= 1:
        num_column = len(pies_titles)
    else:
        num_column = 4
    fig, axes = plt.subplots(num_row, num_column, constrained_layout=False)
    if num_column <= 1:
        axes.axis("off")
    else:
        for x in axes.flatten():
            x.axis("off")
    fig.set_figheight(5 * num_row)
    fig.set_figwidth(5 * num_column)
    while index < len(pies_titles):
        axe = fig.add_subplot(num_row, num_column, index + 1)
        axe.pie(pies_data[index], colors=colors, autopct='%1.1f%%')
        axe.set_title(pies_titles[index], size='x-small')
        index += 1
    pos_patch = mpatches.Patch(color='green', label='Positive')
    neg_patch = mpatches.Patch(color='red', label='Negative')
    obj_patch = mpatches.Patch(color='skyblue', label='Objective')
    plt.figlegend(handles=[pos_patch, neg_patch, obj_patch])
    plt.suptitle("Polarity computation results", size='xx-large')

    # Save PDF
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


def print_polarity_table(file_score_dict):
    """

    Print a table with columns File path, Positive Score, Negative Score and Objective Score.\n
    Notice that displayed scores are rounded values.

    :param file_score_dict: A :obj:`dict` that maps file_paths to a score tuple.
    :type file_score_dict: :obj:`dict` of :obj:`int` : :obj:`tuple`
    """

    import re
    from prettytable import PrettyTable
    import loacore.load.file_load as file_load
    files = file_load.load_database(id_files=file_score_dict.keys(), load_reviews=False, load_sentences=False,
                                    load_words=False, load_deptrees=False)
    file_names = dict([(f.id_file, re.findall(r'.+/(.+\.txt)', f.file_name)[0]) for f in files])
    table = PrettyTable(['File', 'Pos_Score', 'Neg_Score', 'Obj_Score'])
    for id_file in file_score_dict.keys():
        table.add_row([file_names[id_file], "%.3f" % file_score_dict[id_file][0], "%.3f" % file_score_dict[id_file][1],
                       "%.3f" % file_score_dict[id_file][2]])
    print(table)
