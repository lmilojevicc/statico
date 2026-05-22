from enum import Enum
from typing import Text


class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    EMBEDED_IMAGE_TEXT = "image"


def get_text_type_by_delimiter(delimiter):
    match delimiter:
        case "**":
            return TextType.BOLD_TEXT
        case "_":
            return TextType.ITALIC_TEXT
        case "`":
            return TextType.CODE_TEXT
        case _:
            raise ValueError("invalid delimiter")


class TextNode:
    def __init__(self, text: Text, type: TextType, url=None):
        self.text = text
        self.text_type = type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
