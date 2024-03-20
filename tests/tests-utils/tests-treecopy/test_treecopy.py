import unittest
import tempfile
import shutil
import os

from src.utils.treecopy import walk_dir_tree


class TestTreecopy(unittest.TestCase):
    pass


class TestWalkDirTree(unittest.TestCase):
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
            open(file_path, "a").close()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_tmp_files(self):
        for path in self.test_dir_paths:
            self.assertTrue(os.path.exists(path))
            self.assertTrue(os.path.isdir(path))

        for file_path in self.test_file_paths:
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(os.path.isfile(file_path))
            self.assertEqual(os.path.getsize(file_path), 0)

    def test_handles_path_not_exists(self):
        path = "./nope"
        with self.assertRaises(ValueError) as e:
            walk_dir_tree(path)

        self.assertEqual(str(e.exception.args[0]), "path doesn't exist")

    def test_handles_walking_file_path(self):
        path = self.test_file_paths[0]
        with self.assertRaises(ValueError) as e:
            walk_dir_tree(path)

        self.assertEqual(str(e.exception.args[0]), "path is not a valid directory")

    def test_walks_path(self):
        self.maxDiff = None
        tree = walk_dir_tree(self.test_dir)
        print(tree)
        # fmt: off
        want = [
            ( f"{self.test_dir}", ["target-dir", "source-dir"], [],),
            ( f"{self.test_dir}/target-dir", [], ["test_file0.txt"],),
            ( f"{self.test_dir}/source-dir", ["misc", "empty"], ["test_file1.txt"],),
            ( f"{self.test_dir}/source-dir/misc", [], ["test_file2.txt"],),
            ( f"{self.test_dir}/source-dir/empty", [], [],),
        ]
        # fmt: on

        self.assertEqual(tree, want)
