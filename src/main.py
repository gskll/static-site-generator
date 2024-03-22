from src.renderer.generate_page_recursive import generate_page_recursive
from src.utils import tree_copy


def main():
    tree_copy("./static", "./public")
    generate_page_recursive("./content", "./template.html", "./public")


main()
