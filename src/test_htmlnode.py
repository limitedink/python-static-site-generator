import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("", TextType.LINK)
        node2 = TextNode("", TextType.LINK)
        self.assertEqual(node, node2)

    def test_noeq(self):
        node = TextNode("text", TextType.PLAIN, "www.url.com")
        node2 = TextNode("text", TextType.PLAIN, "www.url2.com")
        self.assertNotEqual(node, node2)

    def test_noeq2(self):
        node = TextNode("italics", TextType.ITALIC, None)
        node2 = TextNode("italics", TextType.ITALIC, "www.url.com")
        self.assertNotEqual(node, node2)

    def test_noeq3(self):
        node = TextNode("same", TextType.PLAIN)
        node2 = TextNode("same", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
