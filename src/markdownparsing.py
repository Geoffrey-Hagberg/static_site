import re
from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"
    PARAGRAPH = "paragraph"

def is_heading_block(block):
    if re.search(r"^(#{1,6})", block):
        return True
    else:
        return False

def is_code_block(block):
    begins_block = re.search(r"^(```)", block)
    ends_block = re.search(r"(```)$", block)
    return all([begins_block, ends_block])

def is_quote_block(block_lines):
    return all(re.fullmatch(r">(.*)", line) is not None for line in block_lines)

def is_unordered_list_block(block_lines):
    return all(re.fullmatch(r"(\*|-)(\s.*)", line) is not None for line in block_lines)

def check_ordered_list_sequence(block_lines):
    sequence_booleans = []
    next_item_number = 1
    for line in block_lines:
        first_char = line[0]
        try:
            first_digit = int(first_char)
            if first_digit == next_item_number:
                sequence_booleans.append(True)
            else:
                sequence_booleans.append(False)
        except ValueError:
            return False
        next_item_number += 1
    return all(sequence_booleans)

def is_ordered_list_block(block_lines):
    all_ordered_list_items = all(re.fullmatch(r"\d\.(\s.*)", line) is not None for line in block_lines)
    all_in_sequence = check_ordered_list_sequence(block_lines)
    return all([all_ordered_list_items, all_in_sequence])

def extract_markdown_images(text):
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text):
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links

def markdown_to_blocks(markdown):
    blocks_with_chads = markdown.split("\n\n")
    blocks = []
    for block in blocks_with_chads:
        block_without_chads = block.strip("\n").strip()
        if any(char.isalnum() for char in block):
            blocks.append(block_without_chads)
    return blocks

def block_to_block_type(block):
    block_lines = block.split("\n")
    if is_heading_block(block):
        return BlockType.HEADING
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote_block(block_lines):
        return BlockType.QUOTE
    elif is_unordered_list_block(block_lines):
        return BlockType.UNORDERED
    elif is_ordered_list_block(block_lines):
        return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH