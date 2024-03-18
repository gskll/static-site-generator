import unittest

from src.models.textnode import TextNode, TextNodeType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a different text node", TextNodeType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_text_type(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.TEXT)
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", TextNodeType.BOLD, "someUrl.com")
        node2 = TextNode(
            "This is a different text node", TextNodeType.BOLD, "anotherUrl.com"
        )
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
