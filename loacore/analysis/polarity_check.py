from loacore.conf import RESULT_PATH
import os


def check_polarity(files,
                   analysis_to_check=(
                       "simple", "optimistic", "pessimistic", "pattern_adj_cc", "pattern_adj", "pattern_cc"),
                   ref="label"):
    """
    Prints tables with the rates, in percentages, of correct, false positive and false negative classifications of
    reviews by file for each analysis in *analysis_to_check*, compared with *ref* analysis.

    :param files: Files to process.
    :type files: :obj:`list` of |File|
    :param analysis_to_check: Analysis to check
    :type analysis_to_check: :obj:`sequence` of :obj:`str`
    :param ref: Reference analysis, with which analysis to check are compared.
    :type ref: string
    """
    from prettytable import PrettyTable

    for analysis in analysis_to_check:
        print(analysis)
        table = PrettyTable(["File", "Correct", "False Positive", "False Negative", "False Objective"])
        for file in files:
            correct = 0
            false_positive = 0
            false_negative = 0
            false_objective = 0
            for review in file.reviews:
                if is_correct(review, ref, analysis):
                    correct += 1

                elif is_false_positive(review, ref, analysis):
                    false_positive += 1

                elif is_false_negative(review, ref, analysis):
                    false_negative += 1

                elif is_false_objective(review, ref, analysis):
                    false_objective += 1

            total = correct + false_positive + false_negative + false_objective
            if total > 0:
                table.add_row([file.get_filename(),
                               "%.2f" % (correct / total),
                               "%.2f" % (false_positive / total),
                               "%.2f" % (false_negative / total),
                               "%.2f" % (false_objective / total)])
            else:
                table.add_row([file.get_filename(),
                               str(None),
                               str(None),
                               str(None),
                               str(None)])

        print(table)


def write_polarity_check(files,
                         analysis_to_check=(
                             "simple", "optimistic", "pessimistic", "pattern_adj_cc", "pattern_adj", "pattern_cc"),
                         ref="label",
                         select="all",
                         terminal_print=True,
                         colored_polarity=True,
                         directory_path=os.path.join(RESULT_PATH, 'sentiment_analysis', 'check')):
    """
    Write polarity in .txt files. If *select* is set to all, each review is written with polarities corresponding to
    *ref* and *analysis_to_check*. If *select* is set to *false_positive* or *false_negative*, only the review with a
    false positive or false negative for at least one analysis of *analysis_to_check* are written, with the
    corresponding(s) polarities.

    :param files: Files to process.
    :type files: :obj:`list` of |File|
    :param analysis_to_check: Analysis to compare with *ref*
    :type analysis_to_check: :obj:`sequence` of :obj:`str`
    :param ref: Reference analysis
    :type ref: string
    :param select: Select option
    :type select: :obj:`list` of :obj:`str` : {'all', 'false_positive', 'false_negative'}
    :param terminal_print: If True, print results in the terminal.
    :type terminal_print: boolean
    :param colored_polarity:
        If True, write words with colored polarity. Notice that colors are not display in most of the .txt editors.
        For example, in Linux, use

            .. code-block:: console

                cat file_name.txt

        To show the colored file in terminal.
    :param directory_path:
        Path of the directory in which to write files.
        Default value computed using os.path.join(RESULT_PATH, 'sentiment_analysis', 'check')
    :type directory_path: |path-like-object|
    """
    import loacore.utils.file_writer as file_writer
    for file in files:
        if select == "all":
            check_str =\
                '\n'.join([r.review_str(colored_polarity=colored_polarity, analysis=ref+analysis_to_check)
                           for r in file.reviews])
        else:
            false_str = []
            for review in file.reviews:
                selected_analysis = [ref]
                for analysis in analysis_to_check:
                    if select == "false_positive" and is_false_positive(review, ref, analysis) \
                            or select == "false_negative" and is_false_negative(review, ref, analysis):
                        selected_analysis.append(analysis)

                if len(selected_analysis) > 1:
                    false_str.append(review.review_str(colored_polarity=colored_polarity, analysis=selected_analysis))
            check_str = '\n'.join(false_str)

        if terminal_print:
            print(check_str)

        if colored_polarity:
            file_writer.write(check_str, os.path.join(directory_path, "colored"),
                              "check_" + select + "_" + file.get_filename())
            print("File write : "
                  + str(os.path.join(os.path.join(directory_path, "colored"),
                                     "check_" + select + "_" + file.get_filename())))
        else:
            file_writer.write(check_str, os.path.join(directory_path, "uncolored"),
                              "check_" + select + "_" + file.get_filename())
            print("File write : "
                  + str(os.path.join(os.path.join(directory_path, "uncolored"),
                                     "check_" + select + "_" + file.get_filename())))


def is_correct(review, ref, analysis):
    ref_polarity = review.polarities.get(ref)
    tested_polarity = review.polarities.get(analysis)
    if ref_polarity is not None and tested_polarity is not None:
        if (ref_polarity.is_positive() and tested_polarity.is_positive()
                or ref_polarity.is_negative() and tested_polarity.is_negative()
                or ref_polarity.is_objective() and tested_polarity.is_objective()):
            return True
        return False
    return None


def is_false_positive(review, ref, analysis):
    ref_polarity = review.polarities.get(ref)
    tested_polarity = review.polarities.get(analysis)
    if ref_polarity is not None and tested_polarity is not None:
        if (ref_polarity.is_negative() or ref_polarity.is_objective())\
                and tested_polarity.is_positive():
            return True
        return False


def is_false_negative(review, ref, analysis):
    ref_polarity = review.polarities.get(ref)
    tested_polarity = review.polarities.get(analysis)
    if ref_polarity is not None and tested_polarity is not None:
        if (ref_polarity.is_positive() or ref_polarity.is_objective())\
                and tested_polarity.is_negative():
            return True
        return False


def is_false_objective(review, ref, analysis):
    ref_polarity = review.polarities.get(ref)
    tested_polarity = review.polarities.get(analysis)
    if ref_polarity is not None and tested_polarity is not None:
        if (ref_polarity.is_positive() or ref_polarity.is_negative())\
                and tested_polarity.is_objective():
            return True
        return False


