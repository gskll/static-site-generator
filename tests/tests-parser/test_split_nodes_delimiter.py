import unittest

from src.models.leafnode import LeafNode
from src.models.textnode import TextNode, TextNodeType
from src.parser.split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_handles_unexpected_textnodetype(self):
        node = TextNode("", TextNodeType.TEXT)
        with self.assertRaises(KeyError):
            split_nodes_delimiter([node], TextNodeType.TEXT)

    def test_works_code(self):
        node = TextNode("This is text with a `code block` word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.CODE)

        want = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("code block", TextNodeType.CODE),
            TextNode(" word", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_bold(self):
        node = TextNode("This is text with a **bold** word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.BOLD)

        want = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("bold", TextNodeType.BOLD),
            TextNode(" word", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_italic(self):
        node = TextNode("This is text with a _italic_ word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.ITALIC)

        want = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("italic", TextNodeType.ITALIC),
            TextNode(" word", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_strikethrough(self):
        node = TextNode("This is text with a ~~deleted~~ word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.STRIKETHROUGH)

        want = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("deleted", TextNodeType.STRIKETHROUGH),
            TextNode(" word", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_text(self):
        node = TextNode("This is text only", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.ITALIC)

        want = [
            TextNode("This is text only", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_non_text_node(self):
        node = LeafNode(value="text")
        new_nodes = split_nodes_delimiter([node], TextNodeType.ITALIC)

        want = [LeafNode(value="text")]

        self.assertEqual(new_nodes, want)

    def test_works_text_node_not_text_type(self):
        node = TextNode("This is bold text only", TextNodeType.BOLD)
        new_nodes = split_nodes_delimiter([node], TextNodeType.ITALIC)

        want = [
            TextNode("This is bold text only", TextNodeType.BOLD),
        ]

        self.assertEqual(new_nodes, want)

    def test_fails_mismatched_delimiters(self):
        node = TextNode("This is text with _mismatched delimiters", TextNodeType.TEXT)

        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter([node], TextNodeType.ITALIC)
        self.assertEqual(str(e.exception), "mismatch in delimiters")

    def test_works_multiple_delimiters(self):
        node = TextNode("This _is_ text with _multiple delimiters_", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.ITALIC)

        want = [
            TextNode("This ", TextNodeType.TEXT),
            TextNode("is", TextNodeType.ITALIC),
            TextNode(" text with ", TextNodeType.TEXT),
            TextNode("multiple delimiters", TextNodeType.ITALIC),
        ]
        self.assertEqual(new_nodes, want)

    def test_works_delimiters_open_close(self):
        node = TextNode("**This text is all between delimiters**", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextNodeType.BOLD)

        want = [
            TextNode("This text is all between delimiters", TextNodeType.BOLD),
        ]
        self.assertEqual(new_nodes, want)

    def test_works_mutlple_nodes(self):
        node0 = LeafNode(value="test")
        node1 = TextNode("**This text is all between delimiters**", TextNodeType.TEXT)
        node2 = TextNode("This is text with a *italic* word", TextNodeType.TEXT)
        node3 = TextNode("This is text with a **bold** word", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter(
            [node0, node1, node2, node3], TextNodeType.BOLD
        )

        want = [
            LeafNode(value="test"),
            TextNode("This text is all between delimiters", TextNodeType.BOLD),
            TextNode("This is text with a *italic* word", TextNodeType.TEXT),
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("bold", TextNodeType.BOLD),
            TextNode(" word", TextNodeType.TEXT),
        ]
        self.assertEqual(new_nodes, want)

    def test_works_mutlple_nodes_multiple_passes(self):
        node0 = LeafNode(value="test")
        node1 = TextNode("**This text is all between delimiters**", TextNodeType.TEXT)
        node2 = TextNode("This is text with a _italic_ word", TextNodeType.TEXT)
        node3 = TextNode("This is text with a **bold** word", TextNodeType.TEXT)
        node4 = TextNode("This is text with `some code`", TextNodeType.TEXT)
        new_nodes = split_nodes_delimiter(
            [node0, node1, node2, node3, node4], TextNodeType.BOLD
        )
        new_nodes = split_nodes_delimiter(new_nodes, TextNodeType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, TextNodeType.CODE)

        want = [
            LeafNode(value="test"),
            TextNode("This text is all between delimiters", TextNodeType.BOLD),
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("italic", TextNodeType.ITALIC),
            TextNode(" word", TextNodeType.TEXT),
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("bold", TextNodeType.BOLD),
            TextNode(" word", TextNodeType.TEXT),
            TextNode("This is text with ", TextNodeType.TEXT),
            TextNode("some code", TextNodeType.CODE),
        ]
        self.assertEqual(new_nodes, want)
