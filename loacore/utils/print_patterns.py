
def print_patterns(patterns, PoS_tag_display=False, label_display=False, display=True):
    patterns_str = ''
    for pattern in patterns:
        patterns_str += "( "
        for node in pattern[:-1]:
            patterns_str += str(node.word.word)
            if PoS_tag_display:
                patterns_str += " : " + str(node.word.PoS_tag)
            if label_display:
                patterns_str += " : " + str(node.label)
            patterns_str += ", "
        patterns_str += str(pattern[-1].word.word)
        if PoS_tag_display:
            patterns_str += " : " + str(pattern[-1].word.PoS_tag)
        if label_display:
            patterns_str += " : " + str(pattern[-1].label)
        patterns_str += " )\n"
    if display:
        print(patterns_str)
    return patterns_str
