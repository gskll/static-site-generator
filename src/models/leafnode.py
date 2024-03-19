from src.models.htmlnode import HTMLNode

self_closing_tags = ["img"]


class LeafNode(HTMLNode):
    def __init__(
        self, value: str, tag: str | None = None, props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("leafnode.value required", self)

        if not self.tag:
            return self.value

        props = super().props_to_html()
        open_tag = f"<{self.tag}{props}>"
        close_tag = f"</{self.tag}>"
        if self.tag in self_closing_tags:
            close_tag = ""

        html = open_tag + self.value + close_tag

        return html

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LeafNode):
            return False

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )
