from src.htmlnode import HTMLNode
from src.textnode import TextNode, TextNodeType


def split_nodes_delimiter(
    old_nodes: list[TextNode | HTMLNode], delimiter: str, text_type: TextNodeType
) -> list[TextNode | HTMLNode]:
    new_nodes = list()

    for n in old_nodes:
        if not isinstance(n, TextNode):
            new_nodes.append(n)
            continue

        if n.text_type != TextNodeType.TEXT:
            new_nodes.append(n)
            continue

        parts = n.text.split(delimiter)

        if len(parts) == 1:
            new_nodes.append(n)
            continue

        if len(parts) % 2 == 0:
            raise ValueError("mismatch in delimiters")

        for i, p in enumerate(parts):
            if len(p) == 0:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text=p, text_type=TextNodeType.TEXT))
            else:
                new_nodes.append(TextNode(text=p, text_type=text_type))

    return new_nodes
