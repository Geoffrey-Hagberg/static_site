import unittest
from markdowntohtml import *

class TestTextToInlineNodes(unittest.TestCase):
    def test_single_text(self):
        tag = "p"
        raw_value = "A line of unformatted text."
        node = text_to_inline_nodes(tag, raw_value)
        expected = LeafNode("p", "A line of unformatted text.")
        self.assertEqual(node, expected)
    def test_single_partial_formatted(self):
        tag = "p"
        raw_value = "A line with **bold text** in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_single_fully_formatted(self):
        tag = "p"
        raw_value = "**A completely bold line.**"
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode("b", "A completely bold line.")
        ])
        self.assertEqual(node, expected)
    def test_multiline_text(self):
        tag = "p"
        raw_value = "A line of unformatted text.\nA second line of unformatted text."
        node = text_to_inline_nodes(tag, raw_value)
        expected = LeafNode("p", "A line of unformatted text.\nA second line of unformatted text.")
        self.assertEqual(node, expected)
    def test_multiline_partial_formatted(self):
        tag = "p"
        raw_value = "A line with some **bold text**.\nA second unformatted line."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with some "),
            LeafNode("b", "bold text"),
            LeafNode(None, ".\nA second unformatted line.")
        ])
        self.assertEqual(node, expected)
    def test_multiline_fully_formatted(self):
        tag = "p"
        raw_value = "**First of two bold lines.\nSecond of two bold lines.**"
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode("b", "First of two bold lines.\nSecond of two bold lines.")
        ])
        self.assertEqual(node, expected)
    def test_single_line_multiple_formatting_distinct(self):
        tag = "p"
        raw_value = "A line with **bold text** as well as *italic text* in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " as well as "),
            LeafNode("i", "italic text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_single_line_multiple_formatting_duplicate(self):
        tag = "p"
        raw_value = "A line with **bold text** and **more bold text** in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " and "),
            LeafNode("b", "more bold text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_multiline_fully_formatted_alt(self):
        tag = "p"
        raw_value = "**First of two bold lines.**\n**Second of two bold lines.**"
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode("b", "First of two bold lines."),
            LeafNode(None, "\n"),
            LeafNode("b", "Second of two bold lines.")
        ])
        self.assertEqual(node, expected)
    def test_multiline_multiple_formatting_distinct(self):
        tag = "p"
        raw_value = "First line with **bold text** in it.\nSecond line with *italic text* in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "First line with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in it.\nSecond line with "),
            LeafNode("i", "italic text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_multiline_multiple_formatting_duplicate(self):
        tag = "p"
        raw_value = "First line with *italic text* in it.\nSecond line with *more italic text* in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "First line with "),
            LeafNode("i", "italic text"),
            LeafNode(None, " in it.\nSecond line with "),
            LeafNode("i", "more italic text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_inline_code(self):
        tag = "p"
        raw_value = "A line with some `inline code` in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with some "),
            LeafNode("code", "inline code"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_inline_image(self):
        tag = "p"
        raw_value = "A line with ![a logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with "),
            LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "a logo"}),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)
    def test_inline_link(self):
        tag = "p"
        raw_value = "A line with [a link](https://www.boot.dev) in it."
        node = text_to_inline_nodes(tag, raw_value)
        expected = ParentNode("p", [
            LeafNode(None, "A line with "),
            LeafNode("a", "a link", {"href": "https://www.boot.dev"}),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(node, expected)

class TestBlockToHeading(unittest.TestCase):
    def test_H1_no_inline_formatting(self):
        block = "#First line of heading"
        heading_node = block_to_heading(block)
        expected = LeafNode("h1", "First line of heading")
        self.assertEqual(heading_node, expected)
    def test_H2(self):
        block = "##First line of heading"
        heading_node = block_to_heading(block)
        expected = LeafNode("h2", "First line of heading")
        self.assertEqual(heading_node, expected)
    def test_H6(self):
        block = "######First line of heading"
        heading_node = block_to_heading(block)
        expected = LeafNode("h6", "First line of heading")
        self.assertEqual(heading_node, expected)
    def test_extra_H(self):
        block = "#######First line of heading"
        heading_node = block_to_heading(block)
        expected = LeafNode("h6", "#First line of heading")
        self.assertEqual(heading_node, expected)
    def test_single_inline_formatting(self):
        block = "#Some **bold text** in a heading"
        heading_node = block_to_heading(block)
        expected = ParentNode("h1", [
            LeafNode(None, "Some "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in a heading")
        ])
        self.assertEqual(heading_node, expected)
    def test_multiline_inline_formatting(self):
        block = "##Some **bold text** in the first line of a heading\nSome *italic text* in the second line of a heading"
        heading_node = block_to_heading(block)
        expected = ParentNode("h2", [
            LeafNode(None, "Some "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in the first line of a heading\nSome "),
            LeafNode("i", "italic text"),
            LeafNode(None, " in the second line of a heading")
        ])
        self.assertEqual(heading_node, expected)
    def test_heading_with_whitespace(self):
        block = "#     This heading has whitespace"
        heading_node = block_to_heading(block)
        expected = LeafNode("h1", "This heading has whitespace")
        self.assertEqual(heading_node, expected)

class TestBlockToCode(unittest.TestCase):
    def test_single_no_inline_formatting(self):
        block = "```First line of code block```"
        code_node = block_to_code(block)
        expected = ParentNode("pre", [
            LeafNode("code", "First line of code block")
        ])
        self.assertEqual(code_node, expected)
    def test_singe_inline_formatting(self):
        block = "```First line of code block with **bold text** in it```"
        code_node = block_to_code(block)
        expected = ParentNode("pre", [
            ParentNode("code", [
                LeafNode(None, "First line of code block with "),
                LeafNode("b", "bold text"),
                LeafNode(None, " in it")
            ])
        ])
        self.assertEqual(code_node, expected)
    def test_multiline_no_inline_formatting(self):
        block = "```First line of code block\nSecond line of code block\nThird line of code block```"
        code_node = block_to_code(block)
        expected = ParentNode("pre", [
            LeafNode("code", "First line of code block\nSecond line of code block\nThird line of code block")
        ])
        self.assertEqual(code_node, expected)
    def test_multiline_inline_formatting(self):
        block = "```First line of code block with **bold text**\nSecond line no formatting\nThird line with *italic text*```"
        code_node = block_to_code(block)
        expected = ParentNode("pre", [
            ParentNode("code", [
                LeafNode(None, "First line of code block with "),
                LeafNode("b", "bold text"),
                LeafNode(None, "\nSecond line no formatting\nThird line with "),
                LeafNode("i", "italic text")
            ])
        ])
        self.assertEqual(code_node, expected)

class TestBlockToQuote(unittest.TestCase):
    def test_single_no_inline_formatting(self):
        block_lines = [">Single line blockquote without formatted text in it."]
        quote_node = block_to_quote(block_lines)
        expected = LeafNode("blockquote", "Single line blockquote without formatted text in it.")
        self.assertEqual(quote_node, expected)
    def test_single_inline_formatting(self):
        block_lines = [">Single line blockquote with **bold text** in it."]
        quote_node = block_to_quote(block_lines)
        expected = ParentNode("blockquote", [
            LeafNode(None, "Single line blockquote with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(quote_node, expected)
    def test_multiline_no_inline_formatting(self):
        block_lines = [">First line of blockquote without formatted text in it.", ">Second line of blockquote.", ">Third line of blockquote."]
        quote_node = block_to_quote(block_lines)
        expected = LeafNode("blockquote", "First line of blockquote without formatted text in it.\nSecond line of blockquote.\nThird line of blockquote.")
        self.assertEqual(quote_node, expected)
    def test_multiline_inline_formatting(self):
        block_lines = [">First line of blockquote with **bold text** in it.", ">Second line of blockquote with *italic text*.", ">Third line of blockquote ending in `inline code`"]
        quote_node = block_to_quote(block_lines)
        expected = ParentNode("blockquote", [
            LeafNode(None, "First line of blockquote with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in it.\nSecond line of blockquote with "),
            LeafNode("i", "italic text"),
            LeafNode(None, ".\nThird line of blockquote ending in "),
            LeafNode("code", "inline code")
        ])
        self.assertEqual(quote_node, expected)
    def test_single_whitespace(self):
        block_lines = [">  First line of blockquote."]
        quote_node = block_to_quote(block_lines)
        expected = LeafNode("blockquote", "First line of blockquote.")
        self.assertEqual(quote_node, expected)
    def test_multiline_whitespace(self):
        block_lines = [">  First line of blockquote.", ">  Second line of blockquote."]
        quote_node = block_to_quote(block_lines)
        expected = LeafNode("blockquote", "First line of blockquote.\nSecond line of blockquote.")
        self.assertEqual(quote_node, expected)

class TestBlockToUnordered(unittest.TestCase):
    def test_single_no_inline_formatting(self):
        block_lines = ["* First item of unordered list"]
        unordered_node = block_to_unordered(block_lines)
        expected = ParentNode("ul", [
            LeafNode("li", "First item of unordered list")
        ])
        self.assertEqual(unordered_node, expected)
    def test_single_inline_formatting(self):
        block_lines = ["* First item of unordered list with **bold text**"]
        unordered_node = block_to_unordered(block_lines)
        expected = ParentNode("ul", [
            ParentNode("li", [
                LeafNode(None, "First item of unordered list with "),
                LeafNode("b", "bold text")
            ])
        ])
        self.assertEqual(unordered_node, expected)
    def test_multiline_no_inline_formatting(self):
        block_lines = ["* First item of unordered list", "- Second item of unordered list", "* Third item of unordered list"]
        unordered_node = block_to_unordered(block_lines)
        expected = ParentNode("ul", [
            LeafNode("li", "First item of unordered list"),
            LeafNode("li", "Second item of unordered list"),
            LeafNode("li", "Third item of unordered list")
        ])
        self.assertEqual(unordered_node, expected)
    def test_multiline_inline_formatting(self):
        block_lines = ["* First **bold item** of unordered list", "- Second *italic item* of unordered list", "* Third `inline code item` of unordered list"]
        unordered_node = block_to_unordered(block_lines)
        expected = ParentNode("ul", [
            ParentNode("li", [
                LeafNode(None, "First "),
                LeafNode("b", "bold item"),
                LeafNode(None, " of unordered list")
            ]),
            ParentNode("li", [
                LeafNode(None, "Second "),
                LeafNode("i", "italic item"),
                LeafNode(None, " of unordered list")
            ]),
            ParentNode("li", [
                LeafNode(None, "Third "),
                LeafNode("code", "inline code item"),
                LeafNode(None, " of unordered list")
            ])
        ])
        self.assertEqual(unordered_node, expected)
    def test_whitespace(self):
        block_lines = ["*    First item of unordered list", "*    Second item of unordered list", "*     Third item of unordered list"]
        unordered_node = block_to_unordered(block_lines)
        expected = ParentNode("ul", [
            LeafNode("li", "First item of unordered list"),
            LeafNode("li", "Second item of unordered list"),
            LeafNode("li", "Third item of unordered list")
        ])
        self.assertEqual(unordered_node, expected)

class TestBlockToOrdered(unittest.TestCase):
    def test_single_no_inline_formatting(self):
        block_lines = ["1. First item of ordered list"]
        ordered_node = block_to_ordered(block_lines)
        expected = ParentNode("ol", [
            LeafNode("li", "First item of ordered list")
        ])
        self.assertEqual(ordered_node, expected)
    def test_single_inline_formatting(self):
        block_lines = ["1. First item of ordered list with **bold text**"]
        ordered_node = block_to_ordered(block_lines)
        expected = ParentNode("ol", [
            ParentNode("li", [
                LeafNode(None, "First item of ordered list with "),
                LeafNode("b", "bold text")
            ])
        ])
        self.assertEqual(ordered_node, expected)
    def test_multiline_no_inline_formatting(self):
        block_lines = ["1. First item of ordered list", "2. Second item of ordered list", "3. Third item of ordered list"]
        ordered_node = block_to_ordered(block_lines)
        expected = ParentNode("ol", [
            LeafNode("li", "First item of ordered list"),
            LeafNode("li", "Second item of ordered list"),
            LeafNode("li", "Third item of ordered list")
        ])
        self.assertEqual(ordered_node, expected)
    def test_multiline_inline_formatting(self):
        block_lines = ["1. First **bold item** of ordered list", "2. Second *italic item* of ordered list", "3. Third `inline code item` of ordered list"]
        ordered_node = block_to_ordered(block_lines)
        expected = ParentNode("ol", [
            ParentNode("li", [
                LeafNode(None, "First "),
                LeafNode("b", "bold item"),
                LeafNode(None, " of ordered list")
            ]),
            ParentNode("li", [
                LeafNode(None, "Second "),
                LeafNode("i", "italic item"),
                LeafNode(None, " of ordered list")
            ]),
            ParentNode("li", [
                LeafNode(None, "Third "),
                LeafNode("code", "inline code item"),
                LeafNode(None, " of ordered list")
            ])
        ])
        self.assertEqual(ordered_node, expected)
    def test_whitespace(self):
        block_lines = ["1.   First item of ordered list", "2.    Second item of ordered list", "3.    Third item of ordered list"]
        ordered_node = block_to_ordered(block_lines)
        expected = ParentNode("ol", [
            LeafNode("li", "First item of ordered list"),
            LeafNode("li", "Second item of ordered list"),
            LeafNode("li", "Third item of ordered list")
        ])
        self.assertEqual(ordered_node, expected)

class TestBlockToParagraph(unittest.TestCase):
    def test_single_no_inline_formatting(self):
        block = "First line of a paragraph block with no formatted text."
        paragraph_node = block_to_paragraph(block)
        expected = LeafNode("p", "First line of a paragraph block with no formatted text.")
        self.assertEqual(paragraph_node, expected)
    def test_single_inline_formatting(self):
        block = "First line of a paragraph block with **bold text** in it."
        paragraph_node = block_to_paragraph(block)
        expected = ParentNode("p", [
            LeafNode(None, "First line of a paragraph block with "),
            LeafNode("b", "bold text"),
            LeafNode(None, " in it.")
        ])
        self.assertEqual(paragraph_node, expected)
    def test_multiline_no_inline_formatting(self):
        block = "First line of a paragraph block with no formatted text.\nSecond line of paragraph.\nThird line of paragraph."
        paragraph_node = block_to_paragraph(block)
        expected = LeafNode("p", "First line of a paragraph block with no formatted text.\nSecond line of paragraph.\nThird line of paragraph.")
        self.assertEqual(paragraph_node, expected)
    def test_multiline_inline_formatting(self):
        block = "First line of a paragraph block with **bold text**.\nSecond line with *italic text*.\nThird line with `inline code`"
        paragraph_node = block_to_paragraph(block)
        expected = ParentNode("p", [
            LeafNode(None, "First line of a paragraph block with "),
            LeafNode("b", "bold text"),
            LeafNode(None, ".\nSecond line with "),
            LeafNode("i", "italic text"),
            LeafNode(None, ".\nThird line with "),
            LeafNode("code", "inline code")
        ])
        self.assertEqual(paragraph_node, expected)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_single_heading(self):
        markdown = "###This is a third-tier heading in markdown with ![a logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) in it."
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("h3", [
                LeafNode(None, "This is a third-tier heading in markdown with "),
                LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "a logo"}),
                LeafNode(None, " in it.")
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_single_code(self):
        markdown = "```This is a multiline code block\nwith a second line\nand a third line in it```"
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("pre", [
                LeafNode("code", "This is a multiline code block\nwith a second line\nand a third line in it")
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_single_quote(self):
        markdown = ">This is a multiline blockquote.\n>The second line has *italic text* in it.\n>The third line does not."
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode(None, "This is a multiline blockquote.\nThe second line has "),
                LeafNode("i", "italic text"),
                LeafNode(None, " in it.\nThe third line does not.")
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_single_unordered(self):
        markdown = "* First item in unordered list\n* Second item in unordered list\n* Third item with [a link](https://www.boot.dev)"
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ul", [
                LeafNode("li", "First item in unordered list"),
                LeafNode("li", "Second item in unordered list"),
                ParentNode("li", [
                    LeafNode(None, "Third item with "),
                    LeafNode("a", "a link", {"href": "https://www.boot.dev"})
                ])
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_single_ordered(self):
        markdown = "1. First item in ordered list\n2. Second item in ordered list\n3. Third item with [a link](https://www.boot.dev)"
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ol", [
                LeafNode("li", "First item in ordered list"),
                LeafNode("li", "Second item in ordered list"),
                ParentNode("li", [
                    LeafNode(None, "Third item with "),
                    LeafNode("a", "a link", {"href": "https://www.boot.dev"})
                ])
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_single_paragraph(self):
        markdown = "Just a normal paragraph block.\nIt has multiple lines. Multiple sentences.\nAnd it has some **bold text** and *italic text* to test inline formatting."
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "Just a normal paragraph block.\nIt has multiple lines. Multiple sentences.\nAnd it has some "),
                LeafNode("b", "bold text"),
                LeafNode(None, " and "),
                LeafNode("i", "italic text"),
                LeafNode(None, " to test inline formatting.")
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_multiblock_unique(self):
        markdown = "#**A bold tier-one header**\n\n##Followed by a tier-two header\n\nThen a paragraph block.\nIt has multiple lines in it.\nAnd this line references some `inline code`\n\n```with a code block after that\nthat has multiple lines\nin it as well```"
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("h1", [
                LeafNode("b", "A bold tier-one header")
            ]),
            LeafNode("h2", "Followed by a tier-two header"),
            ParentNode("p", [
                LeafNode(None, "Then a paragraph block.\nIt has multiple lines in it.\nAnd this line references some "),
                LeafNode("code", "inline code")
            ]),
            ParentNode("pre", [
                LeafNode("code", "with a code block after that\nthat has multiple lines\nin it as well")
            ])
        ])
        self.assertEqual(HTML_node, expected)
    def test_multiblock_duplicate(self):
        markdown = "1. First item of first list\n2. Second item of first list\n3. Third item of first list has [a link](https://www.boot.dev)\n\n1. First item of second list also has [a link](https://www.boot.dev)\n2. Second item of second list\n3. Third item of second list\n\n1. First item of third list\n2. Second item of third list with ![a logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) in it\n3. Third item of third list"
        HTML_node = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ol", [
                LeafNode("li", "First item of first list"),
                LeafNode("li", "Second item of first list"),
                ParentNode("li", [
                    LeafNode(None, "Third item of first list has "),
                    LeafNode("a", "a link", {"href": "https://www.boot.dev"})
                ])
            ]),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "First item of second list also has "),
                    LeafNode("a", "a link", {"href": "https://www.boot.dev"})
                ]),
                LeafNode("li", "Second item of second list"),
                LeafNode("li", "Third item of second list")
            ]),
            ParentNode("ol", [
                LeafNode("li", "First item of third list"),
                ParentNode("li", [
                    LeafNode(None, "Second item of third list with "),
                    LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "a logo"}),
                    LeafNode(None, " in it")
                ]),
                LeafNode("li", "Third item of third list")
            ])
        ])
        self.assertEqual(HTML_node, expected)

