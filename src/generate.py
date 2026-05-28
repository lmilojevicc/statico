import os
from pathlib import Path

from extract import extract_title
from parser import markdown_to_html_node

def generate_pages_recursive(
       content_dir_path: str, template_path: str, dest_dir_path: str
   ) -> None:
       content_dir = Path(content_dir_path)
       dest_dir = Path(dest_dir_path)

       for source_path in content_dir.iterdir():
           dest_path = dest_dir / source_path.name

           if source_path.is_dir():
               generate_pages_recursive(str(source_path), template_path, str(dest_path))

           elif source_path.is_file() and source_path.suffix == ".md":
               generate_page(
                   str(source_path),
                   template_path,
                   str(dest_path.with_suffix(".html")),
               )


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_content = ""
    try:
        markdown_content = Path(from_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        markdown_content = ""

    template_content = ""
    try:
        template_content = Path(template_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        template_content = ""

    html_node = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)
    html_content = html_node.to_html()

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)

    path = Path(dest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template_content, encoding="utf-8")
