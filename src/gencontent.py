import os
from block_to_html import markdown_to_html_node


def extract_title(md):
    lines = md.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found.")


def generate_page(from_path, template_path, dest_path):
    print(
        f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"'
    )
    markdown = open(from_path).read()
    template = open(template_path).read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    open(dest_path, "w").write(page)
