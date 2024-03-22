import os
from os.path import isdir, isfile

from src.renderer.generate_page import generate_page
from src.utils.walk_dir_tree import walk_dir_tree


def generate_page_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    validate_paths(dir_path_content, template_path, dest_dir_path)
    content_tree = walk_dir_tree(dir_path_content)
    counter = 0

    for from_dir, _, filenames in content_tree:
        dest_dir = from_dir.replace(dir_path_content, dest_dir_path)

        for filename in filenames:
            from_path = os.path.join(from_dir, filename)

            if not filename.endswith(".md"):
                print(f"Ignoring non markdown file: {filename}")
                continue

            html_filename = filename.replace(".md", ".html")
            dest_path = os.path.join(dest_dir, html_filename)
            generate_page(from_path, template_path, dest_path)
            counter += 1

    print(f"Generated {counter} html files in {dest_dir_path}")


def validate_paths(dir_path_content: str, template_path: str, dest_dir_path: str):
    empty_paths = [p for p in (dir_path_content, template_path, dest_dir_path) if not p]
    if empty_paths:
        raise ValueError(
            f"the following path arguments cannot be empty: {', '.join(empty_paths)}"
        )

    if not isdir(dir_path_content):
        raise FileNotFoundError(
            f"dir_path_content must be a valid directory path: {dir_path_content}"
        )

    if not isdir(dest_dir_path):
        raise FileNotFoundError(
            f"dest_dir_path must be a valid directory path: {dest_dir_path}"
        )

    if not isfile(template_path):
        raise FileNotFoundError(
            f"template_path must be a valid file path: {template_path}"
        )
