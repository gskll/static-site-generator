import unittest

from src.renderer.markdown_to_html_node import (
    block_to_html_node,
    block_to_html_node_code,
    block_to_html_node_heading,
    block_to_html_node_paragraph,
    block_to_html_node_quote,
    block_to_html_node_ulist,
    block_to_html_node_olist,
    markdown_to_html_node,
)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_header_only(self):
        markdown = "# Hello\n"
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        want = "<div><h1>Hello</h1></div>"
        self.assertEqual(want, html)

    def test_header_and_text(self):
        markdown = "# Hello\n\ngoodbye\n"
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        want = "<div><h1>Hello</h1><p>goodbye</p></div>"
        self.assertEqual(want, html)

    def test_inline_elements(self):
        self.maxDiff = None
        markdown = "**Bold** text with some\nnicely `codified` bits and also ~~some~~ a bit of *italic* [links](links.com)\n\n![boo](ghost.jpg)"
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        want = '<div><p><b>Bold</b> text with some\nnicely <code>codified</code> bits and also <s>some</s> a bit of <i>italic</i> <a href="links.com">links</a></p><p><img src="ghost.jpg" alt="boo"></p></div>'
        self.assertEqual(want, html)

    def test_lists(self):
        self.maxDiff = None
        markdown = (
            "# Lists test:\n\nunordered\n\n* oh\n* hi\n\n*ordered*\n\n1. good\n2. bye\n"
        )
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        want = "<div><h1>Lists test:</h1><p>unordered</p><ul><li>oh</li><li>hi</li></ul><p><i>ordered</i></p><ol><li>good</li><li>bye</li></ol></div>"
        self.assertEqual(want, html)

    def test_code_block(self):
        self.maxDiff = None
        markdown = 'javascript\n\n```\nconsole.log("hello")\nfunction boo(x){\n\treturn x}\n```\n\nand python\n\n```print("hello")\n\ndef boo(x):\n\treturn x\n```\n'
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        want = '<div><p>javascript</p><pre><code>\nconsole.log("hello")\nfunction boo(x){\n\treturn x}\n</code></pre><p>and python</p><pre><code>print("hello")\n\ndef boo(x):\n\treturn x\n</code></pre></div>'
        self.assertEqual(want, html)

    def test_block_quotes(self):
        self.maxDiff = None
        markdown = "blockquotes\n\n>to be\n>or not to be\n\nhmm how does it go?\n\n> that is \n>\n>the question\n>> quote by bill\n> ok?\n\n*nested!*"
        node = markdown_to_html_node(markdown)
        html = node.to_html()

        want = "<div><p>blockquotes</p><blockquote><p>to be</p><p>or not to be</p></blockquote><p>hmm how does it go?</p><blockquote><p> that is </p><p>the question</p><blockquote><p> quote by bill</p></blockquote><p> ok?</p></blockquote><p><i>nested!</i></p></div>"
        self.assertEqual(want, html)


class TestBlockToHTMLNode(unittest.TestCase):
    def test_handles_empty(self):
        with self.assertRaises(ValueError) as e:
            block_to_html_node("")

        self.assertEqual(str(e.exception), "empty block")

    def test_paragraph(self):
        block = "This *is* just a **random** paragraph with `some` [formatting](www.formatting.com)"
        node = block_to_html_node(block)
        html = node.to_html()

        want = '<p>This <i>is</i> just a <b>random</b> paragraph with <code>some</code> <a href="www.formatting.com">formatting</a></p>'
        self.assertEqual(html, want)

    def test_heading(self):
        block = "#### **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node(block)
        html = node.to_html()

        want = '<h4><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h4>'
        self.assertEqual(html, want)

    def test_code(self):
        block = """```test = True\ndef tester():\n\treturn False```"""
        node = block_to_html_node(block)
        html = node.to_html()

        want = "<pre><code>test = True\ndef tester():\n\treturn False</code></pre>"
        self.assertEqual(html, want)

    def test_quote(self):
        block = ">to be **or** not to be\n>*that* is the [question](questions.com)\n>* nested list\n>> nested blockquote!"
        node = block_to_html_node(block)
        html = node.to_html()

        want = '<blockquote><p>to be <b>or</b> not to be</p><p><i>that</i> is the <a href="questions.com">question</a></p><ul><li>nested list</li></ul><blockquote><p> nested blockquote!</p></blockquote></blockquote>'
        self.assertEqual(html, want)

    def test_ulist(self):
        block = "* *italic*\n* **bold**\n* `code`\n* normal"
        node = block_to_html_node(block)
        html = node.to_html()

        want = "<ul><li><i>italic</i></li><li><b>bold</b></li><li><code>code</code></li><li>normal</li></ul>"
        self.assertEqual(html, want)

    def test_olist(self):
        block = "1. *italic*\n2. **bold**\n3. `code`\n4. normal"
        node = block_to_html_node(block)
        html = node.to_html()

        want = "<ol><li><i>italic</i></li><li><b>bold</b></li><li><code>code</code></li><li>normal</li></ol>"
        self.assertEqual(html, want)


