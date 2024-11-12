import unittest
from textnode import *
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode("b", "some value")
        props = node.props_to_html()
        expected = ''
        self.assertEqual(props, expected)
    def test_props_empty(self):
        node = HTMLNode("b", "some value", "", {})
        props = node.props_to_html()
        expected = ''
        self.assertEqual(props, expected)
    def test_props_one(self):
        node = HTMLNode("a", "link text", "", {"href": "https://www.google.com"})
        props = node.props_to_html()
        expected = ' href="https://www.google.com"'
        self.assertEqual(props, expected)
    def test_props_two(self):
        node = HTMLNode("a", "link text", "", {"href": "https://www.google.com", "target": "_blank"})
        props = node.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(props, expected)
    def test_eq_generic(self):
        node1 = HTMLNode("a", "link text", "", {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "link text", "", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1, node2)
    def test_eq_leaves(self):
        node1 = LeafNode("b", "This is a bold sentence.",)
        node2 = LeafNode("b", "This is a bold sentence.",)
        self.assertEqual(node1, node2)
    def test_eq_parents(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode(None, "This is the first sentence of a blue paragraph.",),
                LeafNode(None, "This is the second sentence.",)
            ],
            {"style": "color:blue;"}
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode(None, "This is the first sentence of a blue paragraph.",),
                LeafNode(None, "This is the second sentence.",)
            ],
            {"style": "color:blue;"}
        )
        self.assertEqual(node1, node2)
    def test_unequal_tag(self):
        node1 = LeafNode("b", "This is a formatted sentence.",)
        node2 = LeafNode("i", "This is a formatted sentence.",)
        self.assertNotEqual(node1, node2)
    def test_unequal_value(self):
        node1 = LeafNode("b", "This is a bold sentence.",)
        node2 = LeafNode("b", "This is a formatted sentence.",)
        self.assertNotEqual(node1, node2)
    def test_unequal_children_content(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode(None, "This is a leaf sentence.",)
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode(None, "This is a different leaf sentence.",)
            ],
        )
        self.assertNotEqual(node1, node2)
    def test_unequal_children_count(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode(None, "Leaf 1",)
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode(None, "Leaf 1",),
                LeafNode(None, "Leaf 2",)
            ],
        )
        self.assertNotEqual(node1, node2)
    def test_unequal_props_parent(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode(None, "This is the first sentence of a paragraph.",)
            ],
            {"style": "color:blue;"}
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode(None, "This is the first sentence of a paragraph.",)
            ],
            {"style": "color:gray;"}
        )
        self.assertNotEqual(node1, node2)
    def test_unequal_props_child(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("a", "Link text", {"href": "https://www.google.com", "target": "_blank"})
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode("a", "Link text", {"href": "https://www.wikipedia.com", "target": "_blank"})
            ],
        )
        self.assertNotEqual(node1, node2)

class TestLeafNode(unittest.TestCase):
    def test_simple_leaf(self):
        node = LeafNode("b", "This is a short sentence.")
        html = node.to_html()
        expected = '<b>This is a short sentence.</b>'
        self.assertEqual(html, expected)
    def test_empty_tag(self):
        node = LeafNode("", "This is a short sentence.")
        html = node.to_html()
        expected = 'This is a short sentence.'
        self.assertEqual(html, expected)
    def test_no_tag(self):
        node = LeafNode(None, "This is a short sentence.")
        html = node.to_html()
        expected = 'This is a short sentence.'
        self.assertEqual(html, expected)
    def test_empty_value(self):
        node = LeafNode("b", "")
        html = node.to_html()
        expected = '<b></b>'
        self.assertEqual(html, expected)
    def test_no_value(self):
        node = LeafNode("b")
        with self.assertRaises(ValueError):
            node.to_html()
    def test_one_prop_leaf(self):
        node = LeafNode("a", "This is some link text.", {"href": "https://www.google.com"})
        html = node.to_html()
        expected = '<a href="https://www.google.com">This is some link text.</a>'
        self.assertEqual(html, expected)
    def test_two_props_leaf(self):
        node = LeafNode("a", "This is some link text.", {"href": "https://www.google.com", "target": "_blank"})
        html = node.to_html()
        expected = '<a href="https://www.google.com" target="_blank">This is some link text.</a>'
        self.assertEqual(html, expected)

