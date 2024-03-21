from os import makedirs
from os.path import exists, isfile, isdir, dirname
from .extract_page_title import extract_page_title
from .markdown_to_html_node import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    empty_path_args = []
    if from_path == "":
        empty_path_args.append("from_path")
    if template_path == "":
        empty_path_args.append("template_path")
    if dest_path == "":
        empty_path_args.append("dest_path")

    if len(empty_path_args) > 0:
        empty_paths = ", ".join(empty_path_args)
        raise ValueError(f"path args cannot be empty: {empty_paths}")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not exists(from_path) or not isfile(from_path):
        raise FileNotFoundError(f"from_path must be a valid file path: {from_path}")

    with open(from_path, "r") as md_file:
        md_doc = md_file.read()
        if not md_doc:
            raise ValueError(f"from_path file {from_path} is empty")

    if not exists(template_path) or not isfile(template_path):
        raise FileNotFoundError(
            f"template_path must be a valid file path: {template_path}"
        )

    with open(template_path, "r") as tmpl_file:
        tmpl_doc = tmpl_file.read()
        if not tmpl_doc:
            raise ValueError(f"template_path file {template_path} is empty")

    content = markdown_to_html_node(md_doc).to_html()

    try:
        title = extract_page_title(md_doc)
    except Exception as e:
        raise Exception(f"Error extracting page title: {e}")

    page = tmpl_doc.replace("{{ Title }}", title).replace("{{ Content }}", content)

    dest_dir = dirname(dest_path)
    if not exists(dest_dir) or not isdir(dest_dir):
        try:
            makedirs(dest_dir)
        except Exception as e:
            raise Exception(f"Error creating dest_path directory {dest_dir}: {e}")

        print(f"MKDIRS: dest_path directory {dest_dir}")

    with open(dest_path, "w") as html_file:
        html_file.write(page)
