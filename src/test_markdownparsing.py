import unittest
from markdownparsing import *

class TestIsHeadingBlock(unittest.TestCase):
    def test_paragraph(self):
        block = "First line of paragraph.\nSecond line of paragraph.\nThird line of paragraph."
        is_heading = is_heading_block(block)
        self.assertFalse(is_heading)
    def test_H1_single(self):
        block = "#First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_H1_multiline(self):
        block = "#First line of heading\nSecond line of heading\nThird line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_H2(self):
        block = "##First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_H3(self):
        block = "###First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_H4(self):
        block = "####First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_H5(self):
        block = "#####First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_H6(self):
        block = "######First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)
    def test_extra_H(self):
        block = "#######First line of heading"
        is_heading = is_heading_block(block)
        self.assertTrue(is_heading)

class TestIsCodeBlock(unittest.TestCase):
    def test_paragraph(self):
        block = "First line of paragraph.\nSecond line of paragraph.\nThird line of paragraph."
        is_code = is_code_block(block)
        self.assertFalse(is_code)
    def test_code_single(self):
        block = "```first line of code block```"
        is_code = is_code_block(block)
        self.assertTrue(is_code)
    def test_code_multiline(self):
        block = "```first line of code block\nsecond line of code block\nthird line of code block```"
        is_code = is_code_block(block)
        self.assertTrue(is_code)
    def test_code_extra_tick(self):
        block = "````first line of code block```"
        is_code = is_code_block(block)
        self.assertTrue(is_code)
    def test_code_missing_first_tick(self):
        block = "``first line of code block```"
        is_code = is_code_block(block)
        self.assertFalse(is_code)
    def test_code_missing_end_tick(self):
        block = "```first line of code block``"
        is_code = is_code_block(block)
        self.assertFalse(is_code)
    def test_internal_ticks(self):
        block = "```first line of ```code``` block```"
        is_code = is_code_block(block)
        self.assertTrue(is_code)

class TestIsQuoteBlock(unittest.TestCase):
    def test_paragraph(self):
        block_lines = ["First line of paragraph.", "Second line of paragraph.", "Third line of paragraph."]
        is_quote = is_quote_block(block_lines)
        self.assertFalse(is_quote)
    def test_quote_single(self):
        block_lines = [">First line of quote."]
        is_quote = is_quote_block(block_lines)
        self.assertTrue(is_quote)
    def test_quote_multiline(self):
        block_lines = [">First line of quote.", ">Second line of quote.", ">Third line of quote."]
        is_quote = is_quote_block(block_lines)
        self.assertTrue(is_quote)
    def test_quote_whitespace(self):
        block_lines = ["> First line of quote.", "> Second line of quote.", "> Third line of quote."]
        is_quote = is_quote_block(block_lines)
        self.assertTrue(is_quote)
    def test_quote_newline(self):
        block_lines = [">First line of quote.", ">", ">Second line of quote."]
        is_quote = is_quote_block(block_lines)
        self.assertTrue(is_quote)
    def test_quote_inconsistent_lines(self):
        block_lines = [">First line of quote.", "Second line of quote.", ">Third line of quote."]
        is_quote = is_quote_block(block_lines)
        self.assertFalse(is_quote)

