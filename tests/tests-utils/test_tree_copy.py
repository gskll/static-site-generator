from os.path import exists, isdir, join
import unittest
import tempfile
import os
import shutil

from src.utils import tree_copy
from src.utils.walk_dir_tree import walk_dir_tree


class TestTreeCopy(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.src_dir_name = "source-dir"
        self.target_dir_name = "target-dir"
        self.src_dir = os.path.join(self.test_dir, self.src_dir_name)
        self.target_dir = os.path.join(self.test_dir, self.target_dir_name)

        self.test_dir_paths = [
            self.target_dir,
            self.src_dir,
            os.path.join(self.src_dir, "misc"),
            os.path.join(self.src_dir, "empty"),
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

    def test_handles_src_file(self):
        file_path = self.test_file_paths[0]
        with self.assertRaises(ValueError) as e:
            tree_copy(file_path, self.target_dir)
        self.assertEqual(
            str(e.exception.args[0]), "src and target must both be directories"
        )

    def test_handles_target_file(self):
        file_path = self.test_file_paths[0]
        with self.assertRaises(ValueError) as e:
            tree_copy(self.src_dir, file_path)
        self.assertEqual(
            str(e.exception.args[0]), "src and target must both be directories"
        )

    def test_copy_single_empty_dir(self):
        src = self.test_dir_paths[-1]  # "empty" test dir defined in setup
        target = self.target_dir
        prevTime = os.path.getmtime(target)
        tree_copy(src, target)
        newTime = os.path.getmtime(target)
        self.assertTrue(exists(target))
        self.assertTrue(isdir(target))
        self.assertLess(prevTime, newTime)

        normalized_src_tree = normalize_filetree(walk_dir_tree(src))
        normalized_target_tree = normalize_filetree(walk_dir_tree(target))
        self.assertEqual(normalized_src_tree, normalized_target_tree)

    def test_copy_single_dir_single_file(self):
        src = self.test_dir_paths[-2]  # "misc" test dir defined in setup
        target = self.target_dir
        prevTime = os.path.getmtime(target)
        tree_copy(src, target)
        newTime = os.path.getmtime(target)
        self.assertTrue(exists(target))
        self.assertTrue(isdir(target))
        self.assertLess(prevTime, newTime)

        normalized_src_tree = normalize_filetree(walk_dir_tree(src))
        normalized_target_tree = normalize_filetree(walk_dir_tree(target))
        self.assertEqual(normalized_src_tree, normalized_target_tree)

    def test_copies_correctly(self):
        srcdir = self.src_dir
        target = self.target_dir
        prevTime = os.path.getmtime(target)
        tree_copy(srcdir, target)
        newTime = os.path.getmtime(target)
        self.assertTrue(exists(target))

        self.assertTrue(exists(target))
        self.assertTrue(isdir(target))
        self.assertLess(prevTime, newTime)

        normalized_src_tree = normalize_filetree(walk_dir_tree(srcdir))
        normalized_target_tree = normalize_filetree(walk_dir_tree(target))
        self.assertEqual(normalized_src_tree, normalized_target_tree)


# TODO: time to abstract the listtuple directory item to a class/type?
def normalize_filetree(
    tree: list[tuple[str, list[str], list[str]]], new_base: str = ""
) -> list[tuple[str, list[str], list[str]]]:
    old_base = tree[0][0]

    normalized = []
    for path, dirs, files in tree:
        normalized_path = path.replace(old_base, new_base, 1)
        normalized.append((normalized_path, dirs, files))

    return normalized
