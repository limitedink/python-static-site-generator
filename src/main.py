import sys
from shutil import copy
from textnode import TextNode, TextType
from copy_static import copy_static
from gencontent import generate_page, generate_pages_recursive


def main():
    # T_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(T_node)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("./static", "./docs")
    generate_pages_recursive("content", "template.html", basepath)


if __name__ == "__main__":
    main()
