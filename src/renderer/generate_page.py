from os import makedirs
from os.path import isfile, isdir, dirname
from .extract_page_title import extract_page_title
from .markdown_to_html_node import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    validate_paths(from_path, template_path, dest_path)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_doc = read_file(from_path)
    templ_doc = read_file(template_path)

    try:
        html_content = markdown_to_html_node(md_doc).to_html()
    except Exception as e:
        raise Exception(f"Error converting markdown to html: {e}")

    try:
        title = extract_page_title(md_doc)
    except Exception as e:
        raise Exception(f"Error extracting page title: {e}")

    page = templ_doc.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    dest_dir = dirname(dest_path)
    if not isdir(dest_dir):
        try:
            makedirs(dest_dir)
        except Exception as e:
            raise Exception(f"Error creating dest_path directory {dest_dir}: {e}")

        print(f"MKDIRS: dest_path directory {dest_dir}")

    with open(dest_path, "w") as html_file:
        html_file.write(page)


def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            content = f.read()
    except IOError as e:
        raise IOError(f"Error reading file {path}: {e}")

    if not content:
        raise ValueError(f"The file {path} is empty (0 bytes)")

    return content


def validate_paths(from_path: str, template_path: str, dest_path: str) -> None:
    empty_paths = [p for p in (from_path, template_path, dest_path) if not p]
    if empty_paths:
        raise ValueError(
            f"the following path arguments cannot be empty: {', '.join(empty_paths)}"
        )

    if not isfile(from_path):
        raise FileNotFoundError(f"from_path must be a valid file path: {from_path}")

    if not isfile(template_path):
        raise FileNotFoundError(
            f"template_path must be a valid file path: {template_path}"
        )
