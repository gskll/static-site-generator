import re


def extract_markdown_images(text: str) -> list[tuple[str]]:
    image_re = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_re, text)
