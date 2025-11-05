import unittest
from blocktype import block_to_block_type, BlockType

class TestBlockType(unittest.TestCase):
    def test_headings(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_codeblocks(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quoteblocks(self):
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unorderedlist(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED)

    def test_orderedlist(self):
        block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)

    def test_paragraph(self):
        block = "This is just a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unorderedlist_mixed_content(self):
        block = "- one\nplain line"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_orderedlist_single_line(self):
        block = "1. only one line"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED)

    def test_orderedlist_wrong_format_zero_padded(self):
        block = "01. nope\n02. still nope"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_orderedlist_wrong_separator(self):
        block = "1) nope\n2) also nope"
        with self.assertRaises(Exception):
            block_to_block_type(block)

    def test_quote_missing_prefix_on_second_line(self):
        block = "> first\nsecond"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_heading_missing_space(self):
        block = "##NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_starts_with_dash_but_not_list(self):
        block = "-not a list, missing space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
