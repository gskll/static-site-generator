import unittest
import tempfile
import os
import shutil

from src.utils import tree_remove


class TestTreeRemove(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.test_dir_paths = [
            os.path.join(self.test_dir, "target-dir"),
            os.path.join(self.test_dir, "source-dir"),
            os.path.join(self.test_dir, "source-dir", "misc"),
            os.path.join(self.test_dir, "source-dir", "empty"),
        ]
        self.test_file_paths = []

        for i, path in enumerate(self.test_dir_paths):
            os.mkdir(path)
            if path.endswith("empty"):
                continue
            file_path = os.path.join(path, f"test_file{i}.txt")
            self.test_file_paths.append(file_path)
            with open(file_path, "w") as f:
                f.write(file_path)

    def tearDown(self) -> None:
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_setup(self):
        for path in self.test_dir_paths:
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isdir(path))

        for file_path in self.test_file_paths:
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))
            with open(file_path, "r") as f:
                self.assertEqual(f.read(), file_path)

    def test_deletes_empty_dir(self):
        empty_dir = self.test_dir_paths[-1]  # empty
        self.assertTrue(os.path.exists(empty_dir))
        tree_remove(empty_dir)
        self.assertFalse(os.path.exists(empty_dir))

    def test_deletes_single_file(self):
        empty_file = self.test_file_paths[0]
        self.assertTrue(os.path.exists(empty_file))
        tree_remove(empty_file)
        self.assertFalse(os.path.exists(empty_file))

    def test_deletes_non_empty_dir(self):
        dir = self.test_dir_paths[0]
        self.assertTrue(os.path.exists(dir))
        tree_remove(dir)
        self.assertFalse(os.path.exists(dir))

    def test_deletes_whole_non_empty_tree(self):
        dir = self.test_dir
        self.assertTrue(os.path.exists(dir))
        tree_remove(dir)
        self.assertFalse(os.path.exists(dir))

    def test_handles_file_not_exists(self):
        fake_file = os.path.join(self.test_dir, "nope.txt")
        with self.assertRaises(FileNotFoundError):
            tree_remove(fake_file)
