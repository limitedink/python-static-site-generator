import unittest
from extract_links import extract_markdown_images, extract_markdown_links


class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to google](https://google.com)"
        )
        self.assertListEqual([("to google", "https://google.com")], matches)


if __name__ == "__main__":
    unittest.main()
