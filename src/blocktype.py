from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def block_to_block_type(mdblock):
    heading_prefix = []
    for n in range(1, 7):
        heading_prefix.append("#" * n + " ")
    code_prefix = "```"
    quote_prefix = "> "
    ul_prefix = "- "

    lines = mdblock.split("\n")
    if mdblock.startswith("1. "):
        for i, line in enumerate(lines):
            ol_prefix = f"{i + 1}. "
            if not line.startswith(ol_prefix):
                raise Exception("syntax error: ordered list is not correctly ordered")
        return BlockType.ORDERED

    elif mdblock.startswith(tuple(heading_prefix)):
        return BlockType.HEADING

    elif mdblock.startswith(code_prefix):
        if mdblock.endswith(code_prefix):
            if len(mdblock) > 6:
                return BlockType.CODE
        raise Exception("Closing ``` fence for code block not found")

    elif mdblock.startswith(quote_prefix):
        if all(line.startswith("> ") for line in lines):
            return BlockType.QUOTE

    elif mdblock.startswith(ul_prefix):
        for line in lines:
            if not line.startswith(ul_prefix):
                raise Exception('syntax error: unordered_list missing "-" or space')
        return BlockType.UNORDERED

    else:
        return BlockType.PARAGRAPH
