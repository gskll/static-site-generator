import unittest

from src.models.textnode import TextNode, TextNodeType
from src.renderer.text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_works_with_all_node_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        want = [
            TextNode("This is ", TextNodeType.TEXT),
            TextNode("text", TextNodeType.BOLD),
            TextNode(" with an ", TextNodeType.TEXT),
            TextNode("italic", TextNodeType.ITALIC),
            TextNode(" word and a ", TextNodeType.TEXT),
            TextNode("code block", TextNodeType.CODE),
            TextNode(" and an ", TextNodeType.TEXT),
            TextNode("image", TextNodeType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextNodeType.TEXT),
            TextNode("link", TextNodeType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(want, nodes)

    def test_works_with_text_only(self):
        text = "This is just text."
        nodes = text_to_textnodes(text)
        want = [TextNode("This is just text.", TextNodeType.TEXT)]
        self.assertEqual(want, nodes)

    def test_fails_with_mismatched_delimiters(self):
        text = "This is **mismatched text."
        with self.assertRaises(ValueError) as e:
            text_to_textnodes(text)
        self.assertEqual(str(e.exception), "mismatch in delimiters")

    def test_works_with_one_non_text_type(self):
        text = "`This is all code`"
        nodes = text_to_textnodes(text)
        want = [TextNode("This is all code", TextNodeType.CODE)]
        self.assertEqual(want, nodes)

    def test_works_with_not_all_type(self):
        text = "This *text* has **no** [code](google.com/code) or images"
        nodes = text_to_textnodes(text)
        want = [
            TextNode("This ", TextNodeType.TEXT),
            TextNode("text", TextNodeType.ITALIC),
            TextNode(" has ", TextNodeType.TEXT),
            TextNode("no", TextNodeType.BOLD),
            TextNode(" ", TextNodeType.TEXT),
            TextNode("code", TextNodeType.LINK, "google.com/code"),
            TextNode(" or images", TextNodeType.TEXT),
        ]

        self.assertEqual(want, nodes)