class TestExtractTitle(unittest.TestCase):
    def test_one_title_heading(self):
        markdown = "#Title heading\n\nFirst line of paragraph.\nSecond line of paragraph."
        title = extract_title(markdown)
        expected = "Title heading"
        self.assertEqual(title, expected)
    def test_no_title_heading(self):
        markdown = "First line of first paragraph.\nSecond line of first paragraph.\n\nFirst line of second paragraph.\nSecond line of second paragraph."
        with self.assertRaises(Exception, msg="No title heading."):
            title = extract_title(markdown)
    def test_multiple_title_headings(self):
        markdown = "#First title heading\n\nFirst line of first paragraph.\nSecond line of first paragraph.\n\n#Second title heading\n\nFirst line of second paragraph.\nSecond line of second paragraph."
        with self.assertRaises(Exception, msg="Multiple title headings."):
            title = extract_title(markdown)
    def test_multiline_title_heading(self):
        markdown = "#First title\nSecond title\n\nFirst line of paragraph.\nSecond line of paragraph."
        title = extract_title(markdown)
        expected = "First title\nSecond title"
        self.assertEqual(title, expected)
    def test_title_with_whitespace(self):
        markdown = "#     Title with whitespace\n\nFirst line of paragraph.\nSecond line of paragraph."
        title = extract_title(markdown)
        expected = "Title with whitespace"
        self.assertEqual(title, expected)
    def test_one_title_with_other_headings(self):
        markdown = "#Title heading\n\n##Second heading\n\nFirst line of paragraph.\nSecondl ine of paragraph."
        title = extract_title(markdown)
        expected = "Title heading"
        self.assertEqual(title, expected)
    def test_no_title_with_other_headings(self):
        markdown = "##Second heading\n\nFirst line of paragraph.\nSecond line of paragraph."
        with self.assertRaises(Exception, msg="No title heading."):
            title = extract_title(markdown)
    def test_multiple_title_with_other_headings(self):
        markdown = "#First title heading\n\nFirst line of first paragraph.\nSecond line of first paragraph.\n\n#Second title heading\n\nFirst line of second paragraph.\nSecond line of second paragraph."
        with self.assertRaises(Exception, msg="Multiple title headings."):
            title = extract_title(markdown)