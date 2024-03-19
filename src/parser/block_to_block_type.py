import re

from src.models.markdown_blocks import BlockType


def block_to_block_type(block: str) -> BlockType:
    if is_heading(block):
        return BlockType.HEADING

    if is_code_block(block):
        return BlockType.CODE

    if is_quote_block(block):
        return BlockType.QUOTE

    if is_unordered_list(block):
        return BlockType.ULIST

    if is_ordered_list(block):
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def is_heading(block: str) -> bool:
    heading_re = r"^#{1,6} .+"
    matches = re.findall(heading_re, block)
    return len(matches) > 0


def is_code_block(block: str) -> bool:
    return block[:3] == "```" and block[-3:] == "```"


def is_quote_block(block: str) -> bool:
    lines = block.split("\n")
    for line in lines:
        if line[0] != ">":
            return False

    return True


def is_unordered_list(block: str) -> bool:
    lines = block.split("\n")
    for line in lines:
        if line[0] not in "*-":
            return False

    return True


def is_ordered_list(block: str) -> bool:
    lines = block.split("\n")
    for i, line in enumerate(lines):
        if line[0] != f"{i+1}" or line[1] != ".":
            return False

    return True
