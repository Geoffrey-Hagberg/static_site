import os
import shutil
from pathlib import Path
from markdowntohtml import markdown_to_html_node, extract_title
from htmlnode import HTMLNode

def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def copy_directory(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    if os.path.isfile(source):
        shutil.copy(source, destination)
    else:
        contents_list = os.listdir(source)
        for content in contents_list:
            content_path = os.path.join(source, content)
            if os.path.isfile(content_path):
                shutil.copy(content_path, destination)
            else:
                new_destination = os.path.join(destination, content)
                copy_directory(content_path, new_destination)

def generate_pages_recursive(content_dir_path, template_path, destination_dir_path):
    markdown_extension = ".md"
    contents_list = os.listdir(content_dir_path)
    for content in contents_list:
        current_content_path = Path(os.path.join(content_dir_path, content))
        current_destination_path = Path(os.path.join(destination_dir_path, content))
        if os.path.isfile(current_content_path) and current_content_path.suffix.lower() == markdown_extension:
            html_destination_path = current_destination_path.with_suffix(".html")
            generate_page(current_content_path, template_path, html_destination_path)
        elif not os.path.isfile(current_content_path):
            generate_pages_recursive(current_content_path, template_path, current_destination_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path) as source_file:
        markdown = source_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    HTML_node = markdown_to_html_node(markdown)
    HTML_string = HTML_node.to_html()
    page_with_content = template.replace("{{ Content }}", HTML_string)
    title = extract_title(markdown)
    page_with_title = page_with_content.replace("{{ Title }}", title)
    destination_directory = os.path.dirname(dest_path)
    os.makedirs(destination_directory, 0o777, True)
    with open(dest_path, "w") as destination_file:
        destination_file.write(page_with_title)

def main():
    clear_directory("./public")
    copy_directory("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")

main()