from textnode import TextNode, TextType


def main():
    T_node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(T_node)


if __name__ == "__main__":
    main()
