from src.models.textnode import TextNode, TextNodeType


def main():
    tn = TextNode("this is a text node", TextNodeType.BOLD)
    tn2 = TextNode("this is a text node", TextNodeType.BOLD, "url.com")

    print(tn)
    print(tn2)


main()
