from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, value: str, tag: str | None = None, props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("leafnode.value required")

        if not self.tag:
            return self.value

        props = super().props_to_html()
        open_tag = f"<{self.tag}{props}>"
        close_tag = f"</{self.tag}>"
        html = open_tag + self.value + close_tag

        return html
