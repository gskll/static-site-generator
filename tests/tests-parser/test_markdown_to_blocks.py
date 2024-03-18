import unittest

from src.parser.markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_works_with_one_block(self):
        text = "This is a\nmulti-line\nparagraph"
        blocks = markdown_to_blocks(text)
        want = ["This is a\nmulti-line\nparagraph"]
        self.assertEqual(want, blocks)

    def test_works_with_multiple_blocks(self):
        text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        blocks = markdown_to_blocks(text)
        want = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(want, blocks)

    def test_works_with_indentation(self):
        text = "* list item 1\n* list item 2\n\n    * indented list item1\n   *indented list item2"
        blocks = markdown_to_blocks(text)
        want = [
            "* list item 1\n* list item 2",
            "    * indented list item1\n   *indented list item2",
        ]
        self.assertEqual(want, blocks)
