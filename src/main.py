from textnode import TextNode


def main():
    tn = TextNode("this is a text node", "bold")
    tn2 = TextNode("this is a text node", "bold", "url.com")

    print(tn)
    print(tn2)


main()
