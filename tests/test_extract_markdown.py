import unittest

from src.utils.extract_markdown import extract_markdown_images


class TestExtractMarkdownImages(unittest.TestCase):
    def test_works_multiple_matches(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        extracted = extract_markdown_images(text)
        want = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]

        self.assertEqual(extracted, want)

    def test_works_no_matches(self):
        text = "This is just text"
        extracted = extract_markdown_images(text)
        want = []

        self.assertEqual(extracted, want)

    def test_works_empty_alt(self):
        text = "This is text with an ![](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        extracted = extract_markdown_images(text)
        want = [
            ("", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]

        self.assertEqual(extracted, want)

    def test_works_empty_src(self):
        text = "This is text with an ![image]() and ![another](https://i.imgur.com/dfsdkjfd.png)"
        extracted = extract_markdown_images(text)
        want = [
            ("image", ""),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]

        self.assertEqual(extracted, want)

    def test_partial_match(self):
        text = "This is text with (parentheses) and ![an image](https://i.imgur.com/dfsdkjfd.png)"
        extracted = extract_markdown_images(text)
        want = [
            ("an image", "https://i.imgur.com/dfsdkjfd.png"),
        ]

        self.assertEqual(extracted, want)
