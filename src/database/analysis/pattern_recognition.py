

def pos_tag_patterns_recognition(sentences, pattern):

    def pos_tag_rec(results, current_matching_nodes, node, pattern, index):
        if node.word.PoS_tag is not None:
            len_tag = len(pattern[index])
            if pattern[index] == '*' or node.word.PoS_tag[:len_tag] == pattern[index]:
                current_matching_nodes.append(node)
                if index == len(pattern) - 1:
                    results.append(current_matching_nodes)
                else:
                    for child in node.children:
                        pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)
        elif pattern[index] == '*':
            # Allow to match a word withou PoS_tag
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                for child in node.children:
                    pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)

    def children_rec(dt, node):
        results = []
        pos_tag_rec(results, [], node, pattern, 0)
        return results

    matching_nodes = []
    for sentence in sentences:
        dep_tree = sentence.dep_tree

        matching_nodes += children_rec(dep_tree, dep_tree.root)
    return matching_nodes


def label_patterns_recognition(sentences, pattern):

    def label_rec(results, current_matching_nodes, node, pattern, index):
        if pattern[index] == '*' or node.label == pattern[index]:
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                for child in node.children:
                    label_rec(results, current_matching_nodes.copy(), child, pattern, index + 1)

    def children_rec(dt, node):
        results = []
        label_rec(results, [], node, pattern, 0)
        return results

    matching_nodes = []
    for sentence in sentences:
        dep_tree = sentence.dep_tree

        matching_nodes += children_rec(dep_tree, dep_tree.root)
    return matching_nodes


def general_pattern_recognition(sentences, pattern, types):

    def pos_tag_rec(results, current_matching_nodes, node, pattern, types, index):
        if node.word.PoS_tag is not None:
            len_tag = len(pattern[index])
            if '*' in pattern[index] or node.word.PoS_tag[:len_tag] in pattern[index]:
                current_matching_nodes.append(node)
                if index == len(pattern) - 1:
                    results.append(current_matching_nodes)
                else:
                    for child in node.children:
                        if types[index + 1] == 'pos_tag':
                            pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
                        else:
                            label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
        elif '*' in pattern[index]:
            # Allow to match a word withou PoS_tag
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                if types[index + 1] == 'pos_tag':
                    for child in node.children:
                        pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
                else:
                    for child in node.children:
                        label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)

    def label_rec(results, current_matching_nodes, node, pattern, types, index):
        if '*' in pattern[index] or node.label in pattern[index]:
            current_matching_nodes.append(node)
            if index == len(pattern) - 1:
                results.append(current_matching_nodes)
            else:
                if types[index+1] == 'label':
                    for child in node.children:
                        label_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)
                else:
                    for child in node.children:
                        pos_tag_rec(results, current_matching_nodes.copy(), child, pattern, types, index + 1)

    def children_rec(dt, node):
        results = []
        if types[0] == 'label':
            label_rec(results, [], node, pattern, types, 0)
        else:
            pos_tag_rec(results, [], node, pattern, types, 0)
        return results

    matching_nodes = []
    for sentence in sentences:
        dep_tree = sentence.dep_tree

        matching_nodes += children_rec(dep_tree, dep_tree.root)
    return matching_nodes


def opposite_recognition(patterns):
    for pattern in patterns:
        node_synset = pattern[0].word.synset
        child_synset = pattern[1].word.synset
        if node_synset is not None and child_synset is not None:
            if (node_synset.pos_score > node_synset.neg_score
                    and child_synset.neg_score > child_synset.pos_score
                    or node_synset.pos_score < node_synset.neg_score
                    and child_synset.neg_score < child_synset.pos_score):
                print(pattern[0].word.word + ' ' + pattern[1].word.word)
                print(str(node_synset.pos_score) + "    " + str(child_synset.pos_score))
                print(str(node_synset.neg_score) + "    " + str(child_synset.neg_score))