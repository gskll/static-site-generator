import re
from src.models.htmlnode import HTMLNode
from src.models.parentnode import ParentNode
from src.models.leafnode import LeafNode
from src.models.markdown_blocks import BlockType
from src.models.textnode import TextNode
from src.parser.block_to_block_type import block_to_block_type
from src.parser.split_markdown_blocks import split_markdown_blocks
from src.renderer.text_node_to_html_node import text_node_to_html_node
from src.renderer.text_to_textnodes import text_to_textnodes


def markdown_to_html_node(doc: str) -> HTMLNode:
    doc = doc.strip()
    blocks = split_markdown_blocks(doc)
    children = list()

    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)

    p = ParentNode(tag="div", children=children)
    return p


def block_to_html_node(block: str) -> HTMLNode:
    if block == "":
        raise ValueError("empty block")

    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return block_to_html_node_paragraph(block)
        case BlockType.HEADING:
            return block_to_html_node_heading(block)
        case BlockType.CODE:
            return block_to_html_node_code(block)
        case BlockType.QUOTE:
            return block_to_html_node_quote(block)
        case BlockType.ULIST:
            return block_to_html_node_ulist(block)
        case BlockType.OLIST:
            return block_to_html_node_olist(block)

    raise ValueError("invalid block type")


def block_to_html_node_paragraph(block: str) -> HTMLNode:
    children = build_inline_nodes(block)
    node = ParentNode(tag="p", children=children)
    return node


def block_to_html_node_heading(block: str) -> HTMLNode:
    parts = block.split(" ", 1)
    header_tag = f"h{len(parts[0])}"
    textnodes = text_to_textnodes(parts[1])
    children = list()
    for node in textnodes:
        if isinstance(node, TextNode):
            node = text_node_to_html_node(node)

        children.append(node)

    node = ParentNode(tag=header_tag, children=children)
    return node


def block_to_html_node_code(block: str) -> HTMLNode:
    block = block.strip("```")
    block = re.sub(
        "<NL>", "\n", block
    )  # revert newlines that we process on initial block splitting
    child = LeafNode(tag="code", value=block)
    node = ParentNode(tag="pre", children=[child])
    return node


def block_to_html_node_quote(block: str) -> HTMLNode:
    children = list()
    lines = block.split("\n")
    for line in lines:
        if all(c in " >" for c in line):
            continue

        line = line[1:]  # handle nested blockquotes
        child_node = block_to_html_node(line)
        children.append(child_node)

    node = ParentNode(tag="blockquote", children=children)
    return node


def block_to_html_node_ulist(block: str) -> HTMLNode:
    ul_children = list()
    list_items = block.split("\n")
    for li in list_items:
        li = li[2:]
        li_children = build_inline_nodes(li)
        li_node = ParentNode(tag="li", children=li_children)
        ul_children.append(li_node)

    node = ParentNode(tag="ul", children=ul_children)
    return node


# TODO: handle nested lists (ol within ul.li)
# TODO: handle different levels of list
def block_to_html_node_olist(block: str) -> HTMLNode:
    ol_children = list()
    list_items = block.split("\n")
    for li in list_items:
        li = re.sub(r"^\d+\. ", "", li)
        li_children = build_inline_nodes(li)
        li_node = ParentNode(tag="li", children=li_children)
        ol_children.append(li_node)

    node = ParentNode(tag="ol", children=ol_children)
    return node


def build_inline_nodes(text: str) -> list[HTMLNode]:
    textnodes = text_to_textnodes(text)
    children = list()
    for node in textnodes:
        if isinstance(node, TextNode):
            node = text_node_to_html_node(node)

        children.append(node)

    return children
