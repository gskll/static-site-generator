import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    image_re = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_re, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_re = r"\[(.*?)\]\((.*?)\)"
    return re.findall(link_re, text)
