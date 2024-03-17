import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_diff_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "normal")
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", "bold", "someUrl.com")
        node2 = TextNode("This is a different text node", "bold", "anotherUrl.com")
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
