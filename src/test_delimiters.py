import unittest

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter


class TestSplitDelimiter(unittest.TestCase):
    def test_plain(self):
        nodes = [TextNode("plain", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in result], [("plain", TextType.PLAIN)]
        )

    def test_code(self):
        nodes = [TextNode("a `b` c", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in result],
            [("a ", TextType.PLAIN), ("b", TextType.CODE), (" c", TextType.PLAIN)],
        )

    def test_bold(self):
        nodes = [TextNode("a **b** c", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in result],
            [("a ", TextType.PLAIN), ("b", TextType.BOLD), (" c", TextType.PLAIN)],
        )

    def test_italic(self):
        nodes = [TextNode("x _y_ z", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [(n.text, n.text_type) for n in result],
            [("x ", TextType.PLAIN), ("y", TextType.ITALIC), (" z", TextType.PLAIN)],
        )

    def test_missing_delimiter(self):
        nodes = [TextNode("oops `no close", TextType.PLAIN)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