class TestIsUnorderedListBlock(unittest.TestCase):
    def test_paragraph(self):
        block_lines = ["First line of paragraph.", "Second line of paragraph.", "Third line of paragraph."]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertFalse(is_unordered)
    def test_unordered_dash(self):
        block_lines = ["- First unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)
    def test_unordered_star(self):
        block_lines = ["* First unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)
    def test_unordered_without_space(self):
        block_lines = ["-First unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertFalse(is_unordered)
    def test_unordered_multiline_dash(self):
        block_lines = ["- First unordered item", "- Second unordered item", "- Third unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)
    def test_unordered_multiline_star(self):
        block_lines = ["* First unordered item", "* Second unordered item", "* Third unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)
    def test_unordered_mixed_symbols(self):
        block_lines = ["* First unordered item", "- Second unordered item", "* Third unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)
    def test_unordered_whitespace(self):
        block_lines = ["*   First unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)
    def test_unordered_inconsistent_lines(self):
        block_lines = ["* First unordered item", "2. Second unordered item", "* Third unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertFalse(is_unordered)
    def test_unordered_newline(self):
        block_lines = ["* First unordered item", "* ", "* Third unordered item"]
        is_unordered = is_unordered_list_block(block_lines)
        self.assertTrue(is_unordered)

class TestCheckOrderedListSequence(unittest.TestCase):
    def test_invalid(self):
        block_lines = ["- First unordered item", "- Second unordered item", "- Third unordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertFalse(is_sequenced)
    def test_single(self):
        block_lines = ["1. First ordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertTrue(is_sequenced)
    def test_single_late(self):
        block_lines = ["2. First ordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertFalse(is_sequenced)
    def test_multi(self):
        block_lines = ["1. First ordered item", "2. Second ordered item", "3. Third ordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertTrue(is_sequenced)
    def test_multi_late(self):
        block_lines = ["2. First ordered item", "3. Second ordered item", "4. Third ordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertFalse(is_sequenced)
    def test_multi_duplicate(self):
        block_lines = ["1. First ordered item", "1. Second ordered item", "1. Third ordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertFalse(is_sequenced)
    def test_multi_skip(self):
        block_lines = ["1. First ordered item", "3. Second ordered item", "4. Third ordered item"]
        is_sequenced = check_ordered_list_sequence(block_lines)
        self.assertFalse(is_sequenced)

class TestIsOrderedListBlock(unittest.TestCase):
    def test_paragraph(self):
        block_lines = ["First line of paragraph.", "Second line of paragraph.", "Third line of paragraph."]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertFalse(is_ordered)
    def test_ordered_single(self):
        block_lines = ["1. First ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertTrue(is_ordered)
    def test_ordered_multiline(self):
        block_lines = ["1. First ordered item", "2. Second ordered item", "3. Third ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertTrue(is_ordered)
    def test_ordered_missing_dot(self):
        block_lines = ["1 First ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertFalse(is_ordered)
    def test_ordered_missing_space(self):
        block_lines = ["1.First ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertFalse(is_ordered)
    def test_ordered_whitespace(self):
        block_lines = ["1.   First ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertTrue(is_ordered)
    def test_ordered_inconsistent_lines(self):
        block_lines = ["1. First ordered item", "Second ordered item", "3. Third ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertFalse(is_ordered)
    def test_ordered_newline(self):
        block_lines = ["1. First ordered item", "2. ", "3. Third ordered item"]
        is_ordered = is_ordered_list_block(block_lines)
        self.assertTrue(is_ordered)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_images(self):
        text = "This string of text has no images."
        extracted = extract_markdown_images(text)
        expected = []
        self.assertEqual(extracted, expected)
    def test_one_image(self):
        text = "This string has ![an image](https://www.boot.dev/img/bootdev-logo-full-small.webp) in it."
        extracted = extract_markdown_images(text)
        expected = [("an image", "https://www.boot.dev/img/bootdev-logo-full-small.webp")]
        self.assertEqual(extracted, expected)
    def test_multiple_images(self):
        text = "This string has ![an image](https://www.boot.dev/img/bootdev-logo-full-small.webp) and ![another image](https://www.boot.dev/_nuxt/gem-3-150.BBZuRZPH.png) in it."
        extracted = extract_markdown_images(text)
        expected = [("an image", "https://www.boot.dev/img/bootdev-logo-full-small.webp"), ("another image", "https://www.boot.dev/_nuxt/gem-3-150.BBZuRZPH.png")]
        self.assertEqual(extracted, expected)
    def test_other_brackets(self):
        text = "This string has some ![bracketed text] and more [bracketed text]."
        extracted = extract_markdown_images(text)
        expected = []
        self.assertEqual(extracted, expected)
    def test_other_parentheses(self):
        text = "This string has some ](parentheses) and more (parentheses)."
        extracted = extract_markdown_images(text)
        expected = []
        self.assertEqual(extracted, expected)
    def test_link(self):
        text = "This string has [a link](https://www.google.com)"
        extracted = extract_markdown_images(text)
        expected = []
        self.assertEqual(extracted, expected)

class TestExtractMarkdownLikes(unittest.TestCase):
    def test_no_links(self):
        text = "This string of text has no links."
        extracted = extract_markdown_links(text)
        expected = []
        self.assertEqual(extracted, expected)
    def test_one_link(self):
        text = "This string has [a link](https://www.google.com) in it."
        extracted = extract_markdown_links(text)
        expected = [("a link", "https://www.google.com")]
        self.assertEqual(extracted, expected)
    def test_multiple_links(self):
        text = "This string has [a link](https://www.google.com) and [another link](https://www.wikipedia.com) in it."
        extracted = extract_markdown_links(text)
        expected = [("a link", "https://www.google.com"), ("another link", "https://www.wikipedia.com")]
        self.assertEqual(extracted, expected)
    def test_other_brackets(self):
        text = "This string has some ![bracketed text] and more [bracketed text]."
        extracted = extract_markdown_links(text)
        expected = []
        self.assertEqual(extracted, expected)
    def test_other_parentheses(self):
        text = "This string has some ](parentheses) and more (parentheses)."
        extracted = extract_markdown_links(text)
        expected = []
        self.assertEqual(extracted, expected)
    def test_image(self):
        text = "This string has ![an image](https://www.boot.dev/img/bootdev-logo-full-small.webp) in it."
        extracted = extract_markdown_links(text)
        expected = []
        self.assertEqual(extracted, expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block_single_line(self):
        markdown = '''# This is a single line of header text'''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a single line of header text"]
        self.assertEqual(blocks, expected)
    def test_single_block_multiple_lines(self):
        markdown = '''This is the first line of a paragraph block.
This is the second line of a paragraph block.
This is the third line.'''
        blocks = markdown_to_blocks(markdown)
        expected = ["This is the first line of a paragraph block.\nThis is the second line of a paragraph block.\nThis is the third line."]
        self.assertEqual(blocks, expected)
    def test_single_block_leading_chad(self):
        markdown = '''
# This is a single line of header text'''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a single line of header text"]
        self.assertEqual(blocks, expected)
    def test_single_block_tailing_chad(self):
        markdown = '''# This is a single line of header text
'''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a single line of header text"]
        self.assertEqual(blocks, expected)
    def test_single_block_multiple_chads(self):
        markdown = '''

# This is a single line of header text

'''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a single line of header text"]
        self.assertEqual(blocks, expected)
    def test_single_block_whitespace(self):
        markdown = '''     # This is a single line of header text       '''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a single line of header text"]
        self.assertEqual(blocks, expected)
    def test_single_block_whitespace_with_chads(self):
        markdown = '''
        # This is a single line of header text



        '''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is a single line of header text"]
        self.assertEqual(blocks, expected)
    def test_multiple_blocks_single_lines(self):
        markdown = '''# This is the first header

# This is the second header'''
        blocks = markdown_to_blocks(markdown)
        expected = ["# This is the first header", "# This is the second header"]
        self.assertEqual(blocks, expected)
    def test_multiple_blocks_multiple_lines(self):
        markdown = '''This is the first line of the first paragraph.
Second line of first paragraph.
Third line of first paragraph.

This is the first line of the second paragraph.
This is the second line of the second paragraph.
Third line, second paragraph.'''
        blocks = markdown_to_blocks(markdown)
        expected = ["This is the first line of the first paragraph.\nSecond line of first paragraph.\nThird line of first paragraph.", "This is the first line of the second paragraph.\nThis is the second line of the second paragraph.\nThird line, second paragraph."]
        self.assertEqual(blocks, expected)
    def test_multiple_blocks_leading_tailing_chads(self):
        markdown = '''

This is the first line of the first paragraph.
Second line of first paragraph.
Third line of first paragraph.

This is the first line of the second paragraph.
This is the second line of the second paragraph.
Third line, second paragraph.


'''
        blocks = markdown_to_blocks(markdown)
        expected = ["This is the first line of the first paragraph.\nSecond line of first paragraph.\nThird line of first paragraph.", "This is the first line of the second paragraph.\nThis is the second line of the second paragraph.\nThird line, second paragraph."]
        self.assertEqual(blocks, expected)
    def test_multiple_blocks_internal_chads(self):
        markdown = '''This is the first line of the first paragraph.
Second line of first paragraph.
Third line of first paragraph.




This is the first line of the second paragraph.
This is the second line of the second paragraph.
Third line, second paragraph.'''
        blocks = markdown_to_blocks(markdown)
        expected = ["This is the first line of the first paragraph.\nSecond line of first paragraph.\nThird line of first paragraph.", "This is the first line of the second paragraph.\nThis is the second line of the second paragraph.\nThird line, second paragraph."]
        self.assertEqual(blocks, expected)
    def test_multiple_blocks_whitespace(self):
        markdown = '''           This is the first line of the first paragraph.
Second line of first paragraph.
Third line of first paragraph.

This is the first line of the second paragraph.
This is the second line of the second paragraph.
Third line, second paragraph.           '''
        blocks = markdown_to_blocks(markdown)
        expected = ["This is the first line of the first paragraph.\nSecond line of first paragraph.\nThird line of first paragraph.", "This is the first line of the second paragraph.\nThis is the second line of the second paragraph.\nThird line, second paragraph."]
        self.assertEqual(blocks, expected)
    def test_multiple_blocks_whitespace_with_chads(self):
        markdown = '''
        
        This is the first line of the first paragraph.
Second line of first paragraph.
Third line of first paragraph.



        This is the first line of the second paragraph.
This is the second line of the second paragraph.
Third line, second paragraph.   


    '''
        blocks = markdown_to_blocks(markdown)
        expected = ["This is the first line of the first paragraph.\nSecond line of first paragraph.\nThird line of first paragraph.", "This is the first line of the second paragraph.\nThis is the second line of the second paragraph.\nThird line, second paragraph."]
        self.assertEqual(blocks, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_block(self):
        block = "This is the first line of a paragraph.\nSecond line of the paragraph.\nThird line of the paragraph."
        block_type = block_to_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_type, expected)
    def test_heading_block(self):
        block = "#This is the first line of a heading\nSecond line of the heading"
        block_type = block_to_block_type(block)
        expected = BlockType.HEADING
        self.assertEqual(block_type, expected)
    def test_code_block(self):
        block = "```first line of code block\nsecond line of code block\nthird line of code block```"
        block_type = block_to_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(block_type, expected)
    def test_quote_block(self):
        block = ">This is the first line of a quote.\n>Second line of the quote.\n>Third line of the quote."
        block_type = block_to_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(block_type, expected)
    def test_unordered_block(self):
        block = "* First unordered item\n* Second unordered item\n* Third unordered item"
        block_type = block_to_block_type(block)
        expected = BlockType.UNORDERED
        self.assertEqual(block_type, expected)
    def test_ordered_block(self):
        block = "1. First ordered item\n2. Second ordered item\n3. Third ordered item"
        block_type = block_to_block_type(block)
        expected = BlockType.ORDERED
        self.assertEqual(block_type, expected)