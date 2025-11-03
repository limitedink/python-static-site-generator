from types import new_class
from typing import Text
from textnode import TextNode, TextType
from extract_links import extract_markdown_images, extract_markdown_links


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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        imgs = extract_markdown_images(text)

        if not imgs:
            new_nodes.append(node)
            continue

        for alt, url in imgs:
            parts = text.split(f"![{alt}]({url})", 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before:
                new_nodes.append(TextNode(before, TextType.PLAIN))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for label, url in links:
            parts = text.split(f"[{label}]({url})", 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            if before:
                new_nodes.append(TextNode(before, TextType.PLAIN))
            new_nodes.append(TextNode(label, TextType.LINK, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.PLAIN))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes
