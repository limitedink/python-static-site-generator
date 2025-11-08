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

    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)
