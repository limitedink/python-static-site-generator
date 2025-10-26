import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_none_returns_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_multiple_returns_formatted_string(self):
        node = HTMLNode(tag="a", props={"href": "https://x.com", "target": "_blank"})
        expected = ' href="https://x.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_diff_tag(self):
        node = LeafNode("p", "Hello")
        node2 = LeafNode("div", "Hello")
        self.assertNotEqual(node.to_html(), node2.to_html())

    def test_leaf_raw_text_not_equal_tagged(self):
        raw = LeafNode(None, "Hello")
        tagged = LeafNode("p", "Hello")
        self.assertNotEqual(raw.to_html(), tagged.to_html())

    def test_leaf_prop_order(self):
        node = LeafNode("a", "Hello", {"b": "2", "a":"1"})
        rendered = node.to_html()
        self.assertNotEqual(rendered, '<a b="2" a="1">Hello</a>')
        self.assertEqual(rendered, '<a a="1" b="2">Hello</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",)

if __name__ == "__main__":
    unittest.main()
