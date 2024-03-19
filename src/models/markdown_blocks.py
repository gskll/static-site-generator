from enum import Enum

BlockType = Enum(
    "BlockType", ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "ULIST", "OLIST"]
)
