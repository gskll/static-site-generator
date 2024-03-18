import unittest

from src.textnode import TextNode, TextNodeType
from src.leafnode import LeafNode
from src.utils.split_nodes_image import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):
    def test_works_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        want = [
            TextNode("This is text with an ", TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_multiple_images_2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and this is just text.",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        want = [
            TextNode("This is text with an ", TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" and this is just text.", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        want = [
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_two_images_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        want = [
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_no_images(self):
        node = TextNode(
            "no images here",
            TextNodeType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        want = [
            TextNode("no images here", TextNodeType.TEXT),
        ]

        self.assertEqual(new_nodes, want)

    def test_works_multiple_nodes(self):
        node0 = LeafNode(value="test")
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and this is just text.",
            TextNodeType.TEXT,
        )
        node2 = TextNode("just text", TextNodeType.TEXT)
        node3 = TextNode("text and ![another image](./localpath)", TextNodeType.TEXT)
        new_nodes = split_nodes_image([node0, node1, node2, node3])

        want = [
            LeafNode(value="test"),
            TextNode("This is text with an ", TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextNodeType.TEXT),
            TextNode(
                "second image", TextNodeType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" and this is just text.", TextNodeType.TEXT),
            TextNode("just text", TextNodeType.TEXT),
            TextNode("text and ", TextNodeType.TEXT),
            TextNode("another image", TextNodeType.IMAGE, "./localpath"),
        ]

        self.assertEqual(new_nodes, want)
