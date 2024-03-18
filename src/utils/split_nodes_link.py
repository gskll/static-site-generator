from src.htmlnode import HTMLNode
from src.textnode import TextNode, TextNodeType
from src.utils.extract_markdown import extract_markdown_links


def split_nodes_link(
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

        links = extract_markdown_links(n.text)
        if len(links) == 0:
            new_nodes.append(n)
            continue

        text_string = n.text
        for link in links:
            parts = text_string.split(f"[{link[0]}]({link[1]})", 1)
            if len(parts[0]):
                new_nodes.append(TextNode(text=parts[0], text_type=TextNodeType.TEXT))

            new_nodes.append(
                TextNode(text=link[0], text_type=TextNodeType.LINK, url=link[1])
            )
            text_string = parts[1]

        if len(text_string) > 0:
            new_nodes.append(TextNode(text=text_string, text_type=TextNodeType.TEXT))

    return new_nodes
