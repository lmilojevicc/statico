from leaf_node import LeafNode
from text_node import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.EMBEDED_IMAGE_TEXT:
            return LeafNode("img", "", {"href": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Non-existing TextType")
