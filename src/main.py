from shutil import copy
from textnode import TextNode, TextType
from copy_static import copy_static


def main():
    # T_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(T_node)

    copy_static("./static", "./public")


if __name__ == "__main__":
    main()
