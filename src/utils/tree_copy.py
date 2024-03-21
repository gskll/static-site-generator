import os
from os.path import exists, isdir, isfile, islink, join
import shutil

from . import tree_remove, walk_dir_tree


def tree_copy(src: str, target: str):
    if not (isdir(src) and isdir(target)):
        raise ValueError("src and target must both be directories", src, target)

    src_tree = walk_dir_tree(src)

    if exists(target):
        tree_remove(target)
        print(f"TREE_RM: {target}")

    try:
        os.mkdir(target)
        print(f"MKDIR: {target}")
    except Exception as e:
        raise Exception(f"Error creating target dir {target}: {e}")

    not_copied = list()
    for path, _, filenames in src_tree:
        newpath = path.replace(src, target)

        if isdir(path) and not exists(newpath):
            try:
                print(f"MKDIR: {target}")
                os.mkdir(newpath)
            except Exception as e:
                not_copied.append(newpath)
                print(f"Error creating dir {newpath}: {e}")

        for filename in filenames:
            oldfilepath = join(path, filename)
            newfilepath = join(newpath, filename)
            if not (isfile(oldfilepath) or islink(oldfilepath)):
                print(f"Skipping {oldfilepath}: not file or link")
                not_copied.append(oldfilepath)
                continue

            try:
                shutil.copy(oldfilepath, newfilepath)
                print(f"COPY: {oldfilepath} -> {newfilepath}")
            except Exception as e:
                print(f"Error copying from {oldfilepath} to {newfilepath}: {e}")
                not_copied.append(oldfilepath)

    if len(not_copied) > 0:
        print(f"Following entries could not be copied. Check logs above.")
        for nc in not_copied:
            print(nc)
        raise Exception("Errors occurred during tree copy - check logs")
