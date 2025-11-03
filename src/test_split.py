import unittest

from textnode import TextNode, TextType
from split import split_nodes_delimiter, split_nodes_image, split_nodes_link


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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
