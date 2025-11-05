import unittest

from textnode import TextNode, TextType
from split import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)


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

    def test_split_images_no_images(self):
        node = TextNode("This is just plain text with no images.", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [Link to google](https://google.com) and another [Link to Netflix](https://netflix.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("Link to google", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("Link to Netflix", TextType.LINK, "https://netflix.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This is text with no links at all.", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_multiple_input_nodes(self):
        node1 = TextNode(
            "Text with a [first link](https://example.com/1).", TextType.PLAIN
        )
        node2 = TextNode("Just plain text.", TextType.PLAIN)
        node3 = TextNode(
            "And a [second link](https://example.com/2) here.", TextType.PLAIN
        )

        input_nodes = [node1, node2, node3]
        new_nodes = split_nodes_link(input_nodes)

        expected_nodes = [
            TextNode("Text with a ", TextType.PLAIN),
            TextNode("first link", TextType.LINK, "https://example.com/1"),
            TextNode(".", TextType.PLAIN),
            TextNode("Just plain text.", TextType.PLAIN),
            TextNode("And a ", TextType.PLAIN),
            TextNode("second link", TextType.LINK, "https://example.com/2"),
            TextNode(" here.", TextType.PLAIN),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_links_startsends_with_link(self):
        node = TextNode(
            "[Start Link](https://start.com) text in middle [End Link](https://end.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Start Link", TextType.LINK, "https://start.com"),
            TextNode(" text in middle ", TextType.PLAIN),
            TextNode("End Link", TextType.LINK, "https://end.com"),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_links_onlylink(self):
        node = TextNode("[Only Link](https://only.com)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Only Link", TextType.LINK, "https://only.com"),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_links_consecutive_links(self):
        node = TextNode(
            "Text[Link1](https://l1.com)[Link2](https://l2.com)more text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Text", TextType.PLAIN),
            TextNode("Link1", TextType.LINK, "https://l1.com"),
            TextNode("Link2", TextType.LINK, "https://l2.com"),
            TextNode("more text", TextType.PLAIN),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_text_to_textnodes_full_line(self):
        md = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(md)
        expected = [
            TextNode("This is ", TextType.PLAIN, None),
            TextNode("text", TextType.BOLD, None),
            TextNode(" with an ", TextType.PLAIN, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word and a ", TextType.PLAIN, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" and an ", TextType.PLAIN, None),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.PLAIN, None),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
