import os

import os


def walk_dir_tree(
    top: str, accumulator: list[tuple[str, list[str], list[str]]] | None = None
) -> list[tuple[str, list[str], list[str]]]:
    if not os.path.exists(top):
        raise ValueError("path doesn't exist", top)

    if not os.path.isdir(top):
        raise ValueError("path is not a valid directory", top)

    if not accumulator:
        accumulator = list()

    filenames = list()
    dirnames = list()
    entries = os.listdir(top)

    for entry in entries:
        path = os.path.join(top, entry)
        if os.path.isdir(path):
            dirnames.append(entry)
        else:
            filenames.append(entry)

    accumulator.append((top, dirnames, filenames))

    for dir in dirnames:
        dir_path = os.path.join(top, dir)
        walk_dir_tree(dir_path, accumulator)

    return accumulator


def treecopy(src: str, target: str):
    # delete current target directory contents

    # copy src contents to target
    pass
