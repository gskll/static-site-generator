# TODO: we need a different approach to handle codeblocks
# can have /n/n within a codeblock
# fix? preprocess and replace \n with other symbol ("<NL>"" might be good) then fix it when parsing?
import re


def split_markdown_blocks(doc: str) -> list[str]:
    doc = process_text_preserving_code_blocks(doc)
    return doc.split("\n\n")


def process_text_preserving_code_blocks(text: str) -> str:
    code_block_pattern = re.compile(r"```[\s\S]+?```")

    def process_code_block(match: re.Match):
        code_block = match.group(0)
        return re.sub("\n", "<NL>", code_block)

    processed_text = re.sub(code_block_pattern, process_code_block, text)

    return processed_text
