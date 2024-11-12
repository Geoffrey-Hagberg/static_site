from markdownparsing import *
from textparsing import *
from textnode import *
from htmlnode import *

def text_to_inline_nodes(tag, raw_value):
    text_nodes = text_to_text_nodes(raw_value)
    inline_nodes = []
    for text_node in text_nodes:
        inline_node = text_node_to_html_node(text_node)
        inline_nodes.append(inline_node)
    if (len(inline_nodes) == 1) and (inline_nodes[0].tag is None):
        return LeafNode(tag, inline_nodes[0].value)
    else:
        return ParentNode(tag, inline_nodes)

def block_to_heading(block):
    heading_count = block.count("#", 0, 6)
    tag = f"h{heading_count}"
    raw_value = block[heading_count:].strip()
    node = text_to_inline_nodes(tag, raw_value)
    return node

def block_to_code(block):
    tag = "code"
    raw_value = block.strip("```").rstrip("```").strip()
    secondary_node = text_to_inline_nodes(tag, raw_value)
    node = ParentNode("pre", [secondary_node])
    return node

def block_to_quote(block_lines):
    tag = "blockquote"
    raw_value = ""
    for line in block_lines:
        stripped_line = line[1:].strip()
        raw_value += f"{stripped_line}\n"
    node = text_to_inline_nodes(tag, raw_value.rstrip("\n"))
    return node

def block_to_unordered(block_lines):
    tag = "li"
    item_nodes = []
    for line in block_lines:
        raw_value = line[2:].strip()
        inner_node = text_to_inline_nodes(tag, raw_value)
        item_nodes.append(inner_node)
    node = ParentNode("ul", item_nodes)
    return node

def block_to_ordered(block_lines):
    tag = "li"
    item_nodes = []
    for line in block_lines:
        raw_value = line[3:].strip()
        inner_node = text_to_inline_nodes(tag, raw_value)
        item_nodes.append(inner_node)
    node = ParentNode("ol", item_nodes)
    return node

def block_to_paragraph(block):
    tag = "p"
    raw_value = block
    node = text_to_inline_nodes(tag, raw_value)
    return node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_lines = block.split("\n")
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            block_node = block_to_heading(block)
        elif block_type == BlockType.CODE:
            block_node = block_to_code(block)
        elif block_type == BlockType.QUOTE:
            block_node = block_to_quote(block_lines)
        elif block_type == BlockType.UNORDERED:
            block_node = block_to_unordered(block_lines)
        elif block_type == BlockType.ORDERED:
            block_node = block_to_ordered(block_lines)
        elif block_type == BlockType.PARAGRAPH:
            block_node = block_to_paragraph(block)
        block_nodes.append(block_node)
    HTML_node = ParentNode("div", block_nodes)
    return HTML_node

def extract_title(markdown):
    heading_nodes = []
    title_node = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            block_node = block_to_heading(block)
            heading_nodes.append(block_node)
    for node in heading_nodes:
        if node.tag == "h1":
            title_node.append(node)
    if len(title_node) == 0:
        raise Exception("No title heading.")
    elif len(title_node) > 1:
        raise Exception("Multiple title headings.")
    else:
        return title_node[0].value