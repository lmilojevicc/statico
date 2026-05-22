import unittest

from text_node import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        n1 = TextNode("cool", TextType.BOLD)
        n2 = TextNode("cool", TextType.BOLD)
        self.assertEqual(n1, n2)

    def test_eq(self):
        n1 = TextNode("cool", TextType.BOLD, "https://www.boot.dev/lessons")
        n2 = TextNode("cool", TextType.BOLD, "https://www.boot.dev/lessons")
        self.assertEqual(n1, n2)

    def test_not_eq(self):
        n1 = TextNode("cool", TextType.BOLD, "https://www.boot.dev/lessons")
        n2 = TextNode("COOL", TextType.BOLD, "https://www.boot.dev/lessons")
        self.assertNotEqual(n1, n2)

        n1 = TextNode("cool", TextType.BOLD, "https://www.boot.dev/lessons")
        n2 = TextNode("cool", TextType.ITALIC, "https://www.boot.dev/lessons")
        self.assertNotEqual(n1, n2)


if __name__ == "__main__":
    unittest.main()
