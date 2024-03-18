import unittest

from src.models.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_properties(self):
        node = HTMLNode(tag="tag", value="value", props={"a": "b"})
        if not node.props:
            self.fail("props not set correctly")

        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertIsNone(node.children)
        self.assertDictEqual(node.props, {"a": "b"})

    def test_props_to_html(self):
        node = HTMLNode(props={"a": "b", "c": "d"})
        props = node.props_to_html()

        self.assertEqual(props, ' a="b" c="d"')
