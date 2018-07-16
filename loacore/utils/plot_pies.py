import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plot_polarity_pie_charts(file_score_dict, show=True):
    pies_data = [t for t in file_score_dict.values()]
    print(pies_data)

    import loacore.load.file_load as file_load
    files = file_load.load_database(id_files=file_score_dict.keys(), load_reviews=False, load_sentences=False,
                                    load_words=False, load_deptrees=False)
    pies_titles = [re.findall(r'.+/(.+\.txt)', f.file_path)[0] for f in files]
    print(pies_titles)

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
    plt.suptitle("Polarity computation results")

    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('multipage.pdf')
    pp.savefig()
    pp.close()
    #if show:
    #    plt.show()
