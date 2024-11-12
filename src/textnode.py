from enum import Enum

# text is the text content of a node
# text_type is the type of inline text the node contains, a string such as "bold" or "italic"
# url is the URL of a link or image, if the text is a link (defaults to None)
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def validate_type(text_node):
    if not isinstance(text_node.textType, TextType):
        raise ValueError("Invalid text type.")

class TextNode:
    def __init__(self, text, TextType, url=None):
        self.text = text
        self.textType = TextType
        self.url = url
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.textType == other.textType and
            self.url == other.url
        )
    def __repr__(self):
        return f"TextNode({self.text}, {self.textType}, {self.url})"