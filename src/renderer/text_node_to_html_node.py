from src.models.textnode import TextNode, TextNodeType
from src.models.leafnode import LeafNode
from src.models.htmlnode import HTMLNode


def text_node_to_html_node(text_node: TextNode) -> "HTMLNode":
    match text_node.text_type:
        case TextNodeType.TEXT:
            return LeafNode(value=text_node.text)
        case TextNodeType.BOLD:
            return LeafNode(value=text_node.text, tag="b")
        case TextNodeType.ITALIC:
            return LeafNode(value=text_node.text, tag="i")
        case TextNodeType.CODE:
            return LeafNode(value=text_node.text, tag="code")
        case TextNodeType.LINK:
            if not text_node.url:
                raise ValueError("link text_node with no url")
            return LeafNode(
                value=text_node.text, tag="a", props={"href": text_node.url}
            )
        case TextNodeType.IMAGE:
            if not text_node.url:
                raise ValueError("image text_node with no url")
            return LeafNode(
                value="", tag="img", props={"src": text_node.url, "alt": text_node.text}
            )

    raise Exception("text_node.text_type not recognized")
