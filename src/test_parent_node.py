import unittest

from leaf_node import LeafNode
from parent_node import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], None)
        formatted = parent_node.to_html()
        self.assertEqual(formatted, "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node_1 = LeafNode("span", "child1")
        child_node_2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node_1, child_node_2], None)
        formatted = parent_node.to_html()
        self.assertEqual(formatted, "<div><span>child1</span><span>child2</span></div>")

    def test_parent_without_tag(self):
        child_node_1 = LeafNode("span", "child1")
        child_node_2 = LeafNode("span", "child2")
        parent_node = ParentNode(None, [child_node_1, child_node_2], None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_without_children(self):
        parent_node = ParentNode("div", [], None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
