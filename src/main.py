from src.renderer.generate_page import generate_page
from src.utils import tree_copy


def main():
    tree_copy("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()
