from src.models.htmlnode import HTMLNode
from src.models.textnode import TextNode, TextNodeType
from src.parser.split_nodes_delimiter import split_nodes_delimiter
from src.parser.split_nodes_image import split_nodes_image
from src.parser.split_nodes_link import split_nodes_link


def text_to_textnodes(text: str) -> list[TextNode | HTMLNode]:
    node = TextNode(text=text, text_type=TextNodeType.TEXT)
    nodes = split_nodes_image([node])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextNodeType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextNodeType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextNodeType.CODE)

    return nodes
