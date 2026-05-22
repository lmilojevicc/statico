import unittest

from conversion import text_node_to_html_node
from text_node import TextNode, TextType


class TestConversion(unittest.TestCase):
    def test_bold_text_to_html_node(self):
        bold_txt_node = TextNode("cool", TextType.BOLD, None)
        bold_txt_html = text_node_to_html_node(bold_txt_node)
        self.assertEqual(bold_txt_html.tag, "b")
        self.assertEqual(bold_txt_html.value, "cool")
        self.assertEqual(bold_txt_html.to_html(), "<b>cool</b>")

    def test_anchor_text_to_html_node(self):
        link_txt_node = TextNode("cool", TextType.LINK, "https://example.com")
        link_html_node = text_node_to_html_node(link_txt_node)
        self.assertEqual(link_html_node.tag, "a")
        self.assertEqual(link_html_node.value, "cool")
        self.assertEqual(
            link_html_node.to_html(), '<a href="https://example.com">cool</a>'
        )

    def test_image_to_html_node(self):
        img_txt_node = TextNode("cool", TextType.IMAGE, "https://example.com")
        img_html_node = text_node_to_html_node(img_txt_node)
        self.assertEqual(img_html_node.tag, "img")
        self.assertEqual(img_html_node.value, "")
        self.assertEqual(
            img_html_node.to_html(), '<img href="https://example.com" alt="cool"></img>'
        )
