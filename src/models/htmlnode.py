from typing import Sequence


class HTMLNode:
    def __init__(
        self,
        value: str | None = None,
        tag: str | None = None,
        children: Sequence["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        html_props = ""
        for k, v in self.props.items():
            html_props += f' {k}="{v}"'

        return html_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False

        return (
            self.tag != other.tag
            and self.value != other.value
            and self.children != other.children
            and self.props != other.props
        )