class TestBlockToHTMLNodeParagraph(unittest.TestCase):
    def test_converts_simple_block(self):
        block = "This is just a random paragraph"
        node = block_to_html_node_paragraph(block)
        html = node.to_html()
        want = "<p>This is just a random paragraph</p>"
        self.assertEqual(html, want)

    def test_converts_formatted_block(self):
        block = "This *is* just a **random** paragraph with `some` [formatting](www.formatting.com)"
        node = block_to_html_node_paragraph(block)
        html = node.to_html()

        want = '<p>This <i>is</i> just a <b>random</b> paragraph with <code>some</code> <a href="www.formatting.com">formatting</a></p>'
        self.assertEqual(html, want)

    def test_handles_typos(self):
        block = "This is *woops a paragraph with** typos"
        with self.assertRaises(ValueError) as e:
            block_to_html_node_paragraph(block)

        self.assertEqual(str(e.exception), "mismatch in delimiters")


class TestBlockToHTMLNodeHeading(unittest.TestCase):
    def test_works_simple_heading(self):
        block = "# Header"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = "<h1>Header</h1>"
        self.assertEqual(html, want)

    def test_works_formatted_h1(self):
        block = "# **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = '<h1><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h1>'
        self.assertEqual(html, want)

    def test_works_formatted_h2(self):
        block = "## **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = '<h2><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h2>'
        self.assertEqual(html, want)

    def test_works_formatted_h3(self):
        block = "### **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = '<h3><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h3>'
        self.assertEqual(html, want)

    def test_works_formatted_h4(self):
        block = "#### **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = '<h4><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h4>'
        self.assertEqual(html, want)

    def test_works_formatted_h5(self):
        block = "##### **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = '<h5><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h5>'
        self.assertEqual(html, want)

    def test_works_formatted_h6(self):
        block = "###### **Header** with *some* `cool` [formatting](link)"
        node = block_to_html_node_heading(block)
        html = node.to_html()

        want = '<h6><b>Header</b> with <i>some</i> <code>cool</code> <a href="link">formatting</a></h6>'
        self.assertEqual(html, want)


class TestBlockToHTMLNodeCode(unittest.TestCase):
    def test_works_simple(self):
        block = "```simple code block```"
        node = block_to_html_node_code(block)
        html = node.to_html()

        want = "<pre><code>simple code block</code></pre>"
        self.assertEqual(html, want)

    def test_works_multiline(self):
        block = """```test = True\ndef tester():\n\treturn False```"""
        node = block_to_html_node_code(block)
        html = node.to_html()

        want = "<pre><code>test = True\ndef tester():\n\treturn False</code></pre>"
        self.assertEqual(html, want)


class TestBlockToHTMLNodeQuote(unittest.TestCase):
    def test_works_simple(self):
        block = ">one line block quote"
        node = block_to_html_node_quote(block)
        html = node.to_html()

        want = "<blockquote><p>one line block quote</p></blockquote>"
        self.assertEqual(html, want)

    def test_works_formatted(self):
        block = ">one line *block* quote **with formatting**"
        node = block_to_html_node_quote(block)
        html = node.to_html()

        want = "<blockquote><p>one line <i>block</i> quote <b>with formatting</b></p></blockquote>"
        self.assertEqual(html, want)

    def test_works_multiline(self):
        block = ">to be **or** not to be\n>*that* is the [question](questions.com)"
        node = block_to_html_node_quote(block)
        html = node.to_html()

        want = '<blockquote><p>to be <b>or</b> not to be</p><p><i>that</i> is the <a href="questions.com">question</a></p></blockquote>'
        self.assertEqual(html, want)

    def test_works_multiline_nested(self):
        block = ">to be **or** not to be\n>*that* is the [question](questions.com)\n>* nested list\n>> nested blockquote!"
        node = block_to_html_node_quote(block)
        html = node.to_html()

        want = '<blockquote><p>to be <b>or</b> not to be</p><p><i>that</i> is the <a href="questions.com">question</a></p><ul><li>nested list</li></ul><blockquote><p> nested blockquote!</p></blockquote></blockquote>'
        self.assertEqual(html, want)


class TestBlockToHTMLNodeUlist(unittest.TestCase):
    def test_works_one_item(self):
        block = "* item1"
        node = block_to_html_node_ulist(block)
        html = node.to_html()

        want = "<ul><li>item1</li></ul>"
        self.assertEqual(html, want)

    def test_works_several(self):
        block = "* item1\n* item2\n- different"
        node = block_to_html_node_ulist(block)
        html = node.to_html()

        want = "<ul><li>item1</li><li>item2</li><li>different</li></ul>"
        self.assertEqual(html, want)

    def test_works_several_formatted(self):
        block = "* *italic*\n* **bold**\n* `code`\n* normal"
        node = block_to_html_node_ulist(block)
        html = node.to_html()

        want = "<ul><li><i>italic</i></li><li><b>bold</b></li><li><code>code</code></li><li>normal</li></ul>"
        self.assertEqual(html, want)


class TestBlockToHTMLNodeOlist(unittest.TestCase):
    def test_works_one_item(self):
        block = "1. item1"
        node = block_to_html_node_olist(block)
        html = node.to_html()

        want = "<ol><li>item1</li></ol>"
        self.assertEqual(html, want)

    def test_works_several(self):
        block = "1. item1\n2. item2\n3. item3"
        node = block_to_html_node_olist(block)
        html = node.to_html()

        want = "<ol><li>item1</li><li>item2</li><li>item3</li></ol>"
        self.assertEqual(html, want)

    def test_works_several_formatted(self):
        block = "1. *italic*\n2. **bold**\n3. `code`\n4. normal"
        node = block_to_html_node_olist(block)
        html = node.to_html()

        want = "<ol><li><i>italic</i></li><li><b>bold</b></li><li><code>code</code></li><li>normal</li></ol>"
        self.assertEqual(html, want)
