from typing import Sequence
from src.models.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        children: Sequence[HTMLNode],
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(children=children, tag=tag, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode.tag required")
        if not self.children or not len(self.children):
            raise ValueError("ParentNode.children required")

        html = ""
        parent_props = super().props_to_html()
        parent_open = f"<{self.tag}{parent_props}>"
        parent_close = f"</{self.tag}>"

        html += parent_open
        for c in self.children:
            html += c.to_html()

        html += parent_close
        return html
