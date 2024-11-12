from textnode import *
from markdownparsing import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if (len(split_nodes) % 2 == 0) and (len(split_nodes) > 1):
                raise ValueError("Malformed Markdown. Odd number of delimiters in text.")
            else:
                for split in split_nodes:
                    if split_nodes.index(split) % 2 == 0:
                        if split != '':
                            split_node = TextNode(split, TextType.TEXT)
                            new_nodes.append(split_node)
                    else:
                        if split != '':
                            split_node = TextNode(split, text_type)
                            new_nodes.append(split_node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        while True:
            images = extract_markdown_images(current_text)
            if not images:
                if current_text:
                    last_node = TextNode(current_text, TextType.TEXT)
                    new_nodes.append(last_node)
                break
            image_alt, image_URL = images[0]
            split_nodes = current_text.split(f'![{image_alt}]({image_URL})', 1)
            if split_nodes[0] != '':
                first_node = TextNode(split_nodes[0], TextType.TEXT)
                new_nodes.append(first_node)
            second_node = TextNode(image_alt, TextType.IMAGE, image_URL)
            new_nodes.append(second_node)
            if len(split_nodes) > 1:
                current_text = split_nodes[1]
            else:
                break
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        while True:
            links = extract_markdown_links(current_text)
            if not links:
                if current_text:
                    last_node = TextNode(current_text, TextType.TEXT)
                    new_nodes.append(last_node)
                break
            link_anchor, link_URL = links[0]
            split_nodes = current_text.split(f'[{link_anchor}]({link_URL})', 1)
            if split_nodes[0] != '':
                first_node = TextNode(split_nodes[0], TextType.TEXT)
                new_nodes.append(first_node)
            second_node = TextNode(link_anchor, TextType.LINK, link_URL)
            new_nodes.append(second_node)
            if len(split_nodes) > 1:
                current_text = split_nodes[1]
            else:
                break
    return new_nodes

def text_to_text_nodes(text):
    current_nodes = [TextNode(text, TextType.TEXT)]
    current_nodes = split_nodes_delimiter(current_nodes, "`", TextType.CODE)
    current_nodes = split_nodes_delimiter(current_nodes, "**", TextType.BOLD)
    current_nodes = split_nodes_delimiter(current_nodes, "*", TextType.ITALIC)
    current_nodes = split_nodes_image(current_nodes)
    current_nodes = split_nodes_link(current_nodes)
    return current_nodes