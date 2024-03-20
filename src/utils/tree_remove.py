import os
from os.path import isfile, islink, isdir, exists, join
from . import walk_dir_tree


def tree_remove(top: str):
    if not exists(top):
        raise FileNotFoundError(top)

    if isfile(top) or islink(top):
        try:
            os.remove(top)
        except Exception as e:
            print(f"Error removing file/symlink {top}: {e}")
        return

    not_removed = list()
    tree = walk_dir_tree(top)
    for path, dirnames, filenames in tree[::-1]:
        for filename in filenames:
            filepath = join(path, filename)
            if not (isfile(filepath) or islink(filepath)):
                print(f"Skipping: path {filepath} is not a file or link")
                not_removed.append(filepath)
                continue

            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error removing file/link {filepath}: {e}")
                not_removed.append(filepath)

        for dirname in dirnames:
            dirpath = join(path, dirname)
            if not (isdir(dirpath) or islink(dirpath)):
                print(f"Skipping: path {dirpath} is not a directory or link")
                not_removed.append(dirpath)
                continue

            if islink(dirpath):
                try:
                    os.unlink(dirpath)
                except Exception as e:
                    print(f"Error unlinking directory link {dirpath}: {e}")
                    not_removed.append(dirpath)
                continue

            try:
                os.rmdir(dirpath)
            except Exception as e:
                print(f"Error removing directory {dirpath}: {e}")
                not_removed.append(dirpath)

    try:
        os.rmdir(top)
    except Exception as e:
        print(f"Error removing top directory {top}: {e}")
        not_removed.append(top)

    if len(not_removed) > 0:
        print(f"Following entries could not be removed. Check logs above.")
        for nr in not_removed:
            print(nr)
        raise Exception("Errors occurred during tree removal - check logs")
