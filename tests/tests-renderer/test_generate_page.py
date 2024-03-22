import os
import shutil
import tempfile
import unittest

from src.renderer.generate_page import generate_page


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.from_path = os.path.join(self.test_dir, "test.md")
        self.template_path = os.path.join(self.test_dir, "template.html")
        self.dest_path = os.path.join(self.test_dir, "output/test.html")

        self.md_content = "# Title\n\nContent"
        self.template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        self.expected_html = "<html><head><title>Title</title></head><body><div><h1>Title</h1><p>Content</p></div></body></html>"

        with open(self.from_path, "w") as f:
            f.write(self.md_content)

        with open(self.template_path, "w") as f:
            f.write(self.template_content)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_setup(self):
        self.assertTrue(os.path.isdir(self.test_dir))
        self.assertTrue(os.path.isfile(self.from_path))
        self.assertTrue(os.path.isfile(self.template_path))

        with open(self.from_path, "r") as f:
            content = f.read()
            self.assertEqual(content, self.md_content)

        with open(self.template_path, "r") as f:
            content = f.read()
            self.assertEqual(content, self.template_content)

    def test_generates_page(self):
        generate_page(self.from_path, self.template_path, self.dest_path)

        self.assertTrue(os.path.isfile(self.dest_path))
        with open(self.dest_path, "r") as f:
            content = f.read()
            self.assertEqual(content, self.expected_html)

    def test_handles_bad_path(self):
        bad_path = os.path.join(self.test_dir, "fake/dir")
        with self.assertRaises(FileNotFoundError) as e:
            generate_page(bad_path, self.template_path, self.dest_path)

        self.assertTrue(
            str(e.exception).startswith("from_path must be a valid file path")
        )

    def test_handles_empty_path(self):
        with self.assertRaises(ValueError) as e:
            generate_page("", self.template_path, self.dest_path)

        self.assertTrue(
            str(e.exception).startswith("the following path arguments cannot be empty")
        )

    def test_handles_empty_file(self):
        with open(self.template_path, "w") as f:
            f.write("")

        with self.assertRaises(ValueError) as e:
            generate_page(self.from_path, self.template_path, self.dest_path)

        self.assertTrue(str(e.exception).endswith("is empty (0 bytes)"))
