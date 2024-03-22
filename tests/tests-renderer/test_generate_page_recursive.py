import os
from os.path import join, isfile, isdir
import shutil
import tempfile
import unittest

from src.renderer.generate_page_recursive import generate_page_recursive


class TestGeneratePageRecursive(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.content_dir = join(self.test_dir, "content")
        self.content_sub_dir = join(self.test_dir, "content", "sub")
        self.dest_dir = join(self.test_dir, "dest")
        self.content_path = join(self.content_dir, "index.md")
        self.dest_path = join(self.dest_dir, "index.html")
        self.content_sub_path = join(self.content_sub_dir, "index2.md")
        self.dest_path = join(self.dest_dir, "index.html")
        self.dest_path_sub = join(self.dest_dir, "sub", "index2.html")
        self.template_path = join(self.test_dir, "template.html")

        self.md_content = "# Title\n\nContent"
        self.md_content_sub = "# Title 2\n\nContent 2"
        self.template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        self.expected_html = "<html><head><title>Title</title></head><body><div><h1>Title</h1><p>Content</p></div></body></html>"
        self.expected_html_sub = "<html><head><title>Title 2</title></head><body><div><h1>Title 2</h1><p>Content 2</p></div></body></html>"

        os.makedirs(self.content_sub_dir)
        os.mkdir(self.dest_dir)
        with open(self.content_path, "w") as f:
            f.write(self.md_content)

        with open(self.content_sub_path, "w") as f:
            f.write(self.md_content_sub)

        with open(self.template_path, "w") as f:
            f.write(self.template_content)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_setup(self):
        self.assertTrue(isdir(self.test_dir))
        self.assertTrue(isdir(self.content_dir))
        self.assertTrue(isdir(self.content_sub_dir))
        self.assertTrue(isdir(self.dest_dir))
        self.assertTrue(isfile(self.content_path))
        self.assertTrue(isfile(self.content_sub_path))
        self.assertTrue(isfile(self.template_path))

        with open(self.content_path, "r") as f:
            content = f.read()
            self.assertEqual(content, self.md_content)

        with open(self.content_sub_path, "r") as f:
            content = f.read()
            self.assertEqual(content, self.md_content_sub)

        with open(self.template_path, "r") as f:
            content = f.read()
            self.assertEqual(content, self.template_content)

    def test_generates_page(self):
        generate_page_recursive(self.content_dir, self.template_path, self.dest_dir)

        self.assertTrue(isdir(self.dest_dir))
        self.assertTrue(isdir(join(self.dest_dir, "sub")))

        with open(self.dest_path) as f:
            content = f.read()
            self.assertEqual(content, self.expected_html)

        with open(self.dest_path_sub) as f:
            content = f.read()
            self.assertEqual(content, self.expected_html_sub)

    def test_handles_bad_path(self):
        bad_path = os.path.join(self.test_dir, "fake/dir")
        with self.assertRaises(FileNotFoundError) as e:
            generate_page_recursive(bad_path, self.template_path, self.dest_dir)

        self.assertTrue(
            str(e.exception).startswith(
                "dir_path_content must be a valid directory path"
            )
        )

    def test_handles_empty_path(self):
        with self.assertRaises(ValueError) as e:
            generate_page_recursive("", self.template_path, self.dest_dir)

        self.assertTrue(
            str(e.exception).startswith("the following path arguments cannot be empty")
        )

    def test_copies_md_files_only(self):
        with open(join(self.content_dir, "notmd.py"), "w") as f:
            f.write("not markdown")

        generate_page_recursive(self.content_dir, self.template_path, self.dest_dir)

        self.assertFalse(os.path.exists(join(self.dest_dir, "notmd.py")))
