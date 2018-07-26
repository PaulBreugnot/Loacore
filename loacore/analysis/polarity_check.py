

def check_polarity(files,
                   analysis_to_check=[
                       "simple", "optimistic", "pessimistic", "pattern_adj_cc", "pattern_adj", "pattern_cc"],
                   ref="label"):
    from prettytable import PrettyTable

    for analysis in analysis_to_check:
        print(analysis)
        table = PrettyTable(["File", "Correct", "False Positive", "False Negative"])
        for file in files:
            correct = 0
            false_positive = 0
            false_negative = 0
            for review in file.reviews:
                if (review.polarities[ref].is_positive() and review.polarities[analysis].is_positive()
                   or not review.polarities[ref].is_positive() and not review.polarities[analysis].is_positive()):
                    correct += 1

                elif not review.polarities[ref].is_positive() and review.polarities[analysis].is_positive():
                    false_positive += 1

                elif review.polarities[ref].is_positive() and not review.polarities[analysis].is_positive():
                    false_negative += 1

            total = correct + false_positive + false_negative
            table.add_row([file.get_filename(),
                           "%.2f" % (correct/total), "%.2f" % (false_positive/total), "%.2f" % (false_negative/total)])

        print(table)
