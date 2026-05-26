from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


def get_text_type_by_delimiter(delimiter: str) -> TextType:
    match delimiter:
        case "**":
            return TextType.BOLD
        case "_":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case _:
            raise ValueError("invalid delimiter")


class TextNode:
    def __init__(self, text: str, type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
