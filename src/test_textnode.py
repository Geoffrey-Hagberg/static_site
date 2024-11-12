import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        self.assertEqual(node1, node2)
    def test_eq_default(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    def test_eq_None_handling(self):
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    def test_eq_unequal_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a different text node", TextType.BOLD, "https://www.boot.dev/")
        self.assertNotEqual(node1, node2)
    def test_eq_unequal_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev/")
        self.assertNotEqual(node1, node2)
    def test_eq_unequal_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com/")
        self.assertNotEqual(node1, node2)
    def test_validate_type(self):
        node = TextNode("This is a text node", "GARBAGE")
        with self.assertRaises(ValueError, msg="Invalid text type."):
            validate_type(node)