class TestParentNode(unittest.TestCase):
    def test_single_normal_leaf(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "A sentence of normal text.",)
            ],
        )
        html = node.to_html()
        expected = '<p>A sentence of normal text.</p>'
        self.assertEqual(html, expected)
    def test_single_tagged_leaf(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "A sentence of bold text.",)
            ],
        )
        html = node.to_html()
        expected = '<p><b>A sentence of bold text.</b></p>'
        self.assertEqual(html, expected)
    def test_parent_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "A sentence of blue text.",)
            ],
            {"style": "color:blue;"}
        )
        html = node.to_html()
        expected = '<p style="color:blue;">A sentence of blue text.</p>'
        self.assertEqual(html, expected)
    def test_multiple_leaves(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "A sentence of normal text.",),
                LeafNode(None, " Another sentence of normal text.",)
            ],
        )
        html = node.to_html()
        expected = '<p>A sentence of normal text. Another sentence of normal text.</p>'
        self.assertEqual(html, expected)
    def test_nested_parent_first(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "A sentence of normal text.",)
                    ],
                ),
                LeafNode(None, "A sentence outside the paragraph.")
            ],
        )
        html = node.to_html()
        expected = '<body><p>A sentence of normal text.</p>A sentence outside the paragraph.</body>'
        self.assertEqual(html, expected)
    def test_nested_parent_last(self):
        node = ParentNode(
            "body",
            [
                LeafNode(None, "A sentence outside the paragraph.",),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "A sentence of normal text.",)
                    ],
                )
            ],
        )
        html = node.to_html()
        expected = '<body>A sentence outside the paragraph.<p>A sentence of normal text.</p></body>'
        self.assertEqual(html, expected)
    def test_multiple_nested_parents(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "First sentence of first paragraph.",),
                        LeafNode(None, " Second sentence of first paragraph.",)
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "First sentence of second paragraph.",),
                        LeafNode(None, " Second sentence of second paragraph.",)
                    ],
                )
            ],
        )
        html = node.to_html()
        expected = '<body><p>First sentence of first paragraph. Second sentence of first paragraph.</p><p>First sentence of second paragraph. Second sentence of second paragraph.</p></body>'
        self.assertEqual(html, expected)
    def test_multiple_levels_nesting(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "body",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "A sentence of normal text.",)
                            ],
                        )
                    ],
                )
            ],
        )
        html = node.to_html()
        expected = '<html><body><p>A sentence of normal text.</p></body></html>'
        self.assertEqual(html, expected)
    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode(None, "A sentence of normal text.",),
                LeafNode(None, " Another sentence of normal text.",)
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()
    def test_no_child(self):
        node = ParentNode(
            "p",
            None,
            {"style": "color:blue;"}
        )
        with self.assertRaises(ValueError):
            node.to_html()
    def test_complex_node(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Blue Heading", {"style": "color:blue;"}),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "First sentence of gray paragraph.",),
                                LeafNode(None, " Second sentence with",),
                                LeafNode("b", " bold text",),
                                LeafNode(None, " and",),
                                LeafNode("i", " italic text",),
                                LeafNode(None, " in it.",)
                            ],
                            {"style": "color:gray;"}
                        ),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "First sentence of black paragraph.",),
                                LeafNode(None, " Second sentence with",),
                                LeafNode("a", " a hyperlink", {"href": "https://www.google.com", "target": "_blank"}),
                                LeafNode(None, " in it.",)
                            ],
                            {"style": "color:black;"}
                        )
                    ],
                )
            ],
        )
        html = node.to_html()
        expected = '<html><body><h1 style="color:blue;">Blue Heading</h1><p style="color:gray;">First sentence of gray paragraph. Second sentence with<b> bold text</b> and<i> italic text</i> in it.</p><p style="color:black;">First sentence of black paragraph. Second sentence with<a href="https://www.google.com" target="_blank"> a hyperlink</a> in it.</p></body></html>'
        self.assertEqual(html, expected)

class TestTextToHTML(unittest.TestCase):
    def test_text_type(self):
        text_node = TextNode("A string of text.", TextType.TEXT,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode(None, "A string of text.",)
        self.assertEqual(html_node, expected)
    def test_text_type_malformed(self):
        text_node = TextNode("A string of text.", TextType.TEXT, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode(None, "A string of text.",)
        self.assertEqual(html_node, expected)
    def test_no_text(self):
        text_node = TextNode("", TextType.TEXT,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode(None, "",)
        self.assertEqual(html_node, expected)
    def test_bold_type(self):
        text_node = TextNode("A string of text.", TextType.BOLD,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("b", "A string of text.",)
        self.assertEqual(html_node, expected)
    def test_bold_type_malformed(self):
        text_node = TextNode("A string of text.", TextType.BOLD, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("b", "A string of text.",)
        self.assertEqual(html_node, expected)
    def test_italic_type(self):
        text_node = TextNode("A string of text.", TextType.ITALIC,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("i", "A string of text.",)
        self.assertEqual(html_node, expected)
    def test_italic_type_malformed(self):
        text_node = TextNode("A string of text.", TextType.ITALIC, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("i", "A string of text.",)
        self.assertEqual(html_node, expected)
    def test_code_type(self):
        text_node = TextNode("a string of code", TextType.CODE,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("code", "a string of code",)
        self.assertEqual(html_node,expected)
    def test_code_type_malformed(self):
        text_node = TextNode("a string of code", TextType.CODE, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("code", "a string of code",)
        self.assertEqual(html_node, expected)
    def test_link_type(self):
        text_node = TextNode("Link text", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("a", "Link text", {"href": "https://www.google.com"})
        self.assertEqual(html_node, expected)
    def test_link_type_no_text(self):
        text_node = TextNode("", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("a", "", {"href": "https://www.google.com"})
        self.assertEqual(html_node, expected)
    def test_link_type_no_url(self):
        text_node = TextNode("Link text", TextType.LINK,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("a", "Link text", {"href": None})
        self.assertEqual(html_node, expected)
    def test_image_type(self):
        text_node = TextNode("Alt text", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "Alt text"})
        self.assertEqual(html_node, expected)
    def test_image_type_no_text(self):
        text_node = TextNode("", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": ""})
        self.assertEqual(html_node, expected)
    def test_image_type_no_url(self):
        text_node = TextNode("Alt text", TextType.IMAGE,)
        html_node = text_node_to_html_node(text_node)
        expected = LeafNode("img", "", {"src": None, "alt": "Alt text"})
        self.assertEqual(html_node, expected)
    def test_invalid_type(self):
        text_node = TextNode("A string of text.", "GARBAGE", "https://www.google.com")
        with self.assertRaises(ValueError, msg="Invalid text type."):
            text_node_to_html_node(text_node)