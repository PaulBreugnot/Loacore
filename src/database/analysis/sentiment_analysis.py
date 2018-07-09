from prettytable import PrettyTable


def compute_files_polarity(files):

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
        file_score_dict[file.id_file] = (file.file_path, file_pos_score, file_neg_score, file_obj_score)

    return file_score_dict


def print_polarity_table(file_score_dict):
    table = PrettyTable(['File', 'Pos_Score', 'Neg_Score', 'Obj_Score'])
    for file in file_score_dict.keys():
        table.add_row([file_score_dict[file][0], file_score_dict[file][1], file_score_dict[file][2], file_score_dict[file][3]])
    print(table)
