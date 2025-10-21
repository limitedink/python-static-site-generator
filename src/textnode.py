from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                other.text == self.text
                and other.text_type == self.text_type
                and other.url == self.url
            )
        return NotImplemented

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
