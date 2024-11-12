import unittest
from textnode import *
from textparsing import *
from markdownparsing import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_node_text_split_any(self):
        nodes = [
            TextNode("This is a string of text.", TextType.TEXT)
            ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is a string of text.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_nested(self):
        nodes = [
            TextNode("bold text with *italic text* in it", TextType.BOLD)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("bold text with *italic text* in it", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_text_split_any(self):
        nodes = [
            TextNode("This is the first string of text.", TextType.TEXT),
            TextNode("This is a second string of text.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is the first string of text.", TextType.TEXT),
            TextNode("This is a second string of text.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_bold_split_bold(self):
        nodes = [
            TextNode("This string has **bold text** in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This string has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_italic_split_italic(self):
        nodes = [
            TextNode("This string has *italic text* in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This string has ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_code_split_code(self):
        nodes = [
            TextNode("This string has a `code block` in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This string has a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_bold_split_code(self):
        nodes = [
            TextNode("This string has **bold text** in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This string has **bold text** in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_split_at_start(self):
        nodes = [
            TextNode("**Bold beginning** to a text string.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Bold beginning", TextType.BOLD),
            TextNode(" to a text string.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_split_at_end(self):
        nodes = [
            TextNode("This is a text string that ends with **bold text.**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is a text string that ends with ", TextType.TEXT),
            TextNode("bold text.", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_split_many(self):
        nodes = [
            TextNode("This text string has **bold text** and **more bold text** and **even more bold text** in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("even more bold text", TextType.BOLD),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_varied_split_partial(self):
        nodes = [
            TextNode("This text string has both **bold text** and *italic text* in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This text string has both ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and *italic text* in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_varied_split_all(self):
        nodes = [
            TextNode("This text string has both **bold text** and *italic text* in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This text string has both ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_malformed(self):
        nodes = [
            TextNode("This text string has *malformed markdown** in it.", TextType.TEXT)
        ]
        with self.assertRaises(ValueError, msg="Malformed Markdown. Odd number of delimiters in text."):
            new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    def test_nodes_varied_split_all(self):
        nodes = [
            TextNode("This text string has **bold text** in it.", TextType.TEXT),
            TextNode("And this string has *italic text* in it.", TextType.TEXT),
            TextNode("And this has both **bold text** and *italic text* in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it.", TextType.TEXT),
            TextNode("And this string has ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it.", TextType.TEXT),
            TextNode("And this has both ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_node_none(self):
        nodes = [
            TextNode("This text string has no images in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has no images in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_one(self):
        nodes = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_beginning(self):
        nodes = [
            TextNode("![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) This text string begins with a potion.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" This text string begins with a potion.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_end(self):
        nodes = [
            TextNode("This text string ends with a potion. ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string ends with a potion. ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp")
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_multiple_unique(self):
        nodes = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) and ![a baked salmon](https://www.boot.dev/_nuxt/baked-salmon.QSU05kuT.webp) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" and ", TextType.TEXT),
            TextNode("a baked salmon", TextType.IMAGE, "https://www.boot.dev/_nuxt/baked-salmon.QSU05kuT.webp"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_multiple_duplicate(self):
        nodes = [
            TextNode("This text string has not one ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) but two ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has not one ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" but two ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_none(self):
        nodes = [
            TextNode("This text string has no images in it.", TextType.TEXT),
            TextNode("This text string also has no images.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has no images in it.", TextType.TEXT),
            TextNode("This text string also has no images.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_one_first(self):
        nodes = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT),
            TextNode("This text string has no images in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string has no images in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_one_middle(self):
        nodes = [
            TextNode("This text string has no images in it.", TextType.TEXT),
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT),
            TextNode("This text string also has no images.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has no images in it.", TextType.TEXT),
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string also has no images.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_one_last(self):
        nodes = [
            TextNode("This text string has no images in it.", TextType.TEXT),
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has no images in it.", TextType.TEXT),
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_multiple_unique(self):
        nodes = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT),
            TextNode("This text string has ![a baked salmon](https://www.boot.dev/_nuxt/baked-salmon.QSU05kuT.webp) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a baked salmon", TextType.IMAGE, "https://www.boot.dev/_nuxt/baked-salmon.QSU05kuT.webp"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_multiple_duplicate(self):
        nodes = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT),
            TextNode("This text string also has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp).", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string also has ", TextType.TEXT),
            TextNode("a potion", TextType.IMAGE, "https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_link(self):
        nodes = [
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_node_none(self):
        nodes = [
            TextNode("This text string has no links in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has no links in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_one(self):
        nodes = [
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_beginning(self):
        nodes = [
            TextNode("[a link](https://www.boot.dev) This text string begins with a link.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" This text string begins with a link.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_end(self):
        nodes = [
            TextNode("This text string ends with a link. [a link](https://www.boot.dev)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string ends with a link. ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_multiple_unique(self):
        nodes = [
            TextNode("This text string has [a link](https://www.boot.dev) and [a different link](https://www.google.com) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("a different link", TextType.LINK, "https://www.google.com"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_multiple_duplicate(self):
        nodes = [
            TextNode("This text string has not one [a link](https://www.boot.dev) but two [a link](https://www.boot.dev) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has not one ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" but two ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_none(self):
        nodes = [
            TextNode("This text string has no links in it.", TextType.TEXT),
            TextNode("This text string also has no links.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has no links in it.", TextType.TEXT),
            TextNode("This text string also has no links.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_one_first(self):
        nodes = [
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT),
            TextNode("This text string has no links in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string has no links in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_one_middle(self):
        nodes = [
            TextNode("This text string has no links in it.", TextType.TEXT),
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT),
            TextNode("This text string also has no links.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has no links in it.", TextType.TEXT),
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string also has no links.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_one_last(self):
        nodes = [
            TextNode("This text string has no links in it.", TextType.TEXT),
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has no links in it.", TextType.TEXT),
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_multiple_unique(self):
        nodes = [
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT),
            TextNode("This text string has [a different link](https://www.google.com) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a different link", TextType.LINK, "https://www.google.com"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_nodes_multiple_duplicate(self):
        nodes = [
            TextNode("This text string has [a link](https://www.boot.dev) in it.", TextType.TEXT),
            TextNode("This text string also has [a link](https://www.boot.dev).", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" in it.", TextType.TEXT),
            TextNode("This text string also has ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://www.boot.dev"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    def test_node_link(self):
        nodes = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("This text string has ![a potion](https://www.boot.dev/_nuxt/xp-potion.Dn7OFh4o.webp) in it.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

class TestTextToTextNodes(unittest.TestCase):
    def test_Bootdev_sample(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(nodes, expected)