import unittest

from leaf_node import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("span", "text")
        formatted = node.to_html()
        self.assertEqual(formatted, "<span>text</span>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "text")
        formatted = node.to_html()
        self.assertEqual(formatted, "text")
