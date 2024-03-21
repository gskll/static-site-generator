import unittest

from src.renderer.extract_page_title import extract_page_title


class TestExtractPageTitle(unittest.TestCase):
    def test_handles_no_title(self):
        doc = "random\nmarkdown\nstring"
        with self.assertRaises(ValueError) as e:
            extract_page_title(doc)
        self.assertEqual(str(e.exception.args[0]), "page must have one h1 title")

    def test_extracts_title_start(self):
        doc = "# page title\nother\n*lines*\n"
        title = extract_page_title(doc)
        self.assertEqual(title, "page title")

    def test_extracts_title_not_start(self):
        doc = "\n\n# *page* title\nother\n*lines*\n"
        title = extract_page_title(doc)
        self.assertEqual(title, "*page* title")

    def test_handles_multiple_h1(self):
        doc = "# h11 title\nhello\n# h12 title\ngoodbye\n"
        with self.assertRaises(ValueError) as e:
            extract_page_title(doc)
        self.assertEqual(str(e.exception.args[0]), "page must have one h1 title")

    def test_allows_pound_signs_in_test(self):
        doc = "# main title\nwe have #4 apples\n"
        title = extract_page_title(doc)
        self.assertEqual(title, "main title")

    def test_only_title(self):
        doc = "# title"
        title = extract_page_title(doc)
        self.assertEqual(title, "title")

    def test_handles_empty_doc(self):
        with self.assertRaises(ValueError) as e:
            extract_page_title("")

        self.assertEqual(str(e.exception.args[0]), "page must have one h1 title")
