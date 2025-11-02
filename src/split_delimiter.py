from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            rebuilt = []
            parts = node.text.split(delimiter)
            if len(parts) == 1:
                new_nodes.append(node)
                continue
            if len(parts) % 2 == 0:
                raise Exception("invalid Markdown syntax: missing delimiter")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    rebuilt.append(TextNode(part, TextType.PLAIN))
                elif i % 2 != 0:
                    rebuilt.append(TextNode(part, text_type))
            new_nodes.extend(rebuilt)

    return new_nodes
