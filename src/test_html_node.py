import unittest

from html_node import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("b", "text", None, {"href": "https://example.com"})
        formatted_props = node.props_to_html().strip()
        self.assertEqual(formatted_props, 'href="https://example.com"')


if __name__ == "__main__":
    unittest.main()
