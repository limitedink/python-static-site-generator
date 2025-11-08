import re
from htmlnode import HTMLNode, ParentNode
from split import markdown_to_blocks, text_to_textnodes
from blocktype import BlockType, block_to_block_type
from converters import text_node_to_html_node
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_list = []

    def text_to_children(text):
        return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            trimmed = block.lstrip()
            for level in range(1, 7):
                prefix = "#" * level + " "
                if trimmed.startswith(prefix):
                    inner = trimmed[len(prefix) :].strip()
                    children = text_to_children(inner)
                    node = ParentNode(f"h{level}", children)
                    children_list.append(node)
                    break
        elif btype == BlockType.QUOTE:
            lines = [ln for ln in block.splitlines() if ln.strip()]
            stripped = []
            for ln in lines:
                stripped_ln = ln.lstrip()
                if stripped_ln.startswith(">"):
                    # Remove the '>' and any leading space after it
                    stripped_ln = stripped_ln[1:].lstrip()
                stripped.append(stripped_ln)
            inner = " ".join(stripped).strip()
            children = text_to_children(inner)
            node = ParentNode("blockquote", children)
            children_list.append(node)

        elif btype == BlockType.CODE:
            lines = block.splitlines()
            if lines and lines[0].strip() == "```" and lines[-1].strip() == "```":
                inner_lines = lines[1:-1]
                indents = [
                    len(l) - len(l.lstrip(" ")) for l in inner_lines if l.strip()
                ]
                pad = min(indents) if indents else 0
                dedented = [l[pad:] for l in inner_lines]
                inner = "\n".join(dedented) + "\n"
            else:
                inner = block
            code_child = text_node_to_html_node(TextNode(inner, TextType.PLAIN))
            children_list.append(ParentNode("pre", [ParentNode("code", [code_child])]))

        elif btype == BlockType.UNORDERED:
            items = []
            for line in block.splitlines():
                s = line.lstrip()
                if not s:
                    continue
                if s.startswith("- ") or s.startswith("* "):
                    item_text = s[2:]
                    li_children = text_to_children(item_text)
                    items.append(ParentNode("li", li_children))
            children_list.append(ParentNode("ul", items))

        elif btype == BlockType.ORDERED:
            items = []
            for line in block.splitlines():
                s = line.lstrip()
                if not s:
                    continue
                m = re.match(r"^\d+\. (.*)$", s)
                if m:
                    item_text = m.group(1)
                    li_children = text_to_children(item_text)
                    items.append(ParentNode("li", li_children))
            children_list.append(ParentNode("ol", items))

        else:
            inner = " ".join(block.splitlines()).strip()
            inner = " ".join(line.strip() for line in block.splitlines())
            inner = re.sub(r"\s+", " ", inner).strip()
            children = text_to_children(inner)
            node = ParentNode("p", children)
            children_list.append(node)
    return ParentNode(tag="div", children=children_list)
