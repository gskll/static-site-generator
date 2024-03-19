from src.models.htmlnode import HTMLNode
from src.models.textnode import TextNode, TextNodeType
from src.parser.extract_inline_markdown import extract_markdown_images


def split_nodes_image(
    old_nodes: list[TextNode | HTMLNode],
) -> list[TextNode | HTMLNode]:
    new_nodes = list()
    for n in old_nodes:
        if not isinstance(n, TextNode):
            new_nodes.append(n)
            continue

        if n.text_type != TextNodeType.TEXT:
            new_nodes.append(n)
            continue

        if len(n.text) == 0:
            continue

        images = extract_markdown_images(n.text)
        if len(images) == 0:
            new_nodes.append(n)
            continue

        text_string = n.text
        for img in images:
            parts = text_string.split(f"![{img[0]}]({img[1]})", 1)
            if len(parts[0]):
                new_nodes.append(TextNode(text=parts[0], text_type=TextNodeType.TEXT))

            new_nodes.append(
                TextNode(text=img[0], text_type=TextNodeType.IMAGE, url=img[1])
            )
            text_string = parts[1]

        if len(text_string) > 0:
            new_nodes.append(TextNode(text=text_string, text_type=TextNodeType.TEXT))

    return new_nodes
