from prettytable import PrettyTable


def compute_files_polarity(files):
    """

    Perform the easiest sentiment analysis possible : a normalized sum of the positive/negative/objective polarities
    available in all synsets of each file.\n
    Return a dictionnary that map file_paths to a polarity tuple. A polarity tuple is a tuple of length 3, with this
    form : (positive_score, negative_score, objective_score)

    :param files: Files to process
    :type files: :obj:`list` of :class:`File`
    :return: IdFile/Scores dictionnary
    :rtype: :obj:`dict` of :obj:`int` : :obj:`tuple`
    :Example:
    Load all files and compute basic polarities

    >>> import loacore.load.file_load as file_load
    >>> import loacore.analysis.sentiment_analysis as sentiment_analysis
    >>> file_load.load_database(load_deptrees=False)
    >>> polarities = sentiment_analysis.compute_files_polarity(files)
    >>> sentiment_analysis.print_polarity_table(polarities)
    +---------------------------------------------------------------------------------------------------+-----------+...
    |                                                File                                               | Pos_Score |...
    +---------------------------------------------------------------------------------------------------+-----------+...
    |           ../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_EO.txt          |   0.000   |...
    |           ../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_CC.txt          |   0.069   |...
    |           ../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_GR.txt          |   0.000   |...
    |           ../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_JA.txt          |   0.060   |...
    |           ../../data/raw/TempBaja/Balneario2/EncuestaTemporadaBajafinalbalneario2_CD.txt          |   0.080   |...
    |           ../../data/raw/TempBaja/Balneario3/EncuestaTemporadaBajafinalbalneario3_JA.txt          |   0.055   |...
    |           ../../data/raw/TempBaja/Balneario3/EncuestaTemporadaBajafinalbalneario3_CD.txt          |   0.019   |...
    ...

    """

    file_score_dict = {}
    for file in files:
        file_pos_score = 0
        file_neg_score = 0
        file_obj_score = 0
        for review in file.reviews:
            for sentence in review.sentences:
                for word in sentence.words:
                    if word.synset is not None:
                        file_pos_score += word.synset.pos_score
                        file_neg_score += word.synset.neg_score
                        file_obj_score += word.synset.obj_score
        total = file_pos_score + file_neg_score + file_obj_score
        if total > 0:
            file_score_dict[file.id_file] = \
                (file.file_path, file_pos_score / total, file_neg_score / total, file_obj_score / total)

    return file_score_dict


def print_polarity_table(file_score_dict):
    """

    Print a table with columns File path, Positive Score, Negative Score and Objective Score.

    :param file_score_dict: A :obj:`dict` that maps file_paths to a score tuple.
    :type file_score_dict: :obj:`dict` of :obj:`int` : :obj:`tuple`
    """

    table = PrettyTable(['File', 'Pos_Score', 'Neg_Score', 'Obj_Score'])
    for file in file_score_dict.keys():
        table.add_row([file_score_dict[file][0], "%.3f" % file_score_dict[file][1], "%.3f" % file_score_dict[file][2],
                       "%.3f" % file_score_dict[file][3]])
    print(table)
