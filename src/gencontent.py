import os
from block_to_html import markdown_to_html_node


def extract_title(md):
    lines = md.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found.")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(
        f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"'
    )

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath="/"
):
    print(
        f'Generating pages from "{dir_path_content}" to "{dest_dir_path}" using "{template_path}"'
    )

    files = os.listdir(dir_path_content)
    for name in files:
        src_path = os.path.join(dir_path_content, name)
        if os.path.isdir(src_path):
            sub_dest = os.path.join(dest_dir_path, name)
            generate_pages_recursive(src_path, template_path, sub_dest, basepath)
        elif os.path.isfile(src_path) and name.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, os.path.splitext(name)[0] + ".html")
            generate_page(src_path, template_path, dest_path, basepath)
