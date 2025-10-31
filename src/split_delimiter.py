def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        elif node.text_type == TextType.PLAIN:
            text = node.text
            delimiter = ""
            for letter in text:
                if letter == "`":
                    delimiter = "`"
                    parts = node.text.split(delimiter)
                    if parts % 2 == 0:
                        raise Exception("invalid Markdown syntax: missing delimiter")
                    for part in parts:
                        split_nodes_delimiter([part], delimiter, TextType.CODE)

                elif letter == "**":
                    delimiter = "**"
                    split_nodes_delimiter([node], delimiter, TextType.BOLD)

                elif letter == "_":
                    delimiter = "_"
                    split_nodes_delimiter([node], delimiter, TextType.ITALIC)

                else:
                    raise Exception("ERR:no delimiters found.")

    return new_nodes
