import unittest

from src.parser.extract_inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


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


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_works_multiple_matches(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        extracted = extract_markdown_links(text)
        want = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]

        self.assertEqual(extracted, want)

    def test_works_no_matches(self):
        text = "This is just text"
        extracted = extract_markdown_links(text)
        want = []

        self.assertEqual(extracted, want)

    def test_works_empty_anchor(self):
        text = "This is text with a [link](https://www.example.com) and [](https://www.example.com/another)"
        extracted = extract_markdown_links(text)
        want = [
            ("link", "https://www.example.com"),
            ("", "https://www.example.com/another"),
        ]

        self.assertEqual(extracted, want)

    def test_works_empty_href(self):
        text = "This is text with a [link](https://www.example.com) and [another]()"
        extracted = extract_markdown_links(text)
        want = [
            ("link", "https://www.example.com"),
            ("another", ""),
        ]

        self.assertEqual(extracted, want)

    def test_partial_match(self):
        text = "This is text with (parentheses) and [a link](https://www.example.com)"
        extracted = extract_markdown_links(text)
        want = [
            ("a link", "https://www.example.com"),
        ]

        self.assertEqual(extracted, want)
