import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextNodeType
from src.utils.split_nodes_link import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):
    def test_works_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        want = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://www.example.com"),
            TextNode(" and ", TextNodeType.TEXT),
            TextNode("another", TextNodeType.LINK, "https://www.example.com/another"),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_multiple_links_2(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) and more text",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        want = [
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://www.example.com"),
            TextNode(" and ", TextNodeType.TEXT),
            TextNode("another", TextNodeType.LINK, "https://www.example.com/another"),
            TextNode(" and more text", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_link_only(self):
        node = TextNode(
            "[link](https://www.example.com)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        want = [
            TextNode("link", TextNodeType.LINK, "https://www.example.com"),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_two_links_only(self):
        node = TextNode(
            "[link](https://www.example.com)[another](https://www.example.com/another)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        want = [
            TextNode("link", TextNodeType.LINK, "https://www.example.com"),
            TextNode("another", TextNodeType.LINK, "https://www.example.com/another"),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_no_links(self):
        node = TextNode("no links here", TextNodeType.TEXT)
        new_nodes = split_nodes_link([node])
        want = [TextNode("no links here", TextNodeType.TEXT)]

        self.assertEqual(new_nodes, want)

    def test_works_multiple_nodes(self):
        node0 = LeafNode(value="test")
        node1 = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) and more text",
            TextNodeType.TEXT,
        )
        node2 = TextNode("just text", TextNodeType.TEXT)
        node3 = TextNode(
            "wow it's [another link](misc link path) cool", TextNodeType.TEXT
        )
        new_nodes = split_nodes_link([node0, node1, node2, node3])

        want = [
            LeafNode(value="test"),
            TextNode("This is text with a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://www.example.com"),
            TextNode(" and ", TextNodeType.TEXT),
            TextNode("another", TextNodeType.LINK, "https://www.example.com/another"),
            TextNode(" and more text", TextNodeType.TEXT),
            TextNode("just text", TextNodeType.TEXT),
            TextNode("wow it's ", TextNodeType.TEXT),
            TextNode("another link", TextNodeType.LINK, "misc link path"),
            TextNode(" cool", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)
