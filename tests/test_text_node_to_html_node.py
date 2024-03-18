import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextNodeType
from src.utils.text_node_to_html_node import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_TEXT(self):
        textnode = TextNode(text="test", text_type=TextNodeType.TEXT)
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode, LeafNode(value="test"))

    def test_text_node_to_html_node_BOLD(self):
        textnode = TextNode(text="test", text_type=TextNodeType.BOLD)
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode, LeafNode(value="test", tag="b"))

    def test_text_node_to_html_node_ITALIC(self):
        textnode = TextNode(text="test", text_type=TextNodeType.ITALIC)
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode, LeafNode(value="test", tag="i"))

    def test_text_node_to_html_node_CODE(self):
        textnode = TextNode(text="test", text_type=TextNodeType.CODE)
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(htmlnode, LeafNode(value="test", tag="code"))

    def test_text_node_to_html_node_LINK(self):
        textnode = TextNode(text="test", text_type=TextNodeType.LINK, url="test_url")
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(
            htmlnode, LeafNode(value="test", tag="a", props={"href": "test_url"})
        )

    def test_text_node_to_html_node_LINK_no_url(self):
        textnode = TextNode(text="test", text_type=TextNodeType.LINK)
        with self.assertRaises(ValueError) as e:
            text_node_to_html_node(textnode)

        self.assertEqual(str(e.exception), "link text_node with no url")

    def test_text_node_to_html_node_IMAGE(self):
        textnode = TextNode(text="test", text_type=TextNodeType.IMAGE, url="test_url")
        htmlnode = text_node_to_html_node(textnode)
        self.assertIsInstance(htmlnode, LeafNode)
        self.assertEqual(
            htmlnode,
            LeafNode(value="", tag="img", props={"src": "test_url", "alt": "test"}),
        )

    def test_text_node_to_html_node_IMAGE_no_url(self):
        textnode = TextNode(text="test", text_type=TextNodeType.IMAGE)
        with self.assertRaises(ValueError) as e:
            text_node_to_html_node(textnode)

        self.assertEqual(str(e.exception), "image text_node with no url")
