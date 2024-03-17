import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_props(self):
        node = LeafNode(value="a", tag="b", props={"a": "b"})
        if not node.props:
            self.fail("props not set correctly")

        self.assertEqual(node.value, "a")
        self.assertEqual(node.tag, "b")

    def test_to_html_no_props(self):
        node = LeafNode("This is a paragraph of text.", "p")
        html = node.to_html()
        self.assertEqual(html, "<p>This is a paragraph of text.</p>")

    def test_to_html(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        html = node.to_html()
        self.assertEqual(html, '<a href="https://www.google.com">Click me!</a>')
