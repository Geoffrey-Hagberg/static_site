from textnode import *

# tag is a string representing the HTML tag name, such as "p" or "a" or "h1"
# tag defaults to None; node without tag renders as raw text
# value is a string representing the value of the HTML tag, such as the text inside a paragraph
# value defaults to None; node without value is assumed a parent with children
# children is a list of HTMLNode objects representing the children of this node
# children defaults to None; node without children is assumed to have a value
# props is a dictionary of key-value pairs representing the attributes of the HTML tag, such as {"href": "https://www.google.com/"} for an <a> tag
# props defaults to None; node without props has no additional attributes
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("This method should be overridden by child classes.")
    def props_to_html(self):
        if self.props == None:
            return ""
        formatted_props = ""
        for key in self.props:
            formatted_props = formatted_props + ' ' + f'{key}' + '=' + f'"{self.props[key]}"'
        return formatted_props
    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, "", props)
    def to_html(self):
        if self.value is None:
            raise  ValueError("No value; value is required.")
        elif (self.tag is None) or (self.tag == ""):
            return self.value
        else:
            html_props = super().props_to_html()
            return f'<{self.tag}{html_props}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, "", children, props)
    def to_html(self):
        if (self.tag is None) or (self.tag == ""):
            raise ValueError("No tag; tag is required.")
        elif (self.children is None) or (self.children == ""):
            raise ValueError("No children; child node is required.")
        else:
            children_html = ''
            html_props = super().props_to_html()
            for child in self.children:
                child_html = f'{child.to_html()}'
                children_html = children_html + child_html
            return f'<{self.tag}{html_props}>{children_html}</{self.tag}>'

def text_node_to_html_node(text_node):
    validate_type(text_node)
    if text_node.textType == TextType.TEXT:
        html_tag = None
        html_value = text_node.text
        html_props = None
        return LeafNode(html_tag, html_value, html_props)
    elif text_node.textType == TextType.BOLD:
        html_tag = "b"
        html_value = text_node.text
        html_props = None
        return LeafNode(html_tag, html_value, html_props) 
    elif text_node.textType == TextType.ITALIC:
        html_tag = "i"
        html_value = text_node.text
        html_props = None
        return LeafNode(html_tag, html_value, html_props)
    elif text_node.textType == TextType.CODE:
        html_tag = "code"
        html_value = text_node.text
        html_props = None
        return LeafNode(html_tag, html_value, html_props)
    elif text_node.textType == TextType.LINK:
        html_tag = "a"
        html_value = text_node.text
        html_props = {"href": text_node.url}
        return LeafNode(html_tag, html_value, html_props)
    elif text_node.textType == TextType.IMAGE:
        html_tag = "img"
        html_value = ""
        html_props = {"src": text_node.url, "alt": text_node.text}
        return LeafNode(html_tag, html_value, html_props)