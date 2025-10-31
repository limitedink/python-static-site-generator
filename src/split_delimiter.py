def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if old_nodes.text_type != TextType.PLAIN:
        new_nodes.append(old_nodes)

    return new_nodes
