import unittest

from parser import split_nodes_delimiter, split_nodes_image, split_nodes_link
from text_node import TextNode, TextType


class TestImageAndLinkParsing(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text with an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_text_after(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This is text with a link(https://i.imgur.com/zjjcJKZ.png) and another link(https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link(https://i.imgur.com/zjjcJKZ.png) and another link(https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )


class TestInlineMarkdown(unittest.TestCase):
    def text_regular_text(self):
        node = TextNode("This is text with words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with words", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
