import unittest

from src.leafnode import LeafNode
from src.parentnode import ParentNode

leaf_children = [
    LeafNode("Bold text", "b"),
    LeafNode("Normal text"),
    LeafNode("italic text", "i"),
    LeafNode("Normal text"),
]

children_html = "<b>Bold text</b>Normal text<i>italic text</i>Normal text"


class TestParentNode(unittest.TestCase):
    def test_properties(self):
        node = ParentNode(tag="a", props={"b": "c"}, children=leaf_children)
        if not node.props:
            self.fail("props should exist")
        if not node.children:
            self.fail("children should exist")
        self.assertEqual(node.tag, "a")
        self.assertDictEqual(node.props, {"b": "c"})
        self.assertSequenceEqual(node.children, leaf_children)

    def test_to_html_no_props(self):
        node = ParentNode(tag="p", children=leaf_children)
        html = node.to_html()

        want = f"<p>{children_html}</p>"
        self.assertEqual(html, want)

    def test_to_html_with_props(self):
        node = ParentNode(tag="p", props={"class": "text"}, children=leaf_children)
        html = node.to_html()

        want = f'<p class="text">{children_html}</p>'
        self.assertEqual(html, want)

    def test_to_html_nested_parent_nodes(self):
        p_node = ParentNode(tag="p", children=leaf_children)
        node = ParentNode(tag="div", children=[p_node])
        html = node.to_html()
        want = f"<div><p>{children_html}</p></div>"
        self.assertEqual(html, want)

    def test_to_html_nested_list(self):
        header_1 = LeafNode(tag="h2", value="List 1")
        list_1 = ParentNode(
            tag="ul",
            children=[
                LeafNode(tag="li", value="1", props={"class": "item"}),
                LeafNode(tag="li", value="2", props={"class": "item"}),
            ],
        )
        header_2 = LeafNode(tag="h2", value="List 2")
        list_2 = ParentNode(
            tag="ul",
            children=[
                LeafNode(tag="li", value="3", props={"class": "item"}),
                LeafNode(tag="li", value="4", props={"class": "item"}),
            ],
        )
        node = ParentNode(tag="div", children=[header_1, list_1, header_2, list_2])
        html = node.to_html()
        want = f'<div><h2>List 1</h2><ul><li class="item">1</li><li class="item">2</li></ul><h2>List 2</h2><ul><li class="item">3</li><li class="item">4</li></ul></div>'
        self.assertEqual(html, want)
