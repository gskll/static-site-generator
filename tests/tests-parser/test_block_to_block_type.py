import unittest

from src.parser.block_to_block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        block = "# Valid h1"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Valid h6"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.HEADING)

    def test_heading_no_space(self):
        block = "###Invalid heading"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_heading_too_deep(self):
        block = "####### Invalid heading"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```valid code block```"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```valid code block\nover several lines```"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.CODE)

    def test_code_block_invalid_open(self):
        block = "``invalid code block```"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_code_block_invalid_close(self):
        block = "```invalid code block"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> valid quote"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.QUOTE)

    def test_quote_block_multiline(self):
        block = "> valid quote\n> valid quote2\n> valid quote 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.QUOTE)

    def test_quote_block_line_missing(self):
        block = "> valid quote\n> valid quote2\n valid quote 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_quote_block_line_space_before(self):
        block = "> valid quote\n> valid quote2\n > valid quote 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_unordered_list_dash(self):
        block = "- item 1"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.ULIST)

    def test_unordered_list_dash_multiline(self):
        block = "- item 1\n- item 2\n- item 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.ULIST)

    def test_unordered_list_star(self):
        block = "* item 1"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.ULIST)

    def test_unordered_list_start_multiline(self):
        block = "* item 1\n* item 2\n* item 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.ULIST)

    def test_unordered_list_mixed_multiline(self):
        block = "- item 1\n* item 2\n- item 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.ULIST)

    def test_unordered_list_missing_space(self):
        block = "-item\n-hello"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_unordered_list_missing(self):
        block = "- item 1\n* item 2\nitem 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_unordered_list_indentation(self):
        block = "- item 1\n* item 2\n - item 3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. item 1"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.OLIST)

    def test_ordered_list_multiline(self):
        block = "1. item 1\n2. item2\n3. item3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.OLIST)

    def test_ordered_list_missing_space(self):
        block = "1.item\n2.hello"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_ordered_list_misnumbered(self):
        block = "0. item 1\n2. item2\n3. item3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_ordered_list_misnumbered2(self):
        block = "1. item 1\n1. item2\n3. item3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_ordered_list_missing_dot(self):
        block = "0. item 1\n2 item2\n3. item3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_ordered_list_missing_symbol(self):
        block = "0. item 1\n2. item2\nitem3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)

    def test_ordered_list_misindented(self):
        block = "0. item 1\n2. item2\n 3. item3"
        bt = block_to_block_type(block)
        self.assertEqual(bt, BlockType.PARAGRAPH)
