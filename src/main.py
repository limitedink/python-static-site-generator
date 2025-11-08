from shutil import copy
from textnode import TextNode, TextType
from copy_static import copy_static
from gencontent import generate_page


def main():
    # T_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(T_node)

    copy_static("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
